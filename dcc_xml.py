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
import sys
import shutil
import itertools
import json
import query_database as db

from datetime import datetime
from zipfile import ZipFile

from os import listdir
import glob
from os.path import isfile, join, basename
import time

import xml.etree.ElementTree as ET
import Climb as c
import validate_procedure as v

g_ImpcCode = ''
g_ColonyId =''

# Globals
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

def getBackgroundStrainId():
  return 'MGI:3056279'


# By convention if a task with no mice needs to record the line
#   then she stores it in an output named "JR". But she only stores the five digit code
def findColonyId(proc):
      outputLs = proc['outputs']
      for output in outputLs:
        if output["outputName"] == 'JR':           
          setColonyId(output["outputName"] + output["outputValue"])

# TODO - get from YAML file            
def getDatadir():
      return "C:\\Users\\michaelm\\Source\\Workspaes\\Teams\\Lab Informatics\\JAXLIMS\\Main\\DccReporter\\data\\"

def getFtpServer():
      return 'sftp://bhjlk02lp.jax.org/'
    
# XML XML XML
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

def createSimpleParameter(procedureNode,impcCode, strVal,statusCode):
    paramNode = ET.SubElement(procedureNode, 'simpleParameter', { 'parameterID': '{code}'.format(code=impcCode)})
    valueNode = ET.SubElement(paramNode, 'value')
    valueNode.text = strVal
    if len(statusCode) > 0:
        statusNode = ET.SubElement(paramNode,'statusCode')
        statusNode.text = statusCode
        
    return procedureNode

def createMetadata(procedureNode,impcCode, strVal):
    paramNode = ET.SubElement(procedureNode, 'procedureMetadata', { 'parameterID': '{code}'.format(code=impcCode)})
    valueNode = ET.SubElement(paramNode, 'value')
    valueNode.text = strVal
    return procedureNode

# <seriesMediaParameter parameterID="IMPC_XRY_048_001">
#    <value incrementValue="1" URI="ftp://images/image1.jpg" fileType="img/jpg">
#    <value incrementValue="1" URI="ftp://images/image1.jpg" fileType="img/jpg">
#</seriesMediaParameter>
# Must be included just before the metadata!!!
def createSeriesMediaParameter(procedureNode,impcCode, strVal,statusCode, directoryName):
      
    if len(strVal) == 0:
          return procedureNode # bail
        
    imageLs = strVal.split()
    
    # Temporary kluge - she is putting "no" as the value of images when not present
    if len(imageLs) > 0 and (imageLs[0] == "no" or imageLs[0] == "yes"):
          return procedureNode # bail
        
    paramNode = ET.SubElement(procedureNode, 'seriesMediaParameter', { 'parameterID': '{code}'.format(code=impcCode)})
    
    incrementValue = 1  # We only support startig from 1 for now. May need to get smarter.
                        # The values are stored in KOMP.DccParameterDetails.
    for image in imageLs:
      filenameSplit = image.split('\\')
      filenameOnly = filenameSplit[len(filenameSplit)-1]
      valueNode = ET.SubElement(paramNode, 'value', {'incrementValue': str(incrementValue), 'URI': getFtpServer() + directoryName + "/" + filenameOnly})
      incrementValue += 1
    
    if len(statusCode) > 0:
        statusNode = ET.SubElement(paramNode,'statusCode')
        statusNode.text = statusCode
        
    return procedureNode # procedureNode
  
# e.g. for Primary Viability
"""
  <seriesParameter parameterID="IMPC_VIA_037_001">
                    <value incrementValue="litterID1">RIKEN-Rln1-AB5_01</value>
                    <value incrementValue="litterID2">RIKEN-Rln1-AB5_01</value>
                    <value incrementValue="litterID3">RIKEN-Rln1-AB5_03</value>
                </seriesParameter>
"""
def createSeriesParameter(procedureNode,impcCode, strVal,statusCode):    
    if len(strVal) == 0:
          return procedureNode # bail
  
    paramNode = ET.SubElement(procedureNode, 'seriesParameter', { 'parameterID': '{code}'.format(code=impcCode)})
    
    incrementValue = 'litterID1'   # TODO - make smarter 
    valueNode = ET.SubElement(paramNode, 'value', {'incrementValue': incrementValue})
    valueNode.text = strVal
    
    if len(statusCode) > 0:
        statusNode = ET.SubElement(paramNode,'statusCode')
        statusNode.text = statusCode
        
    return procedureNode # procedureNode

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
                              'strainID': '{strainID}'.format(strainID=getBackgroundStrainId()),
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
                              'strainID': '{strainID}'.format(strainID=specimenRecord["strainID"]),
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
          
          # for each procedure in the list build up the XML
          numberOfProcs += 1
          # for line calls we need the colony ID. This is recorded in CLIMB as an output with the name "JR"
          #   It is a five digit number preceded by "JR"
          findColonyId(proc)
          
          #experimentNode = createExperiment(centerNode,(proc['workflowTaskName'] + ' - ' + str(proc["taskInstanceKey"])), proc['dateComplete']) # TODO Add in task key
          #experimentNode = createColonyId(experimentNode,getColonyId())
          lineNode = createColonyId(centerNode,getColonyId())
          procedureNode = createProcedure(lineNode,db.databaseSelectProcedureCode(proc['workflowTaskName']))
          
          # Now create the metadata from the inputs and outputs
          procedureNode = buildParameters(procedureNode,proc)
          
          procedureNode = buildMetadata(procedureNode,proc)
          # Clear the colony Id
          setColonyId('')
          
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
      # We have to do this because CLIMB does not allow importation of inputs so some matadata are outputs
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
                outputVal = output['outputValue'].strip()
                if len(outputVal) > 0: # only if there is a value there.
                  procedureNode = createMetadata(procedureNode, impcCode, outputVal)
              
      return procedureNode
    
def buildParameters(procedureNode,proc):
      # Get the data from the Outputs
      
      # Get short version of code e.g. BWT
      procedureImpcCode = extractThreeLetterCode(
                                                db.databaseSelectProcedureCode(proc['workflowTaskName']))
      
      # Returns a list of tuples (impccode, climb_key, dccType_key) from komp.cv_dcctypes
      parameterDefLs = db.databaseSelectImpcData(procedureImpcCode,False, False)
      
      # Now get the full code e.g. IMPC_BWT_001
      procedureImpcCode = db.databaseSelectProcedureCode(proc['workflowTaskName'])
      
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
          
        if outputVal is None:
              continue
              
        if len(outputVal.strip()) > 0:
          if dccType == 1:
              procedureNode = createSimpleParameter(procedureNode, impcCode, outputVal,"")
          elif dccType == 2: #  Ontology TBD
              procedureNode = createSimpleParameter(procedureNode, impcCode, outputVal,"")
          elif dccType == 3: # Media - ABR (014) and ERG (047)
              procedureNode = createSimpleParameter(procedureNode, impcCode, outputVal,"")
          elif dccType == 4: # Series TBD 
              procedureNode = createSeriesParameter(procedureNode, impcCode, outputVal,"")
          elif dccType == 5: # SeriesMedia  TBD
              procedureNode = createSeriesMediaParameter(procedureNode, impcCode, outputVal,"",procedureImpcCode)
          elif dccType == 8:  # colony ids are stored as ouputs for line calls
                setColonyId(outputVal)
          elif dccType == 6: # MediaSample - unsupported
              print("MediaSample for an output type? Output key:" + str(outputKey))
          else:
              print("Metadata for an output? Output key:" + str(outputKey))
                    
              
      return procedureNode
    
def orig_buildParameters(procedureNode,proc):
      # Get the data from the Outputs
      
      # Get short version of code e.g. BWT
      procedureImpcCode = extractThreeLetterCode(
                                                db.databaseSelectProcedureCode(proc['workflowTaskName']))
      
      # Returns a list of tuples (impccode, climb_key, dccType_key)
      parameterDefLs = db.databaseSelectImpcData(procedureImpcCode,False, False)
      
      # Now get the full code e.g. IMPC_BWT_001
      procedureImpcCode = db.databaseSelectProcedureCode(proc['workflowTaskName'])
      
      # Go through the outputs an if there is a climb_key match add the value
      outputLs = proc['outputs']
      # TBD - Sort by _DccType_key because simples must precede and series?
      for output in outputLs:
        outputKey = output['outputKey']
        impcCode = None
        dccType = None
        for i, v in enumerate(parameterDefLs):
          if v[1] == outputKey:
                impcCode = v[0]
                dccType = v[2]
                break
        
        if not impcCode == None and output['outputValue'] is not None:
          # Get the IMPC code from metadataDefLs and the value from output
          outputVal = output['outputValue']
          
          if outputVal is None:
                continue
              
          if len(outputVal.strip()) > 0:
            if dccType == 1:
                procedureNode = createSimpleParameter(procedureNode, impcCode, outputVal,"")
            elif dccType == 2: #  Ontology TBD
                procedureNode = createSimpleParameter(procedureNode, impcCode, outputVal,"")
            elif dccType == 3: # Media - ABR (014) and ERG (047)
                procedureNode = createSimpleParameter(procedureNode, impcCode, outputVal,"")
            elif dccType == 4: # Series TBD 
                procedureNode = createSeriesParameter(procedureNode, impcCode, outputVal,"")
            elif dccType == 5: # SeriesMedia  TBD
                procedureNode = createSeriesMediaParameter(procedureNode, impcCode, outputVal,"",procedureImpcCode)
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
    #animalInfoGroup = animalInfoLs["animalInfo"]
   
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
      specimenRecord["dob"] = animal["dateBorn"][0:10]
      specimenRecord["gender"] = animal["sex"]
      specimenRecord["isBaseline"] = line["stock"] == '005304'
      if specimenRecord["isBaseline"] == False:
        specimenRecord["colonyId"]  = "JR" + line["stock"][1:6]
      else:
        specimenRecord["colonyId"]  = ""
      specimenRecord["strainID"] = line["references"]
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
        return ""

""" 
genotypes = List of dicts with keys genotypeKey, date, assay, genotype, modifiedBy, dateModified.
"""

def extractGenotype(genotypes):
  zygosity = '?/?'
  for genotype in genotypes:
    if genotype["genotype"] == '+/+':
        zygosity = 'wild type'
    elif  genotype["genotype"] == '-/+' or zygosity == '+/-' :
        zygosity  = 'heterozygous'
    elif genotype["genotype"] == '-/-':
        zygosity = 'homozygous'
    elif genotype["genotype"] == '-/Y':
        zygosity = 'hemizygous'
        
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


if __name__ == '__main__':
    ### Get task info based on the given filter
    # Get filter from file - temporary
    #with open("filters-with-mice.json") as f:
    with open("filters.json") as f:
      filterLines = f.read().splitlines()
    
    db.init()  # Create a db connection for IMPC codes and logging
    
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
            
      # Generate the specimen portion of the XML  
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
        
      

      # Using the same filter get the task data
      if procedureHasAnimals(json.loads(climbFilter)): 
        results = c.getTaskInfoFromFilter(json.loads(climbFilter))    # For procs with animals
      else:
        results = c.getProceduresGivenFilter(json.loads(climbFilter))  # For line calls
      
      # We get the exp filename now so we can log it.
      expFileName = getNextExperimentFilename(getDatadir())
      
      taskLs = results["taskInfo"]   # A list of dictionaries
      for task in taskLs:  # task should be a dictionary { "animal" : [], "taskInstance": []}
        success, message = v.validateProcedure(task)  # Sets the task status to 'Failed QC' if it fails.
        if success == False:
            print("Rejected task: " + message)
        else:
            animalName = ''  # Not all tasks have animals
            if "animal" in task:
                animalName = task["animal"][0]["animalName"]
                  
            if len(task["taskInstance"]) > 0:
              db.recordSubmissionAttempt(expFileName.split('\\')[-1],animalName, task["taskInstance"][0], 
                                        getProcedureImpcCode(), v.getReviewedDate())
      
      root = createProcedureRoot()
      centerNode = createCentre(root)
      
      if procedureHasAnimals(json.loads(climbFilter)):
            numberOfProcs = generateExperimentXML(taskLs, centerNode) 
      else:
            numberOfProcs = generateLineCallExperimentXML(taskLs, centerNode)
      
      
      if(numberOfProcs > 0):      # write the new XML file
        tree = ET.ElementTree(indent(root))
        tree.write(expFileName, xml_declaration=True, encoding='utf-8')
        
        # Now zip it up.
        zipfilename = expFileName.replace('experiment.','').replace('xml','zip')
        with ZipFile(zipfilename,'w') as zipper:
          zipper.write(expFileName,basename(expFileName))
          zipper.close()
    # End of filter loop
    
    # All done
    db.close()      
    
  
    print("SUCCESS")
