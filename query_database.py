#

import mysql.connector
from mysql.connector import errorcode

g_mysqldb = None
g_MysqlCursor=None

def getDbServer():
    return 'rslims-dev.jax.org'

def getDbUsername():
    return 'dba'

def getDbPassword():
    return 'rsdba'

def getDbSchema():
    return 'komp'


def databaseInsertQualityErrorMessage(msg):
    """ Given  dictionary pull out the elements and insert it into the database """
    insertStmt = "INSERT INTO komp.dccQualityIssues (AnimalName, Taskname, TaskInstanceKey, ImpcCode, StockNumber, DateDue, Issue) VALUES ( '{0}','{1}',{2},'{3}','{4}','{5}','{6}')".\
        format(msg['AnimalName'], msg['TaskName'], int(msg['TaskInstanceKey']), msg['ImpcCode'], msg['StockNumber'], msg['DateDue'], msg['Issue'])

    try:    
        print(insertStmt)
        g_MysqlCursor.execute(insertStmt)
        g_mysqldb.commit()
        
    except Exception as e:
        print("INSERT FAILED for " + insertStmt)

def databaseSelectProcedureCode(procName):
    sqlStatement = 'SELECT ImpcCode FROM komp.taskimpccodes WHERE TaskName = \'{0}\''.format(procName)
    print(sqlStatement)
     
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
        whereStr = whereStr + ' AND IsInput = 1'    
    else:
        whereStr = whereStr + ' AND IsInput = 0' 
         
    selectStmt = 'SELECT ImpcCode, _ClimbType_key, _DccType_key FROM komp.dccparameterdetails WHERE _ClimbType_key IS NOT NULL AND ImpcCode LIKE \'%{0}%\' AND '.format(threeLetterCode) + whereStr

    print(selectStmt)
    
    lsOfTuples = []
    try:
        g_MysqlCursor.execute(selectStmt)
        
        for (ImpcCode, _ClimbType_key, _DccType_key) in g_MysqlCursor:
            lsOfTuples.append((ImpcCode,_ClimbType_key, _DccType_key))
            
        
    except Exception as e:
        print('SELECT FAILED FOR: ' + selectStmt)
    
    return lsOfTuples

# Given a 3 letter procedure code, get the metadata definitions
def getImpcCodes(procedureCode, usingInputs, metadataOnly):
    
    impcCodeLs = []
    
    
    return impcCodeLs

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
    # IMPC 3 letter code, isMetadata, lookAtInputsOnly
    dccTuples = databaseSelectImpcData('ABR',True, True)
    print(dccTuples)
    impcCodeStr = 'IMPC_ABR_037_001'
    result = next((i for i, v in enumerate(dccTuples) if v[0] == impcCodeStr), None)
    print(result)
    myTuple = dccTuples[result]
    print(myTuple)
    print(myTuple[0])
    print(myTuple[1])
    print(myTuple[2])
    #s = databaseSelectProcedureCode('Heart Weight')
    #print(s)
    #print(s[0])
    close()