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

from os import listdir
import glob
from os.path import isfile, join
import time

import xml.etree.ElementTree as ET
import Climb as c
import validate_procedure as v

g_ImpcCode = ""

def setProcedureImpcCode(code):
  global g_ImpcCode
  g_ImpcCode=code
      
def getProcedureImpcCode():
  global g_ImpcCode
  return g_ImpcCode

def getFtpServer():
      return 'ftp://bhjlk01.jax.org/'
    
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
    return  centerNode # center node

def createExperiment(centerNode, expName, expDate):
      
    experimentDictKeys = [ "experimentID", "dateOfExperiment" ]
    experimentDict = dict.fromkeys(experimentDictKeys)
    experimentDict["experimentID"] = expName
    experimentDict["dateOfExperiment"] = expDate
    experimentNode = ET.SubElement(centerNode, 'experiment', experimentDict)
    return experimentNode # experimentNode
		
def createSpecimen(experimentNode,animalName):
    specimenNode = ET.SubElement(experimentNode, 'specimenID')
    specimenNode.text = animalName
    return experimentNode # experimentNode

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
        
    return procedureNode # procedureNode

def createMetadata(procedureNode,impcCode, strVal):
    paramNode = ET.SubElement(procedureNode, 'procedureMetadata', { 'parameterID': '{code}'.format(code=impcCode)})
    valueNode = ET.SubElement(paramNode, 'value')
    valueNode.text = strVal
    return procedureNode # procedureNode

# <seriesMediaParameter parameterID="IMPC_XRY_048_001">
#    <value incrementValue="1" URI="ftp://images/image1.jpg" fileType="img/jpg">
#    <value incrementValue="1" URI="ftp://images/image1.jpg" fileType="img/jpg">
#</seriesMediaParameter>
# Must be included just before the metadata!!!
def createSeriesMediaParameter(procedureNode,impcCode, strVal,statusCode):
    
    # She has bad data for her images. Need to fix that first 
    #return procedureNode
  
    if len(strVal) == 0:
          return procedureNode
        
    imageLs = strVal.split()
    
    # Temporary kluge - she is putting "no" as the value of images when not present
    if len(imageLs) > 0 and (imageLs[0] == "no" or imageLs[0] == "yes"):
          return procedureNode
        
    paramNode = ET.SubElement(procedureNode, 'seriesMediaParameter', { 'parameterID': '{code}'.format(code=impcCode)})
    
    incrementValue = 1
    for image in imageLs:
      valueNode = ET.SubElement(paramNode, 'value')
      valueNode.text = "incrementValue=" + "\"" + str(incrementValue) + "\"" + " URI=\"" + getFtpServer() + impcCode + "/" + image + "\"" # Don't need the file type
      incrementValue += 1
    
    if len(statusCode) > 0:
        statusNode = ET.SubElement(paramNode,'statusCode')
        statusNode.text = statusCode
        
    return procedureNode # procedureNode
  
# TODO
def createSeriesParameter(procedureNode,impcCode, strVal,statusCode):
    return procedureNode

def createStatusCode(procedureNode, statusCode):
    statusNode = ET.SubElement(procedureNode, 'statusCode')
    statusNode.text = statusCode
    return procedureNode
  
def createSpecimenRecord(specimenRecord,specimenSetNode,statusCode):
  
  if v.validateMouseFields(specimenRecord) == True:
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

# KLUGE KLUGE KLUGE KLUGE KLUGE KLUGE because these tests were created with no inputs. Yuck
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
  # End of metadata kluge

# Create experiment XMLs
def generateExperimentXML(taskInfoLs, centerNode):
    # Given a dictionary parse out the animal info and the procedure info
    # It looks like "taskInfo" [ { "animal" [] , "taskInstance" : [] }, { "animal" [] , "taskInstance" : [] }, ...]
    # If an animal has multiple procedures the animal will only appear once.
    # Get the list of mouse info. For KOMP it should always be 1 element
    
    #taskInfoLs = resultsPackage["taskInfo"]
    if taskInfoLs == None:
          return 0
    
    # Else we have some data
    db.init() # Create database connection for IMPC codes
    
    numberOfProcs = 0
    for exps in taskInfoLs:
        mouseInfoLs = exps["animal"]   # 
        for mouseInfo in mouseInfoLs:
          procLs = exps["taskInstance"]
          for proc in procLs:
            if proc["taskStatus"]  == "Failed QC" or proc["taskStatus"]  == "Already submitted":
                  continue # We failed it or we've already submitted it.
            
            # for each procedure in the list build up the XML
            numberOfProcs += 1
            # # root node
            experimentNode = createExperiment(centerNode,(proc['workflowTaskName'] + ' - ' +  mouseInfo['animalName'] + ' - ' + str(proc["taskInstanceKey"])), proc['dateComplete']) # TODO Add in task key
            experimentNode = createSpecimen(experimentNode,mouseInfo['animalName'])
            procedureNode = createProcedure(experimentNode,db.databaseSelectProcedureCode(proc['workflowTaskName']))
            
            # Now create the metadata from the inputs and outputs
            procedureNode = buildParameters(procedureNode,proc)
            procedureNode = buildMetadata(procedureNode,proc)
    
    db.close()
    return numberOfProcs

def buildMetadata(procedureNode,proc):
      
      # Ugly - If there are no inputs then this may be an embryo lethal ask that was unfortunately created with no inputs.
      if len(proc['inputs']) == 0:
            embryoKluge(proc['workflowTaskName'],procedureNode)
            return procedureNode
          
      # Returns a list of tuples (impccode, climb_key, dccType_key)
      setProcedureImpcCode(extractThreeLetterCode(db.databaseSelectProcedureCode(proc['workflowTaskName'])))
      metadataDefLs = db.databaseSelectImpcData(getProcedureImpcCode(), True, True)
      
      # Merge with metadata from the outputs
      metadataDefLs = metadataDefLs + db.databaseSelectImpcData(getProcedureImpcCode(), True, False)
      
      # Go through the inputs and if there is a climb_key match add the value
      inputLs = proc['inputs']
      for input in inputLs:
            inputKey = input['inputKey']
            impcCode = None
            for i, v in enumerate(metadataDefLs):
              if v[1] == inputKey:
                   impcCode = v[0]
                  
            if not impcCode == None:
              # Get the IMPC code from metadataDefLs and the value from input
              if input['inputValue'] is not None:
                inputVal = input['inputValue'].strip()
                if len(inputVal) > 0:  # only if there is a value there.
                  if db.isExperimenterID(impcCode) == True:
                    inputVal = db.databaseGetExperimenterIdCode(inputVal)
                  procedureNode = createMetadata(procedureNode, impcCode, inputVal)
      
      # Go through the outputs and if there is a climb_key match add the value
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
      # Get the metadata from the Inputs
      # Returns a list of tuples (impccode, climb_key, dccType_key)
      parameterDefLs = db.databaseSelectImpcData(extractThreeLetterCode(
                                                db.databaseSelectProcedureCode(proc['workflowTaskName'])), 
                                                False, False)
      
      # Go through the inputs an if there is a climb_key match add the value
      outputLs = proc['outputs']
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
          # Get the IMPC code from metadataDefLs and the value from input
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
                procedureNode = createSeriesMediaParameter(procedureNode, impcCode, outputVal,"")
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
    
    # Else we have some data
    db.init() # Create database connection
    
    animalInfoGroup = animalInfoLs["animalInfo"]
   
    specimenRecord = {}
    # Hardcoded / constants
    specimenRecord["pipeline"] = 'JAX_001'
    specimenRecord["productionCenter"] = 'J'
    specimenRecord["phenotypingCenter"] = 'J'
    specimenRecord["project"] = 'JAX'
    
    for animalInfo in animalInfoGroup:
      # Get the four entities
      animal = animalInfo["animal"]
      line = animalInfo["line"]
      litter = animalInfo["litter"]
      genotypes = animalInfo["genotypes"]
      
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
      
      createSpecimenRecord(specimenRecord,centerNode,"")

    db.close()
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
    
def getImpcInfoGivenTypeKey(key, isOutput):
    return # a dictionary of information about this type

def validateMandatoryParameters():
    return

def validateMetadata():
    return

# Take something like IMPC_BWT_001 and return BWT  
def extractThreeLetterCode(s):
      try:
        return s[(s.index('_') + 1):(s.index('_') + 4)]
      except ValueError:
        return ""

def extractGenotype(genotypes):
      
  zygosity = '-/+'
  # Need algorithm to return the real zygosity
  #    and convert it to human readable string
  
  if zygosity == '+/+':
       zygosity = 'wild type'
  elif  zygosity == '-/+' or zygosity == '+/-' :
      zygosity  = 'heterozygous'
  elif zygosity == '-/-':
      zygosity = 'homozygous'
  elif zygosity == '-/Y':
      zygosity = 'hemizygous'
  return zygosity

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

animalStr = ""
dataDir = "C:\\Users\\michaelm\\Source\\Workspaes\\Teams\\Lab Informatics\\JAXLIMS\\Main\\DccReporter\\data\\"
resultsStr = ""

if __name__ == '__main__':
    ### Get task info based on the given filter
    # Get filter from file - temporary
    with open("filters.json") as f:
      filterLines = f.read().splitlines()
    
    for climbFilter in filterLines:
      # Start the new specimen XML file
      root = createSpecimenRoot()
      centerNode = createSpecimenCentre(root)
      
      # Get the animals and validate
      results = c.getAnimalInfoFromFilter(json.loads(climbFilter))
      # TODO Check for None or no animalInfo
      animalLs = results["animalInfo"]
      for animal in animalLs:
        isValid = v.validateAnimal(animal)
        if isValid == False:
              animalLs.remove(animal)
            
      # Generate the specimen portion of the XML  
      generateSpecimenXML(results, centerNode)
      tree = ET.ElementTree(indent(root))
      specimenFileName = getNextSpecimenFilename(dataDir)
      tree.write(specimenFileName, xml_declaration=True, encoding='utf-8')
      
      
      
      # Start the new XML file
      root = createProcedureRoot()
      centerNode = createCentre(root)
      
      expFileName = getNextExperimentFilename(dataDir)
      results = c.getTaskInfoFromFilter(json.loads(climbFilter))
      
      db.init()
      
      print(results)
      
      taskLs = results["taskInfo"]   # TODO Cycle through
      for task in taskLs:
        success, message = v.validateProcedure(task)  # Sets the task status to 'Failed QC' if it fails.
        if success == False:
            print("Rejected task: " + message)
        else:
            if len(task["animal"]) > 0 and len(task["taskInstance"]) > 0:
              db.recordSubmissionAttempt(expFileName.split('\\')[-1],task["animal"][0], task["taskInstance"][0], 
                                        getProcedureImpcCode(), v.getReviewedDate())
      
      numberOfProcs = generateExperimentXML(taskLs, centerNode)
      
      db.close()
      if(numberOfProcs > 0):      
        tree = ET.ElementTree(indent(root))
        tree.write(expFileName, xml_declaration=True, encoding='utf-8')
          
    
  
    print("SUCCESS")
