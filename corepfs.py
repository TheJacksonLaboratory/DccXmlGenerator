
from logging import NullHandler
import requests
from requests.auth import HTTPBasicAuth
import sys
import json
from datetime import datetime
import csv
import query_database as db

#?$filter= JAX_EXPERIMENT_STATUS eq 'Review Completed'&
baseURL = 'https://jacksonlabstest.platformforscience.com/DEV_KOMP/odata/'
endpoint = 'KOMP_REQUEST?$expand=REV_MOUSESAMPLELOT_KOMPREQUEST($expand=SAMPLE/pfs.MOUSE_SAMPLE)&$count=true'
#experimentEndpoint = 'KOMP_OPEN_FIELD_EXPERIMENT?$expand=EXPERIMENT_SAMPLES($expand=ASSAY_DATA/pfs.KOMP_OPEN_FIELD_ASSAY_DATA,ENTITY/pfs.MOUSE_SAMPLE_LOT($expand=SAMPLE/pfs.MOUSE_SAMPLE))'
experimentEndpointTemplate = "KOMP_{exp}_EXPERIMENT?$filter= JAX_EXPERIMENT_STATUS eq 'Review Completed'&$expand=EXPERIMENT_SAMPLES($expand=ASSAY_DATA/pfs.KOMP_{exp}_ASSAY_DATA,ENTITY/pfs.MOUSE_SAMPLE_LOT($expand=SAMPLE/pfs.MOUSE_SAMPLE))"


username = 'svc-corePFS@jax.org'
password = ''

"""
kompExperimentNames = [
"AUDITORY_BRAINSTEM_RESPONSE",
"BODY_COMPOSITION",
"BODY_WEIGHT",
"CLINICAL_BLOOD_CHEMISTRY",
"ELECTROCARDIOGRAM",
"ELECTRORETINOGRAPHY",
"EYE_MORPHOLOGY_SLIT_LAMP",
"FUNDUS_IMAGING",
"GLUCOSE_TOLERANCE_TEST",
"GRIP_STRENGTH",
"HEART_WEIGHT",
"HEMATOLOGY",
"HOLEBOARD",
"LIGHT_DARK_BOX",
"OPEN_FIELD",
"PEN_CARD_CREATION",
"SHIRPA_DYSMORPHOLOGY",
"STARTLE_PPI"
]
"""
kompExperimentNames = ["BODY_WEIGHT"]

############################# MICE/SAMPLES #################
def getKompMice():
    
    try:
        my_auth = HTTPBasicAuth(username, password)
        query = baseURL + endpoint

        result = requests.get(query, auth=my_auth,headers = {"Prefer": "odata.maxpagesize=5000"})    
        wgJson = result.json()
        
        #Get list of values
        valueLs = wgJson.get('value')
        totalCount = wgJson.get('@odata.count')

        return totalCount,valueLs
    except requests.exceptions.Timeout as e: 
        #print(e.message())
        raise 
    except requests.exceptions.InvalidHeader as e:  
        #print(e.message())
        raise 
    except requests.exceptions.InvalidURL as e:  
        #print(e.message())
        raise 
    except requests.exceptions.RequestException as e:  # All others
        #print(e.message())
        raise 
    
    pass

# This function returns a list of animalInfo.
# Each element in the list is animal dictional, a line dictionary and a genotypes list of dictionaries.
# Ex:
#{
#    "animal": {
#        "animalName": "A-560",
#        "dateBorn": "2022-02-21T05:00:00",
#        "sex": "Male",
#        "generation": "E18.5",
#        },
#    "line": {
#        "stock": "034083",
#    "litter": {
#        "birthID": null,
#    },
#    "genotypes": [
#        {
#            "genotype": "-/-",
#        }
#    ]
#},
#

def getSampleList(kompRequestlist):
    # Give "value": [ <blah>, REV_MOUSESAMPLELOT_KOMPREQUEST [ { "EntityTypeName": "MOUSE_SAMPLE_LOT", ... "SAMPLE": { <the good stuff> }]
    sampleDictls = []
    for kompRequest in kompRequestlist:
        mouseSampleLotList = kompRequest["REV_MOUSESAMPLELOT_KOMPREQUEST"]
        for mouseSampleLot in mouseSampleLotList:
            sampleDict = mouseSampleLot["SAMPLE"]
            # TEMP - filter out garbage from test env
            if sampleDict["JAX_MOUSESAMPLE_ALLELE"] == None or "(JR0" not in sampleDict["JAX_MOUSESAMPLE_ALLELE"]:
                continue
            # End of TEMP
            tmpDict = {}
            animalDict = {}
            lineDict = {} 
            litterDict = {}
            genotypesLs = []
            genotypeDict = {}
            
            animalDict["animalName"] = sampleDict["JAX_SAMPLE_EXTERNALID"]
            animalDict["dateBorn"] = sampleDict["JAX_MOUSESAMPLE_DATEOFBIRTH"]
            sex =''
            if sampleDict["JAX_MOUSESAMPLE_SEX"] == 'M':
                sex = 'Male'
            else:
                sex = 'Female'
            animalDict["sex"] = sex
            
            animalDict["generation"] = "F1"
            tmpDict["animal"] = animalDict
            
            lineDict["stock"] = jaxstrainToStocknumber(sampleDict["JAX_MOUSESAMPLE_ALLELE"])
            tmpDict["line"]  =  lineDict
            
            litterDict["birthID"] = sampleDict["JAX_MOUSESAMPLE_LITTERNUMBER"]
            tmpDict["litter"] = litterDict
            
            genotypeDict["genotype"] = sampleDict["JAX_MOUSESAMPLE_GENOTYPE"]
            genotypeDict["assay"] = sampleDict["JAX_MOUSESAMPLE_ALLELE"]
            
            genotypesLs.append(genotypeDict)
            
            tmpDict["genotypes"]  =  genotypesLs #list of dict ; each dict has one element { "genotype: "}
            
            sampleDictls.append(tmpDict)

    return sampleDictls

def jaxstrainToStocknumber(jaxstrain):
    # Find last occurance of "JR"
    # Copy the next 6 characters
    index = jaxstrain.rfind('JR')
    if index != -1:
        return jaxstrain[index+2:index+8]
    else:
        return jaxstrain

def jaxstrainToAssay(jaxstrain):
    # Find last occurance of "JR"
    # Copy the next 6 characters
    index = jaxstrain.rfind('JR')
    if index != -1:
        return jaxstrain[0:index]
    else:
        return jaxstrain

def getPfsAnimalInfo():
    # Return a list of animal info
    numberOfKompRequest, valuelist = getKompMice()
    return getSampleList(valuelist)



def getExperimentData(experimentEndpoint):
        
    try:
        my_auth = HTTPBasicAuth(username, password)
        query = baseURL + experimentEndpoint

        result = requests.get(query, auth=my_auth,headers = {"Prefer": "odata.maxpagesize=5000"})    
        wgJson = result.json()
        
        #Get list of values
        valueLs = wgJson.get('value')
        totalCount = wgJson.get('@odata.count')

        return len(valueLs),valueLs
    except requests.exceptions.Timeout as e: 
        #print(e.message())
        raise 
    except requests.exceptions.InvalidHeader as e:  
        #print(e.message())
        raise 
    except requests.exceptions.InvalidURL as e:  
        #print(e.message())
        raise 
    except requests.exceptions.RequestException as e:  # All others
        #print(e.message())
        raise 
    
    return 0,None
    
# The results will be taskInfo [ animal [], taskInstance [ inputs [] , outputs [] ] ]
def buildTaskInfoList(expDataLs):
    # Return a list of dictionaries where each element is a list of dictionaries.
    taskInfoLs = []
    for procedure in expDataLs:
        animal = []
        animalInfo = {}
        inputs = getInputs(procedure) # We get the inputs from the procedure
        
        
        dateStr = procedure['JAX_EXPERIMENT_STARTDATE']
        for expSample in procedure['EXPERIMENT_SAMPLES']:
            taskInfo = {}
            animal = []
            sampleEntity = expSample['ENTITY']
            animalInfo["animalName"] = sampleEntity['SAMPLE']['JAX_SAMPLE_EXTERNALID']
            animalInfo['stock'] = expSample['ASSAY_DATA']['JAX_ASSAY_STRAINNAME']
            animal.append(animalInfo)
            taskInfo['animal'] = animal
            
            taskInfo['taskInstance'] = getTaskInfo(procedure)
            taskInfo['taskInstance'][0]['inputs'] = inputs;
            taskInfo['taskInstance'][0]['outputs'] = getOutputs(expSample['ASSAY_DATA'],dateStr);
            #print(taskInfo)
            #print()
            #print()
            taskInfoLs.append(taskInfo)
    
    #with open("taskInfoList.json","w") as outfile:
    #    outfile.write(json.dumps(taskInfoLs,indent=4))
        
    return taskInfoLs

def getTaskInfo(procedure):
    # Extract experiment data into inputs and assay data into outputs
    taskInstanceLs = [] # List of one dict the dict is some procedure data followed by a list of inputs followed by a list of outputs
    taskInstanceInfo = {}
    taskInstanceInfo['taskInstanceKey'] = procedure['Id']
    taskInstanceInfo['workflowTaskName'] =  procedure['EntityTypeName']
    taskInstanceInfo['dateComplete'] = procedure['JAX_EXPERIMENT_STARTDATE']
    taskInstanceInfo['reviewedBy'] = 'Ame Willett'
    taskInstanceInfo['dateReviewed'] = procedure['JAX_EXPERIMENT_STARTDATE']
    taskInstanceInfo['taskStatus'] = procedure['JAX_EXPERIMENT_STATUS']
    
    taskInstanceLs.append(taskInstanceInfo)
    return taskInstanceLs

def getInputs(procedure):
    inputLs = []
    # If the name of the input can be found in KOMP.DCCPARAMETERDETAILS then include it.
    keyList = list(procedure.keys())
    for keystr in keyList:
        inputDict = {}
        inputKey = db.verifyImpcCode(keystr)
        if inputKey > 0:
            inputDict['name']= keystr
            inputDict['inputValue'] = procedure[keystr]
            inputDict['inputKey'] = inputKey
            inputLs.append(inputDict)
            
    return inputLs

def getOutputs(expSample,dateStr):
    outputLs = []
    keyList = list(expSample.keys())
    for keystr in keyList:
        outputDict = {}
        outputKey = db.verifyImpcCode(keystr)
        if  outputKey > 0:
            outputDict['name']= keystr
            outputDict['outputValue'] = expSample[keystr]
            outputDict['outputKey'] = outputKey
            outputDict['collectedBy'] = "Amelia Willett"
            outputDict['collectedDate'] = dateStr
            outputLs.append(outputDict)
            
    return outputLs

    

def getPfsTaskInfo():
    
    taskInfoList= {} # For each experiment type
    taskInfoListList= [] #
    
    for expName in kompExperimentNames:
        expEndpoint = experimentEndpointTemplate.format(exp=expName)
        taskInfoList={}
        numberOfKompRequest, valuelist = getExperimentData(expEndpoint)
        print(numberOfKompRequest)
          
        taskInfoList["taskInfo"] = buildTaskInfoList(valuelist)     
        taskInfoListList.append(taskInfoList)

    with open("taskInfoLsLs.json","w") as outfile:
        outfile.write(json.dumps(taskInfoListList,indent=4))
        
    return taskInfoListList
    
if __name__ == '__main__':
    
    
    """
    Get all KOMP Mice
    numberOfKompRequest, valuelist = getKompMice()
    animalInfo = getSampleList(valuelist)
    
    with open("samples.json","w") as outfile:
        outfile.write(json.dumps(animalInfo,indent=4))
    """
    
    with open("taskInfoList.json","w") as outfile:
        outfile.write(json.dumps(getPfsTaskInfo(),indent=4))
         
    print("SUCCESS")
