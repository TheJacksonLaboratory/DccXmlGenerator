
from logging import NullHandler
import requests
from requests.auth import HTTPBasicAuth
import os
import json
from datetime import datetime
import jaxlims_api as db

import read_config as cfg
from datetime import timedelta

import re

import my_logger
import csv


impcCodeLookups = {
'IMPC_ABR_001_001': '',
'IMPC_ABR_004_001': '',
'IMPC_ABR_006_001': '',
'IMPC_ABR_008_001': '',
'IMPC_ABR_010_001': '',
'IMPC_ABR_012_001': '',
'IMPC_ABR_014_001': '',
'IMPC_ABR_028_001': '',
'IMPC_ABR_036_001': '',
'IMPC_ABR_037_001': '',
'IMPC_ABR_038_001': '',
'IMPC_ABR_039_001': '',
'IMPC_ABR_040_001': '',
'IMPC_ABR_041_001': '',
'IMPC_ABR_042_001': '',
'IMPC_ABR_043_001': '',
'IMPC_ABR_044_001': '',
'IMPC_ABR_045_001': '',
'IMPC_ABR_046_001': '',
'IMPC_ABR_047_001': '',
'IMPC_ABR_048_001': '',
'IMPC_ABR_049_001': '',
'IMPC_ABR_050_001': '',
'IMPC_ABR_051_001': '',
'IMPC_ABR_052_001': '',
'IMPC_ABR_053_001': '',
'IMPC_ABR_054_001': '',
'IMPC_ACS_001_001': '',
'IMPC_ACS_002_001': '',
'IMPC_ACS_003_001': '',
'IMPC_ACS_004_001': '',
'IMPC_ACS_005_001': '',
'IMPC_ACS_006_001': '',
'IMPC_ACS_007_001': '',
'IMPC_ACS_008_001': '',
'IMPC_ACS_009_001': '',
'IMPC_ACS_010_001': '',
'IMPC_ACS_011_001': '',
'IMPC_ACS_012_001': '',
'IMPC_ACS_013_001': '',
'IMPC_ACS_014_001': '',
'IMPC_ACS_015_001': '',
'IMPC_ACS_016_001': '',
'IMPC_ACS_017_001': '',
'IMPC_ACS_018_001': '',
'IMPC_ACS_019_001': '',
'IMPC_ACS_020_001': '',
'IMPC_ACS_021_001': '',
'IMPC_ACS_022_001': '',
'IMPC_ACS_023_001': '',
'IMPC_ACS_024_001': '',
'IMPC_ACS_025_001': '',
'IMPC_ACS_026_001': '',
'IMPC_ACS_027_001': '',
'IMPC_ACS_028_001': '',
'IMPC_ACS_029_001': '',
'IMPC_ACS_030_001': '',
'IMPC_ACS_031_001': '',
'IMPC_ACS_032_001': '',
'IMPC_ACS_033_001': '',
'IMPC_ACS_034_001': '',
'IMPC_ACS_035_001': '',
'IMPC_ACS_036_001': '',
'IMPC_ACS_037_001': '',
'IMPC_ACS_038_001': '',
'IMPC_ACS_039_001': '',
'IMPC_ACS_040_001': '',
'IMPC_BWT_001_001': '',
'IMPC_BWT_002_001': '',
'IMPC_BWT_003_001': '',
'IMPC_BWT_004_001': '',
'IMPC_BWT_005_001': '',
'IMPC_BWT_007_001': '',
'IMPC_CBC_001_001': '',
'IMPC_CBC_002_001': '',
'IMPC_CBC_003_001': '',
'IMPC_CBC_004_001': '',
'IMPC_CBC_005_001': '',
'IMPC_CBC_006_001': '',
'IMPC_CBC_007_001': '',
'IMPC_CBC_008_001': '',
'IMPC_CBC_009_001': '',
'IMPC_CBC_010_001': '',
'IMPC_CBC_011_001': '',
'IMPC_CBC_012_001': '',
'IMPC_CBC_013_001': '',
'IMPC_CBC_014_001': '',
'IMPC_CBC_015_001': '',
'IMPC_CBC_016_001': '',
'IMPC_CBC_017_001': '',
'IMPC_CBC_018_001': '',
'IMPC_CBC_026_001': '',
'IMPC_CBC_033_001': '',
'IMPC_CBC_034_001': '',
'IMPC_CBC_035_001': '',
'IMPC_CBC_036_001': '',
'IMPC_CBC_037_001': '',
'IMPC_CBC_038_001': '',
'IMPC_CBC_039_001': '',
'IMPC_CBC_040_001': '',
'IMPC_CBC_041_001': '',
'IMPC_CBC_042_001': '',
'IMPC_CBC_043_001': '',
'IMPC_CBC_044_001': '',
'IMPC_CBC_045_001': '',
'IMPC_CBC_046_001': '',
'IMPC_CBC_047_001': '',
'IMPC_CBC_048_001': '',
'IMPC_CBC_049_001': '',
'IMPC_CBC_051_001': '',
'IMPC_CBC_056_001': '',
'IMPC_CBC_057_001': '',
'IMPC_CBC_059_001': '',
'IMPC_CSD_001_001': '',
'IMPC_CSD_002_001': '',
'IMPC_CSD_003_001': '',
'IMPC_CSD_004_001': '',
'IMPC_CSD_005_001': '',
'IMPC_CSD_006_001': '',
'IMPC_CSD_007_001': '',
'IMPC_CSD_008_001': '',
'IMPC_CSD_009_001': '',
'IMPC_CSD_010_001': '',
'IMPC_CSD_011_001': '',
'IMPC_CSD_012_001': '',
'IMPC_CSD_013_001': '',
'IMPC_CSD_014_001': '',
'IMPC_CSD_015_001': '',
'IMPC_CSD_016_001': '',
'IMPC_CSD_017_001': '',
'IMPC_CSD_018_001': '',
'IMPC_CSD_019_001': '',
'IMPC_CSD_020_001': '',
'IMPC_CSD_021_001': '',
'IMPC_CSD_022_001': '',
'IMPC_CSD_023_001': '',
'IMPC_CSD_024_001': '',
'IMPC_CSD_025_001': '',
'IMPC_CSD_026_001': '',
'IMPC_CSD_027_001': '',
'IMPC_CSD_028_001': '',
'IMPC_CSD_029_001': '',
'IMPC_CSD_030_001': '',
'IMPC_CSD_031_001': '',
'IMPC_CSD_032_001': '',
'IMPC_CSD_033_001': '',
'IMPC_CSD_034_001': '',
'IMPC_CSD_035_001': '',
'IMPC_CSD_036_001': '',
'IMPC_CSD_037_001': '',
'IMPC_CSD_038_001': '',
'IMPC_CSD_039_001': '',
'IMPC_CSD_040_001': '',
'IMPC_CSD_040_002': '',
'IMPC_CSD_041_001': '',
'IMPC_CSD_041_002': '',
'IMPC_CSD_042_001': '',
'IMPC_CSD_042_002': '',
'IMPC_CSD_043_001': '',
'IMPC_CSD_043_002': '',
'IMPC_CSD_044_001': '',
'IMPC_CSD_044_002': '',
'IMPC_CSD_045_001': '',
'IMPC_CSD_045_002': '',
'IMPC_CSD_046_001': '',
'IMPC_CSD_047_001': '',
'IMPC_CSD_048_001': '',
'IMPC_CSD_048_002': '',
'IMPC_CSD_049_001': '',
'IMPC_CSD_049_002': '',
'IMPC_CSD_050_001': '',
'IMPC_CSD_050_002': '',
'IMPC_CSD_051_001': '',
'IMPC_CSD_051_002': '',
'IMPC_CSD_052_001': '',
'IMPC_CSD_052_002': '',
'IMPC_CSD_053_001': '',
'IMPC_CSD_053_002': '',
'IMPC_CSD_054_001': '',
'IMPC_CSD_054_002': '',
'IMPC_CSD_055_001': '',
'IMPC_CSD_055_002': '',
'IMPC_CSD_056_001': '',
'IMPC_CSD_057_001': '',
'IMPC_CSD_058_001': '',
'IMPC_CSD_059_001': '',
'IMPC_CSD_060_001': '',
'IMPC_CSD_061_001': '',
'IMPC_CSD_062_001': '',
'IMPC_CSD_063_001': '',
'IMPC_CSD_064_001': '',
'IMPC_CSD_065_001': '',
'IMPC_CSD_066_001': '',
'IMPC_CSD_067_001': '',
'IMPC_CSD_068_001': '',
'IMPC_CSD_069_001': '',
'IMPC_CSD_070_001': '',
'IMPC_CSD_071_001': '',
'IMPC_CSD_072_001': '',
'IMPC_CSD_073_001': '',
'IMPC_CSD_074_001': '',
'IMPC_CSD_075_001': '',
'IMPC_CSD_076_001': '',
'IMPC_CSD_077_001': '',
'IMPC_CSD_078_001': '',
'IMPC_CSD_079_001': '',
'IMPC_CSD_080_001': '',
'IMPC_CSD_081_001': '',
'IMPC_CSD_082_001': '',
'IMPC_CSD_083_001': '',
'IMPC_CSD_084_001': '',
'IMPC_CSD_085_001': '',
'IMPC_CSD_086_001': '',
'IMPC_DXA_001_001': '',
'IMPC_DXA_002_001': '',
'IMPC_DXA_003_001': '',
'IMPC_DXA_004_001': '',
'IMPC_DXA_005_001': '',
'IMPC_DXA_006_001': '',
'IMPC_DXA_007_001': '',
'IMPC_DXA_008_001': '',
'IMPC_DXA_009_001': '',
'IMPC_DXA_010_001': '',
'IMPC_DXA_011_001': '',
'IMPC_DXA_012_001': '',
'IMPC_DXA_013_001': '',
'IMPC_DXA_014_001': '',
'IMPC_DXA_015_001': '',
'IMPC_DXA_016_001': '',
'IMPC_ECG_001_001': '',
'IMPC_ECG_002_001': '',
'IMPC_ECG_003_001': '',
'IMPC_ECG_004_001': '',
'IMPC_ECG_005_001': '',
'IMPC_ECG_006_001': '',
'IMPC_ECG_007_001': '',
'IMPC_ECG_008_001': '',
'IMPC_ECG_009_001': '',
'IMPC_ECG_009_002': '',
'IMPC_ECG_010_001': '',
'IMPC_ECG_011_001': '',
'IMPC_ECG_012_001': '',
'IMPC_ECG_013_001': '',
'IMPC_ECG_014_001': '',
'IMPC_ECG_015_001': '',
'IMPC_ECG_016_001': '',
'IMPC_ECG_017_001': '',
'IMPC_ECG_018_001': '',
'IMPC_ECG_019_001': '',
'IMPC_ECG_020_001': '',
'IMPC_ECG_025_001': '',
'IMPC_ECG_026_001': '',
'IMPC_ECG_028_001': '',
'IMPC_ECG_030_001': '',
'IMPC_ECG_031_001': '',
'IMPC_EYE_001_001': '',
'IMPC_EYE_002_001': '',
'IMPC_EYE_003_001': '',
'IMPC_EYE_004_001': '',
'IMPC_EYE_005_001': '',
'IMPC_EYE_006_001': '',
'IMPC_EYE_007_001': '',
'IMPC_EYE_008_001': '',
'IMPC_EYE_009_001': '',
'IMPC_EYE_010_001': '',
'IMPC_EYE_011_001': '',
'IMPC_EYE_012_001': '',
'IMPC_EYE_013_001': '',
'IMPC_EYE_014_001': '',
'IMPC_EYE_015_001': '',
'IMPC_EYE_016_001': '',
'IMPC_EYE_017_001': '',
'IMPC_EYE_018_001': '',
'IMPC_EYE_019_001': '',
'IMPC_EYE_020_001': '',
'IMPC_EYE_021_001': '',
'IMPC_EYE_022_001': '',
'IMPC_EYE_023_001': '',
'IMPC_EYE_024_001': '',
'IMPC_EYE_025_001': '',
'IMPC_EYE_026_001': '',
'IMPC_EYE_027_001': '',
'IMPC_EYE_028_001': '',
'IMPC_EYE_029_001': '',
'IMPC_EYE_030_001': '',
'IMPC_EYE_031_001': '',
'IMPC_EYE_032_001': '',
'IMPC_EYE_033_001': '',
'IMPC_EYE_034_001': '',
'IMPC_EYE_035_001': '',
'IMPC_EYE_036_001': '',
'IMPC_EYE_043_001': '',
'IMPC_EYE_044_001': '',
'IMPC_EYE_045_001': '',
'IMPC_EYE_046_001': '',
'IMPC_EYE_047_001': '',
'IMPC_EYE_050_001': '',
'IMPC_EYE_051_001': '',
'IMPC_EYE_080_001': '',
'IMPC_EYE_081_001': '',
'IMPC_EYE_082_001': '',
'IMPC_EYE_083_001': '',
'IMPC_GRS_001_001': '',
'IMPC_GRS_002_001': '',
'IMPC_GRS_003_001': '',
'IMPC_GRS_004_001': '',
'IMPC_GRS_005_001': '',
'IMPC_GRS_006_001': '',
'IMPC_GRS_007_001': '',
'IMPC_GRS_008_001': '',
'IMPC_GRS_009_001': '',
'IMPC_GRS_010_001': '',
'IMPC_GRS_011_001': '',
'IMPC_GRS_012_001': '',
'IMPC_GRS_013_001': '',
'IMPC_GRS_014_001': '',
'IMPC_HEM_001_001': '',
'IMPC_HEM_002_001': '',
'IMPC_HEM_003_001': '',
'IMPC_HEM_004_001': '',
'IMPC_HEM_005_001': '',
'IMPC_HEM_006_001': '',
'IMPC_HEM_007_001': '',
'IMPC_HEM_008_001': '',
'IMPC_HEM_009_001': '',
'IMPC_HEM_010_001': '',
'IMPC_HEM_011_001': '',
'IMPC_HEM_012_001': '',
'IMPC_HEM_013_001': '',
'IMPC_HEM_014_001': '',
'IMPC_HEM_015_001': '',
'IMPC_HEM_016_001': '',
'IMPC_HEM_017_001': '',
'IMPC_HEM_018_001': '',
'IMPC_HEM_020_001': '',
'IMPC_HEM_021_001': '',
'IMPC_HEM_022_001': '',
'IMPC_HEM_024_001': '',
'IMPC_HEM_026_001': '',
'IMPC_HWT_001_001': '',
'IMPC_HWT_003_001': '',
'IMPC_HWT_005_001': '',
'IMPC_HWT_006_001': '',
'IMPC_HWT_007_001': '',
'IMPC_HWT_008_001': '',
'IMPC_HWT_010_001': '',
'IMPC_HWT_011_001': '',
'IMPC_IPG_001_001': '',
'IMPC_IPG_002_001': '',
'IMPC_IPG_003_001': '',
'IMPC_IPG_004_001': '',
'IMPC_IPG_005_001': '',
'IMPC_IPG_006_001': '',
'IMPC_IPG_007_001': '',
'IMPC_IPG_008_001': '',
'IMPC_IPG_013_001': '',
'JAX_ERG_001_001': '',
'JAX_ERG_002_001': '',
'JAX_ERG_003_001': '',
'JAX_ERG_004_001': '',
'JAX_ERG_005_001': '',
'JAX_ERG_006_001': '',
'JAX_ERG_007_001': '',
'JAX_ERG_008_001': '',
'JAX_ERG_009_001': '',
'JAX_ERG_010_001': '',
'JAX_ERG_011_001': '',
'JAX_ERG_012_001': '',
'JAX_ERG_013_001': '',
'JAX_ERG_014_001': '',
'JAX_ERG_015_001': '',
'JAX_ERG_016_001': '',
'JAX_ERG_017_001': '',
'JAX_ERG_018_001': '',
'JAX_ERG_019_001': '',
'JAX_ERG_020_001': '',
'JAX_ERG_021_001': '',
'JAX_ERG_022_001': '',
'JAX_ERG_023_001': '',
'JAX_ERG_024_001': '',
'JAX_ERG_025_001': '',
'JAX_ERG_026_001': '',
'JAX_ERG_027_001': '',
'JAX_ERG_028_001': '',
'JAX_ERG_029_001': '',
'JAX_ERG_030_001': '',
'JAX_ERG_031_001': '',
'JAX_ERG_032_001': '',
'JAX_ERG_033_001': '',
'JAX_ERG_034_001': '',
'JAX_ERG_035_001': '',
'JAX_ERG_036_001': '',
'JAX_ERG_037_001': '',
'JAX_ERG_038_001': '',
'JAX_ERG_039_001': '',
'JAX_ERG_040_001': '',
'JAX_ERG_041_001': '',
'JAX_ERG_042_001': '',
'JAX_ERG_044_001': '',
'JAX_ERG_045_001': '',
'JAX_ERG_046_001': '',
'JAX_ERG_047_001': '',
'JAX_ERG_048_001': '',
'JAX_ERG_049_001': '',
'JAX_ERG_050_001': '',
'JAX_ERG_051_001': '',
'JAX_ERG_052_001': '',
'JAX_ERG_053_001': '',
'JAX_ERG_054_001': '',
'JAX_ERG_055_001': '',
'JAX_ERG_056_001': '',
'JAX_ERG_057_001': '',
'JAX_ERG_058_001': '',
'JAX_ERG_059_001': '',
'JAX_HBD_001_001': '',
'JAX_HBD_002_001': '',
'JAX_HBD_003_001': '',
'JAX_HBD_004_001': '',
'JAX_HBD_005_001': '',
'JAX_HBD_006_001': '',
'JAX_HBD_007_001': '',
'JAX_HBD_008_001': '',
'JAX_HBD_009_001': '',
'JAX_HBD_010_001': '',
'JAX_LDT_001_001': '',
'JAX_LDT_002_001': '',
'JAX_LDT_003_001': '',
'JAX_LDT_004_001': '',
'JAX_LDT_005_001': '',
'JAX_LDT_006_001': '',
'JAX_LDT_007_001': '',
'JAX_LDT_008_001': '',
'JAX_LDT_009_001': '',
'JAX_LDT_010_001': '',
'JAX_LDT_011_001': '',
'JAX_LDT_012_001': '',
'JAX_LDT_013_001': '',
'JAX_LDT_014_001': '',
'JAX_LDT_015_001': '',
'JAX_LDT_016_001': '',
'JAX_LDT_017_001': '',
'JAX_LDT_018_001': '',
'JAX_LDT_019_001': '',
'JAX_OFD_005_001': '',
'JAX_OFD_006_001': '',
'JAX_OFD_007_001': '',
'JAX_OFD_008_001': '',
'JAX_OFD_009_001': '',
'JAX_OFD_010_001': '',
'JAX_OFD_011_001': '',
'JAX_OFD_012_001': '',
'JAX_OFD_013_001': '',
'JAX_OFD_014_001': '',
'JAX_OFD_015_001': '',
'JAX_OFD_016_001': '',
'JAX_OFD_017_001': '',
'JAX_OFD_018_001': '',
'JAX_OFD_019_001': '',
'JAX_OFD_020_001': '',
'JAX_OFD_021_001': '',
'JAX_OFD_022_001': '',
'JAX_OFD_023_001': '',
'JAX_OFD_024_001': '',
'JAX_OFD_025_001': '',
'JAX_OFD_026_001': '',
'JAX_OFD_027_001': '',
'JAX_OFD_028_001': '',
'JAX_OFD_029_001': '',
'JAX_OFD_030_001': '',
'JAX_OFD_031_001': '',
'JAX_OFD_032_001': '',
'JAX_OFD_033_001': '',
'JAX_OFD_034_001': '',
'JAX_OFD_035_001': '',
'JAX_OFD_036_001': '',
'JAX_OFD_037_001': '',
'JAX_OFD_038_001': '',
'JAX_OFD_039_001': '',
'JAX_OFD_041_001': '',
'JAX_OFD_051_001': '',
'JAX_OFD_052_001': ''
}

kompExperimentNames = [
"BODY_WEIGHT",
"AUDITORY_BRAINSTEM_RESPONSE",
"BODY_COMPOSITION",
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
"""
IMPC_GRS_001_001
IMPC_GRS_002_001
IMPC_IPG_002_001
JAX_HBD_002_001
JAX_OFD_005_001     Distance travelled
JAX_OFD_006_001  ??? Number of rears - not colllected
"""

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
def getKompMice():
    
    mycfg = cfg.parse_config(path="config.yml")
      # Setup credentials for database
    baseURL = mycfg['corepfs_database']['baseURL']
    mouseEndpoint = mycfg['corepfs_database']['mouseEndpoint']
    username = mycfg['corepfs_database']['username']
    password = mycfg['corepfs_database']['password']
      
    try:
        my_auth = HTTPBasicAuth(username, password)
        query = baseURL + mouseEndpoint
        result = requests.get(query, auth=my_auth,headers = {"Prefer": "odata.maxpagesize=5000"})    
        wgJson = result.json()
        
        #Get list of values
        valueLs = wgJson.get('value')
        # Make sure we got all the mice
        totalCount = wgJson.get('@odata.count')

        return totalCount,valueLs
    except requests.exceptions.Timeout as e: 
        print(repr(e))
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        print(repr(e))
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        print(repr(e))
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        print(repr(e))
        my_logger.info(repr(e))
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
    # TODO Can I filter out previously uploaded mice?
    sampleDictls = []
    for kompRequest in kompRequestlist:
        mouseSampleLotList = kompRequest["REV_MOUSESAMPLELOT_KOMPREQUEST"]
        for mouseSampleLot in mouseSampleLotList:
            if mouseSampleLot["SAMPLE"] is None:
                continue
            
            sampleDict = mouseSampleLot["SAMPLE"]
            
            # TEMP - filter out garbage from test env
            #if sampleDict["JAX_MOUSESAMPLE_ALLELE"] == None or "(JR0" not in sampleDict["JAX_MOUSESAMPLE_ALLELE"]:
            #    continue
            
            # End of TEMP
            tmpDict = {}
            animalDict = {}
            lineDict = {} 
            litterDict = {}
            genotypesLs = []
            genotypeDict = {}
            
            animalDict["barcode"] = sampleDict["Barcode"]
            animalDict["animalName"] = sampleDict["JAX_SAMPLE_EXTERNALID"]
            animalDict["dateBorn"] = sampleDict["JAX_MOUSESAMPLE_DATEOFBIRTH"]
            sex =''
            if sampleDict["JAX_MOUSESAMPLE_SEX"] == 'M':
                sex = 'Male'
            else:
                sex = 'Female'
            animalDict["sex"] = sex
            
            animalDict["generation"] = "F1"  # Is this OK
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


def updateAssayWithFailReason(expName,assayBarcode,failreason,failcomments):
    # Update the assay failed reason and comments
  
    put_data = getAssay(expName,assayBarcode)
    put_data['Barcode'] = assayBarcode
    put_data['JAX_ASSAY_ASSAYFAILREASON'] = failreason
    put_data['JAX_ASSAY_ASSAYFAILCOMMENTS'] = failcomments
    
    mycfg = cfg.parse_config(path="config.yml")
    baseURL = mycfg['corepfs_database']['baseURL']
    username = mycfg['corepfs_database']['username']
    password = mycfg['corepfs_database']['password']
    
    my_auth = HTTPBasicAuth(username, password)
    query = baseURL + "KOMP_{0}_ASSAY_DATA('{1}')".format(expName,assayBarcode) # expName is like BODY_WEIGHT

    #print(put_data)
    my_logger.info(put_data)
    
    result = requests.put(query, data=json.dumps(put_data), auth=my_auth,headers = {"Content-Type": "application/json", "If-Match": "*" })  
    
    #print(result.text)
    my_logger.info(result.text)
    # Did it work? Chekc for code 200
    return 200
    
def updateExperimentStatus(expName,expBarcode,status='Data Sent to DCC',comments=''):
   
    put_data = getExperiment(expName,expBarcode)
    put_data['Barcode'] = expBarcode
    put_data['JAX_EXPERIMENT_STATUS'] = status
    put_data['JAX_EXPERIMENT_COMMENTS'] = comments
    my_logger.info("PUT data:" + str(put_data))
    s = f"Name: {expName} Barcode: {expBarcode} Status: {status} Comments: {comments}"
    my_logger.info(s)
    
    
    mycfg = cfg.parse_config(path="config.yml")
    baseURL = mycfg['corepfs_database']['baseURL']
    username = mycfg['corepfs_database']['username']
    password = mycfg['corepfs_database']['password']

    
    my_auth = HTTPBasicAuth(username, password)
    query = baseURL + "{0}('{1}')".format(expName,expBarcode) # expName is like KOMP_BODY_WEIGHT_EXPERIMENT

    result = requests.put(query, data=json.dumps(put_data), auth=my_auth,headers = {"Content-Type": "application/json", "If-Match": "*" })  
    my_logger.info(result.text)
    # Did it work? Chekc for code 200   
    if result.status_code == 200 or result.status_code == 5000: # CORE bug : returns error 5000 but PUT works
        my_logger.info("BARCODE " + expBarcode + " succesfully update to " + status)  
    else:
        #print("BARCODE " + expBarcode + " failed to update to " + status)
        my_logger.info("BARCODE " + expBarcode + " failed to update to " + status + ". Return code: " + str(result.status_code))  
                
        
  
def getExperiment(expName:str, expBarcode:str) -> dict:
    # Get the experiment from the barcode and return it as a dict
    try:
        mycfg = cfg.parse_config(path="config.yml")
        baseURL = mycfg['corepfs_database']['baseURL']
        username = mycfg['corepfs_database']['username']
        password = mycfg['corepfs_database']['password']
        
        my_auth = HTTPBasicAuth(username, password)
        query = baseURL + "{0}('{1}')".format(expName, expBarcode) # expName is like BODY_WEIGHT

        result = requests.get(query, auth=my_auth,headers = {"Content-Type": "application/json", "If-Match": "*" })  
        cont = result.content
        if cont == None:
            my_logger.info("No content returned for {0} {1}".format(expName,expBarcode))    
            return {}
        d = json.loads(cont.decode('utf-8'))
        d.pop("@odata.context", None)
    except Exception as e:
        my_logger.info(repr(e))
        return {}
    return d
      
      
def getAssay(expName:str, assayBarcode:str) -> dict:
    # Get the experiment from the barcode and return it as a dict
    mycfg = cfg.parse_config(path="config.yml")
    baseURL = mycfg['corepfs_database']['baseURL']
    username = mycfg['corepfs_database']['username']
    password = mycfg['corepfs_database']['password']
    
    my_auth = HTTPBasicAuth(username, password)
    query = baseURL + "KOMP_{0}_ASSAY_DATA('{1}')".format(expName, assayBarcode) # expName is like BODY_WEIGHT

    result = requests.get(query, auth=my_auth,headers = {"Content-Type": "application/json", "If-Match": "*" })  
    cont = result.content
    
    d = json.loads(cont.decode('utf-8'))
    d.pop("@odata.context", None)
    return d

"""
    This function updates the experiment status in the PFS database using RESTful API calls.
    It logs in, updates the status for each experiment in the provided list, and then logs out.
    
    No return value, but logs the success or failure of each update.
    
    status_message: The status message to set for the experiments.
    experiment_name: The name of the experiment type (e.g., "KOMP_BODY_WEIGHT_EXPERIMENT"). 
    exp_ls: A list of experiment barcodes to update.
"""
def restful_update(status_message,experiment_name,exp_ls):

    mycfg = cfg.parse_config(path="config.yml")
    baseURL = mycfg['corepfs_database']['baseURL']
    name = mycfg['corepfs_database']['username']
    password = mycfg['corepfs_database']['password']
    # Right now looks only for PROD or TEST  
    tenant = "PROD" if "PROD" in baseURL else "TEST" 

    loginUrl =  "https://jacksonlabstest.platformforscience.com/sdklogin/"
    updateUrl = "https://jacksonlabstest.platformforscience.com/sdk/"

    headers = {
        'Content-Type':'application/json',
        'If-Match': '*',
        'Accept': 'application/json'
    }
    
    # login template
    login_template = { 
            "request" : 
            { "sdkCmd": "sdk-login",
                "typeParam": "*",
                "data": {
                "lims_userName": "",
                "lims_password": "",
                "accountRef": { "name": "" }
            },
            "responseOptions": []
            } 
        }

    login_template["request"]["data"]["lims_userName"] = name
    login_template["request"]["data"]["lims_password"] = password
    login_template["request"]["data"]["accountRef"]["name"] = tenant  # e.g. PROD
    
    session= requests.Session()
    resp = session.post(loginUrl, headers=headers, data=json.dumps(login_template))

    if resp.status_code == 200:
        my_logger.info("Login successful")
    else:
        my_logger.info("Login failed")
        my_logger.info(resp.content)
        return  # Bail
    
    # Add cookie with jsessionId
    jsessionId = json.loads(resp.content)["response"]["data"]["jsessionid"]
    session.cookies.set("JSESSIONID", jsessionId)
    
    update_body_template = {
          "request": {
            "sdkCmd": "update",
            "data": {
            "values": {
                "JAX_EXPERIMENT_STATUS": {
                    "stringData": ""
                }
            },
            "name": "",
            "active": 1,
            "barcode": ""
        },
        "responseOptions": [
            "CONTEXT_GET",
            "MESSAGE_LEVEL_WARN"
        ],
        "typeParam": "",
        "logicOptions": [
            "EXECUTE_TRIGGERS"
        ]
     }
     }
   
    # Loop through the experiment list
    try:
       experiment_name = experiment_name.replace("_", " ")
       update_body_template["request"]["data"]["values"]["JAX_EXPERIMENT_STATUS"]["stringData"] = status_message
       update_body_template["request"]["typeParam"] = experiment_name
       
       for barcode in exp_ls:
           # Now the UPDATE
           update_body_template["request"]["data"]["barcode"] = barcode
           update_body_template["request"]["data"]["name"] = barcode
           # Yes, we use a GET to do the update  
           resp = session.get(updateUrl, headers=headers, data=json.dumps(update_body_template))
        
           # Check if the response is successful
           if resp.status_code == 200:
            my_logger.info("Update successful: " + barcode)
           else:
            my_logger.info("Update failed: " + barcode)
            my_logger.info(resp.content)
            
    except Exception as e:
        my_logger.info(f"UPDATE error occurred: {e}")

   # Always logout
    finally:
        login_template["request"]["data"]["sdkCmd"] = "sdk-logout"
        resp = session.post(loginUrl+"?sessionid="+jsessionId, headers=headers, data=json.dumps(login_template))
   
        # Check if the response is successful
        if resp.status_code == 200:
            my_logger.info("Logout successful")
        else:
            my_logger.info("Logout failed")
            my_logger.info(resp.content)

    

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



def getExperimentData(experimentname):
        
    try:
        mycfg = cfg.parse_config(path="config.yml")
        baseURL = mycfg['corepfs_database']['baseURL']
        username = mycfg['corepfs_database']['username']
        password = mycfg['corepfs_database']['password']
        experimentEndpointTemplate = mycfg['corepfs_database']['experimentEndpointTemplate']
        
        experimentEndpoint = experimentEndpointTemplate.format(exp=experimentname)
        
        my_auth = HTTPBasicAuth(username, password)
        query = baseURL + experimentEndpoint

        result = requests.get(query, auth=my_auth,headers = {"Prefer": "odata.maxpagesize=5000"})    
        wgJson = result.json()
        
        #Get list of values
        valueLs = []
        totalCount = 0
        if 'value' in wgJson.keys(): # A list of dicts
            valueLs = wgJson.get('value') 
            totalCount = wgJson.get('@odata.count')
        else:   # A single dict
            valueLs.append(wgJson)
            totalCount = 1
            
        my_logger.info("Number of requests for {0}:".format(experimentname) + str(totalCount))  
        
        if valueLs != None:
            return len(valueLs),valueLs
        else:
            return 0, []
        
    except requests.exceptions.Timeout as e: 
        print(repr(e))
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        print(repr(e))
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        print(repr(e))
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        print(repr(e))
        my_logger.info(repr(e))
        raise 
    
    
# The results will be taskInfo [ animal [], taskInstance [ inputs [] , outputs [] ] ]
def buildTaskInfoList(expDataLs):
    # Return a list of dictionaries where each element is a list of dictionaries.
    taskInfoLs = []
    for procedure in expDataLs:
        animal = []
        animalInfo = {}
        taskInfo = {}
        inputs = getInputs(procedure) # We get the inputs from the procedure (experiment)
        
        # Remove? dateStr = procedure['JAX_EXPERIMENT_STARTDATE']
        for expSample in procedure['EXPERIMENT_SAMPLES']:
            taskInfo = {}
            animal = []
            animalInfo = {}
            # Get the date from the assay data but if not possible
            #  use today's date. If the task is cancelled then the date is today's date
            dateStr = None  # Cancelled assays might not have complete dates
            
            if expSample['ASSAY_DATA'] == None:
                continue
            
            if 'JAX_ASSAY_TEST_DATE' in expSample['ASSAY_DATA'].keys():
                dateStr =  expSample['ASSAY_DATA']['JAX_ASSAY_TEST_DATE']
            elif 'JAX_ASSAY_TESTDATE' in expSample['ASSAY_DATA'].keys():
                dateStr =  expSample['ASSAY_DATA']['JAX_ASSAY_TESTDATE']
            elif 'IMPC_CBC_046_001' in expSample['ASSAY_DATA'].keys():
                dateStr =  expSample['ASSAY_DATA']['IMPC_CBC_046_001']
            
            if dateStr == None:    
                dateStr = datetime.now().strftime("%Y-%m-%d")
                
            sampleEntity = expSample['ENTITY']
            animalInfo["animalName"] = sampleEntity['SAMPLE']['JAX_SAMPLE_EXTERNALID']
            
            assayData = expSample['ASSAY_DATA'] 
            if 'JAX_ASSAY_STRAINNAME' not in assayData.keys():  # Some CSD seems to be missing these...
                my_logger.info("No JAX_ASSAY_STRAINNAME in " + str(assayData))  
                continue    # Skip it
            
            animalInfo['stock'] = assayData['JAX_ASSAY_STRAINNAME']
            animal.append(animalInfo)
            taskInfo['animal'] = animal
            
            taskInfo['taskInstance'] = getTaskInfo(procedure,expSample['Id'])
            taskInfo['taskInstance'][0]['dateComplete'] = dateStr   # from the ASSAY
            taskInfo['taskInstance'][0]['inputs'] = inputs   # from the EXPERIMENT - not the ASSAY
            taskInfo['taskInstance'][0]['outputs'] = getOutputs(expSample['ASSAY_DATA'],dateStr)  # dateStr unneeded
            
            taskInfo["taskInstance"][0]["taskStatus"] = expSample['ASSAY_DATA']['JAX_ASSAY_ASSAYFAILREASON'] # Is dash OK?
            taskInfoLs.append(taskInfo)
    return taskInfoLs

def getTaskInfo(procedure,taskInstanceKey):
    # Extract experiment data into inputs and assay data into outputs
    taskInstanceLs = [] # List of one dict the dict is some procedure data followed by a list of inputs followed by a list of outputs
    taskInstanceInfo = {}
    taskInstanceInfo['taskInstanceKey'] =   taskInstanceKey
    taskInstanceInfo['workflowTaskName'] =  procedure['EntityTypeName']
    # TODO - remove taskInstanceInfo['dateComplete'] = procedure['JAX_EXPERIMENT_STARTDATE']
    taskInstanceInfo['reviewedBy'] = 'Ame Willett'
    taskInstanceInfo['dateReviewed'] = procedure['JAX_EXPERIMENT_STARTDATE']
    # Cancelled at the ASSAY level. Not at experiment 
    taskInstanceInfo['taskStatus'] = "Complete"  # The default. Assume complete until proven otherwise
    taskInstanceInfo['barcode'] = procedure['Barcode']  
    
    taskInstanceLs.append(taskInstanceInfo)
    return taskInstanceLs

def getInputs(procedure):
    inputLs = []
    # If the name of the input can be found in KOMP.DCCPARAMETERDETAILS then include it.
    keyList = list(procedure.keys())
    for keystr in keyList:
        inputDict = {}
        inputKey = db.getKeyFromImpcCode(keystr)
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
            else:
                continue  # Skip it??
        elif isMediaSeries(keystr):# We must construct it
            outputDict = getMediaSeriesOutput(expSample,keystr,dateStr)
            if outputDict != None:
                outputLs.append(outputDict)
        else:  # Simple type or ignore
            if 'JAX_' in keystr or 'IMPC_' in keystr:
                outputKey = db.getKeyFromImpcCode(keystr)
                if  outputKey > 0:
                    outputDict['name']= keystr
                    outputDict['outputValue'] = removeUnderscoresFromCvValue(keystr,expSample[keystr])
                    outputDict['outputKey'] = outputKey
                    outputDict['collectedBy'] = expSample["JAX_ASSAY_TESTER"]
                    if 'JAX_ASSAY_TEST_DATE' in expSample.keys():
                        outputDict['collectedDate'] = expSample["JAX_ASSAY_TEST_DATE"]
                    elif 'JAX_ASSAY_TESTDATE' in expSample.keys():
                        outputDict['collectedDate'] = expSample["JAX_ASSAY_TESTDATE"]
                    elif 'IMPC_CBC_046_001' in expSample.keys():  # "Date-Time Collection"
                        outputDict['collectedDate'] = expSample["IMPC_CBC_046_001"]
                    else:    
                        outputDict['collectedDate'] = ""
                    
                    outputLs.append(outputDict)
            
    return outputLs


def getSeriesOutput(expSample,keystr,dateStr):
    outputDictValue = {}
    outputDict = {}
    idx=15 # For "JAX_"
    # Build up the series. A dictionary. Key is increment value is value
    if keystr == FIRST_GTT_SERIES: # t0, t15, t30, t60, t120
        outputDictValue["0"] = expSample[keystr]
        outputDictValue["15"] = expSample[keystr.replace('T0','T15')]
        outputDictValue["30"] = expSample[keystr.replace('T0','T30')]
        outputDictValue["60"] = expSample[keystr.replace('T0','T60')]
        outputDictValue["120"] = expSample[keystr.replace('T0','T120')] 
        idx = 16 # i.e. IMPC_
    elif  keystr == FIRST_OFD_DISTANCE_TRAVELLED_SERIES: # 1st5, 2nd5, 3rd5, 4th5
        outputDictValue["5"] = expSample[keystr]
        outputDictValue["10"] = expSample[keystr.replace('1ST5','2ND5')]
        outputDictValue["15"] = expSample[keystr.replace('1ST5','3RD5')]
        outputDictValue["20"] = expSample[keystr.replace('1ST5','4TH5')]
    elif keystr == FIRST_GRS_FORELIMB_SERIES or keystr == FIRST_GRS_FOREHINDLIMB_SERIES:  #t1, t2, t3
        outputDictValue["1"] = expSample[keystr]
        outputDictValue["2"] = expSample[keystr.replace('T1','T2')]
        outputDictValue["3"] = expSample[keystr.replace('T1','T3')]
        idx = 16 # i.e. IMPC_
    elif keystr == FIRST_HBD_HOLEPOKE_SEQUENCE_SERIES:  # Comes in as a single string. Needs to be converted
        pokes = expSample[keystr]
        if pokes == None:
            my_logger.info("Output value for Holeboard Holepoke Sequence is None!")
            return None
        if '-' in pokes:
            pokes = expSample[keystr].split('-')
            for i in range(len(pokes)):
                outputDictValue[str(i)] = str(pokes[i])
        else:
            my_logger.info("Output value for Holeboard Holepoke Sequence {0}: {1}".format(keystr,pokes))
            outputDictValue["0"] = pokes
    else:
        # Error
        return None
    
    outputDict['name'] = keystr[0:idx]
    outputDict['outputValue'] = outputDictValue
    outputDict['outputKey'] = db.getKeyFromImpcCode(keystr[0:idx])  # Must exist
    outputDict['collectedBy'] = expSample["JAX_ASSAY_TESTER"]
    outputDict['collectedDate'] = expSample["JAX_ASSAY_TEST_DATE"]
    if 'JAX_ASSAY_TEST_DATE' in expSample.keys():
        outputDict['collectedDate'] =  expSample['JAX_ASSAY_TEST_DATE']
    elif 'JAX_ASSAY_TESTDATE' in expSample.keys():
        outputDict['collectedDate'] = expSample['JAX_ASSAY_TESTDATE']
    else:    
        outputDict['collectedDate'] = ""
    
    return outputDict 

def mediaFileSftpName(directory_name,fullyQualifedPath):
    # build the destination of this file on the SFTP server
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
    outputDict['outputKey'] = db.getKeyFromImpcCode(keystr[0:idx])  # Must exist
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

def getPfsTaskInfo():
    taskInfoList= {} # For each experiment type
    taskInfoListList= [] #
    
    # Are we overiding the hard-coded list of experimens?
    mycfg = cfg.parse_config(path="config.yml")
      # Setup credentials for database
    exps = mycfg['impc_proc_codes']['impc_code_list']
    if len(exps) > 0:   # Else use the default list. See line 18 or thereabouts
        kompExperimentNames = exps.split(',')
        
    
    for expName in kompExperimentNames:
        taskInfoList={}
        numberOfKompRequest, valuelist = getExperimentData(expName)
        #print("Number of requests:" + str(numberOfKompRequest))
        my_logger.info("Number of requests for {0}:".format(expName) + str(numberOfKompRequest))
          
        taskInfoList["taskInfo"] = buildTaskInfoList(valuelist)     
        taskInfoListList.append(taskInfoList)

    with open("taskInfoLsLs.json","w") as outfile:
        outfile.write(json.dumps(taskInfoListList,indent=4))
        
    return taskInfoListList

def write_data_sent_experiments_to_csv():
        mycfg = cfg.parse_config(path="config.yml")
        baseURL = mycfg['corepfs_database']['baseURL']
        username = mycfg['corepfs_database']['username']
        password = mycfg['corepfs_database']['password']
        experimentOnlyEndpoint = mycfg['corepfs_database']['experimentOnlyEndpointTemplate']
        impc_all_codes = mycfg['impc_proc_codes']['impc_all_code_list']
        all_code_ls = impc_all_codes.split(',')

        my_auth = HTTPBasicAuth(username, password)
        
        with open('data_sent_to_dcc.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['EntityTypeName', 'Barcode'])
            
            for code in all_code_ls:
                endpoint = experimentOnlyEndpoint.format(code)  # e.g. KOMP_BODY_WEIGHT_EXPERIMENT
                query = baseURL + endpoint
                result = requests.get(query, auth=my_auth, headers={"Prefer": "odata.maxpagesize=5000"})
                wgJson = result.json()
                valueLs = wgJson.get('value')
                
                for val in valueLs:
                    writer.writerow([val['EntityTypeName'], val['Barcode']])



if __name__ == '__main__':
    
    # Gets the list of experiments that have been sent to the DCC
    #write_data_sent_experiments_to_csv()
    
    # A way to update the status of an experiment from the list generated by write_data_sent_experiments_to_csv()
    """
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR1','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR10','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR11','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR12','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR13','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR14','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR15','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR16','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR17','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR18','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR19','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR2','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR20','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR21','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR22','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR23','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR24','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR25','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR26','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR27','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR28','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR29','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR30','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR31','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR32','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR33','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR34','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR35','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR36','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR37','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR38','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR39','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR4','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR40','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR41','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR5','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR6','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR7','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR8','Review Completed')
    updateExperimentStatus('KOMP_AUDITORY_BRAINSTEM_RESPONSE_EXPERIMENT','KABR9','Review Completed')
    """
    
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE1','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE2','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE4','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE5','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE6','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE7','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE8','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE9','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE10','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE11','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE12','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE13','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE14','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE15','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE16','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE17','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE18','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE19','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE20','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE21','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE22','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE23','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE24','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE26','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE27','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE28','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE29','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE30','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE31','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE32','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE33','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE34','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE35','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE36','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE37','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE38','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE39','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE40','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE41','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE42','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE43','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE44','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE45','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE46','Review Completed')
    updateExperimentStatus('KOMP_SHIRPA_DYSMORPHOLOGY_EXPERIMENT','KSDE47','Review Completed')
    
    """
    # Get column headers for attribute names
    mycfg = cfg.parse_config(path="config.yml")
    baseURL = mycfg['corepfs_database']['baseURL']
    username = mycfg['corepfs_database']['username']
    password = mycfg['corepfs_database']['password']
    
    my_auth = HTTPBasicAuth(username, password)
    for impccode in impcCodeLookups.keys():
        query = baseURL + f"TYPE_ATTRIBUTE?$filter=AttributeName eq '{impccode}'&$select=ColumnHeader"
        #print(query)
        result = requests.get(query, auth=my_auth,headers = {"Prefer": "odata.maxpagesize=5000"})    
        wgJson = result.json()
        if len(wgJson['value']) == 0:
            print("No value for " + impccode)
            continue
        
        valueLs = wgJson.get('value')
        impcCodeLookups[impccode] = valueLs[0]['ColumnHeader']  
        #print(impccode + " " + impcCodeLookups[impccode])   
    
    #print(impcCodeLookups)  
        
    with open("column_hdrs.json","w") as outfile:
        outfile.write(json.dumps(impcCodeLookups,indent=4))
        
    """
    
    #Get all KOMP Mice
    """
    numberOfKompRequest, valuelist = getKompMice()
    animalInfo = getSampleList(valuelist)
    
    with open("samples.json","w") as outfile:
        outfile.write(json.dumps(animalInfo,indent=4))
    """
    """
    db.init()
    with open("taskInfoList.json","w") as outfile:
        outfile.write(json.dumps(getPfsTaskInfo(),indent=4))
    db.close()
    """
    print("SUCCESS")
