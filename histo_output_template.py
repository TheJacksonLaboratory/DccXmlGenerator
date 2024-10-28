"""
    The list fo all suported Histopathology parameters supported by us. 
    
    I used the query 
    SELECT "{'outputKey' : ",_ClimbType_key, ", 'outputName' :'", ImpcCode, "', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'}," FROM komp.dccparameterdetails where _ClimbType_key > 0 AND ImpcCode LIKE '%_HIS_%' AND _DccType_key <> 7; -- AND ImpcCode IN (

     
    For those that we report on we will replace the None value with the actual value.   
"""


import mysql.connector

histo_items_ls = None

"""
[
{'outputKey' : 825, 'outputName' :'IMPC_HIS_117_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 824, 'outputName' :'IMPC_HIS_139_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 1053, 'outputName' :'IMPC_HIS_140_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 829, 'outputName' :'IMPC_HIS_142_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 826, 'outputName' :'IMPC_HIS_143_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 830, 'outputName' :'IMPC_HIS_144_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 832, 'outputName' :'IMPC_HIS_145_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 1061, 'outputName' :'IMPC_HIS_146_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 833, 'outputName' :'IMPC_HIS_147_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 837, 'outputName' :'IMPC_HIS_148_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 834, 'outputName' :'IMPC_HIS_149_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 838, 'outputName' :'IMPC_HIS_150_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 840, 'outputName' :'IMPC_HIS_163_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 1069, 'outputName' :'IMPC_HIS_164_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 841, 'outputName' :'IMPC_HIS_165_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 845, 'outputName' :'IMPC_HIS_166_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 842, 'outputName' :'IMPC_HIS_167_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 846, 'outputName' :'IMPC_HIS_168_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 848, 'outputName' :'IMPC_HIS_169_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 1105, 'outputName' :'IMPC_HIS_170_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 849, 'outputName' :'IMPC_HIS_171_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 853, 'outputName' :'IMPC_HIS_172_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 850, 'outputName' :'IMPC_HIS_173_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 965, 'outputName' :'IMPC_HIS_174_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 1117, 'outputName' :'IMPC_HIS_177_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 831, 'outputName' :'IMPC_HIS_202_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 839, 'outputName' :'IMPC_HIS_203_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 847, 'outputName' :'IMPC_HIS_206_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 855, 'outputName' :'IMPC_HIS_207_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 835, 'outputName' :'IMPC_HIS_356_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 827, 'outputName' :'IMPC_HIS_391_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12000, 'outputName' :'IMPC_HIS_003_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12001, 'outputName' :'IMPC_HIS_009_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12002, 'outputName' :'IMPC_HIS_015_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12003, 'outputName' :'IMPC_HIS_021_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12004, 'outputName' :'IMPC_HIS_027_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12005, 'outputName' :'IMPC_HIS_033_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12006, 'outputName' :'IMPC_HIS_039_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12007, 'outputName' :'IMPC_HIS_045_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12008, 'outputName' :'IMPC_HIS_051_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12009, 'outputName' :'IMPC_HIS_057_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12010, 'outputName' :'IMPC_HIS_063_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12011, 'outputName' :'IMPC_HIS_069_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12012, 'outputName' :'IMPC_HIS_075_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12013, 'outputName' :'IMPC_HIS_081_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12014, 'outputName' :'IMPC_HIS_087_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12015, 'outputName' :'IMPC_HIS_093_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12016, 'outputName' :'IMPC_HIS_099_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12017, 'outputName' :'IMPC_HIS_105_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12018, 'outputName' :'IMPC_HIS_123_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12019, 'outputName' :'IMPC_HIS_129_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12020, 'outputName' :'IMPC_HIS_135_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12021, 'outputName' :'IMPC_HIS_179_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12022, 'outputName' :'IMPC_HIS_180_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12023, 'outputName' :'IMPC_HIS_181_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12024, 'outputName' :'IMPC_HIS_182_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12025, 'outputName' :'IMPC_HIS_183_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12026, 'outputName' :'IMPC_HIS_184_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12027, 'outputName' :'IMPC_HIS_185_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12028, 'outputName' :'IMPC_HIS_186_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12029, 'outputName' :'IMPC_HIS_187_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12030, 'outputName' :'IMPC_HIS_188_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12031, 'outputName' :'IMPC_HIS_189_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12032, 'outputName' :'IMPC_HIS_190_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12033, 'outputName' :'IMPC_HIS_191_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12034, 'outputName' :'IMPC_HIS_192_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12035, 'outputName' :'IMPC_HIS_193_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12036, 'outputName' :'IMPC_HIS_194_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12037, 'outputName' :'IMPC_HIS_195_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12038, 'outputName' :'IMPC_HIS_196_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12039, 'outputName' :'IMPC_HIS_197_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12040, 'outputName' :'IMPC_HIS_198_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12041, 'outputName' :'IMPC_HIS_199_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12042, 'outputName' :'IMPC_HIS_200_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12043, 'outputName' :'IMPC_HIS_201_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12044, 'outputName' :'IMPC_HIS_204_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12045, 'outputName' :'IMPC_HIS_205_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12046, 'outputName' :'IMPC_HIS_206_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12047, 'outputName' :'IMPC_HIS_207_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12051, 'outputName' :'IMPC_HIS_350_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12052, 'outputName' :'IMPC_HIS_353_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12053, 'outputName' :'IMPC_HIS_357_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12054, 'outputName' :'IMPC_HIS_358_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12055, 'outputName' :'IMPC_HIS_360_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12056, 'outputName' :'IMPC_HIS_361_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12057, 'outputName' :'IMPC_HIS_362_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12058, 'outputName' :'IMPC_HIS_364_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12059, 'outputName' :'IMPC_HIS_365_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12060, 'outputName' :'IMPC_HIS_366_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12061, 'outputName' :'IMPC_HIS_367_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12062, 'outputName' :'IMPC_HIS_371_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12063, 'outputName' :'IMPC_HIS_384_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12064, 'outputName' :'IMPC_HIS_385_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12065, 'outputName' :'IMPC_HIS_386_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12066, 'outputName' :'IMPC_HIS_387_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12067, 'outputName' :'IMPC_HIS_388_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12068, 'outputName' :'IMPC_HIS_390_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12069, 'outputName' :'IMPC_HIS_392_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12070, 'outputName' :'IMPC_HIS_393_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12071, 'outputName' :'IMPC_HIS_397_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12072, 'outputName' :'IMPC_HIS_399_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12073, 'outputName' :'IMPC_HIS_420_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12048, 'outputName' :'IMPC_HIS_422_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12049, 'outputName' :'IMPC_HIS_423_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 12050, 'outputName' :'IMPC_HIS_424_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'}
]"""


def generate_histo_template():
  
  selectStmt = "SELECT _ClimbType_key, ImpcCode FROM KOMP.dccparameterdetails WHERE _ClimbType_key > 0 AND ImpcCode LIKE '%_HIS_%' AND _DccType_key <> 7 ORDER BY _DccType_key"

  histo_template = []
  histo_dict = {'outputKey' : 12050, 'outputName' :'IMPC_HIS_424_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'}

  try:    
    mysqldb = mysql.connector.connect(host="rslims", user="dba", password="rsdba", database="komp")
        
    mysqlCursor = mysqldb.cursor()
    mysqlCursor.execute(selectStmt)
        
    for (_ClimbType_key, ImpcCode) in mysqlCursor:
      histo_dict['outputKey'] = _ClimbType_key
      histo_dict['outputName'] = ImpcCode
      histo_template.append(histo_dict)       
      histo_dict = {'outputKey' : 12050, 'outputName' :'IMPC_HIS_424_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'}
  except Exception as e:
        print('SELECT FAILED FOR: ' + selectStmt)
        print(e)  
  finally:
        if mysqldb.is_connected():
            mysqlCursor.close()
            mysqldb.close()
        
  return histo_template   


def find_dict_by_key_value(key, value):
  global histo_items_ls
  if histo_items_ls is None:
    histo_items_ls = generate_histo_template()
  return next((d for d in histo_items_ls if d.get(key) == value), None)


if __name__ == "__main__":
  d = find_dict_by_key_value('outputKey', 12050)  
  d = find_dict_by_key_value('outputKey', 12051)  
  d = find_dict_by_key_value('outputKey', 12052)  
  d = find_dict_by_key_value('outputKey', 12053)  
  print(d)