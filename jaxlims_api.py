#
import mysql.connector
from mysql.connector import errorcode
import read_config as cfg
import json

# GLOBALS for this module
g_mysqldb = None
g_MysqlCursor=None

g_code_keys = {}

#ImpcCode,IncrementStartValue,IncrementValue)
series_info = {
'IMPC_ALZ_075_001':  (1,1),
'IMPC_ALZ_076_001':  (1,1),
'IMPC_CSD_085_001':  (1,1),
'IMPC_ECG_025_001':  (1,1),
'IMPC_ELZ_064_001':  (1,1),
'IMPC_EMA_001_001':  (0,1),
'IMPC_EMA_017_001':  (1,1),
'IMPC_EMO_001_001':  (0,1),
'IMPC_EMO_017_001':  (1,1),
'IMPC_EOL_001_001':  (0,1),
'IMPC_EOL_012_001':  (0,1),
'IMPC_EYE_050_001':  (1,1),
'IMPC_EYE_051_001':  (1,1),
'IMPC_GEL_044_001':  (1,1),
'IMPC_GEL_044_001':  (0,1),
'IMPC_GEM_049_001':  (1,1),
'IMPC_GEM_049_001':  (0,1),
'IMPC_GEO_050_001':  (1,1),
'IMPC_GEO_050_001':  (0,1),
'IMPC_GEP_064_001':  (1,1),
'IMPC_GEP_064_001':  (0,1),
'IMPC_GPL_007_001':  (1,1),
'IMPC_GPL_007_001':  (0,1),
'IMPC_GPM_007_001':  (1,1),
'IMPC_GPM_007_001':  (0,1),
'IMPC_GPO_007_001':  (1,1),
'IMPC_GPO_007_001':  (0,1),
'IMPC_GPP_007_001':  (1,1),
'IMPC_GPP_007_001':  (0,1),
'IMPC_GRS_001_001':  (1,1),
'IMPC_GRS_002_001':  (1,1),
'IMPC_HIS_177_001':  (0,1),
'IMPC_IPG_002_001':  (0,15),
'IMPC_VIA_037_001':  (1,1),
'IMPC_VIA_038_001':  (1,1),
'IMPC_VIA_039_001':  (1,1),
'IMPC_VIA_040_001':  (1,1),
'IMPC_VIA_041_001':  (1,1),
'IMPC_VIA_042_001':  (1,1),
'IMPC_VIA_043_001':  (1,1),
'IMPC_VIA_044_001':  (1,1),
'IMPC_VIA_045_001':  (1,1),
'IMPC_VIA_046_001':  (1,1),
'IMPC_VIA_047_001':  (1,1),
'IMPC_VIA_048_001':  (1,1),
'IMPC_WEL_003_001':  (1,1),
'IMPC_XRY_034_001':  (1,1),
'IMPC_XRY_048_001':  (1,1),
'IMPC_XRY_049_001':  (1,1),
'IMPC_XRY_050_001':  (1,1),
'IMPC_XRY_051_001':  (1,1),
'JAX_ERG_028_001':  (1,1),
'JAX_HBD_002_001':  (1,1),
'JAX_OFD_005_001':  (5,5),
'JAX_OFD_006_001':  (5,5),
'JAX_ROT_001_001':  (1,1),
'JAXIP_WEL_003_001':  (1,1)
}


def isExperimenterID(impcCode):
    # Returns true if IMPC code is for an experimenter ID
    return impcCode in [
'IMPC_ABR_053_001',
'IMPC_ACS_014_001',
'IMPC_BWT_005_001',
'IMPC_CBC_049_001',
'IMPC_CBC_051_001',
'IMPC_CSD_081_001',
'IMPC_DXA_016_001',
'IMPC_ECG_020_001',
'IMPC_EMA_002_001',
'IMPC_EMA_002_001',
'IMPC_EMO_002_001',
'IMPC_EOL_002_001',
'IMPC_EYE_036_001',
'IMPC_GEL_045_001',
'IMPC_GEM_050_001',
'IMPC_GEO_051_001',
'IMPC_GEP_065_001',
'IMPC_GPL_008_001',
'IMPC_GPM_008_001',
'IMPC_GPO_008_001',
'IMPC_GPP_008_001',
'IMPC_GRS_012_001',
'IMPC_HEM_024_001',
'IMPC_HEM_017_001',
'IMPC_HIS_208_001',
'IMPC_HWT_003_001',
'IMPC_IPG_008_001',
'IMPC_PAT_052_002',
'JAX_ERG_029_001',
'JAX_ERG_048_001',
'JAX_HBD_003_001',
'JAX_LDT_013_001',
'JAX_OFD_035_001'
]


def databaseGetExperimenterIdCode(expName):
    # Given a first and last name return the PK from te lookup table
    tupleName = tuple(map(str,expName.split(' ')))
    
    queryStatement = ""
    if len(tupleName) > 1:
        queryStatement = "SELECT _experimenterId_key FROM komp.experimenterid WHERE FirstName = '{0}' AND LastName = '{1}'" \
                            .format(tupleName[0], tupleName[1])
    else:
        queryStatement = "SELECT _experimenterId_key FROM komp.experimenterid WHERE FirstName = '{0}' AND LastName = '{1}'" \
                            .format(tupleName[0], '')
                           
    expId = ""
    try:
        g_MysqlCursor.execute(queryStatement)
        
        for _experimenterId_key in g_MysqlCursor:
            expId=_experimenterId_key[0]
            
    except Exception as e:
        print('SELECT FAILED FOR: ' + queryStatement)
    
    return str(expId)
    
def databaseInsertQualityErrorMessage(msg):
    """ Given  dictionary pull out the elements and insert it into the database """
    insertStmt = "INSERT INTO komp.dccQualityIssues (AnimalName, Taskname, TaskInstanceKey, ImpcCode, StockNumber, DateDue, Issue) VALUES ( '{0}','{1}',{2},'{3}','{4}','{5}','{6}')".\
        format(msg['AnimalName'], msg['TaskName'], int(msg['TaskInstanceKey']), msg['ImpcCode'], msg['StockNumber'], msg['DateDue'], msg['Issue'].replace("'", "\""))

    try:    
        g_MysqlCursor.execute(insertStmt)
        g_mysqldb.commit()
        
    except Exception as e:
        print("INSERT FAILED for " + insertStmt)

def databaseSelectProcedureCode(procName):
    sqlStatement = 'SELECT ImpcCode FROM komp.taskimpccodes WHERE TaskName = \'{0}\''.format(procName)
     
    threeLetterCode = ''
    try:
        g_MysqlCursor.execute(sqlStatement)
        
        for ImpcCode in g_MysqlCursor:
            threeLetterCode=ImpcCode[0]
            
    except Exception as e:
        print('SELECT FAILED FOR: ' + sqlStatement)
    
    return threeLetterCode


def isRequired(impcCode:str) -> bool:
    # Look up IMPC code in komp.dccparametedetils and return truw if IsRequired isnon-zero
         
    selectStmt = "SELECT IsRequired FROM komp.dccparameterdetails WHERE ImpcCode= \'{0}\'".format(impcCode)

    isRequired = False
    try:
        g_MysqlCursor.execute(selectStmt)
        
        for IsRequired in g_MysqlCursor:
            isRequired = (IsRequired[0] == 1)
    except Exception as e:
        print('SELECT FAILED FOR: ' + selectStmt)
    
    return isRequired


def isDate(impcCode:str) -> bool:
    # Look up IMPC code in komp.dccparametedetils and return truw if IsRequired isnon-zero
         
    selectStmt = "SELECT IsDate FROM komp.dccparameterdetails WHERE ImpcCode= \'{0}\'".format(impcCode)

    isDate = False
    try:
        g_MysqlCursor.execute(selectStmt)
        
        for IsDate in g_MysqlCursor:
            isDate = (IsDate[0] == 1)
    except Exception as e:
        print('SELECT FAILED FOR: ' + selectStmt)
    
    return isDate


def isDateTime(impcCode:str) -> bool:
    # Look up IMPC code in komp.dccparametedetils and return truw if IsRequired isnon-zero
         
    selectStmt = "SELECT IsDateTime FROM komp.dccparameterdetails WHERE ImpcCode= \'{0}\'".format(impcCode)

    isDateTime = False
    try:
        g_MysqlCursor.execute(selectStmt)
        
        for IsDateTime in g_MysqlCursor:
            isDateTime = (IsDateTime[0] == 1)
    except Exception as e:
        print('SELECT FAILED FOR: ' + selectStmt)
    
    return isDateTime


def databaseSelectImpcData(threeLetterCode, isMetatdata, usingInputs):
    
    whereStr = ' _DccType_key <> 7 '
    if isMetatdata == True:
        whereStr = ' _DccType_key = 7 '
    
    if usingInputs == True:
        whereStr = whereStr + ' AND IsInput = 1 ORDER BY _DccType_key'    
    else:
        whereStr = whereStr + ' AND IsInput = 0 ORDER BY _DccType_key' 
         
    selectStmt = 'SELECT ImpcCode, _ClimbType_key, _DccType_key FROM komp.dccparameterdetails WHERE _ClimbType_key > 0 AND ImpcCode LIKE \'%{0}%\' AND '.format(threeLetterCode) + whereStr

    lsOfTuples = []
    try:
        g_MysqlCursor.execute(selectStmt)
        
        for (ImpcCode, _ClimbType_key, _DccType_key) in g_MysqlCursor:
            lsOfTuples.append((ImpcCode,_ClimbType_key, _DccType_key))
            
        
    except Exception as e:
        print('SELECT FAILED FOR: ' + selectStmt)
    
    return lsOfTuples


def getLastReviewedDate(animal,procedure):
    
    lastReviewDate = None
    selectStmt = "SELECT MAX(DateReviewed) FROM komp.submittedProcedures WHERE AnimalName = '{0}' AND ExperimentName = '{1}'".format(animal,procedure)
    
    try:
        g_MysqlCursor.execute(selectStmt)
        
        for DateReviewed in g_MysqlCursor:
            lastReviewDate = DateReviewed[0]
    except Exception as e:
        print('SELECT FAILED FOR: ' + selectStmt)
    
    return lastReviewDate

def getLastReviewedDate(taskInstanceKey):
    
    lastReviewDate = None

    selectStmt = "SELECT MAX(DateReviewed) FROM komp.submittedProcedures WHERE TaskInstanceId = '{0}'".format(taskInstanceKey)
    
    try:
        g_MysqlCursor.execute(selectStmt)
        
        for DateReviewed in g_MysqlCursor:
            lastReviewDate = DateReviewed[0]
    except Exception as e:
        print('SELECT FAILED FOR: ' + selectStmt)
    
    return lastReviewDate

def recordSubmissionAttempt(fileName, animalName, procedure, impcCode, reviewDate):  
    procedureName = procedure["workflowTaskName"]
    taskInstanceId = int(procedure["taskInstanceKey"])
    
    """ Given  dictionary pull out the elements and insert it into the database """
    insertStmt = "INSERT INTO komp.submittedProcedures (AnimalName, ExperimentName, ImpcCode, XmlFilename, DateReviewed, TaskInstanceId) VALUES ( '{0}','{1}','{2}','{3}','{4}',{5})".\
        format(animalName, procedureName, impcCode, fileName, reviewDate, taskInstanceId)

    try:    
        #print(insertStmt)
        g_MysqlCursor.execute(insertStmt)
        g_mysqldb.commit()
       
    except Exception as e:
        print('INSERT FAILED FOR: ' + insertStmt)        
    return

def recordMediaSubmission(srcFilename, destFilename, taskKey, impcCode):  
    # Escape the backslashes, Must be a better way...
    srcFilenameRaw = fr"{srcFilename}".replace('\\', '\\\\')
    insertStmt = "INSERT INTO komp.imagefileuploadstatus (SourceFileName, DestinationFileName, TaskKey, ImpcCode) VALUES ( '{0}','{1}',{2},'{3}')".\
        format(srcFilenameRaw, destFilename, taskKey, impcCode)

    try:    
        g_MysqlCursor.execute(insertStmt)
        g_mysqldb.commit()
       
    except Exception as e:
        print('INSERT FAILED FOR: ' + insertStmt)        
    return

def populateGlobalImpcCodeKeys():
    selectStmt = "SELECT ImpcCode, _ClimbType_key FROM komp.dccparameterdetails"
    typeKey = 0
    try:
        g_MysqlCursor.execute(selectStmt)
        
        for ImpcCode, _ClimbType_key in g_MysqlCursor:
            g_code_keys[ImpcCode] = _ClimbType_key
    except Exception as e:
        print('SELECT FAILED FOR: ' + selectStmt)
    


def getKeyFromImpcCode(impc_code:str):
    if len(g_code_keys) == 0:
        # populate it
        populateGlobalImpcCodeKeys()
        
    if impc_code in g_code_keys.keys():
        return g_code_keys[impc_code]
    else:
        return 0
    
def verifyImpcCode(impccode):   
    selectStmt = "SELECT _ClimbType_key FROM komp.dccparameterdetails WHERE ImpcCode = '{0}'".format(impccode)
    typeKey = 0
    try:
        g_MysqlCursor.execute(selectStmt)
        
        for _ClimbType_key in g_MysqlCursor:
            typeKey = _ClimbType_key[0]
    except Exception as e:
        print('SELECT FAILED FOR: ' + selectStmt)
    
    if typeKey == None:
        typeKey = 0
        
    return typeKey

def isSeries(output:dict):
    if 'Series' in output["dccTypeKey"]:
        return True
    return False

"""
Get the mice the procedures we are trying to upload.
"""
def getMice(procedure_instance_key_ls:list):
    # Make the passed in list part of the WHERE clause
    query_stmt = """
    SELECT DISTINCT
        OrganismID AS animalName, 
        DateBirth AS dateBorn,
        Sex as sex,
        generation,
        StockNumber AS stock,
        '' AS birthID,
        GenotypeSymbol AS genotype,
        MarkerSymbol AS assay
    FROM
        Organism 
        INNER JOIN ProcedureInstanceOrganism USING (_Organism_key)
        INNER JOIN ProcedureInstance USING (_ProcedureInstance_key)
        INNER JOIN cv_sex USING (_Sex_key)
        INNER JOIN Line USING (_Line_key)
        INNER JOIN LineMarker USING (_Line_key)
        INNER JOIN Marker USING (_Marker_key)
        INNER JOIN Genotype USING (_Organism_key)
        INNER JOIN cv_GenotypeSymbol USING (_GenotypeSymbol_key)
        INNER JOIN cv_Generation USING (_Generation_key)
    WHERE _ProcedureInstance_key IN ({0}) 
    """
    pi_key_str = ''
    for pikey in procedure_instance_key_ls:
        pi_key_str = pi_key_str + str(pikey) + ','
    pi_key_str = pi_key_str + '0'  # sentinel
    
    query_stmt = query_stmt.format(pi_key_str)
    
    genotypesLs = []
    animalDictLs = []
    animalInfoDict = {}
    
    try:    
        g_MysqlCursor.execute(query_stmt)
        for  animalName,dateBorn,sex,generation, stock, birthID, genotype,assay in g_MysqlCursor:
            animalDict = {}
            lineDict = {}
            litterDict = {}
            genotypeDict = {}
            genotypesLs = []
            animalInfoDict = {}
            
            animalDict['animalName'] = animalName
            animalDict['dateBorn'] = str(dateBorn)
            animalDict['sex'] = sex
            animalDict['generation'] = generation
            
            lineDict['stock'] = stock
            litterDict['birthID'] = birthID
            genotypeDict['genotype'] = genotype
            genotypeDict['assay'] = assay
            
            animalInfoDict['animal'] = animalDict
            animalInfoDict['line'] = lineDict
            animalInfoDict['litter'] = litterDict
            genotypesLs.append(genotypeDict)
            animalInfoDict['genotypes'] = genotypesLs
            
            animalDictLs.append(animalInfoDict)
    except Exception as e:
        print('SELECT FAILED FOR: ' + query_stmt) 
 
    return animalDictLs


"""
    Return a list of the specimen and experiment data
"""

def getCombinedProcedureSpecimenData(impc_code:str,pipeline:str,whereClause:str):
    taskInfoDictLs = [] # List taskInfo dicts
    taskInfoDict = {}   # Dict where each dict has 'animal' list and a 'taskInstance'list.
    pi_keys = []
    animalDictLs, taskInstanceDictLs = getProcedureData(impc_code,pipeline,whereClause) # one to one
    # Get the inputs and outputs for each task instance
    for taskInstanceDict,animalDict in zip(taskInstanceDictLs,animalDictLs):
        taskInfoDict = {}
        localTaskDictLs=[]
        localAnimalDictLs=[]
        taskInfoDict = {}
        
        pi_keys.append(int(taskInstanceDict['taskInstanceKey']))
        
        inputDictLs = getInputData(int(taskInstanceDict['taskInstanceKey']))
        outputDictLs = getOutputData(int(taskInstanceDict['taskInstanceKey']))
        taskInstanceDict['outputs'] = outputDictLs
        taskInstanceDict['inputs'] = inputDictLs
        
        localAnimalDictLs.append(animalDict)
        localTaskDictLs.append(taskInstanceDict)
        
        taskInfoDict['animal'] = localAnimalDictLs
        taskInfoDict['taskInstance'] = localTaskDictLs
        
        taskInfoDictLs.append(taskInfoDict)
        
    return pi_keys, taskInfoDictLs
     
"""
    Get the procedure data for the given IMPC code. Return the data in JSON
    List of dicts 
        Each dict has a list called 'taskInfo' which contains a list called 'animal' and a list called 'taskInstance'.
"""
def getProcedureData(impc_code:str,pipeline:str,whereClause:str=''):
    # Return the animal dict list and the taskinstance dict list
    proc_query = """ 
    SELECT 
        _ProcedureInstance_key AS taskInstanceKey, 
        ProcedureAlias AS workflowTaskName, 
        DateCompleteMap.DateComplete AS dateComplete,
        'JaxLIMS User' AS reviewedBy,
        ProcedureInstance.DateModified AS dateReviewed,
        ProcedureStatus AS taskStatus,
        OrganismID AS animalName,
        CONCAT('JR',RIGHT(StockNumber,5)) AS stock
    FROM
        ProcedureInstance 
        INNER JOIN rslims.ProcedureInstanceOrganism USING (_ProcedureInstance_key)
        INNER JOIN rslims.Organism USING (_Organism_key)
        INNER JOIN rslims.Line USING (_Line_key)
        INNER JOIN rslims.DateCompleteMap USING  (_ProcedureInstance_key)
        INNER JOIN rslims.cv_ProcedureStatus USING (_ProcedureStatus_key)
        INNER JOIN rslims.ProcedureDefinitionVersion USING (_ProcedureDefinitionVersion_key)
        INNER JOIN rslims.ProcedureDefinition USING (_ProcedureDefinition_key)
        INNER JOIN rslims.OrganismStudy USING (_Organism_key)
        INNER JOIN rslims.Study USING (_Study_key)
    WHERE 
        ProcedureDefinition.ExternalID = '{0}'
        AND _LevelTwoReviewAction_key = 13
        AND Study.StudyName = '{1}'
        AND DateCompleteMap.DateComplete IS NOT NULL
        AND _ProcedureStatus_key NOT IN (1,27,37,28) 
    """
    proc_query = proc_query.format(impc_code,pipeline) + whereClause
    taskInstanceDict = {}
    animalDict = {}
    animalDictLs = []
    taskInstanceDictLs = []
    
    try:    
        g_MysqlCursor.execute(proc_query)
        for  taskInstanceKey,workflowTaskName,dateComplete,reviewedBy,dateReviewed,taskStatus,animalName,stock in g_MysqlCursor:
            taskInstanceDict = {}
            animalDict = {}
            taskInstanceDict['taskInstanceKey'] = taskInstanceKey
            taskInstanceDict['workflowTaskName'] = workflowTaskName
            taskInstanceDict['dateComplete'] = dateComplete
            taskInstanceDict['reviewedBy'] = reviewedBy
            taskInstanceDict['dateReviewed'] = str(dateReviewed)
            taskInstanceDict['taskStatus'] = taskStatus
            animalDict['animalName'] = animalName
            animalDict['stock'] = stock
            taskInstanceDictLs.append(taskInstanceDict)
            animalDictLs.append(animalDict)
    except Exception as e:
        print('SELECT FAILED FOR: ' + proc_query)     
        
    return animalDictLs,taskInstanceDictLs

def getInputData(procedure_instance_key:int):
    # Given a procedure instance PK return the inputs and value for those with IMPC codes
    # _Input_key AS outputKey => _Climb_key, rslim.dccparameterdetails => komp.dccparameterdetails
    input_query = """
    SELECT Input.ExternalID as name, InputValue as inputValue, _ClimbType_key AS inputKey
    FROM  
        InputInstance 
        INNER JOIN Input USING (_Input_key) 
        INNER JOIN komp.dccparameterdetails ON (Input.ExternalID = komp.dccparameterdetails.ImpcCode)
    WHERE
        InputInstance._ProcedureInstance_key = {0}
    """
    input_query = input_query.format(procedure_instance_key)
    inputInstanceDict = {}
    inputInstanceDictLs = []
    
    try:    
        g_MysqlCursor.execute(input_query)
        for  name,inputvalue,inputKey in g_MysqlCursor:
            inputInstanceDict = {}
            inputInstanceDict['name'] = name
            inputInstanceDict['inputValue'] = inputvalue
            inputInstanceDict['inputKey'] = inputKey
            inputInstanceDictLs.append(inputInstanceDict)
    except Exception as e:
        print('SELECT FAILED FOR: ' + input_query)     
        
    return inputInstanceDictLs


def getOutputData(procedure_instance_key:int):
    # Given a procedure instance PK return the outputs and value for those with IMPC codes
    # _Output_key AS outputKey => _ClimbType_key, rslim.dccparameterdetails => komp.dccparameterdetails
    output_query = """
    SELECT Output.ExternalID as name, 
        _OutputInstance_key AS sequenceId,
        OutputValue as outputValue, 
        _ClimbType_key AS outputKey, 
        'TBD' AS collectedBy, 
        DateCompleteMap.DateComplete AS collectedDate,
        OutputStatus AS statusCode,
        TypeName AS dccType,
        komp.dccparameterdetails.IsRequired AS required,
        _DccType_key
    FROM  
        rslims.OutputInstanceSet 
        INNER JOIN rslims.OutputInstance USING (_OutputInstanceSet_key)
        INNER JOIN rslims.Output USING (_Output_key)
        INNER JOIN rslims.DateCompleteMap USING (_ProcedureInstance_key)
        INNER JOIN komp.dccparameterdetails ON (Output.ExternalID = komp.dccparameterdetails.ImpcCode)
        INNER JOIN rslims.cv_dccType USING (_DccType_key)
        LEFT OUTER JOIN rslims.cv_OutputStatus USING (_OutputStatus_key)
    WHERE
        OutputInstanceSet._ProcedureInstance_key = {0}
        ORDER BY _DccType_key,name
    """
    output_query = output_query.format(procedure_instance_key)
    outputInstanceDict = {}
    outputInstanceDictLs = []
    
    try:    
        g_MysqlCursor.execute(output_query)
        for  name,sequenceId,outputValue,outputKey, collectedBy,collectedDate, statusCode, dccType,_DccType_key,required  in g_MysqlCursor:
            outputInstanceDict = {}
            outputInstanceDict['name'] = name
            outputInstanceDict['outputValue'] = outputValue
            outputInstanceDict['outputKey'] = outputKey
            outputInstanceDict['collectedBy'] = collectedBy
            outputInstanceDict['collectedDate'] = collectedDate
            outputInstanceDict['statusCode'] = statusCode
            outputInstanceDict['dccType'] = dccType
            outputInstanceDict['sequenceId'] = sequenceId
            outputInstanceDict['required'] = required
            outputInstanceDictLs.append(outputInstanceDict)
    except Exception as e:
        print('SELECT FAILED FOR: ' + output_query)     
    
    # If there is a series or media series, let's take care of it now.
    i = 0
    for outputInstanceDict in  outputInstanceDictLs:
        if 'mediaseries' in outputInstanceDict['dccType'].lower():
            outputInstanceDictLs = resolveMediaSeries(outputInstanceDictLs,i)
        elif 'series' in outputInstanceDict['dccType'].lower():
            outputInstanceDictLs = resolveSeries(outputInstanceDictLs,i)
        
        i = i + 1
    
    # If there is a missing required parameter, let's take care of it now.
    for outputInstanceDict in  outputInstanceDictLs:
        if outputInstanceDict['statusCode'] == None or len(outputInstanceDict['statusCode']) == 0: # If set skip this code
            # Else check for missing status code of bad data item
            if outputInstanceDict['required'] == 1 and \
                (outputInstanceDict['outputValue'] is None or len(outputInstanceDict['outputValue']) == 0):
                        outputInstanceDict['statusCode'] = 'Parameter not measured - Equipment Failed'
            
    return outputInstanceDictLs

def getNextIncrement(impc_code:str, previous_increment:int):
    # Unfortunately, IPG (aka GTT) is a special case
    increment_start_val, increment_step = series_info[impc_code]
    
    if previous_increment is None:    # First time. Return the start value
        return increment_start_val
    elif impc_code == 'IMPC_IPG_002_001':  # Arg! Special case
        if previous_increment == 0:
            return 15
        elif previous_increment == 15:
            return 30
        elif previous_increment == 30:
            return 60
        elif previous_increment == 60:
            return 120
    else:
        return previous_increment + increment_step
        
        
def resolveSeries(outputInstanceDictLs:list, first_index:int):
    # The i-th element is the start of the series
    seriesVal = {}
    i = first_index
    
    output_key = outputInstanceDictLs[i]['outputKey']
    impc_code = outputInstanceDictLs[i]['name']
    
    increment_val = None
    while outputInstanceDictLs[i]['outputKey'] == output_key:
        increment_val=getNextIncrement(impc_code,increment_val)
        seriesVal[str(increment_val)]  = outputInstanceDictLs[i]['outputValue']
        
        i = i + 1
        if i >= len(outputInstanceDictLs):
            break
        
    # Set the first output to be the new list (series)
    outputInstanceDictLs[first_index]['outputValue'] = seriesVal
    
    # Remove the old outputs that were turned into a series
    i = i - 1
    while i > first_index: 
        outputInstanceDictLs.pop(i)
        i = i - 1
        
    return outputInstanceDictLs
                      
def resolveMediaSeries(outputInstanceDictLs:list, first_index:int):
    # The i-th element is the start of the series
    seriesVal = {}
    i = first_index
    
    output_key = outputInstanceDictLs[i]['outputKey']
    impc_code = outputInstanceDictLs[i]['name']
    
    increment_val = None
    while outputInstanceDictLs[i]['outputKey'] == output_key:
        increment_val=getNextIncrement(impc_code,increment_val)
        # TODO : Turn the value of the image to the version on the sftp server.
        seriesVal[str(increment_val)]  = outputInstanceDictLs[i]['outputValue']
        i = i + 1
        if i >= len(outputInstanceDictLs):
            break
        
    # Set the first output to be the new list (series)
    outputInstanceDictLs[first_index]['outputValue'] = seriesVal
    
    # Remove the old outputs that were turned into a series
    i = i - 1
    while i > first_index: 
        outputInstanceDictLs.pop(i)
        i = i - 1
        
    return outputInstanceDictLs
              
def setupDatabaseConnection():
    
    try:
        mycfg = cfg.parse_config(path="config.yml")
        # Setup credentials for database
        mySqlHost = mycfg['jaxlims_database']['host']
        mySqlUser = mycfg['jaxlims_database']['user']
        mySqlPassword = mycfg['jaxlims_database']['password']
        mySqlSchema = mycfg['jaxlims_database']['name']
        
        global g_mysqldb
        g_mysqldb = mysql.connector.connect(host=mySqlHost, user=mySqlUser, password=mySqlPassword, database=mySqlSchema)
        
        global g_MysqlCursor
        g_MysqlCursor = g_mysqldb.cursor()
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    except:
        print('Connection failed')
    
    return

def init():
    setupDatabaseConnection()
    
def close():
    g_mysqldb.close()

if __name__ == '__main__':
    init()
   
    taskInfoDictLs = [] # List taskInfo dicts
    taskInfoDict = {}   # Dict where each dict has 'animal' list and a 'taskInstance'list.
    
    animalDictLs, taskInstanceDictLs = getProcedureData('IMPC_IPG_001','KOMP Phenotype') # one to one
    # Get the inputs and outputs for each task instance
    for taskInstanceDict,animalDict in zip(taskInstanceDictLs,animalDictLs):
        taskInfoDict = {}
        localTaskDictLs=[]
        localAnimalDictLs=[]
        taskInfoDict = {}
        
        inputDictLs = getInputData(int(taskInstanceDict['taskInstanceKey']))
        outputDictLs = getOutputData(int(taskInstanceDict['taskInstanceKey']))
        taskInstanceDict['outputs'] = outputDictLs
        taskInstanceDict['inputs'] = inputDictLs
        
        localAnimalDictLs.append(animalDict)
        localTaskDictLs.append(taskInstanceDict)
        
        taskInfoDict['animal'] = localAnimalDictLs
        taskInfoDict['taskInstance'] = localTaskDictLs
        
        taskInfoDictLs.append(taskInfoDict)
    
    
    pi_key_ls = [21953,21954,21955,21956,21957,21958,136207,3703872,3704055]
    animalInfoDict = getMice(pi_key_ls)
    
    f = open("rslims-exps.json","w")
    s = str(taskInfoDictLs).replace('\'','"')
    s = str(s).replace('None','""')
    print(json.dumps(json.loads(s),indent=4))
    
    f.write("\nExperiments {0}:".format(len(taskInfoDictLs)))
    
    f.write(json.dumps(json.loads(s),indent=4))
    
    f.write("\n\nAnimals ({0}):".format(len(animalInfoDict)))
    s = str(animalInfoDict).replace('\'','"').replace('None','""')
    
    print(json.dumps(json.loads(s),indent=4))
    f.write(json.dumps(json.loads(s),indent=4))
    f.close()
    
    #id = databaseGetExperimenterIdCode("Kristina Palmer")
    #print(getLastReviewedDate(0))
    #print(id)
    close()