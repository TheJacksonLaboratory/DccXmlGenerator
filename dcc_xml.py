# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 12:45:44 2020

This module is responsible for generating the XML files for the DCC upload.

There are two XMLs to be generated: 
  J.YYYY-MM-DD.NN.specimen.impc.xml for specimens 
    and
  J.YYYY-MM-DD.NN.experiment.impc.xml for experiments
  
This module queries CLIMB for data based on a filter
set up by the user. It then gathers DCC-specific information from
a table in the MySQL schema `komp` table names `dccparameterdetails` and
`taskimpccodes`.

Given that information it can create the XML files.

It determines the XML file name and writes it out to the working directory.

@author: michaelm
"""

import pandas as pd
import json
import glob

import argparse
from datetime import datetime
from os import listdir
from os.path import isfile, join, basename
import time

from zipfile import ZipFile
import xml.etree.ElementTree as ET

import read_config as cfg
import logging
from logging.handlers import TimedRotatingFileHandler
import re

# Our code
import jaxlims_api as db
import climb_api as c
import validate_procedure as v
import core_api as pfs

# Globals - set either from the command line or config file
g_ImpcCode = ''
g_ColonyId =''
g_DataSrc = ''   # CLIMB, PFS, or JAXLIMS
g_dataDir = ''
g_filterFileName = 'filters-with-mice.json'
g_image_dir = '.'
g_logger = None
# "environment variables"

# From YAML file            
def getDatadir():
  global g_dataDir
  return g_dataDir

def setClimbFilterFile(filename:str):
  global g_filterFileName
  g_filterFileName = filename

def getClimbFilterFile():
  global g_filterFileName
  return g_filterFileName

def setDataDir(datadir:str):
  global g_dataDir
  g_dataDir = datadir

def getDataSrc():
      global g_DataSrc
      return g_DataSrc

def setDataSrc(sourceName:str): 
  # sourceName: JAXLIMS, PFS, or CLIMB
  global g_DataSrc
  g_DataSrc = sourceName
  
def getFtpServer():
      return 'sftp://bhjlk02lp.jax.org/'

# Global map: Look up a proc status string and return the IMPC code
procedure_status_message_map = {
'Incomplete' : 'IMPC_PSC_015',
'Removed' : 'IMPC_PSC_001',
'Cancelled' : 'IMPC_PSC_006',
'Incomplete' : 'IMPC_PSC_015',
'Cancelled - Pipeline stopped - scheduling' : 'IMPC_PSC_006',
'Cancelled - Pipeline stopped - welfare' : 'IMPC_PSC_005',
'Cancelled - Single procedure not performed - welfare' : 'IMPC_PSC_003',
'Incomplete - Procedure Failed - Equipment Failed' : 'IMPC_PSC_007',
'Incomplete - Single procedure not performed - schedule' : ' IMPC_PSC_004',
'Procedure Failed - Insufficient Sample' : 'IMPC_PSC_009',
'Procedure Failed - Process Failed' : 'IMPC_PSC_010',
'Procedure Failed - Sample Lost' : 'IMPC_PSC_008',
'Procedure QC Failed' : 'IMPC_PSC_011',
'Removed - Mouse culled' : 'IMPC_PSC_002',
'Removed - Mouse died' : 'IMPC_PSC_001',
'LIMS not ready' : 'IMPC_PSC_012',
'Software failure' : 'IMPC_PSC_013',
'Uncooperative mouse' : 'IMPC_PSC_014',
'Incomplete - see comments' : 'IMPC_PSC_015:Wrong_pipeline',
'Withdrawn' : 'IMPC_PSC_015:Withdrawn'
}

# Global map: Look up a output status string and return the IMPC code
output_status_message_map = {
'Parameter not measured - Equipment Failed' : 'IMPC_PARAMSC_001',
'Parameter not measured - Sample Lost' : 'IMPC_PARAMSC_002',
'Parameter not measured - Insufficient sample' : 'IMPC_PARAMSC_003',
'Parameter not recorded - welfare issue' : 'IMPC_PARAMSC_004',
'Parameter not recorded - Welfare issue' : 'IMPC_PARAMSC_004',
'Free Text of Issues' : 'IMPC_PARAMSC_005',
'Extra Information' : 'IMPC_PARAMSC_006',
'Parameter not measured - not in SOP' : 'IMPC_PARAMSC_007',
'Parameter not measured - Not in SOP' : 'IMPC_PARAMSC_007',
'Above upper limit of quantitation' : 'IMPC_PARAMSC_008',
'Below lower limit of quantitation' : 'IMPC_PARAMSC_009',
'Parameter QC Failed' : 'IMPC_PARAMSC_010',
'LIMS not ready yet' : 'IMPC_PARAMSC_011',
'Software failure' : 'IMPC_PARAMSC_012',
'Uncooperative mouse' : 'IMPC_PARAMSC_013'
}

def createLogHandler(log_file):
        logger = logging.getLogger(__name__)
        date = datetime.now().strftime("%B-%d-%Y")
        FORMAT = "[%(asctime)s->%(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
        logging.basicConfig(format=FORMAT, filemode="w", level=logging.DEBUG, force=True)
        handler =TimedRotatingFileHandler(f"{log_file}_{date}.log" , when="midnight", backupCount=10)
        handler.setFormatter(logging.Formatter(FORMAT))
        handler.suffix = "%Y%m%d"
        handler.extMatch = re.compile(r"^\d{8}$")
        logger.addHandler(handler)
        return logger


def setProcedureImpcCode(code):
  global g_ImpcCode
  g_ImpcCode=code
      
def getProcedureImpcCode():
  global g_ImpcCode
  return g_ImpcCode

def getColonyId():
  global g_ColonyId
  return g_ColonyId

def setColonyId(colonyId):
  global g_ColonyId
  g_ColonyId = colonyId

# By convention if a task with no mice needs to record the line
#   then she stores it in an output named "JR". But she only stores the five digit code
def findColonyId(proc):
  outputLs = proc["outputs"]
  if outputLs == None or len(outputLs) == 0:
      return ""
  
  for output in outputLs:
      # For line calls we need the JR# - or Stock Number - so lets store it for later -- just one more kluge
      if output["outputName"] == "JR":
          setColonyId('JR' + output["outputValue"])
      elif output["outputName"] == "Stock Number":
          # Different formats of JRs and Stock Numbers!!
          sn = output["outputValue"]
          if sn[0] == '0':
            sn = sn[1:]
          setColonyId('JR' + sn)
        
  return getColonyId()
  
def getBackgroundStrainId():
  # C57BL/6NJ
  return 'MGI:3056279'

def checkAnimalKeys(mouseInfo):
  # If the animal object does not have the keys required to help build an experiment, return false
  # Should  never happen in the real world
  is_ok = False
  if "animalName" in mouseInfo:
    if mouseInfo["animalName"] != None:
      is_ok = True
  return is_ok

# XML XML XML
def createSpecimenXML(animalLs):
    root = createSpecimenRoot()
    centerNode = createSpecimenCentre(root)
    generateSpecimenXML(animalLs, centerNode)
      
    # Write it out
    tree = ET.ElementTree(indent(root))
    specimenFileName = getNextSpecimenFilename(getDatadir())
    tree.write(specimenFileName, xml_declaration=True, encoding='utf-8')
      
    # Now zip it up.
    zipfilename = specimenFileName.replace('specimen.','').replace('xml','zip')
    with ZipFile(zipfilename,'w') as zipper:
      zipper.write(specimenFileName,basename(specimenFileName))
      zipper.close()
      
      
def createExperimentXML(experimentLs, procedureHasAnimals):
    root = createProcedureRoot()
    centerNode = createCentre(root)
    
    if procedureHasAnimals:
          numberOfProcs = generateExperimentXML(experimentLs, centerNode) 
    else:
          numberOfProcs = generateLineCallExperimentXML(experimentLs, centerNode)
    
    expFileName = getNextExperimentFilename(getDatadir())
    if(numberOfProcs > 0):      # write the new XML file
      tree = ET.ElementTree(indent(root))
      tree.write(expFileName, xml_declaration=True, encoding='utf-8')
      
      # Now zip it up.
      zipfilename = expFileName.replace('experiment.','').replace('xml','zip')
      with ZipFile(zipfilename,'w') as zipper:
        zipper.write(expFileName,basename(expFileName))
        zipper.close()  
       
def createProcedureRoot():
    root = ET.Element('centreProcedureSet', {'xmlns':'http://www.mousephenotype.org/dcc/exportlibrary/datastructure/core/procedure'})
    return root
  
def createSpecimenRoot():
    root = ET.Element('centreSpecimenSet', {'xmlns':'http://www.mousephenotype.org/dcc/exportlibrary/datastructure/core/specimen'})
    return root

def createCentre(root):
    centerNode = ET.SubElement(root, 'centre', {'centreID':'J', 'pipeline':'JAX_001', 'project':'JAX'})
    return  centerNode 

def createSpecimenCentre(root):
    centerNode = ET.SubElement(root, 'centre', {'centreID':'J'})
    return  centerNode

def createCentreSpecimenSet(root):
    centerNode = ET.SubElement(root, 'centreSpecimenSet', {'centreID':'J', 'pipeline':'JAX_001', 'project':'JAX'})
    return  centerNode

def createExperiment(centerNode, expName, expDate):
    # Generate the bones of the experiment node. No procedure or specimen info yet  
    experimentDictKeys = [ "experimentID", "dateOfExperiment" ]
    experimentDict = dict.fromkeys(experimentDictKeys)
    experimentDict["experimentID"] = expName
    experimentDict["dateOfExperiment"] = expDate
    experimentNode = ET.SubElement(centerNode, 'experiment', experimentDict)
    
    return experimentNode
		
def createSpecimen(experimentNode,animalName):
    specimenNode = ET.SubElement(experimentNode, 'specimenID')
    specimenNode.text = animalName
    return experimentNode # experimentNode
		
def createColonyId(experimentNode,colonyId):
    lineNode = ET.SubElement(experimentNode, 'line', {'colonyID': '{jr}'.format(jr=colonyId)} )
    return lineNode # experimentNode

def createProcedure(experimentNode, procId):
    procedureNode = ET.SubElement(experimentNode, 'procedure', {'procedureID': '{proc}'.format(proc=procId) })
    return procedureNode # procedureNode


def createMetadata(procedureNode,impcCode, strVal):
    paramNode = ET.SubElement(procedureNode, 'procedureMetadata', { 'parameterID': '{code}'.format(code=impcCode)})
    valueNode = ET.SubElement(paramNode, 'value')
    valueNode.text = strVal
    return procedureNode

def createSimpleParameter(procedureNode,impcCode, strVal,statusCode):
    paramNode = ET.SubElement(procedureNode, 'simpleParameter', { 'parameterID': '{code}'.format(code=impcCode)})
    if len(statusCode) > 0:
        statusNode = ET.SubElement(paramNode,'statusCode')
        statusNode.text = statusCode   
    else:
      valueNode = ET.SubElement(paramNode, 'value')
      valueNode.text = strVal
    
    return procedureNode

# <seriesMediaParameter parameterID="IMPC_XRY_048_001">
#    <value incrementValue="1" URI="ftp://images/image1.jpg" fileType="img/jpg">
#    <value incrementValue="1" URI="ftp://images/image1.jpg" fileType="img/jpg">
#</seriesMediaParameter>
# Must be included just before the metadata!!!
def createSeriesMediaParameter(procedureNode,impc_code, strVal,procedureImpcCode,taskKey):
    
  if strVal == None:
    return procedureNode # bail
        
    # The value is a dictionary with the key as the increment and the value as the value
  paramNode = ET.SubElement(procedureNode, 'seriesMediaParameter', { 'parameterID': '{code}'.format(code=impc_code)})
    
    # strVal is a string but must be a dict with the increment as the key and the output value as the value
  dictVal = validateSeriesParameter(strVal)
  for key in dictVal:
    image = dictVal[key]  # Looks like \\jax\jax\phenotype\EKG\KOMP\images\blah.jpg
    filenameSplit = image.split('\\')
    filenameOnly = filenameSplit[len(filenameSplit)-1]
    filenameOnly = filenameOnly.replace(' ','_',)
    valueNode = ET.SubElement(paramNode, 'value', {'incrementValue': str(key), 'URI': getFtpServer() + 'images/' + procedureImpcCode + "/" + filenameOnly})
    #valueNode.text = ???
    db.recordMediaSubmission(image, (getFtpServer() + 'images/' + procedureImpcCode + "/" + filenameOnly) ,taskKey,impc_code)

  return procedureNode

def validateSeriesParameter(seriesValue: str): # Comes in a str, returns a dict
  # series parameters must be in dict format. If not make it so.
  # Both key and value need to be strings!!!
  paramDict = {}
  try:
    seriesValue = seriesValue.replace("\'","\"")  # Single quote check
    seriesValue = seriesValue.replace("None","-1")  # Can't handle Nones. Should never see.
    paramDict = json.loads(seriesValue) # Turn to dict
    # Values need to be str's!
    for k,v in paramDict.items():
      paramDict[k] = str(v)
    
    # TODO : Handle viability -> paramDict["noLitter"] = seriesValue  # VIA only for now
  except Exception as e:
    print(seriesValue)
    print(repr(e))
    
  return paramDict  
# e.g. for Primary Viability
"""
  <seriesParameter parameterID="IMPC_VIA_037_001">
                    <value incrementValue="litterID1">RIKEN-Rln1-AB5_01</value>
                    <value incrementValue="litterID2">RIKEN-Rln1-AB5_01</value>
                    <value incrementValue="litterID3">RIKEN-Rln1-AB5_03</value>
                </seriesParameter>
"""
def createSeriesParameter(procedureNode, impcCode, strVal):
    if strVal == None:
          return procedureNode # bail
        
    # The value is a dictionary with the key as the increment and the value as the value
    paramNode = ET.SubElement(procedureNode, 'seriesParameter', { 'parameterID': '{code}'.format(code=impcCode)})
    
    # strVal is a string but must be a dict with the increment as the key and the output value as the value
    dictVal = validateSeriesParameter(strVal)
    for key in dictVal:
      valueNode = ET.SubElement(paramNode, 'value', {'incrementValue': key})
      valueNode.text = dictVal[key]
      
    return procedureNode

def createStatusCode(procedureNode, statusCode):
    statusNode = ET.SubElement(procedureNode, 'statusCode')
    statusNode.text = statusCode
    return procedureNode
  
def createSpecimenRecord(specimenRecord,specimenSetNode,statusCode):
  
  # fairly weak check but it is true
  isEmbryo = specimenRecord["generation"][0] == 'E'
  
  if v.validateMouseFields(specimenRecord) == True:
    if isEmbryo == True:
        paramNode = ET.SubElement(specimenSetNode, 'embryo', {
                              'stage': '{stage}'.format(stage=specimenRecord["generation"][1:]),
                              'stageUnit': 'DPC',
                              'isBaseline': '{isBaseline}'.format(isBaseline=str(specimenRecord["isBaseline"]).lower()),
                              'colonyID': '{colonyID}'.format(colonyID=specimenRecord["colonyId"]),'strainID': '{strainID}'.format(strainID=getBackgroundStrainId()),
                              'specimenID': '{specimenID}'.format(specimenID=specimenRecord["specimenID"]),
                              'gender': '{gender}'.format(gender=specimenRecord["gender"].lower()),
                              'zygosity': '{zygosity}'.format(zygosity=specimenRecord["zygosity"]),
                              'litterId': '{litterId}'.format(litterId=specimenRecord["litterId"]),
                              'pipeline': '{pipeline}'.format(pipeline=specimenRecord["pipeline"]),
                              'productionCentre': '{productionCentre}'.format(productionCentre=specimenRecord["productionCenter"]),
                              'phenotypingCentre': '{phenotypingCentre}'.format(phenotypingCentre=specimenRecord["phenotypingCenter"]),
                              'project': '{project}'.format(project=specimenRecord["project"]) })
    else:
      paramNode = ET.SubElement(specimenSetNode, 'mouse', {
                              'DOB': '{dob}'.format(dob=specimenRecord["dob"]),
                              'colonyID': '{colonyID}'.format(colonyID=specimenRecord["colonyId"]),
                              'isBaseline': '{isBaseline}'.format(isBaseline=str(specimenRecord["isBaseline"]).lower()),
                              'strainID': '{strainID}'.format(strainID=getBackgroundStrainId()), 
                              'specimenID': '{specimenID}'.format(specimenID=specimenRecord["specimenID"]),
                              'gender': '{gender}'.format(gender=specimenRecord["gender"].lower()),
                              'zygosity': '{zygosity}'.format(zygosity=specimenRecord["zygosity"]),
                              'litterId': '{litterId}'.format(litterId=specimenRecord["litterId"]),
                              'pipeline': '{pipeline}'.format(pipeline=specimenRecord["pipeline"]),
                              'productionCentre': '{productionCentre}'.format(productionCentre=specimenRecord["productionCenter"]),
                              'phenotypingCentre': '{phenotypingCentre}'.format(phenotypingCentre=specimenRecord["phenotypingCenter"]),
                              'project': '{project}'.format(project=specimenRecord["project"]) })
    if len(statusCode) > 0:
      statusNode = ET.SubElement(paramNode,'statusCode')
      statusNode.text = statusCode
    
  return specimenSetNode

# BEGIN -- KLUGE KLUGE KLUGE KLUGE KLUGE KLUGE because these tests were created with no inputs. Yuck
# Hopefully this will be temporary
def embryoKluge(taskName, parentNode):
    # If this is an embryo gross morphology or placenta task
    # we may have to create the metadata because there were many tasks
    # created before the inputs were created.
  
  expName = v.getCollectedBy()
  expId = db.databaseGetExperimenterIdCode(expName)
  
  if taskName ==  "E9.5 Embryo Gross Morphology":
    createMetadata(parentNode,"IMPC_GEL_045_001", expId)
    createMetadata(parentNode,"IMPC_GEL_046_001", "0")
    createMetadata(parentNode,"IMPC_GEL_047_001", "Leica")
    createMetadata(parentNode,"IMPC_GEL_048_001", "MC170HD")
    createMetadata(parentNode,"IMPC_GEL_049_001", "4% PFA")
    createMetadata(parentNode,"IMPC_GEL_050_001", "12:00")
    createMetadata(parentNode,"IMPC_GEL_051_001", "48")
    createMetadata(parentNode,"IMPC_GEL_052_001", "19:00")
    createMetadata(parentNode,"IMPC_GEL_053_001", "07:00")
  elif taskName == "E9.5 Placenta Morphology":
    createMetadata(parentNode,"IMPC_GPL_008_001", expId)
    createMetadata(parentNode,"IMPC_GPL_009_001", "0")
    createMetadata(parentNode,"IMPC_GPL_010_001", "Leica")
    createMetadata(parentNode,"IMPC_GPL_011_001", "MC170HD")
    createMetadata(parentNode,"IMPC_GPL_012_001", "4% PFA")
    createMetadata(parentNode,"IMPC_GPL_013_001", "12:00")
    createMetadata(parentNode,"IMPC_GPL_014_001", "48")
    createMetadata(parentNode,"IMPC_GPL_015_001", "19:00")
    createMetadata(parentNode,"IMPC_GPL_016_001", "07:00")
  elif taskName == "E12.5 Embryo Gross Morphology":
    createMetadata(parentNode,"IMPC_GEM_050_001", expId)
    createMetadata(parentNode,"IMPC_GEM_051_001", "0")
    createMetadata(parentNode,"IMPC_GEM_052_001", "Leica")
    createMetadata(parentNode,"IMPC_GEM_053_001", "MC170HD")
    createMetadata(parentNode,"IMPC_GEM_054_001", "4% PFA")
    createMetadata(parentNode,"IMPC_GEM_055_001", "12:00")
    createMetadata(parentNode,"IMPC_GEM_056_001", "48")
    createMetadata(parentNode,"IMPC_GEM_057_001", "19:00")
    createMetadata(parentNode,"IMPC_GEM_058_001", "07:00")
  elif taskName == "E12.5 Placenta Morphology":
    createMetadata(parentNode,"IMPC_GPM_008_001", expId)
    createMetadata(parentNode,"IMPC_GPM_009_001", "0")
    createMetadata(parentNode,"IMPC_GPM_010_001", "Leica")
    createMetadata(parentNode,"IMPC_GPM_011_001", "MC170HD")
    createMetadata(parentNode,"IMPC_GPM_012_001", "4% PFA")
    createMetadata(parentNode,"IMPC_GPM_013_001", "12:00")
    createMetadata(parentNode,"IMPC_GPM_014_001", "48")
    createMetadata(parentNode,"IMPC_GPM_015_001", "19:00")
    createMetadata(parentNode,"IMPC_GPM_016_001", "07:00")
  elif taskName == "E15.5 Embryo Gross Morphology":
    createMetadata(parentNode,"IMPC_GEO_051_001", expId)
    createMetadata(parentNode,"IMPC_GEO_052_001", "0")
    createMetadata(parentNode,"IMPC_GEO_053_001", "Leica")
    createMetadata(parentNode,"IMPC_GEO_054_001", "MC170HD")
    createMetadata(parentNode,"IMPC_GEO_055_001", "4% PFA")
    createMetadata(parentNode,"IMPC_GEO_056_001", "12:00")
    createMetadata(parentNode,"IMPC_GEO_057_001", "48")
    createMetadata(parentNode,"IMPC_GEO_058_001", "19:00")
    createMetadata(parentNode,"IMPC_GEO_059_001", "07:00")
  elif taskName == "E15.5 Placenta Morphology":
    createMetadata(parentNode,"IMPC_GPO_008_001", expId)
    createMetadata(parentNode,"IMPC_GPO_009_001", "0")
    createMetadata(parentNode,"IMPC_GPO_010_001", "Leica")
    createMetadata(parentNode,"IMPC_GPO_011_001", "MC170HD")
    createMetadata(parentNode,"IMPC_GPO_012_001", "4% PFA")
    createMetadata(parentNode,"IMPC_GPO_013_001", "12:00")
    createMetadata(parentNode,"IMPC_GPO_014_001", "48")
    createMetadata(parentNode,"IMPC_GPO_015_001", "19:00")
    createMetadata(parentNode,"IMPC_GPO_016_001", "07:00")
  elif taskName == "E18.5 Embryo Gross Morphology":
    createMetadata(parentNode,"IMPC_GEP_065_001", expId)
    createMetadata(parentNode,"IMPC_GEP_066_001", "0")
    createMetadata(parentNode,"IMPC_GEP_067_001", "Leica")
    createMetadata(parentNode,"IMPC_GEP_068_001", "MC170HD")
    createMetadata(parentNode,"IMPC_GEP_069_001", "4% PFA")
    createMetadata(parentNode,"IMPC_GEP_070_001", "12:00")
    createMetadata(parentNode,"IMPC_GEP_071_001", "48")
    createMetadata(parentNode,"IMPC_GEP_072_001", "19:00")
    createMetadata(parentNode,"IMPC_GEP_073_001", "07:00")
  elif taskName == "E18.5 Placenta Morphology":
    createMetadata(parentNode,"IMPC_GPP_008_001", expId)
    createMetadata(parentNode,"IMPC_GPP_009_001", "0")
    createMetadata(parentNode,"IMPC_GPP_010_001", "Leica")
    createMetadata(parentNode,"IMPC_GPP_011_001", "MC170HD")
    createMetadata(parentNode,"IMPC_GPP_012_001", "4% PFA")
    createMetadata(parentNode,"IMPC_GPP_013_001", "12:00")
    createMetadata(parentNode,"IMPC_GPP_014_001", "48")
    createMetadata(parentNode,"IMPC_GPP_015_001", "19:00")
    createMetadata(parentNode,"IMPC_GPP_016_001", "07:00")
  else:
    return False

  return True
  # End --  of embryo metadata kluge

# Create experiment XMLs
def generateExperimentXML(taskInfoLs, centerNode):
    # Given a dictionary parse out the animal info and the procedure info
    # It looks like "taskInfo" [ { "animal" [] , "taskInstance" : [] }, { "animal" [] , "taskInstance" : [] }, ...]
    # If an animal has multiple procedures the animal will only appear once.
    # Get the list of mouse info. For KOMP it should always be 1 element
    if taskInfoLs == None:
          return 0
    
    # otherwise, we have some data
    numberOfProcs = 0
    for exps in taskInfoLs:
        # For each animal thee are one or more tasks 
        mouseInfoLs = exps["animal"]
        for mouseInfo in mouseInfoLs:
          if checkAnimalKeys(mouseInfo) == False: # Should never happen in real world
            continue
          
          procLs = exps["taskInstance"]
          for proc in procLs:
            if proc["taskStatus"]  == "Failed QC" or proc["taskStatus"]  == "Already submitted":
                  continue # We failed it or we've already submitted it.
            
            
            # for each procedure in the list build up the XML
            numberOfProcs += 1
            experimentNode = createExperiment(centerNode,(proc['workflowTaskName'] + ' - ' +  mouseInfo['animalName'] + ' - ' + str(proc["taskInstanceKey"])), proc['dateComplete'])
            experimentNode = createSpecimen(experimentNode,mouseInfo['animalName'])
            procedureNode = createProcedure(experimentNode,db.databaseSelectProcedureCode(proc['workflowTaskName']))
            
            # Now create the metadata from the inputs and outputs
            procedureNode = buildParameters(procedureNode,proc)
            procedureNode = buildMetadata(procedureNode,proc)
            
            experimentNode = buildExperimentStatusCode(experimentNode,getProcedureStatusCode(proc))
    
    return numberOfProcs

# Create experiment XMLs
def generateLineCallExperimentXML(taskInfoLs, centerNode):
    # Given a dictionary parse out the animal info and the procedure info
    # It looks like "taskInfo" [ { "animal" [] , "taskInstance" : [] }, { "animal" [] , "taskInstance" : [] }, ...]
    # If an animal has multiple procedures the animal will only appear once.
    # Get the list of mouse info. For KOMP it should always be 1 element
    if taskInfoLs == None:
          return 0
    
    # Else we have some data
    numberOfProcs = 0
    for exps in taskInfoLs:
      procLs = exps["taskInstance"]
      for proc in procLs:
          if proc["taskStatus"]  == "Failed QC" or proc["taskStatus"]  == "Already submitted":
                continue # We failed it or we've already submitted it.
          
          findColonyId(proc)
          
          # for each procedure in the list build up the XML
          numberOfProcs += 1
            
          lineNode = createColonyId(centerNode,getColonyId())
          procedureNode = createProcedure(lineNode,db.databaseSelectProcedureCode(proc['workflowTaskName']))  # TODO Add status code is present
          
          # Now create the metadata from the inputs and outputs
          procedureNode = buildParameters(procedureNode,proc)
          
          procedureNode = buildMetadata(procedureNode,proc)
          
          lineNode = buildExperimentStatusCode(lineNode,getProcedureStatusCode(proc))  # ??????
          # Clear the colony Id
          #setColonyId('')
          
    return numberOfProcs

def buildMetadata(procedureNode,proc):
      # Ugly - If there are no inputs then this may be an embryo lethal ask that was unfortunately created with no inputs.
      if len(proc['inputs']) == 0:
            embryoKluge(proc['workflowTaskName'],procedureNode)
            return procedureNode
          
      # Returns a list of tuples (impccode, climb_key, dccType_key)
      setProcedureImpcCode(extractThreeLetterCode(db.databaseSelectProcedureCode(proc['workflowTaskName'])))
      # Get inputs -- last boolean = true
      metadataDefLs = db.databaseSelectImpcData(getProcedureImpcCode(), True, True)
      
      # Merge with metadata from the outputs (last boolean = false)
      metadataDefLs = metadataDefLs + db.databaseSelectImpcData(getProcedureImpcCode(), True, False)
      
      # Go through the inputs and if there is a climb_key match add the value
      inputLs = proc['inputs']
      for input in inputLs:
            inputKey = input['inputKey']
            impcCode = None
            for i, v in enumerate(metadataDefLs):
              if v[1] == inputKey: # If the climb key matches, store the IMPC code
                   impcCode = v[0] # For the input
                  
            if not impcCode == None:
              # Get the value from input
              if input['inputValue'] is not None:
                inputVal = input['inputValue'].strip()
                if len(inputVal) > 0:  # only if there is a value there.
                  if db.isExperimenterID(impcCode) == True:  # Can't use real names. Must insert numerical value
                    inputVal = db.databaseGetExperimenterIdCode(inputVal)
                  procedureNode = createMetadata(procedureNode, impcCode, inputVal)
      
      # Go through the outputs and if there is a climb_key match add the value
      # We have to do this because CLIMB and PFS do not allow importation of inputs so some matadata are outputs
      outputLs = proc['outputs']
      for output in outputLs:
            outputKey = output['outputKey']
            impcCode = None
            for i, v in enumerate(metadataDefLs):
              if v[1] == outputKey:
                   impcCode = v[0]
                    
            if not impcCode == None:
              if output['outputValue'] is not None:
                # Get the IMPC code from metadataDefLs and the value from input
                outputVal = str(output['outputValue']).strip()
                if len(outputVal) > 0: # only if there is a value there.
                  if db.isExperimenterID(impcCode) == True:  # Can't use real names. Must insert numerical value
                    outputVal = db.databaseGetExperimenterIdCode(outputVal)
                  
                  procedureNode = createMetadata(procedureNode, impcCode, outputVal)
              
      return procedureNode
    
def getProcedureStatusCode(proc:dict): 
  impc_status_code = ""
  if 'taskStatus' in proc and proc['taskStatus'] is not None:
    if proc['taskStatus'] in procedure_status_message_map:
      impc_status_code = procedure_status_message_map[proc['taskStatus']]
  
  return impc_status_code

# For adding to XML
def buildExperimentStatusCode(experimentNode, status_code):
  if status_code != '':
      status_node = ET.SubElement(experimentNode,'statusCode')
      status_node.text = status_code
      
  return experimentNode
  
def getOutputStatusCode(output:dict):
  impc_status_code = ""
  if 'statusCode' in output and \
      output['statusCode'] is not None and \
      output['statusCode'] in output_status_message_map:
        impc_status_code = output_status_message_map[output['statusCode']]
      
  return impc_status_code

def buildParameters(procedureNode,proc):
      # Get the data from the Outputs
      
      # Get short version of code e.g. BWT
      procedureImpcCode = extractThreeLetterCode(
                                                db.databaseSelectProcedureCode(proc['workflowTaskName']))
      
      # Returns a list of tuples (impccode, climb_key, dccType_key) from komp.cv_dcctypes
      parameterDefLs = db.databaseSelectImpcData(procedureImpcCode,False, False)
      
      # Now get the full code e.g. IMPC_BWT_001
      procedureImpcCode = db.databaseSelectProcedureCode(proc['workflowTaskName'])
      
      output_status_code = ''
      # Go through the outputs and if there is a climb_key match add the value
      outputLs = proc['outputs']
      # TBD - Sort by _DccType_key because simples must precede and series?
      for i, v in enumerate(parameterDefLs):
        impcCode = None
        dccType = None
        for output in outputLs:
          
          outputKey = output['outputKey']
          if v[1] == outputKey:
                  impcCode = v[0]
                  dccType = v[2]
                  break
                
        outputVal=None
        if not impcCode == None and output['outputValue'] is not None:
          # Get the IMPC code from metadataDefLs and the value from output
          outputVal = output['outputValue']
          output_status_code = getOutputStatusCode(output)
          
        if outputVal is None:
              continue
        if type(outputVal) != type(""): # TODO - Handle floats an ints
          outputVal = str(outputVal)    
        
        if len(outputVal) > 0:
          if dccType == 1:
              procedureNode = createSimpleParameter(procedureNode, impcCode, outputVal,output_status_code)
          elif dccType == 2: #  Ontology TBD
              procedureNode = createSimpleParameter(procedureNode, impcCode, outputVal,output_status_code)
          elif dccType == 3: # Media - ABR (014) and ERG (047)
              procedureNode = createSimpleParameter(procedureNode, impcCode, outputVal,output_status_code)
          elif dccType == 4: # Series 
              outputVal = outputVal.replace("\'","\"")  # TODO - will this handle VIABILITY?
              procedureNode = createSeriesParameter(procedureNode, impcCode, json.loads(json.dumps(outputVal)))
          elif dccType == 5: # SeriesMedia 
              taskKey = int(proc["taskInstanceKey"])
              procedureNode = createSeriesMediaParameter(procedureNode, impcCode, outputVal,procedureImpcCode,taskKey)
          elif dccType == 8:  # colony ids are stored as ouputs for line calls
                setColonyId(outputVal)
          elif dccType == 6: # MediaSample - unsupported
              print("MediaSample for an output type? Output key:" + str(outputKey))
          else:
              print("Metadata for an output? Output key:" + str(outputKey))
                    
              
      return procedureNode

# SPECIMEN
def generateSpecimenXML(animalInfoLs, centerNode):  # List of dictionaries
    if  animalInfoLs == None:
        return
      
    if len(animalInfoLs) == 0:
          return
    
    # Otherwise we have some data
   
    specimenRecord = {}
    # Hardcoded / constants
    specimenRecord["pipeline"] = 'JAX_001'
    specimenRecord["productionCenter"] = 'J'
    specimenRecord["phenotypingCenter"] = 'J'
    specimenRecord["project"] = 'JAX'
    
    for animalInfo in animalInfoLs:
      # Get the four entities
      animal = animalInfo["animal"]
      line = animalInfo["line"]
      litter = animalInfo["litter"]
      genotypes = animalInfo["genotypes"]   # List of dicts with keys genotypeKey, date, assay, genotype, modifiedBy, dateModified.
      
      specimenRecord["specimenID"] = animal["animalName"]
      if animal["dateBorn"] is not None:
        specimenRecord["dob"] = animal["dateBorn"][0:10]
      specimenRecord["gender"] = animal["sex"]
      specimenRecord["isBaseline"] = line["stock"] == '005304'
      if specimenRecord["isBaseline"] == False:
        specimenRecord["colonyId"]  = "JR" + line["stock"][1:6]
      else:
        specimenRecord["colonyId"]  = ""
      #specimenRecord["strainID"] = line["references"]
      specimenRecord["zygosity"] = extractGenotype(genotypes)   # must be present
      specimenRecord["litterId"] = litter['birthID']
      specimenRecord["generation"] = animal['generation']
      
      createSpecimenRecord(specimenRecord,centerNode,"")

    return # root

# UTILITIES
def getNextExperimentFilename(dataDir):
      filename = ''
      # The experiment filename has a format of
      # J.YYYY-MM-DD.NN.experiment.impc.xml
      filter = 'J.' + datetime.today().strftime('%Y-%m-%d') + '.{counterVal}.experiment.impc.xml'.format(counterVal='*')
      
      fileLs = glob.glob(dataDir + filter)
      max = 49
      
      for a in fileLs:
            parts = a.split('.')
            cntr = parts[2]
            if max < int(cntr):
                  max = int(cntr)
            
      newFileName = 'J.' + datetime.today().strftime('%Y-%m-%d') + '.{counterVal}.experiment.impc.xml'.format(counterVal=str(max+1))
      
      return dataDir + newFileName;

def getNextSpecimenFilename(dataDir):
    filename = ''
    # The specimen filename has a format of
    # J.YYYY-MM-DD.NN.specimen.impc.xml
    filter = 'J.' + datetime.today().strftime('%Y-%m-%d') + '.{counterVal}.specimen.impc.xml'.format(counterVal='*')
      
    fileLs = glob.glob(dataDir + filter)

    max = 0
      
    for a in fileLs:
      parts = a.split('.')
      cntr = parts[2]
      if max < int(cntr):
        max = int(cntr)
            
    newFileName = 'J.' + datetime.today().strftime('%Y-%m-%d') + '.{counterVal}.specimen.impc.xml'.format(counterVal='{:02d}'.format(max+1))
      
    return dataDir + newFileName;
  
# Take something like IMPC_BWT_001 and return BWT  
def extractThreeLetterCode(s):
      try:
        return s[(s.index('_') + 1):(s.index('_') + 4)]
      except ValueError:
        print("Could not resolve three letter code for" + s)
        return ""

""" 
genotypes = List of dicts with keys genotypeKey, date, assay, genotype, modifiedBy, dateModified.
"""

def extractGenotype(genotypes):
  zygosity = '?/?'
  for genotype in genotypes:
    if genotype["genotype"] == '+/+':
        zygosity = 'wild type'
    elif  genotype["genotype"] == '-/+' or genotype["genotype"] == '+/-' :
        zygosity  = 'heterozygous'
    elif genotype["genotype"] == '-/-':
        zygosity = 'homozygous'
    elif genotype["genotype"] == '-/Y':
        zygosity = 'hemizygous'
    elif genotype["genotype"] == '+/Y':
        zygosity = 'anzygous'
        
    return zygosity

lineCallProcedures = ["Viability E18.5 Secondary Screen", "Viability E15.5 Secondary Screen", 
                      "Viability E12.5 Secondary Screen", "Viability E9.5 Secondary Screen", 
                      "Fertility of Homozygous Knock-out Mice", "Viability Primary Screen v2"]

# Check it against a list of possible line-based procedures
def   procedureHasAnimals(climbFilter):
      
    taskName = climbFilter.get("taskInstance").get("workflowTaskName")
    hasAnimals = True
    if taskName in lineCallProcedures:
          hasAnimals = False
          
    return hasAnimals
  
def getAnimalNameFromTaskInfo(task):
  animalName = ''  # Not all tasks have animals
  if "animal" in task:
    animalName = task["animal"][0]["animalName"]  # This one does
  else:  # line based procedure. No animal - need JR number / colony ID
    animalName = findColonyId(task["taskInstance"][0])  # It' too bad but the colony id is stored at the output level rather than the task level. Thanks CLIMB!          
  return animalName

#pretty print method
def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem

def handleClimbData(filterFileName):
    # Get filter from file - temporary
    with open(filterFileName) as f:
      filterLines = f.read().splitlines()
      
    c.setWorkgroup()  # Inits CLIMB
    
    # Each line in the input file can be a filter and 
    #   can generate a specimen and experiment XML
    for climbFilter in filterLines:
      # Get the animals and validate
      results = c.getAnimalInfoFromFilter(json.loads(climbFilter))
      animalLs = results["animalInfo"]
      
      for animal in reversed(animalLs):  # Remove those animals that failed
        isValid = v.validateAnimal(animal)
        if isValid == False:
              animalLs.remove(animal)
      
      createSpecimenXML(animalLs) # With the remaining embryos that have passed
          
      # Using the same filter get the task data
      if procedureHasAnimals(json.loads(climbFilter)):  # i.e. not a line call like fertility
        results = c.getTaskInfoFromFilter(json.loads(climbFilter))    # For procs with animals
      else:
        results = c.getProceduresGivenFilter(json.loads(climbFilter))  # For line calls
      
      taskLs = results["taskInfo"]  # A list of dictionaries
      for task in reversed(taskLs):  # task should be a dictionary { "animal" : [], "taskInstance": []}
        success, message = v.validateProcedure(task)  # Sets the task status to 'Failed QC' if it fails.
        if success == False:
          taskLs.remove(task)  # Do not record it 
        elif success == True and task["taskInstance"][0]['taskStatus'] == 'Already submitted':
          taskLs.remove(task)  # Do not record it 
        else: # Record it as submitted
          animalName = getAnimalNameFromTaskInfo(task)
          if len(animalName) > 0: # Need a JR or animal name. 
            expFileName = getNextExperimentFilename(getDatadir()) # We get the exp filename now so we can log it as submitted.
            if len(task["taskInstance"]) > 0:
              db.recordSubmissionAttempt(expFileName.split('\\')[-1],animalName, task["taskInstance"][0], 
                                        getProcedureImpcCode(), v.getReviewedDate())
      
      #End of loop 
      createExperimentXML(taskLs,procedureHasAnimals(json.loads(climbFilter)))
      

def handlePfsData():
    # For CORE PFS komp mice
    
    animalLs = pfs.getPfsAnimalInfo()
    
    for animal in reversed(animalLs):  # Remove those animals that failed
        if v.validateAnimal(animal) == False:
              animalLs.remove(animal)
    
    createSpecimenXML(animalLs)
    
    # Now the procedures
    resultsLs = pfs.getPfsTaskInfo()  # This should return a list of lists where each element corresponds to an experiment type
    
    # We get the exp filename now so we can log it.
    expFileName = getNextExperimentFilename(getDatadir())
                
    for results in resultsLs:
      taskLs = results["taskInfo"]  # A list of dictionaries
      for task in reversed(taskLs):  # task should be a dictionary { "animal" : [], "taskInstance": []}
        animalName = ''  # Not all tasks have animals
        success, message = v.validateProcedure(task)  # Sets the task status to 'Failed QC' if it fails.
        if success == False:
            print("Rejected task: " + message)
            taskLs.remove(task)  # Do not record it 
            continue
          
      # OK. With list cleaned up, lets create the experiment XML
      createExperimentXML(taskLs, True)
      
      # task is a list of taskInstances but there will only be one for KOMP
      for task in taskLs:
        if len(task["taskInstance"]) > 0:
          animalName = task["animal"][0]["animalName"]
          db.recordSubmissionAttempt(expFileName.split('\\')[-1],animalName, task["taskInstance"][0], 
                                        getProcedureImpcCode(), v.getReviewedDate(task["taskInstance"][0]))
          # TODO - Update the EXPERIMENT status to "Data Sent to DCC"
     
      return

def handleJaxLimsData():
  try:
      mycfg = cfg.parse_config(path="config.yml")
      # Setup credentials for database
      impc_pipeline = mycfg['impc_pipeline']['pipeline']
      impc_proc_ls = mycfg['impc_proc_codes']['impc_code_list'].split(',')
      jax_study = mycfg['jax_study']['study']
      setDataDir(mycfg['directories']['dest'])
      
      all_mice = []
      pi_key_ls = []
      
      # For each procedure code in the list, generate an experient XML file
      for proc_code in impc_proc_ls:
        pi_key_ls, taskInstanceDictLs = db.getCombinedProcedureSpecimenData(proc_code,jax_study)
        createExperimentXML(taskInstanceDictLs,True)  # Second arg is 'experimentHasAnimals?'
        # TODO Record the submission
        # db.recordSubmissionAttempt(expFilename, animalName, taskInstance, procedure code, review date)
        all_mice.extend(pi_key_ls)

      
      animalLs = db.getMice(all_mice)
      for animal in reversed(animalLs):  # Remove those animals that failed
        if v.validateAnimal(animal) == False:
              animalLs.remove(animal)
              
      createSpecimenXML(animalLs)
      
  except Exception as e:
      print('handleJaxLimsData() failed')
      print(str(e))
  return    
    
def add_arguments(argparser):
    argparser.add_argument(
            '-f', '--filter_file', type=str, help='File that contains the filter for specimen and experiments', required=True
        )
    argparser.add_argument(
            '-s', '--source', type=str, help='Source for data, i.e. CLIMB or PFS', required=True
        )
    
    argparser.add_argument(
            '-i', '--images', type=str, help='Images folder', required=False  #TODO
        )
        
    args = argparser.parse_args()
    
    setDataSrc(args.source)
    setDataDir(args.datadir)
    
    g_filterFileName = args.filter_file
    g_image_dir = args.images
    
    return




if __name__ == '__main__':
  
    # Uncomment out the next two lines when running from the commandline
    #args = argparse.ArgumentParser()
    #add_arguments(args)
    # Otherwise, hard coded
    setDataDir("C:\\Users\\michaelm\\Source\\Workspaes\\Teams\\Lab Informatics\\JAXLIMS\\Main\\DccReporter\\data\\")
    setDataSrc('PFS')
    
    mycfg = cfg.parse_config(path="config.yml")
    # Setup properties for any of the three sources
    log_dir = mycfg['directories']['log_path']
      
    g_logger = createLogHandler(log_dir+'/xml-generator')  
    g_logger.info('Logger has been created')
	
    
    db.init()  # Create a db connection to JAXLIMS for IMPC codes and 
               # logging no matter what data source we are using.
    
    if getDataSrc() == 'CLIMB':
      handleClimbData()
    elif getDataSrc() == 'JAXLIMS':
      handleJaxLimsData()
    elif getDataSrc() == 'PFS':
      handlePfsData()
    else:
      print("The data source {0} is invalid. Must be CLIMB, JAXLIMS, or PFS".format(getDataSrc()))
      
    # All done
    db.close()      
    
  
    print("SUCCESS")
