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


def databaseInsert(msg):
    """ Given  dictionary pull out the elements and insert it into the database """
    insertStmt = "INSERT INTO komp.TgsAction (DbAction, RequestID, OrganismID, Marker, NewGenotype, PreviousGenotype, AdditionalComment, CreatedBy, DateCreated, ModifiedBy, DateModified ) VALUES ( '{0}','{1}','{2}','{3}','{4}','{5}','{6}','TgsClimbApp',NOW(),'TgsClimbApp', NOW() )".\
        format(msg['DbAction'], msg['RequestID'], msg['OrganismID'], msg['Marker'], msg['NewGenotype'], msg['PreviousGenotype'],\
           msg['AdditionalComment'] )
    try:    
        #print(insertStmt)
        g_MysqlCursor.execute(insertStmt)
        g_mysqldb.commit()
        
    except Exception as e:
        print("INSERT FAILED for " + msg['OrganismID'] + ' and allele ' + msg['Marker'])
    
def databaseSelect(threeLetterCode, isMetatdata, usingInputs):
    
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
            
        g_MysqlCursor.close()
        
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


if __name__ == '__main__':
    setupDatabaseConnection()
    # IMPC 3 letter code, isMetadata, lookAtInputsOnly
    dccTuples = databaseSelect('ABR',False, True)
    
    impcCodeStr = 'IMPC_ABR_008_001'
    result = next((i for i, v in enumerate(dccTuples) if v[0] == impcCodeStr), None)
    print(result)
    myTuple = dccTuples[result]
    print(myTuple)
    
    g_mysqldb.close()
    print(dccTuples)