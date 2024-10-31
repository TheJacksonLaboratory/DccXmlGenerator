import jaxlims_api as db
from datetime import datetime

"""
This module runs the IMPC specific validation for mice and procedures
based on a number of business rules.

Most return a tuple of pass/fail and a message 

The caller should catch any exception and continue 
processing.
"""

# Globals that are pulled out of the results and stored for later use in building the XML.
g_CollectedBy = ""      #i.e. Experimenter ID
g_DateCollected = ""    # date of test
g_ReviewedBy = ""       # Reviewer - means the task has ben review
g_ReviewedDate = ""     # We store the reviewed date and if the new one is newer we submit it. Else we ignore it.
g_colonyId = ""         # We store the JR number as the colonyID for building the XML and recording the submission for line based calls.

# Is the procedure completed or cancelled? i.e. not 'Active'
def testTaskStatus(proc):
    # Assume it is active
    # TODO - What about a dash?
    msg = ''
    success = True
    
    if proc["taskStatus"] == 'Active':  # or task status == NULL? would that work for CLIMB?
        success = False
        msg = 'Task status is not complete or cancelled.'
        
    return success, msg


# Is there a date of experiment?
def testCollectedDate(output):

    if output["collectedDate"]  == None or len(output["collectedDate"]) == 0:
        return False, "No collected date."
    
    #setDateCollected(output)
    return True, ""

# Is there a collectedBy value, i.e. experimneterID?
def testCollectedBy(output):
    
    if output["collectedBy"]  == None or len(output["collectedBy"]) == 0:
        return False, "No 'collected by' value."
    
    #setCollectedBy(output)
    return True, ""

# make sure this has been reviewed by someone
def testReviewedBy(proc):
    if proc["reviewedBy"] == None or len(proc["reviewedBy"]) == 0:
        return False, "Review By is missing."
    
    # I need to set it as a global
    #setReviewedBy(proc)
    #setReviewedDate(proc)
    
    return True, ""

# Are all inputs set? 
def testInputs(proc):
    msg = ""
    success = True
    inputLs = proc["inputs"]
    if inputLs == None or len(inputLs) == 0:
        msg = "No inputs!"
        success = False

    return success, msg

# Are all outputs set? 
def testOutputs(proc):
    # This function assumes that the validity of individual outputs are already done
    msg = ""
    success = True
    if "outputs" not in proc.keys():
        return False, "No outputs!" # TODO - This is a bug in the API
    
    outputLs = proc["outputs"]
    if outputLs == None or len(outputLs) == 0:
        msg = "No outputs!"
        success = False
        return success, msg
    
    for output in outputLs:  # TODO - testCollectedXXX returns a tuple, not a boolean. If success setCollectedXXX will be called
        keystr = ''
        if "outputName" in output.keys():
            keystr = "outputName"   # CLIMB
        elif "name" in output.keys():
            keystr = "name"   # the others
            
        if db.isRequired(output[keystr]):
            if (output['outputValue'] == None or output['outputValue'] == ''):
                if 'statusCode' in output.keys() == False: # Is there a statusCode field? No
                    success = False
                    msg = "Missing mandatory parameter " + output[keystr]
                elif len(output['statusCode'])== 0:  # Status code field but no code
                    success = False
                    msg = "Missing mandatory parameter " + output[keystr]
                
                
        ok, err = testCollectedBy(output) 
        success = (ok and success)
        msg = msg + err
        
        ok, err = testCollectedDate(output)
        success = (ok and success)
        msg = msg + err
        
        output['outputValue'] = validateSeriesType(output)
       
    return success, msg
def validateSeriesType(output):
    # TODO - if it is a series or mediaSeries it must be a dict 
    return output["outputValue"]
   
def validateMouseFields(specimenRecord):
      msg = ""
      msgDict = { "AnimalName":"", "TaskName":"", "TaskInstanceKey":0, "ImpcCode":"", "StockNumber":"", "DateDue":"", "Issue":"" }
      
      # Make sure all the mandatory fields are present
      # May be empty if checkForValue(specimenRecord["colonyId"]) == False:
      #      msg = " Colony ID missing" + str(specimenRecord)
      #if checkForValue(specimenRecord["strainID"]) == False:
      #      msg = msg + " strain ID missing" + str(specimenRecord)
      if checkForValue(specimenRecord["specimenID"]) == False:
            msg = " specimen ID missing" + str(specimenRecord)
      if checkForValue(specimenRecord["gender"]) == False:
            msg = msg +  " gender missing" + str(specimenRecord)
      if checkForValue(specimenRecord["zygosity"]) == False:
            msg = msg +  " zygosity missing" + str(specimenRecord)
      if checkForValue(specimenRecord["pipeline"]) == False:
            msg = msg +  " pipeline ID missing" + str(specimenRecord)
      if checkForValue(specimenRecord["productionCenter"]) == False:
            msg = msg +  " production center ID missing" + str(specimenRecord)
      if checkForValue(specimenRecord["phenotypingCenter"]) == False:
            msg = msg +  " phenotyping ID missing" + str(specimenRecord)
      if checkForValue(specimenRecord["project"]) == False:
            msg = msg +  " project ID missing" + str(specimenRecord)
      
      if len(msg) == 0:
        return True
      else:
        msgDict["AnimalName"] = specimenRecord["specimenID"]
        #msgDict["StockNumber"] = specimenRecord["strainID"]
        msgDict["Issue"] = msg
        db.databaseInsertQualityErrorMessage(msgDict)
        return False
   
    
def checkForValue(valuestr):
      if valuestr is not None and len(valuestr) > 0:
            return True
      else:
            return False
          
# Is there a mouse? It needs sex, generation and genotypes
def testMouseInfo(animal):
    # Does it have a generation? Sex? Name?
    result = True
    msg = ""
    if animal == None:
        msg = "No mouse to test!"
        result = False
    
    animalInfo = animal["animal"]
        
    if animalInfo["animalName"] == None or len(animalInfo["animalName"]) == 0:
        msg += " No mouse name."
        result = False

    if animalInfo["generation"] == None or len(animalInfo["generation"]) == 0:
        msg = " No mouse generation."
        result = False         
    
    if animalInfo["dateBorn"] == None or len(animalInfo["dateBorn"]) == 0:
        msg = " No birth date."
        result = False         
        
    if animalInfo["sex"] == None or len(animalInfo["sex"]) == 0:
        msg = " No mouse sex."
        result = False
    
    assayName = ''
    zygosity = ''
    genotypeInfo = animal["genotypes"]
    genotypeResult, genotypeMsg, assayName, zygosity = testGenotypeInfo(genotypeInfo)
    if genotypeResult == False:
        result = False
        msg += " " + genotypeMsg
    
    lineInfo = animal["line"]
    lineResult, lineMsg = testLineInfo(lineInfo)
    if lineResult == False:
        result = False
        msg += " " + lineMsg
    
    return result, msg

# Is there a genotype? Not in the taskInstance information 
def testGenotypeInfo(genotypes):
    
    msg = "No KOMP assay name"
    success = False
    zygosity = "none"
    assayName = "none"
    for genotype in genotypes:
        if not genotype["assay"] == None:
            # Exclude assays we don't care about. 
            if "Generic" not in genotype["assay"] and "Sex Determination Assay" not in genotype["assay"]:
                zygosity = genotype["genotype"]
                assayName = genotype["assay"]
                if zygosity not in ['-/-','-/+','+/-','-/Y','+/+','+/Y']:
                    success = False
                    msg = 'Zygostiy {zygosity} is invalid.'.format(zygosity=zygosity)
                else:
                    success = True
                    msg = ""
    
    return success, msg, assayName, zygosity

# Is there a line with  StockNumber and Reference?
def testLineInfo(line):
    msg = ""
    success = True
    
    legalLineStatus = [ 'KOMP Active', 'KOMP Complete', 'Embryo Lethal Complete', 'Embryo Lethal Active' ]
    
    if line["stock"] == None or len(line["stock"]) == 0:
        msg = 'StockNumber is not set for ' + line["name"] + ';'
        success = False

# BUG - Our code is not returning lineStatus    
#    if not line["lineStatus"] in legalLineStatus:
#        msg = msg + str(line["name"]) + ' status is not in supported list of ' + str(legalLineStatus) + ';'
#        success = False   
        
#    if line["references"] == None or len(line["references"]) == 0:
#        msg = msg + 'The References field is not set. It should containg the MGI reference for KOMP lines.' + ';'
#        success = False    

          
    return success, msg

# Assumes all parameters are valid dictionaries with the keys required or None type 
def createLogEntry(animalInfo, procedureInfo, lineInfo, genotypeInfo, issueStr):

    msgDict = {"AnimalName":"", "TaskName":"", "TaskInstanceKey":0, "ImpcCode": "", "StockNumber":"", "DateDue":"", "Issue":"" }
    
    if animalInfo != None:
        msgDict["AnimalName"] = animalInfo["animalName"]
    else:
        msgDict["AnimalName"] = "N/A"
    
    if procedureInfo != None:
        msgDict["TaskName"] = procedureInfo["workflowTaskName"]
        msgDict["TaskInstanceKey"] = procedureInfo["taskInstanceKey"]
        #msgDict["ImpcCode"] = procedureInfo["impcCode"]
        msgDict["ImpcCode"] = 'TBD'
        # msgDict["DateDue"] = procedureInfo["dateDue"]  # TODO Not in dict
    else:
        msgDict["TaskName"] = "N/A"
        msgDict["TaskInstanceKey"] = 0
        msgDict["ImpcCode"] = "N/A"
        msgDict["DateDue"] = "1900-01-01"
    
    if lineInfo != None:    
        msgDict["StockNumber"] = lineInfo["stock"]
    else:
        msgDict["StockNumber"] = "N/A"
        
    msgDict["Issue"] = issueStr
    
    db.databaseInsertQualityErrorMessage(msgDict)
    return

# A speciemen looks like { "animal": <dictionary>, "line": <dictionary>, "litter": <dictionary>, "genotypes": <list of dictionaries> }
def validateAnimal(specimen):
    successMouse = True
    successStockNumber = True
    # For writing to the database
    msg = ""
    
    successMouse, msg = testMouseInfo(specimen)
   
    if successMouse == False:
        createLogEntry(specimen["animal"], None, specimen["line"], specimen["genotypes"], msg)

    return (successMouse and successStockNumber)

def validateProcedure(proc):
    
    lineInfo = None
    specimen = None
    if "animal" in proc:
        specimenLs = proc["animal"]
        specimen = specimenLs[0]  # TODO - Handle multiple mice?
        #lineInfo = { "stock" : specimen["stock"] }  # TODO Specimen has no stock number??
        
    taskLs = proc["taskInstance"] 
    if len(taskLs) == 0:
        return False,"No task returned by query" 
    
    task = taskLs[0] # TODO - Handle multiple procedures?
    
    msg = ""
    overallMsg = ""
    overallSuccess = True
  
    success, msg = testOutputs(task)
    overallSuccess = overallSuccess and success
    if len(msg) > 0:
        overallMsg = overallMsg + "; " + msg
        
    success, msg = testReviewedBy(task)
    overallSuccess = overallSuccess and success
    if len(msg) > 0:
        overallMsg = overallMsg + "; " + msg
        
    #success, msg = testPreviouslySubmitted(task) # TODO This is a no-op
    #overallSuccess = overallSuccess and success
    #if len(msg) > 0:
    #    overallMsg = overallMsg + "; " + msg
    
    success, msg = testTaskStatus(task)
    overallSuccess = overallSuccess and success
    if len(msg) > 0:
        overallMsg = overallMsg + "; " + msg
    
    #success, msg = testInputs(task) # Embryo lethal tasks were erronoeusly created with no inputs
    
    if task['dateComplete'] == None or len(task['dateComplete']) == 0:
        overallSuccess = False
        overallMsg = overallMsg + "; " + "No completion date"
        
    # TBD - Need to task key  for line submissions
    #lastReviewedDate = db.getLastReviewedDate(specimen["animalName"],task["workflowTaskName"])
    lastReviewedDate = db.getLastReviewedDate(task["taskInstanceKey"])
    reviewedDateStr = task["dateReviewed"]
    if reviewedDateStr != None and len(reviewedDateStr) > 0:
        currentReviewedDate = datetime.strptime(reviewedDateStr, "%Y-%m-%d")
    else:
        overallMsg = overallMsg + " No Reviewed Date task."
        overallSuccess = False
        
    # Exclude those we have already successfully uploaded
    if lastReviewedDate is not None and currentReviewedDate is not None:
        if lastReviewedDate >= currentReviewedDate:  # Is the SME resubmitting this procedure?
            print("Already submitted but submitting anyway.")
            #task["taskStatus"]  = 'Already submitted'  # else remove the Complete or Cancelled status to avoid unnecessary resubmission
            #createLogEntry(specimen, task, lineInfo, None, overallMsg + ' *Already submitted')
      
    if overallSuccess == False:
        createLogEntry(specimen, task, lineInfo, None, overallMsg)
        task["taskStatus"]  = 'Failed QC'  # Local to this app
    
    return overallSuccess, overallMsg