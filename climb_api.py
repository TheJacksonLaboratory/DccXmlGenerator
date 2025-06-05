#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import csv
import pandas as pd
import my_logger

import histo_output_template as hot # Output template for histopathology    

seriesParameter = [
{ "outputKey" :673, "impcCode" : "IMPC_VIA_037_001" } ,
{ "outputKey" :674, "impcCode" : "IMPC_VIA_038_001" } ,
{ "outputKey" :675, "impcCode" : "IMPC_VIA_039_001" } ,
{ "outputKey" :676, "impcCode" : "IMPC_VIA_040_001" } ,
{ "outputKey" :677, "impcCode" : "IMPC_VIA_041_001" } ,
{ "outputKey" :678, "impcCode" : "IMPC_VIA_042_001" } ,
{ "outputKey" :679, "impcCode" : "IMPC_VIA_043_001" } ,
{ "outputKey" :680, "impcCode" : "IMPC_VIA_044_001" } ,
{ "outputKey" :682, "impcCode" : "IMPC_VIA_045_001" } ,
{ "outputKey" :683, "impcCode" : "IMPC_VIA_046_001" } ,
{ "outputKey" :684, "impcCode" : "IMPC_VIA_047_001" } ,
{ "outputKey" :685, "impcCode" : "IMPC_VIA_048_001" }
]

seriesMediaParameter = [
{ "outputKey" :1150, "impcCode" : "IMPC_EMO_001_001" } ,
{ "outputKey" :977, "impcCode" : "IMPC_HIS_177_001" } ,
{ "outputKey" :978, "impcCode" : "IMPC_HIS_177_001" } ,
{ "outputKey" :1145, "impcCode" : "IMPC_HIS_177_001" } ,
{ "outputKey" :1146, "impcCode" : "IMPC_HIS_177_001" } ,
{ "outputKey" :65, "impcCode" : "IMPC_GEM_049_001" } ,
{ "outputKey" :23, "impcCode" : "IMPC_GEL_044_001" } ,
{ "outputKey" :155, "impcCode" : "IMPC_GEP_064_001" } ,
{ "outputKey" :112, "impcCode" : "IMPC_GEO_050_001" } ,
{ "outputKey" :658, "impcCode" : "IMPC_EMA_001_001" } ,
{ "outputKey" :46, "impcCode" : "IMPC_GPL_007_001" } ,
{ "outputKey" :195, "impcCode" : "IMPC_GPM_007_001" } ,
{ "outputKey" :193, "impcCode" : "IMPC_GPO_007_001" } ,
{ "outputKey" :192, "impcCode" : "IMPC_GPP_007_001" } ,
{ "outputKey" :653, "impcCode" : "IMPC_GEL_044_001" } ,
{ "outputKey" :654, "impcCode" : "IMPC_GPL_007_001" } ,
{ "outputKey" :647, "impcCode" : "IMPC_GEM_049_001" } ,
{ "outputKey" :648, "impcCode" : "IMPC_GPM_007_001" } ,
{ "outputKey" :649, "impcCode" : "IMPC_GEO_050_001" } ,
{ "outputKey" :650, "impcCode" : "IMPC_GPO_007_001" } ,
{ "outputKey" :651, "impcCode" : "IMPC_GEP_064_001" } ,
{ "outputKey" :652, "impcCode" : "IMPC_GPP_007_001" }
]

"""
This module provides the necessary fucntions to query and update genotypes in CLIMB.
For RESTful info see: https://api.climb.bio/docs/index.html
"""

g_WorkgroupName = 'KOMP-JAX Lab'
myToken = ''

def username():
    return 'mike'

def password():
    return '1banana1'

def isHistopathologyTask(outputls):
    if hot.find_dict_by_key_value("outputKey", outputls[0]["outputKey"]) != None:  # Check for series
        return True
    return False

def find_dict_index(list_of_dicts, key, value):
    for i, dict_item in enumerate(list_of_dicts):
        if key in dict_item and dict_item[key] == value:
            return i
    return -1  # Return -1
    
def prepareHistopathologyOutputValues(outputsOnly):
    # The template has all possible outputs fpr histopathology with defaulted values and status codes.
    # We need to match the outputKey and outputValue
    hist_templ_ls = hot.histo_items_ls
    for output in outputsOnly:
        idx = find_dict_index(hist_templ_ls, "outputKey", output["outputKey"])      
        if idx >= 0:
            if output["outputValue"] != None:
                hist_templ_ls[idx] = output # Replace the template with the actual output   
        else:
            print(f"Output key {output['outputKey']} and name {output['outputName']} not found in histopathology template")     
    
    # Now we add the series media if any
    mediaSeriesValue = hot.build_histo_image(outputsOnly) # This is a dictionary of images
    if len(mediaSeriesValue) > 0:
        hist_templ_ls[len(hist_templ_ls)-1]["outputValue"] = mediaSeriesValue
        hist_templ_ls[len(hist_templ_ls)-1]["parameterStatus"] = ''
    
    return hist_templ_ls

                    
#### CSV funcs #########################################
def createInputCsvFileHeader():
    header = ['TaskName', 'InputName', 'InputKey' ]
    f = open('inputs.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(header)
    return

def createInputCsv(taskName, inputDictLs):
    with open('inputs.csv', 'a', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        for x in inputDictLs:
            row = []
            row.append(taskName)
            row.append(x.get("name"))
            row.append(x.get("input_key"))
            #row.append(x.get("inputKey"))  Native version
            # write a row to the csv file
            writer.writerow(row)
    return

def createOutputCsvFileHeader():
    header = ['TaskName', 'OutputName', 'OutputKey' ]
    f = open('outputs.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(header)
    return
    
def createOutputCsv(taskName, inputDictLs):
    with open('outputs.csv', 'a', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        for x in inputDictLs:
            row = []
            row.append(taskName)
            row.append(x.get("name"))
            row.append(x.get("output_key"))
            # row.append(x.get("outputKey"))  Native version
            # write a row to the csv file
            writer.writerow(row)
    return

def createUserCsv(userDictLs):
    with open("C:\\TEMP\\users.csv", 'a', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        for x in userDictLs:
            row = []
            row.append(userDictLs)
            row.append(x.get("userFirstName"))
            row.append(x.get("userLastName"))
            writer.writerow(row)
    return
###############  END OF CSV funcs ########################################

# TOKEN TOKEN TOKEN 
def getToken(username, password):
    try:
        """ Given a username and password, return an access token good for an hour."""
        response = requests.get('http://climb-admin.azurewebsites.net/api/token',auth=(username,password), timeout=15)
        myContent = response.json()
        token = myContent['access_token']
        my_logger.info(token)
        return token
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise Exception(e)
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise ValueError(e)
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise ValueError(e)
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise SystemExit(e)
    
def getTokenEx():
    try:
        """ Given a username and password, return an access token good for an hour."""
        response = requests.get('http://bhlit01wd.jax.org:8000/api/Token/2346')
        token = response.json()
        return token
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise Exception(e)
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise ValueError(e)
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise ValueError(e)
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise SystemExit(e)


def setMyToken(token):
    global myToken
    myToken = token

def token():
    global myToken
    if myToken == '':
        myToken = getTokenEx()
    return myToken

def endpoint():
    return 'http://bhlit01wd.jax.org:8000/api'
    #return 'https://api.climb.bio/api'

def escapeHtmlCharacter(html):
    html = html.replace(" ","%20")
    html = html.replace("/","%2F")
    return html

def getTaskNames():
    return ['Histopathology','E12.5 Embryo Gross Morphology', 'E12.5 Placenta Morphology', 'E15.5 Embryo Gross Morphology', 'E15.5 Placenta Morphology', 'E18.5 Embryo Gross Morphology', 'E18.5 Placenta Morphology', 'E9.5 Embryo Gross Morphology', 'E9.5 Placenta Morphology', 'MicroCT 18.5', 'MicroCT 15.5']

    
 
# WORKGROUPS WORKGROUPS WORKGROUPS 

"""
Get the list of workgroups
Ex:
{'workgroupKey': 210, 'workgroupName': 'KOMP-JAX Lab Training', 'isCurrent': True}
{'workgroupKey': 266, 'workgroupName': 'Model-AD Testing', 'isCurrent': False}

"""
def getWorkgroups():
    try:
        call_header = {'Authorization' : 'Bearer ' + token()}
        wgResponse = requests.get(endpoint()+'/workgroups', headers=call_header, timeout=60)
        wgJson = wgResponse.json()
        # Check for number of items
        total_item_count = wgJson.get('totalItemCount')
        outer_dict = wgJson.get('data')
        dict_list = outer_dict.get('items')
        return dict_list
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise 
    
def setWorkgroup(workgroupName=None):
    if workgroupName == None or workgroupName == '':
        workgroupName=g_WorkgroupName
        
    dict_list = getWorkgroups()
    success = False

    for x in dict_list:
        if x['workgroupName'] == workgroupName:
            call_header = {'Authorization' : 'Bearer ' + token()}
            status_code = requests.put(endpoint() +'/workgroups/'+str(x['workgroupKey']), headers=call_header)
            success = True

    if success == False:
        print(f'"Could not change workgroup to {workgroupName}')
        raise SystemExit(f'"Could not change workgroup to {workgroupName}')

    # Remember to get a new access token!
    setMyToken(getTokenEx())

################################################################################
def getClimbUsers():
    climbUsers = []
    call_header = {'Authorization' : 'Bearer ' + token()}
    
    endpointUrl = 'https://api.climb.bio/api/workgroupusers?PageSize=200'
    response = requests.get(endpointUrl, headers=call_header, timeout=60)
    responseJson = response.json()
    outer_dict = responseJson.get('data')
    inner_dict = outer_dict.get("items")
    return inner_dict
####################################################

def getWorkflowTaskNameKey(taskName):
    # https://api.climb.bio/api/WorkflowTasks?TaskName=Eye%20Morphology
    try:
        call_header = {'Authorization' : 'Bearer ' + token()}
        endpointUrl = endpoint() +'/WorkflowTasks?TaskName=' + taskName
        response = requests.get(endpointUrl, headers=call_header, timeout=15)
        responseJson = response.json()
        
        # Check for number of items
        total_item_count = responseJson.get('totalItemCount')
        outer_dict = responseJson.get('data')
        inner_dict = outer_dict.get("items")
        # Native version -- wfKey = inner_dict[0].get("workflowTaskKey")
        wfKey = inner_dict[0].get("workflow_task_key")
        return wfKey

    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise 
    
    return 0

def getInputsFromTaskName(taskName):
    # Given a task name, get the input definitions
    key = getWorkflowTaskNameKey(taskName)
    
    if key == None:
        return []
    
    call_header = {'Authorization' : 'Bearer ' + token()}
    endpointUrl = endpoint() +'/WorkflowTasks/inputs?WorkflowTaskKey=' + str(key) + '&PageNumber=0&PageSize=100'
    
    response = requests.get(endpointUrl, headers=call_header, timeout=15)
    responseJson = response.json()
    # Check for number of items
    total_item_count = responseJson.get('totalItemCount')
    outer_dict = responseJson.get('data')
    dict_list = outer_dict.get('items')
    return dict_list

def getInputsFromTaskNames():
    # For each task get the inputs and write them to a CSV file
    createInputCsvFileHeader()
    taskNames = getTaskNames()
    for taskName in taskNames:
        inputDictLs = getInputsFromTaskName(escapeHtmlCharacter(taskName))
        createInputCsv(taskName,inputDictLs)
    return inputDictLs


def getOutputsFromTaskName(taskName):
    # Get the put defintions for the given task
    key = getWorkflowTaskNameKey(taskName)
    
    if key == None:
        return []
    
    call_header = {'Authorization' : 'Bearer ' + token()}
    endpointUrl = endpoint() +'/WorkflowTasks/outputs?WorkflowTaskKey=' + str(key) + '&PageNumber=0&PageSize=100'
    
    response = requests.get(endpointUrl, headers=call_header, timeout=15)
    responseJson = response.json()
    
    # Check for number of items
    total_item_count = responseJson.get('totalItemCount')
    outer_dict = responseJson.get('data')
    dict_list = outer_dict.get('items')
    return dict_list

def getOutputsFromTaskNames():
    # For each task get the outputs and write them to a CSV file
    createOutputCsvFileHeader()
    taskNames = getTaskNames()
    for taskName in taskNames:
        outputDictLs = getOutputsFromTaskName(escapeHtmlCharacter(taskName))
        createOutputCsv(taskName,outputDictLs)
    return outputDictLs

def getTaskInfoFromFilter(taskInfoFiler):
    # A main entry point to get procedure data from CLIMB
    taskInfoLs = {}
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        wgResponse = requests.post(endpoint()+'/taskAnimalInfo', data=json.dumps(taskInfoFiler), headers=call_header, timeout=60)
        taskInfoLs = wgResponse.json()
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  
    
    # Do any post-processing required for generating XML
    if taskInfoLs != None:
        for taskInfo in taskInfoLs["taskInfo"]:
            if "taskInstance" in taskInfo:
                if len(taskInfo["taskInstance"]):
                    if "outputs" in taskInfo["taskInstance"][0]:
                        post_process_outputs(taskInfo["taskInstance"][0]["outputs"]) # Check for existence of outputs
        
    return taskInfoLs


def getAnimalInfoFromFilter(whereClause):
    # A main entry point to get animal data from CLIMB
    my_logger.info("Animal info: " + whereClause)
    animalInfoLs = []
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        wgResponse = requests.get(endpoint()+'/animals' + whereClause + '&PageNumber=0&PageSize=2000', headers=call_header, timeout=300)
        
        if wgResponse.status_code == 500: # Server error
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 422:
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 200:
            response = wgResponse.json()
            animalInfoLs = response["data"]["items"]
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  
       
    return animalInfoLs


def getAnimalInfoFromFilterEx(whereClause):
    # A main entry point to get animal data from CLIMB
    my_logger.info("Animal info: " + whereClause)
    animalInfoLs = []
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        wgResponse = requests.get(endpoint()+'/animals' + whereClause + '&PageNumber=0&PageSize=2000', headers=call_header, timeout=300)
        
        if wgResponse.status_code == 500: # Server error
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 422:
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 200:
            response = wgResponse.json()
            animalInfoLs = response["data"]["items"]
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  
       
    return animalInfoLs


def getGenotypesGivenLineKey(lineKey):
    line_ls = []
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        wgResponse = requests.get(endpoint()+'/genotypes?LineKey=' + str(lineKey) , headers=call_header, timeout=300)
        
        if wgResponse.status_code == 500: # Server error
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 422:
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 200:
            response = wgResponse.json()
            line_ls = response["data"]["items"]
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  
       
    return line_ls

def getLineGivenLineName(lineName):
    line_ls = []
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        wgResponse = requests.get(endpoint()+'/lines?Name=' + lineName , headers=call_header, timeout=300)
        
        if wgResponse.status_code == 500: # Server error
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 422:
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 200:
            response = wgResponse.json()
            line_ls = response["data"]["items"]
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  
       
    return line_ls

def getLineGivenLineKey(lineKey):
    line_ls = []
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        wgResponse = requests.get(endpoint()+'/lines?LineKey=' + str(lineKey) , headers=call_header, timeout=300)
        
        if wgResponse.status_code == 500: # Server error
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 422:
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 200:
            response = wgResponse.json()
            line_ls = response["data"]["items"]
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  
       
    return line_ls

def getBirthGivenBirthId(birthId):
    litter_ls = []
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        wgResponse = requests.get(endpoint()+'/birth?BirthID=' + str(birthId) , headers=call_header, timeout=300)
        
        if wgResponse.status_code == 500: # Server error
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 422:
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 200:
            response = wgResponse.json()
            litter_ls = response["data"]["items"]
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  
       
    return litter_ls


def getGenotypesGivenMaterialKey(materialKey):
    # A main entry point to get genotype. Zero will return all genotypes!
    gt_ls = []
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        wgResponse = requests.get(endpoint()+'/genotypes?MaterialKey=' + str(materialKey) , headers=call_header, timeout=300)
        
        if wgResponse.status_code == 500: # Server error
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 422:
            my_logger.info(wgResponse.content)
        elif wgResponse.status_code == 200:
            response = wgResponse.json()
            gt_ls = response["data"]["items"]
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  
       
    return gt_ls

def getMinMaxFromOutput(key):  # TBD if needed
    min = None
    max = None
    return min, max

def intersection(lst1, lst2):
    lst3 = [set(lst1)+set(lst2)]
    return lst3

######## SOME USEFUL, SPECIAL CLIMB METHODS

""" Return a dictionary with a root of taskInfo

	"taskInfo": [
		{
			"animal": [
				{
					"animalId": 37072,
					"materialKey": 38604,
					"animalName": "A-3955",
					"sex": "Female",
					"generation": "E9.5",
					"status": "Alive",
					"line": "C57BL/6NJ-Fbrs<em1(IMPC)J>/Mmjax",
					"use": "Study Cohort",
					"stock": "036867",
					"dateBorn": "2022-09-09T04:00:00"
				}
			],
			"taskInstance": [
				{
					"taskInstanceKey": 8289,
					"workflowTaskName": "E9.5 Placenta Morphology",
					"taskAlias": "E9.5 Placenta Morphology",
					"taskStatus": "Complete",
					"assignedTo": "",
					"dateDue": "",
					"completedBy": "Kristy",
					"dateComplete": "2022-09-09",
					"reviewedBy": "Kristy",
					"dateReviewed": "2022-11-11",
					"modifiedBy": "kjp",
					"dateModified": "2022-11-11T14:39:11.263",
					"inputs": [
						{
							"taskInputKey": 4837,
							"inputKey": 336,
							"inputName": "Date equipment last calibrated",
							"inputValue": "",
							"modifiedBy": "KJP",
							"dateModified": "2022-09-09T17:57:53.303"
						},
      ...
					],
					"outputs": [
						{
							"taskOutputKey": 103669,
							"outputKey": 41,
							"outputName": "Placenta size",
							"outputValue": "unobservable",
							"collectedBy": "Kristy",
							"collectedDate": "2022-09-09",
							"taskAlias": "E9.5 Placenta Morphology",
							"workflowTaskName": "E9.5 Placenta Morphology",
							"modifiedBy": "kjp",
							"dateModified": "2022-11-11T14:39:06.68"
						},
      ...
					]
				}
			]
		}
	]
}

Filter at server:
http://bhlit01wp.jax.org:8000/api/taskinstances?WorkflowTaskName=E18.5%20MicroCT&CompletedStartDate=2024-05-01&CompletedEndDate=2024-08-01&PageNumber=1&PageSize=50
"""
def getProceduresGivenFilter(taskNameFilter,page=1,pageSize=500):
    
    # Return a list of dictionaries where each dictionary is a procedure
    # This will also work when there are no animals associated with the task.
    if taskNameFilter is None or taskNameFilter["taskInstance"] is None:
        return []
    
    workFlowTaskName =  taskNameFilter["taskInstance"]["workflowTaskName"]
    if workFlowTaskName is None:
        return []
    
    whereClause = workFlowTaskName
    
    # OK. Let's extract the filters
    if 'completedStartDate' in  taskNameFilter["taskInstance"].keys():
        whereClause = whereClause + '&CompletedStartDate=' +  taskNameFilter["taskInstance"]["completedStartDate"]
        
    if 'completedEndDate' in  taskNameFilter["taskInstance"].keys():
        whereClause = whereClause + '&CompletedEndDate=' +  taskNameFilter["taskInstance"]["completedEndDate"]
    
    workFlowTaskStatusFilter = ""
    if 'workflowTaskStatus' in  taskNameFilter["taskInstance"].keys():
        workFlowTaskStatusFilter = taskNameFilter["taskInstance"]["workflowTaskStatus"]
    
    reviewedOnlyFilter = taskNameFilter["taskInstance"]["isReviewed"] == True
    
    # end of filters (we can expand as needed)
    
    taskInfoLs = [] # Response from CLIMB
    taskInfoDictLs = { "taskInfo":[] } # What we return - a list of dictionaries
    
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        # Start calls to CLIMB -- first are tasks
        endpointUrl = endpoint() +'/taskinstances?WorkflowTaskName=' + escapeHtmlCharacter(whereClause) + f'&PageNumber={page}&PageSize={pageSize}'
        wgResponse = requests.get(endpointUrl, headers=call_header, timeout=60)
        taskInfoLs = wgResponse.json()
        taskInfoLs = taskInfoLs["data"]["items"]
        
        totalItemCount = wgResponse.json()["data"]["totalItemCount"]
        pageNumber = wgResponse.json()["data"]["pageNumber"]
        pageCount = wgResponse.json()["data"]["pageCount"]   # Total pages
        pageSize = wgResponse.json()["data"]["pageSize"]   
        if totalItemCount - (pageSize * pageNumber) > 0:
            page = pageNumber + 1
        else:
            page = 0  # We're done
        
        
        # Big loop: Remove tasks that fail the filter
        for taskinstance in reversed(taskInfoLs):
            # Are we filtering by status?
            if len(workFlowTaskStatusFilter) > 0 and taskinstance["taskStatus"] != workFlowTaskStatusFilter:
                taskInfoLs.remove(taskinstance)
                continue
            
            # Are we filtering by reviewed only?
            isReviewed = (taskinstance["reviewedBy"] != None) and (taskinstance["reviewedBy"] != '') # some value for reviewedBy
            if isReviewed == False and reviewedOnlyFilter == True:
                    taskInfoLs.remove(taskinstance)
                    continue
            else:   
                taskInfoDictLs["taskInfo"].append(taskinstance) 
        
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        return taskInfoDictLs 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        return taskInfoDictLs 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        return taskInfoDictLs 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e)) 
        return taskInfoDictLs  
    
    if page > 0:
        d = getProceduresGivenFilter(taskNameFilter,page,pageSize)  
        if d != None and "taskInfo" in d.keys():
            taskInfoDictLs["taskInfo"] = taskInfoDictLs["taskInfo"] + d["taskInfo"]
            
    return taskInfoDictLs



def getProceduresGivenFilterWithIO(taskNameFilter,page=1,pageSize=500):
    
    # Return a list of dictionaries where each dictionary is a procedure
    # This will also work when there are no animals associated with the task.
    if taskNameFilter is None or taskNameFilter["taskInstance"] is None:
        return []
    
    workFlowTaskName =  taskNameFilter["taskInstance"]["workflowTaskName"]
    if workFlowTaskName is None:
        return []
    
    whereClause = workFlowTaskName
    
    # OK. Let's extract the filters
    if 'completedStartDate' in  taskNameFilter["taskInstance"].keys():
        whereClause = whereClause + '&CompletedStartDate=' +  taskNameFilter["taskInstance"]["completedStartDate"]
        
    if 'completedEndDate' in  taskNameFilter["taskInstance"].keys():
        whereClause = whereClause + '&CompletedEndDate=' +  taskNameFilter["taskInstance"]["completedEndDate"]
    
    workFlowTaskStatusFilter = ""
    if 'workflowTaskStatus' in  taskNameFilter["taskInstance"].keys():
        workFlowTaskStatusFilter = taskNameFilter["taskInstance"]["workflowTaskStatus"]
    
    reviewedOnlyFilter = taskNameFilter["taskInstance"]["isReviewed"] == True
    
    # end of filters (we can expand as needed)
    
    taskInfoLs = [] # Response from CLIMB
    #taskInfoDictLs = { "taskInfo":[] }  # A list of one
    
    taskInfoDictLs = []  # A list of one
    
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        # Start calls to CLIMB -- first are tasks
        endpointUrl = endpoint() +'/taskinstances?WorkflowTaskName=' + escapeHtmlCharacter(whereClause) + f'&PageNumber={page}&PageSize={pageSize}'
        wgResponse = requests.get(endpointUrl, headers=call_header, timeout=60)
        taskInfoLs = wgResponse.json()
        taskInfoLs = taskInfoLs["data"]["items"]
        
        totalItemCount = wgResponse.json()["data"]["totalItemCount"]
        pageNumber = wgResponse.json()["data"]["pageNumber"]
        pageCount = wgResponse.json()["data"]["pageCount"]   # Total pages
        pageSize = wgResponse.json()["data"]["pageSize"]   
        if totalItemCount - (pageSize * pageNumber) > 0:
            page = pageNumber + 1
        else:
            page = 0  # We're done
        
        
        # Big loop: Remove tasks that fail the filter
        for taskinstance in reversed(taskInfoLs):
            # Are we filtering by status?
            if len(workFlowTaskStatusFilter) > 0 and taskinstance["taskStatus"] != workFlowTaskStatusFilter:
                taskInfoLs.remove(taskinstance)
                continue
            
            # Are we filtering by reviewed only?
            isReviewed = (taskinstance["reviewedBy"] != None) and (taskinstance["reviewedBy"] != '') # some value for reviewedBy
            if isReviewed == False and reviewedOnlyFilter == True:
                    taskInfoLs.remove(taskinstance)
                    continue
            
        # End of loop
        
        for taskinstance in taskInfoLs:
            # TBD - Make more meaningful?
            taskinstance["barcode"] = "TBD"
            # Get the inputs
            endpointUrl = endpoint() +'/taskinstances/taskInputs?TaskInstanceKey=' + str(taskinstance["taskInstanceKey"]) + '&PageNumber=0&PageSize=200'
            wgResponse = requests.get(endpointUrl, headers=call_header, timeout=60)
            inputLs = wgResponse.json()
            inputsOnly = inputLs["data"]["items"]
            # clean up unwanted input objects
            inputsOnly = cleanupInputs(inputsOnly) # Remove unwanted key+value pairs
            taskinstance["inputs"] = inputsOnly
            
        # Get the outputs
            endpointUrl = endpoint() +'/taskinstances/taskOutputs?TaskInstanceKey=' + str(taskinstance["taskInstanceKey"]) + '&PageNumber=0&PageSize=200'
            wgResponse = requests.get(endpointUrl, headers=call_header, timeout=60)
            outputLs = wgResponse.json()
            outputsOnly = outputLs["data"]["items"]
            # clean up unwanted output objects
            outputsOnly = cleanupOutputs(outputsOnly) # Remove unwanted key+value pairs
            outputsOnly = prepareSeriesAndSeriesMediaOutputValues(outputsOnly)
            taskinstance["outputs"] = outputsOnly
            
            # List inside a dict inside a list
            outer_dict = {}
            outer_dict["taskInstance"] = []
            outer_dict["taskInstance"].append(taskinstance)  
            taskInfoDictLs.append(outer_dict)
        
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  
    
    if page > 0:
        d = getProceduresGivenFilterWithIO(taskNameFilter,page,pageSize)  
        if d != None and "taskInfo" in d.keys():
            taskInfoDictLs = taskInfoDictLs + d   # UNTESTED           
    
    return taskInfoDictLs


def getInputs(taskInstanceKey):
    # Get the inputs
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        endpointUrl = endpoint() +'/taskinstances/taskInputs?TaskInstanceKey=' + str(taskInstanceKey) + '&PageNumber=0&PageSize=200'
        wgResponse = requests.get(endpointUrl, headers=call_header, timeout=60)
        inputLs = wgResponse.json()
        inputsOnly = inputLs["data"]["items"]
        # clean up unwanted input objects
        inputsOnly = cleanupInputs(inputsOnly) # Remove unwanted key+value pairs
        return inputsOnly
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  
                
def getOutputs(taskInstanceKey):
            
    # Get the outputs
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        endpointUrl = endpoint() +'/taskinstances/taskOutputs?TaskInstanceKey=' + str(taskInstanceKey) + '&PageNumber=0&PageSize=200'
        wgResponse = requests.get(endpointUrl, headers=call_header, timeout=60)
        outputLs = wgResponse.json()
        outputsOnly = outputLs["data"]["items"]
        # clean up unwanted output objects
        outputsOnly = cleanupOutputs(outputsOnly) # Remove unwanted key+value pairs
        outputsOnly = prepareSeriesAndSeriesMediaOutputValues(outputsOnly)
        if isHistopathologyTask(outputsOnly):
            outputsOnly = prepareHistopathologyOutputValues(outputsOnly)
        return outputsOnly
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  
        
"""
{
        "taskInputKey": 3497,
        "inputKey": 326,
        "taskInstanceKey": 8132,
        "inputValue": null,
        "inputName": "Date equipment last calibrated",
        "materialKeys": [],
        "workflowTaskKey": 17,
        "workflowTaskName": "E9.5 Embryo Gross Morphology",
        "createdBy": "ccm",
        "dateCreated": "2022-09-01T17:30:13.21",
        "modifiedBy": "ccm",
        "dateModified": "2022-09-01T17:30:13.21"
      },
"""
def cleanupInputs(inputsLs):
    for inputObj in inputsLs:
        del inputObj["taskInstanceKey"]
        del inputObj["materialKeys"]
        del inputObj["createdBy"]
        del inputObj["dateCreated"]
        #del inputObj["workGroupKey"]
        #del inputObj["validatedInputValue"]
    return inputsLs


"""
     {
        "taskOutputKey": 9358,
        "taskOutputSetKey": 425,
        "taskInstanceKey": 993,
        "outputKey": 8,
        "outputName": "Allantois morphology",
        "outputValue": "Normal",
        "collectedDate": "",
        "collectedBy": null,
        "taskAlias": "E9.5 Embryo Gross Morphology",
        "workflowTaskKey": 17,
        "workflowTaskName": "E9.5 Embryo Gross Morphology",
        "materialKeys": [
          437
        ],
        "createdBy": "cynthiac",
        "dateCreated": "2021-04-08T17:45:00.447",
        "modifiedBy": "system",
        "dateModified": "2023-06-16T00:17:02.89"
      }
"""
def cleanupOutputs(outputLs):
    for outputObj in outputLs:
        del outputObj["taskOutputSetKey"]
        del outputObj["taskInstanceKey"]
        del outputObj["taskAlias"]
        del outputObj["workflowTaskKey"]
        del outputObj["workflowTaskName"]
        del outputObj["materialKeys"]
        del outputObj["createdBy"]
        del outputObj["dateCreated"]
    return outputLs

def post_process_outputs(outputLs):
    # Do what needs to be done to prepare the outputs for the XML generator
    return prepareSeriesAndSeriesMediaOutputValues(outputLs)

def prepareSeriesAndSeriesMediaOutputValues(outputLs):
    # Sereies types and seriesMedia types must be in the format of a JSON object dictionay.
    incrVal = "noLitter"
    for outputObj in outputLs:
        # if the output key in in either of the lists of series parameters, munge it to a dict
        tmp = next((item for item in seriesParameter if item["outputKey"] == int(outputObj["outputKey"])), None)
        if tmp == None:
            tmp = next((item for item in seriesMediaParameter if item["outputKey"] == int(outputObj["outputKey"])), None)
            if tmp !=None:
                incrVal = "1" # TODO - Increment if multiple images for one embryo
        
        # Increment value should be incrementable except if Viability, then it must be noLitter
        if tmp != None and outputObj["outputValue"] != None:
           dictVal = {}
           dictVal[incrVal] = outputObj["outputValue"]  # Must be noLitter for VIA. 
           outputObj["outputValue"] = str(dictVal)
    
    return outputLs


"""
Construct a list of these. The list is in a dict and its key is "animalInfo"
The larger structure is used for speciemns. The "animal" dict is used for tasks
animalInfo": [
    {
      "animal": {
        "animalId": 32759,
        "materialKey": 33464,
        "animalName": "A-1030",
        "exitReason": null,
        "physicalMarker": null,
        "dateBorn": "2022-04-18T04:00:00",
        "dateExit": null,
        "externalIdentifier": null,
        "comments": null,
        "species": "Mouse",
        "sex": "Male",
        "generation": "E18.5",
        "markerType": "Ear Notch",
        "arrivalDate": "2022-04-18T04:00:00",
        "clinicalObservationsCount": 0,
        "status": "Alive",
        "taskInstanceCount": 3,
        "modifiedBy": "kjp",
        "dateModified": "2022-05-26T17:48:39.92"
        "stock": "036867",  <<--
        "line": "C57BL/6NJ-Fbrs<em1(IMPC)J>/Mmjax" << --
      },
      "line": {
        "lineKey": 148,
        "active": true,
        "name": "C57BL/6NJ-Bicra<em1(IMPC)J>/Mmjax",
        "shortName": "Bicra",
        "stock": "035759",
        "lineType": "Endonuclease mediated mutation (em)",
        "lineStatus": "Embryo Lethal Complete",
        "species": "Mouse",
        "construct": null,
        "genotypeAssaysCount": 2,
        "technician": "ccm",
        "parentLine": null,
        "backgroundLine": "C57BL6/NJ",
        "breedingStrategy": "Het X WT",
        "development": null,
        "externalLink": null,
        "references": "MGI:2154263",
        "comment": null,
        "defaultLocation": "All GRS Locations",
        "createdBy": "ccm",
        "dateCreated": "2021-09-24T16:27:53.767",
        "modifiedBy": "mike",
        "dateModified": "2022-10-26T15:59:06.517"
      },
      "litter": {
        "birthID": null,
        "matingID": null,
        "housingID": null,
        "weanDate": null
      },
      "genotypes": [
        {
          "genotypeKey": 102109,
          "date": "Feb 24 2023  5:00AM",
          "assay": "Bicra<em1(IMPC)J>",
          "genotype": "-/-",
          "modifiedBy": "kjp",
          "dateModified": "2023-02-24T15:29:08.903"
        }
      ]
    }
"""

# Given a material key return an animalInfo list
# We want to return a dict that has four elements.
# The keys are "animal", "line", "litter", and genotypes.
# See comment around line 684 for an example.
def getAnimalGivenMaterialKey(materialKey,animaFilter):
    mouseDict = { "animal": None, "line": None, "litter": None, "genotypes": None }
    # Filters?
    dictLs = getAnimalInfoFromFilter(f'?MaterialKey={materialKey}') # Zero or one
    if len(dictLs) > 0:
        mouseDict = dictLs[0]
        if "generation" in animaFilter.keys():
            if mouseDict["generation"] != animaFilter["generation"]:
                return None # No match
            
        if "animalName" in animaFilter.keys(): # If there is an animal name filter check it
            if not animaFilter["animalName"] in  mouseDict["generation"]:
                return None  # Not there
            
        # TODO likeKeys = getLineKeys(animaFilter)
        # Get the genotype
        if mouseDict["genotypesCount"] > 0:
            # Get genotypes
            gt_ls = getGenotypesGivenMaterialKey(materialKey)
        # OK. We have a mouse
    
    return mouseDict


######## END OF USEFUL, SPECIAL CLIMB METHODS

def getMiceAndProcedures(filterDict:dict) -> tuple[list, list]:
    
    # Get all the procedures
    taskInfoReturn_Ls_Dict = getProceduresGivenFilter(filterDict)
        
    # Get the taskInfo list
    taskInfo_ls = taskInfoReturn_Ls_Dict["taskInfo"]  # taskInfo_ls is list that has a list of "taskInstance" that is also a list
   
    # Get all the mice and put them in a dataframe for filtering
    df = animalsToDataframe(filterDict)
    # test for empty dataframe
    if df.empty:
        return [], []   # BAIL
    
    
    
    # There returned lists: one for mice and one for mice/task combos
    final_mouse_info_ls = []
    final_task_info_ls = []
 
    # Now cycle through the filtered tasks and find the filtered mouse in the dataframe
    for taskInfo in taskInfo_ls:
        # Dict nodes for lists
        taskMouseInfo = {"animal":[], "taskInstance" : []}
        mouseInfo = { "animal": {} , "line": {} , "litter": {} , "genotypes": [] }
        
        materialKey = taskInfo["materialKeys"][0]  # Check for empty list. In KOMP it should be exactly one.
        specific_data = df.loc[df['materialKey'] == materialKey]  
        
        if specific_data.empty:
            continue
        
        # Got a mouse. Is it a keeper? 
        #print(specific_data.to_dict(orient="index"))    
        dict_from_mouse_df = specific_data.to_dict(orient="index") # Exactly one element 
        mouse = next(iter(dict_from_mouse_df.values())) # The value of the dict is the dict we are looking for 
        
        # Test generation if present
        animalFilter = filterDict["animal"]
        if "generation" in animalFilter.keys():
            if animalFilter["generation"] != mouse["generation"]:
                continue # Bail
            
        # Test for a line filter
        line_ls = getLineGivenLineKey(int(mouse['lineKey'])) # One element
        line_filter_ls = filterDict["lines"]
        if len(line_filter_ls) > 0:  # Also zero or one in filter
            line = { "line": None, "stock": None, "name": None}
            if "stock" in line_filter_ls[0].keys():
                if line_filter_ls[0]["stock"] != line_ls[0]['stock']:
                    continue  # Bail
                
                # Copy the stock number info up to the mouse for conveniece later
                mouse["stock"] = line_ls[0]['stock']
                line["stock"] = line_ls[0]['stock']
            
            if "name" in line_filter_ls[0].keys():
                if line_filter_ls[0]["name"] != line_ls[0]['shortName']:
                    continue  # Bail
            
                line["name"] = line_ls[0]['shortName']
                # Copy the stock number info up to the mouse for conveniece later
                mouse["line"] = line_ls[0]['name']
            
        # Any other filters ? No? OK
        # Look like we have a winner. Add Genotypes and litter
        gt_line = getGenotypesGivenMaterialKey(int(mouse['materialKey']))
        birth_ls = getBirthGivenBirthId(mouse['birthId'])
        
        # Mouse info node for final_mouse_info_ls
        mouseInfo["animal"] = mouse
        mouseInfo["line"] = line_ls[0]
        if len(birth_ls) > 0:
            mouseInfo["litter"] = birth_ls[0]
        else:
            mouseInfo["litter"] = None
            
        mouseInfo["genotypes"] = gt_line
        
        # Add to returned mouse list
        final_mouse_info_ls.append(mouseInfo)  # Done with mouse
        
        taskMouseInfo["animal"] = [ mouse ]
        taskMouseInfo["taskInstance"] = [ taskInfo ]
        # Let's grab those inputs and outputs
        taskMouseInfo["taskInstance"][0]["outputs"] = getOutputs(taskInfo["taskInstanceKey"]) 
        taskMouseInfo["taskInstance"][0]["inputs"] = getInputs(taskInfo["taskInstanceKey"])
        taskMouseInfo["taskInstance"][0]["barcode"] = "TBD"  #TBD    
        
        final_task_info_ls.append(taskMouseInfo)
        
    return  final_mouse_info_ls, final_task_info_ls

def animalsToDataframe(filter:dict, page:int=1, pageSize:int=2000) -> pd.DataFrame:
    
    # Filter the mice, and stick them in a dataframe
    animalFilter = filter["animal"] 
    animalInfoLs = []
    animalName = None
    if "animalName" in animalFilter.keys():
        animalName = animalFilter["animalName"]
    else:
        return pd.DataFrame()  # Empty dataframe
    
    whereClause = f'?AnimalName={animalName}&AnimalNameSearchOptions=StartsWith'
    
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        wgResponse = requests.get(endpoint()+'/animals' + whereClause + f'&PageNumber={page}&PageSize={pageSize}', headers=call_header, timeout=300)
        
        if wgResponse.status_code == 500: # Server error
            my_logger.info(wgResponse.content)
            return pd.DataFrame()  # Empty dataframe
        elif wgResponse.status_code == 422:
            my_logger.info(wgResponse.content)
            return pd.DataFrame()  # Empty dataframe
        elif wgResponse.status_code == 200:
            response = wgResponse.json()
            
            animalInfoLs = response["data"]["items"]
            totalItemCount = response["data"]["totalItemCount"]
            pageNumber = response["data"]["pageNumber"]
            pageCount = response["data"]["pageCount"]   # Total pages
            pageSize = response["data"]["pageSize"]   
            
    except requests.exceptions.Timeout as e: 
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidHeader as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.InvalidURL as e:  
        my_logger.info(repr(e))
        raise 
    except requests.exceptions.RequestException as e:  # All others
        my_logger.info(repr(e))
        raise  

    df = pd.DataFrame(animalInfoLs) 
    if totalItemCount - (pageSize * pageNumber) > 0:
        page = pageNumber + 1
        df = pd.concat([df,animalsToDataframe(filter, page, pageSize)])
    
    return df


if __name__ == '__main__':
    setWorkgroup('KOMP-JAX Lab')
    setMyToken(getTokenEx())
    
    #filterDict = { "taskInstance": { "workflowTaskName": "E18.5 MicroCT", "completedStartDate": "2024-07-01", "completedEndDate": "2024-07-01", "isReviewed": True}, "animal": { "animalName":"A-3976", "generation":"E18.5"}, "lines": [] }
    filterDict = { "taskInstance": { "workflowTaskName": "Histopathology", "isReviewed": True}, "animal": { "animalName":"A-3"}, "lines": [] }
    
    mice_ls, task_ls = getMiceAndProcedures(filterDict)
    
    jsonDictLs = json.dumps(task_ls , indent=4)
    with open("climb-api-results.json","w") as f:
        json.dump(task_ls,f,indent=4)
    
    jsonDictLs = json.dumps(mice_ls , indent=4)
    with open("mouseResults.json","w") as f:
        json.dump(mice_ls,f,indent=4)
        
    print("SUCCESS")
    
    