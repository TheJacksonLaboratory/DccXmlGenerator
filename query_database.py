#
import mysql.connector
from mysql.connector import errorcode

g_mysqldb = None
g_MysqlCursor=None

def getDbServer():
    return 'rslims.jax.org'

def getDbUsername():
    return 'dba'

def getDbPassword():
    return 'rsdba'

def getDbSchema():
    return 'komp'

def isExperimenterID(impcCode):
    return impcCode in ["IMPC_GEL_045_001","IMPC_GPL_008_001", 
                    "IMPC_GEM_050_001","IMPC_GPM_008_001", 
                    "IMPC_GPO_009_001", "IMPC_GEO_051_001", 
                    "IMPC_GEP_065_001", "IMPC_GPP_008_001",
                    "IMPC_EMA_002_001", "IMPC_EMO_002_001"]


def databaseGetExperimenterIdCode(expName):
    
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


def databaseSelectImpcData(threeLetterCode, isMetatdata, usingInputs):
    
    whereStr = ' _DccType_key <> 7 '
    if isMetatdata == True:
        whereStr = ' _DccType_key = 7 '
    
    if usingInputs == True:
        whereStr = whereStr + ' AND IsInput = 1 ORDER BY _DccType_key'    
    else:
        whereStr = whereStr + ' AND IsInput = 0 ORDER BY _DccType_key' 
         
    selectStmt = 'SELECT ImpcCode, _ClimbType_key, _DccType_key FROM komp.dccparameterdetails WHERE _ClimbType_key IS NOT NULL AND ImpcCode LIKE \'%{0}%\' AND '.format(threeLetterCode) + whereStr

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

def setupDatabaseConnection():
    
    try:
        
        mySqlHost = getDbServer()
        mySqlUser = getDbUsername()
        mySqlPassword = getDbPassword()
        mySqlSchema = getDbSchema()

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
    #id = databaseGetExperimenterIdCode("Kristina Palmer")
    #print(getLastReviewedDate(0))
    #print(id)
    close()