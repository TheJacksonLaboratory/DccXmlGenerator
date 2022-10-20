import query_database as db

"""
This module runs the IMPC specific validate a procedure
based on a number of business rules.

They throw an exception if the test fails.
The caller should catch the exception and continue 
processing.
"""
g_CollectedBy = ""
g_DateCollected = ""

# Is the procedure completed or cancelled? i.e. not 'Active'
def testTaskStatus(proc):
    msg = ""
    return True, msg

def setCollectedBy(output):
    global g_CollectedBy  
    if output["collectedBy"] != None:
        g_CollectedBy = output["collectedBy"]
    return

def setDateCollected(output):
    global g_DateCollected
    g_DateCollected = output["dateCollected"]
    return    
    
def getCollectedBy(output):
    global g_CollectedBy  
    return g_CollectedBy

def getDateCollected(output):
    global g_DateCollected
    return g_DateCollected
    
# Have we submitted this successfully before?
def testPreviouslySubmitted(proc):
    msg = ""
    return True, msg

# Is there a date of experiment?
def testCollectedDate(output):
    msg = ""
    return True

# Is there a date of experiment?
def testCollectedBy(output):
    msg = ""
    return True

# Are all inputs set? 
def testInputs(proc):
    msg = ""
    success = True
    inputLs = proc["inputs"]
    if inputLs == None or len(inputLs) == 0:
        msg = "No inputs!"
        print(msg)
        success = False
        return success, msg

    return (success, msg);


# Are all outputs set? 
def testOutputs(proc):
    msg = ""
    success = True
    outputLs = proc["outputs"]
    if outputLs == None or len(outputLs) == 0:
        msg = "No outputs!"
        print(msg)
        success = False
        return success, msg
    
    for output in outputLs:
        if testCollectedBy(output) == True:
            setCollectedBy(output)
        if testCollectedDate(output) == True:
            setDateCollected(output)
        
    return (success, msg);

# Do we have an experimenter ID? 
def testCollectedBy(outputs):
    msg = ""
    return True, msg

# Is there a mouse?
def testMouseInfo(animal):
    # Does it have a generation? Sex? Name?
    result = True
    msg = ""
    if animal == None:
        msg = "No mouse to test!"
        result = False
        
    if animal["animalName"] == None or len(animal["animalName"]) == 0:
        msg = "No mouse name."
        result = False
         
    if animal["generation"] == None or len(animal["generation"]) == 0:
        msg = "No mouse generation."
        result = False         
        
    if animal["sex"] == None or len(animal["sex"]) == 0:
        msg = "No mouse sex."
        result = False
        
    return result, msg

# Is there a genotype?
def testGenotypeInfo(genotypes):
    msg = "No KOMP assay name"
    success = False
    zygosity = "none"
    assayName = ""
    
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
    
    if line["stock"] == None or len(line["stock"]) == 0:
        msg = 'StockNumber is not set for ' + line["name"] + ';'
        success = False
    
    if line["lineStatus"] != None and "KOMP" not in line["lineStatus"]:
        msg = msg + line["name"] + ' status is not KOMP Active or KOMP Complete ' + ';'
        success = False   
         
    if line["lineStatus"] == None:
        msg = msg + line["name"] + ' status is not KOMP Active or KOMP Complete ' + ';'
        success = False    
        
    if line["references"] == None or len(line["references"]) == 0:
        msg = msg + 'The References field is not set. It should containg teh MGI reference for KOMP lines.' + ';'
        success = False    
    
    if line["references"] == None or len(line["references"]) == 0:
        msg = msg + 'The References field is not set. It should contain the MGI reference for KOMP lines.' + ';'
        success = False
          
    return success, msg

# Assumes all parameters are valid dictionaries with the keys required or None type 
def createLogEntry(animalInfo, procedureInfo, lineInfo, genotypeInfo, issueStr):
    print('///////////')
    print(procedureInfo)
    print('////////////')
    
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
    # procedureInfo = { "taskInstanceKey": "N/A", "impcCode": "N/A", "dateDue": "N/A"}
    success = True
    msgDict = {"AnimalName":"", "TaskName":"", "TaskInstanceKey":0, "ImpcCode": "", "StockNumber":"", "DateDue":"", "Issue":"" }
    msg = ""
    
    success, msg = testMouseInfo(specimen["animal"])
   
    if success == False:
        createLogEntry(specimen["animal"], None, specimen["line"], specimen["genotypes"], msg)
    
    success, msg = testLineInfo(specimen["line"])
    if success == False:
        createLogEntry(specimen["animal"], None, specimen["line"], specimen["genotypes"], msg)
   
    success, msg, assayName, genotype = testGenotypeInfo(specimen["genotypes"]) # return the active genotype
    
    if success == False:
        createLogEntry(specimen["animal"], None, specimen["line"], assayName + ' ' + genotype, msg)   
           
    return success

def validateProcedure(proc):
    
    specimenLs = proc["animal"]
    specimen = specimenLs[0]
    lineInfo = { "stock" : specimen["stock"] }
    taskLs = proc["taskInstance"] 
    task = taskLs[0] 
    
    msg = ""
    
    print("PROCEDURE:")
    print(proc)
    print("")
    print("TASK:")
    print(task)
    print("")
    print("SPECIMEN:")
    print(specimen)
    print("")
    print("Line Info:")
    print(lineInfo)
    
    success, msg = testOutputs(task)
    print('Msg= ' + msg)
    print('Success= ' + str(success))
    
    if success == False:
        createLogEntry(specimen, task, lineInfo, None, msg)
    success = True
    return success