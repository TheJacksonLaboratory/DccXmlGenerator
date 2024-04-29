
"""
This module validates the procedues from CORE PFS that have been
approved for upload to the DCC. That is, the status is 'Review Conplete'

Rules:
1. All mandatory parameters (assasy attributes) have values.
2. All mandatory parameters have legal values based on some value range.
3. All experiment attributes (metadata) that go up to the DCC are set.
4. Experimenters can be resolved to an experimenter numeric ID.
5. Date ranges make sense. For example, date of experiment compared due date, age of mouse...
6. Very that parameters that use a CV have values form that CV.
7. Verify that there ARE parameters for assays that aren't failed.
8. Procedure versions are valid. 
9. Verify that the mice have ID, DOB, sex, genotype, exit reason if it makes sense, litter ID, life status...
10. Check experiment status: 'Data Reviewed'
11. Check for status codes in assays
12. Images: Check for existence? What of file does not exist? (path and/or name)
"""

from logging import NullHandler
import os
import json
from datetime import datetime
import jaxlims_api as db
import core_api as api


kompExperimentNames = [
"AUDITORY_BRAINSTEM_RESPONSE",
"BODY_COMPOSITION",
"BODY_WEIGHT",
"CLINICAL_BLOOD_CHEMISTRY",
"ELECTROCARDIOGRAM",
"ELECTRORETINOGRAPHY",
"EYE_MORPHOLOGY",
"FUNDUS_IMAGING",
"GLUCOSE_TOLERANCE_TEST",
"GRIP_STRENGTH",
"HEART_WEIGHT",
"HEMATOLOGY",
"HOLEBOARD",
"LIGHT_DARK_BOX",
"OPEN_FIELD",
"SHIRPA_DYSMORPHOLOGY",
"STARTLE_PPI"
]


# Constants
DCC_SIMPLE_TYPE = 1
DCC_MEDIA_TYPE = 3
DCC_SERIES_TYPE = 4
DCC_SERIES_MEDIA_TYPE = 5
DCC_METADATA_TYPE = 7

FIRST_GTT_SERIES =                      'IMPC_IPG_002_001_T0' # t0, t15, t30, t60, t120
FIRST_OFD_DISTANCE_TRAVELLED_SERIES =   'JAX_OFD_005_001_1ST5' # 1st5, 2nd5, 3rd5, 4th5
FIRST_GRS_FORELIMB_SERIES =             'IMPC_GRS_001_001_T1' #t1, t2, t3
FIRST_GRS_FOREHINDLIMB_SERIES =         'IMPC_GRS_002_001_T1' #t1, t2, t3
FIRST_HBD_HOLEPOKE_SEQUENCE_SERIES =    'JAX_HBD_002_001'  # Comes in as a single string. Needs to be converted into a series.
FIRST_SHIRPA_DYS_IMAGE_SERIES =         'IMPC_CSD_051_001_1'
FIRST_EYE_SLITLAMP_IMAGE_SERIES =       'IMPC_EYE_051_001_1'
FIRST_EYE_FUNDUS_IMAGE_SERIES =         'IMPC_EYE_050_001_1'
FIRST_ECG_IMAGE_SERIES =                'IMPC_ECG_025_001_f1'


seriesImpcCodes = [
    FIRST_GTT_SERIES, 
    FIRST_OFD_DISTANCE_TRAVELLED_SERIES,
    FIRST_GRS_FORELIMB_SERIES,
    FIRST_GRS_FOREHINDLIMB_SERIES,
    FIRST_HBD_HOLEPOKE_SEQUENCE_SERIES
]

"""
IMPC_CSD_085_001
IMPC_ECG_025_001
IMPC_EYE_050_001
IMPC_EYE_051_001
"""
# TODO Get from PFS
seriesMediaImpcCodes = [
FIRST_SHIRPA_DYS_IMAGE_SERIES,
FIRST_EYE_SLITLAMP_IMAGE_SERIES,
FIRST_EYE_FUNDUS_IMAGE_SERIES,
FIRST_ECG_IMAGE_SERIES
]

############################# MICE/SAMPLES #################

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

def removeUnderscoresFromCvValue(key, outputvalue):
    # The jerks at Thermo Fisher can't handle commas in their CVs.
    if isinstance(outputvalue,str):
        if 'EYE' in key:
            return outputvalue.replace('_',',')
        if 'CSD' in key:
            return outputvalue.replace('_',',') 
    
    return outputvalue
 
def getOutputs(expSample,dateStr):
    outputLs = []
    keyList = list(expSample.keys())
    for keystr in keyList:
        outputDict = {}
        # Check for failed output
        if (keystr+'_QC') in expSample:
            outputDict['statusCode'] = expSample[(keystr+'_QC')]  
            if outputDict['statusCode'] == '-':
                outputDict['statusCode'] = ''  # Status code of '-' means no qc issue
        else:
                outputDict['statusCode'] = ''
        
        if isSeries(keystr): # We must construct it
            outputDict = getSeriesOutput(expSample,keystr,dateStr)
            if outputDict != None:
                outputLs.append(outputDict)
        elif isMediaSeries(keystr):# We must construct it
            outputDict = getMediaSeriesOutput(expSample,keystr,dateStr)
            if outputDict != None:
                outputLs.append(outputDict)
        else:  # Simple type or ignore
            if 'JAX_' in keystr or 'IMPC_' in keystr:
                outputKey = db.verifyImpcCode(keystr)
                if  outputKey > 0:
                    outputDict['name']= keystr
                    outputDict['outputValue'] = removeUnderscoresFromCvValue(keystr,expSample[keystr])
                    outputDict['outputKey'] = outputKey
                    outputDict['collectedDate'] = dateStr
                    
                    outputLs.append(outputDict)
            
    return outputLs


def getSeriesOutput(expSample,keystr,dateStr):
    outputDictValue = {}
    outputDict = {}
    idx=15 # For "JAX_"
    # Build up the series. A dictionary. Key is increment value is value
    if keystr == FIRST_GTT_SERIES: # t0, t15, t30, t60, t120
        outputDictValue["0"] = expSample[keystr]
        outputDictValue["15"] = expSample[keystr.replace('t0','t15')]
        outputDictValue["30"] = expSample[keystr.replace('t0','t30')]
        outputDictValue["60"] = expSample[keystr.replace('t0','t60')]
        outputDictValue["120"] = expSample[keystr.replace('t0','t120')]
        idx = 16 # i.e. IMPC_
    elif  keystr == FIRST_OFD_DISTANCE_TRAVELLED_SERIES: # 1st5, 2nd5, 3rd5, 4th5
        outputDictValue["1"] = expSample[keystr]
        outputDictValue["2"] = expSample[keystr.replace('1ST5','2ND5')]
        outputDictValue["3"] = expSample[keystr.replace('1ST5','3RD5')]
        outputDictValue["4"] = expSample[keystr.replace('1ST5','4TH5')]
    elif keystr == FIRST_GRS_FORELIMB_SERIES or keystr == FIRST_GRS_FOREHINDLIMB_SERIES:  #t1, t2, t3
        outputDictValue["1"] = expSample[keystr]
        outputDictValue["2"] = expSample[keystr.replace('T1','T2')]
        outputDictValue["3"] = expSample[keystr.replace('T1','T3')]
        idx = 16 # i.e. IMPC_
    elif keystr == FIRST_HBD_HOLEPOKE_SEQUENCE_SERIES:  # Comes in as a single string. Needs to be converted
        pokes = expSample[keystr].split('-')
        for i in range(len(pokes)):
            outputDictValue[str(i)] = str(pokes[i])
    else:
        # Error
        return None
    
    outputDict['name'] = keystr[0:idx]
    outputDict['outputValue'] = outputDictValue
    outputDict['outputKey'] = db.verifyImpcCode(keystr[0:idx])  # Must exist
    outputDict['collectedBy'] = "Amelia Willett"  # TODO Get from config file?
    outputDict['collectedDate'] = dateStr
    
    return outputDict 

def mediaFileSftpName(directory_name,fullyQualifedPath):
    # build the destination of this file on the SFTP server
    # TODO - Test for existence.
    if fullyQualifedPath is None or len(fullyQualifedPath) == 0:
        return None
    
    filename_only = os.path.basename(fullyQualifedPath)
    str = 'sftp://bhjlk02lp.jax.org/images/' + directory_name + filename_only 
    
    return str
 

def getMediaSeriesOutput(expSample,keystr,dateStr):
    
    outputDictValue = {}
    outputDict = {}
    idx = 16
    # Build up the series. A dictionary. Key is increment value is value
    if keystr == FIRST_SHIRPA_DYS_IMAGE_SERIES: 
        outputDictValue["1"] = mediaFileSftpName('IMPC_CSD_003',expSample[keystr])
        outputDictValue["2"] = mediaFileSftpName('IMPC_CSD_003',expSample[keystr.replace('1','2')])
        outputDictValue["3"] = mediaFileSftpName('IMPC_CSD_003',expSample[keystr.replace('1','3')])
        outputDictValue["4"] = mediaFileSftpName('IMPC_CSD_003',expSample[keystr.replace('1','4')])
        outputDictValue["5"] = mediaFileSftpName('IMPC_CSD_003',expSample[keystr.replace('1','5')])
        outputDictValue["6"] = mediaFileSftpName('IMPC_CSD_003',expSample[keystr.replace('1','6')])
    elif  keystr == FIRST_EYE_SLITLAMP_IMAGE_SERIES:
        outputDictValue["1"] = mediaFileSftpName('IMPC_EYE_001',expSample[keystr])
        outputDictValue["2"] = mediaFileSftpName('IMPC_EYE_001',expSample[keystr.replace('1','2')])
        outputDictValue["3"] = mediaFileSftpName('IMPC_EYE_001',expSample[keystr.replace('1','3')])
        outputDictValue["4"] = mediaFileSftpName('IMPC_EYE_001',expSample[keystr.replace('1','4')])
        outputDictValue["5"] = mediaFileSftpName('IMPC_EYE_001',expSample[keystr.replace('1','5')])
        outputDictValue["6"] = mediaFileSftpName('IMPC_EYE_001',expSample[keystr.replace('1','6')])
    elif keystr == FIRST_EYE_FUNDUS_IMAGE_SERIES:
        outputDictValue["1"] = mediaFileSftpName('IMPC_EYE_001',expSample[keystr])
        outputDictValue["2"] = mediaFileSftpName('IMPC_EYE_001',expSample[keystr.replace('1','2')])
        outputDictValue["3"] = mediaFileSftpName('IMPC_EYE_001',expSample[keystr.replace('1','3')])
        outputDictValue["4"] = mediaFileSftpName('IMPC_EYE_001',expSample[keystr.replace('1','4')])
        outputDictValue["5"] = mediaFileSftpName('IMPC_EYE_001',expSample[keystr.replace('1','5')])
    elif keystr == FIRST_ECG_IMAGE_SERIES:  # Comes in as a single string. Needs to be converted
        outputDictValue["1"] = mediaFileSftpName('IMPC_ECG_003',expSample[keystr])
        outputDictValue["2"] = mediaFileSftpName('IMPC_ECG_003',expSample[keystr.replace('f1','f2')])
    else:
        # Error
        return None
    # Remove any None's from the Series
    for key in outputDictValue:
        if outputDictValue[key] is None:
            outputDictValue.pop(key)
            
    outputDict['name'] = keystr[0:idx]
    outputDict['outputValue'] = outputDictValue
    outputDict['outputKey'] = db.verifyImpcCode(keystr[0:idx])  # Must exist
    outputDict['collectedBy'] = "Amelia Willett"  # TODO Get from config file?
    outputDict['collectedDate'] = dateStr
    
    return outputDict 

def isSeries(impcCode):
    # If this is the IMPC code for a series and if it is the first one in the series, return True, else False
    if impcCode.upper() in seriesImpcCodes or isMediaSeries(impcCode):
        return True
    
    return False

def isMediaSeries(impcCode):
    # If this is the IMPC code for a series and if it is the first one in the series, return True, else False
    if impcCode.upper() in seriesMediaImpcCodes:
        return True
    
    return False

def getPfsAnimalInfo():
    # Return a list of animal info
    numberOfKompRequest, valuelist = api.getKompMice()

def getPfsTaskInfo():
    taskInfoList= {} # For each experiment type
    taskInfoListList= [] #
    
    for expName in kompExperimentNames:
        taskInfoList={}
        numberOfKompRequest, valuelist = api.getExperimentData(expName)
        print("Number of requests:" + str(numberOfKompRequest))
          
        with open(expName+".json","w") as outfile:
            outfile.write(json.dumps(valuelist,indent=4))
        
    return valuelist

"""
Example of a PUT
URL = https://jacksonlabstest.platformforscience.com/KOMP_UAT_Testing_01202024/odata/KOMP_BODY_WEIGHT_ASSAY_DATA('XBWE1')
Body =
{
    "Barcode": "XBWE1",
    "JAX_ASSAY_PENBARCODE": "PN26407",
    "JAX_ASSAY_PRIMARYIDVALUE": "R",
    "JAX_ASSAY_SEX": "F",
    "JAX_ASSAY_DATEOFBIRTH": "2024-01-19",
    "JAX_ASSAY_STRAINNAME": "JR038347",
    "JAX_ASSAY_TEST_DATE": "2024-02-14",
    "JAX_ASSAY_TESTER": "Jade Kaplan",
    "IMPC_BWT_001_001": 18.72,
    "IMPC_BWT_001_001_QC": "Above upper limit of quantitation",
    "IMPC_BWT_002_001": "-",
    "JAX_ASSAY_ASSAYFAILREASON": "Procedure QC Failed",
    "JAX_ASSAY_ASSAYFAILCOMMENTS": "Did this work?",
    "IMPC_BWT_005_001": "EM732"
}
"""

if __name__ == '__main__':
    
    api.updateAssayWithFailReason('BODY_WEIGHT','XBWE1','Procedure QC Failed','monday, april 29')
    api.updateExperimentStatus('BODY_WEIGHT','KBWE1','Data Public','monday the 29th')
    """
    Get all KOMP Mice))
    """
    db.init()
    with open("taskInfoList.json","w") as outfile:
        outfile.write(json.dumps(getPfsTaskInfo(),indent=4))
    db.close()
    print("SUCCESS")
