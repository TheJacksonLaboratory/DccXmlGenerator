import query_database as db

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

# Is the procedure completed or cancelled? i.e. not 'Active'
def testTaskStatus(proc):
    # Assume it is active
    msg = "Task not set to Complete or Cancelled"
    success = False
    
    if proc["taskStatus"] == 'Complete' or proc["taskStatus"] == 'Cancelled':
        success = True
        msg = ''
        
    return success, msg

# Used to set the experimenter id
def setCollectedBy(output):
    global g_CollectedBy  
    if output["collectedBy"] != None:
        g_CollectedBy = output["collectedBy"]
    return

# Used to set the date of experiment
def setDateCollected(output):
    global g_DateCollected
    g_DateCollected = output["collectedDate"]
    return    


def getCollectedBy(output):
    global g_CollectedBy  
    return g_CollectedBy

def getDateCollected(output):
    global g_DateCollected
    return g_DateCollected

# Not really used but for now needs to have some value.
def setReviewedBy(proc):
    global g_ReviewedBy
    g_ReviewedBy = proc["reviewedBy"]

def getReviewedBy():
    global g_ReviewedBy
    return g_ReviewedBy

# Newer than the store date means it is a resubmission
def setReviewedDate(proc):
    global g_ReviewedDate
    g_ReviewedDate = proc["dateReviewed"]

def getReviewedDate():
    global g_ReviewedDate
    return g_ReviewedDate

# Have we submitted this successfully before?
# Look up the test in the database and compare reviewed dates
def testPreviouslySubmitted(proc):
    msg = ""
    return True, msg

# Is there a date of experiment?
def testCollectedDate(output):

    if output["collectedDate"]  == None or len(output["collectedDate"]) == 0:
        return False, "No collected date."
    
    setDateCollected(output)
    return True, ""

# Is there a date of experiment?
def testCollectedBy(output):
    
    if output["collectedBy"]  == None or len(output["collectedBy"]) == 0:
        return False, "No 'collected by' value."
    
    setCollectedBy(output)
    return True, ""

# make sure this has been reviewed by someone
def testReviewedBy(proc):
    if proc["reviewedBy"] == None or len(proc["reviewedBy"]) == 0:
        return False, "Review By is missing."
    
    # I need to set it as a global
    setReviewedBy(proc)
    setReviewedDate(proc)
    
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
    msg = ""
    success = True
    outputLs = proc["outputs"]
    if outputLs == None or len(outputLs) == 0:
        msg = "No outputs!"
        success = False
        return success, msg
    
    for output in outputLs:
        if testCollectedBy(output) == True:
            setCollectedBy(output)
        if testCollectedDate(output) == True:
            setDateCollected(output)
        
    return success, msg

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
        # Exclude assays we don't care about. 
        if "Generic" not in genotype["assay"] and "Sex Determination Assay" not in genotype["assay"]:
            zygosity = genotype["genotype"]
            assayName = genotype["assay"]
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
        
    if line["references"] == None or len(line["references"]) == 0:
        msg = msg + 'The References field is not set. It should containg the MGI reference for KOMP lines.' + ';'
        success = False    

          
    return success, msg

# Assumes all parameters are valid dictionaries with the keys required or None type 
def createLogEntry(animalInfo, procedureInfo, lineInfo, genotypeInfo, issueStr):

    msgDict = {"AnimalName":"", "TaskName":"", "TaskInstanceKey":0, "ImpcCode": "", "StockNumber":"", "DateDue":"", "Issue":"" }
    db.init()
    
    if animalInfo != None:
        msgDict["AnimalName"] = animalInfo["animalName"]
    else:
        msgDict["AnimalName"] = "N/A"
    
    if procedureInfo != None:
        msgDict["TaskName"] = procedureInfo["workflowTaskName"]
        msgDict["TaskInstanceKey"] = procedureInfo["taskInstanceKey"]
        #msgDict["ImpcCode"] = procedureInfo["impcCode"]
        msgDict["ImpcCode"] = 'TBD'
        msgDict["DateDue"] = procedureInfo["dateDue"]
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
    db.close()
    return

# A speciemen looks like { "animal": <dictionary>, "line": <dictionary>, "litter": <dictionary>, "genotypes": <list of dictionaries> }
def validateAnimal(specimen):
    successMouse = True
    successStockNumber = True
    # For writing to the database
    msgDict = {"AnimalName":"", "TaskName":"", "TaskInstanceKey":0, "ImpcCode": "", "StockNumber":"", "DateDue":"", "Issue":"" }
    msg = ""
    
    successMouse, msg = testMouseInfo(specimen)
   
    if successMouse == False:
        createLogEntry(specimen["animal"], None, specimen["line"], specimen["genotypes"], msg)

    return (successMouse and successStockNumber)

def validateProcedure(proc):
    
    specimenLs = proc["animal"]
    specimen = specimenLs[0]  # TODO - Handle multiple mice?
    lineInfo = { "stock" : specimen["stock"] }
    taskLs = proc["taskInstance"] 
    if len(taskLs) == 0:
        return "No task returned by query", False
    
    task = taskLs[0] # TODO - Handle multiple procedures?
    
    msg = ""
    
    overallMsg = ""
    overallSuccess = True
    
#    We don't need to do validateAnimal(). Each animal is evaluated separately    
#    success, msg = validateAnimal(specimen)
#    overallSuccess = overallSuccess and success
#    if len(msg) > 0:
#        overallMsg = overallMsg + "; " + msg
    
    success, msg = testOutputs(task)
    overallSuccess = overallSuccess and success
    if len(msg) > 0:
        overallMsg = overallMsg + "; " + msg
        
    success, msg = testReviewedBy(task)
    overallSuccess = overallSuccess and success
    if len(msg) > 0:
        overallMsg = overallMsg + "; " + msg
        
    success, msg = testPreviouslySubmitted(task)
    overallSuccess = overallSuccess and success
    if len(msg) > 0:
        overallMsg = overallMsg + "; " + msg
    
    success, msg = testTaskStatus(task)
    overallSuccess = overallSuccess and success
    if len(msg) > 0:
        overallMsg = overallMsg + "; " + msg
    
    print('Msg= ' + overallMsg)
    print('Success= ' + str(overallSuccess))
    
    #success, msg = testInputs(task) # Embryo lethal tasks were erronoeusly created with no inputs
    
    if overallSuccess == False:
        createLogEntry(specimen, task, lineInfo, None, overallMsg)
        task["taskStatus"]  = 'Failed QC'  # Local to this app
        
    return overallSuccess