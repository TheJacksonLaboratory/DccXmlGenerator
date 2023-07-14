#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import NullHandler
import requests
import sys
import json
from datetime import datetime
import logging
import csv


"""
This module provides the necessary fucntions to query and update genotypes in CLIMB.
For RESTful info see: https://api.climb.bio/docs/index.html
"""

myToken = ''

def username():
    return 'mike'

def password():
    return '1banana1'

# TOKEN TOKEN TOKEN 
def getToken(username, password):
    try:
        """ Given a username and password, return an access token good for an hour."""
        response = requests.get('http://climb-admin.azurewebsites.net/api/token',auth=(username,password), timeout=15)
        myContent = response.json()
        token = myContent['access_token']
        #print(token)
        return token
    except requests.exceptions.Timeout as e: 
        #print(e.message())
        raise Exception(e)
    except requests.exceptions.InvalidHeader as e:  
        #print(e.message())
        raise ValueError(e)
    except requests.exceptions.InvalidURL as e:  
        #print(e.message())
        raise ValueError(e)
    except requests.exceptions.RequestException as e:  # All others
        #print(e.message())
        raise SystemExit(e)
    
def getTokenEx(username, password):
    try:
        """ Given a username and password, return an access token good for an hour."""
        response = requests.get('http://bhclimb01wd.jax.org:8000/api/Token/2346')
        token = response.json()
        return token
    except requests.exceptions.Timeout as e: 
        #print(e.message())
        raise Exception(e)
    except requests.exceptions.InvalidHeader as e:  
        #print(e.message())
        raise ValueError(e)
    except requests.exceptions.InvalidURL as e:  
        #print(e.message())
        raise ValueError(e)
    except requests.exceptions.RequestException as e:  # All others
        #print(e.message())
        raise SystemExit(e)


def setMyToken(token):
    global myToken
    myToken = token

def token():
    global myToken
    if myToken == '':
        myToken = getTokenEx(username(), password())
    return myToken

def endpoint():
    return 'http://bhclimb01wd.jax.org:8000/api'
    #return 'https://api.climb.bio/api'

def escapeHtmlCharacter(html):
    html = html.replace(" ","%20")
    html = html.replace("/","%2F")
    return html

def getTaskNames():
    #taskNames = ['Eye Morphology', 'Body Weight', 'First Body Weight', 'Open Field', 'Grip Strength', 'Light/Dark', 'Holeboard', 'EKGv3', 'GTT', 'Body Composition', 'Heart Weight', 'Clinical Blood Chemistry', 'Hematology', 'SHIRPA', 'Startle/PPI', 'Dysmorphology', 'ABR', 'ERGv2']
    taskNames = ['E12.5 Embryo Gross Morphology', 'E12.5 Placenta Morphology', 'E15.5 Embryo Gross Morphology', 'E15.5 Placenta Morphology', 'E18.5 Embryo Gross Morphology', 'E18.5 Placenta Morphology', 'E9.5 Embryo Gross Morphology', 'E9.5 Placenta Morphology']
    return taskNames
    
 
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

def setWorkgroup(workgroupName):
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
    
    return 0

def getInputsFromTaskName(taskName):
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
    createInputCsvFileHeader()
    taskNames = getTaskNames()
    for taskName in taskNames:
        inputDictLs = getInputsFromTaskName(escapeHtmlCharacter(taskName))
        createInputCsv(taskName,inputDictLs)
    return inputDictLs


def getOutputsFromTaskName(taskName):
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
    createOutputCsvFileHeader()
    taskNames = getTaskNames()
    for taskName in taskNames:
        outputDictLs = getOutputsFromTaskName(escapeHtmlCharacter(taskName))
        createOutputCsv(taskName,outputDictLs)
    return outputDictLs

def getTaskInfoFromFilter(taskInfoFiler):
    taskInfoLs = []
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        print(">"+json.dumps(taskInfoFiler)+"<")
        wgResponse = requests.post(endpoint()+'/taskAnimalInfo', data=json.dumps(taskInfoFiler), headers=call_header, timeout=60)
        taskInfoLs = wgResponse.json()
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
       
    return taskInfoLs

def getAnimalInfoFromFilter(animalInfoFilter):
    animalInfoLs = []
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        wgResponse = requests.post(endpoint()+'/animalInfo', data=json.dumps(animalInfoFilter), headers=call_header, timeout=300)
        
        if wgResponse.status_code == 500: # Server error
            print(wgResponse.content)
        elif wgResponse.status_code == 422:
            print(wgResponse.content)
        elif wgResponse.status_code == 200:
            animalInfoLs = wgResponse.json()
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
       
    return animalInfoLs

def getMinMaxFromOutput(key):
    min = None
    max = None
    
    return min, max

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

"""
def getProceduresGivenFilter(taskNameFilter):
    # Return a list of dictionaries where each dictionary is a procedure
    # This will also work when there are no animals associated with the task.
    if taskNameFilter is None or taskNameFilter["taskInstance"] is None:
        return []
    
    workFlowTaskName =  taskNameFilter["taskInstance"]["workflowTaskName"]
    if workFlowTaskName is None:
        return []
    
    # OK. Let's extract the filters
    startDateFilter = None;
    if 'completedStartDate' in  taskNameFilter["taskInstance"].keys():
        startDateFilter =  taskNameFilter["taskInstance"]["completedStartDate"]
        
    endDateFilter = None;
    if 'completedStartDate' in  taskNameFilter["taskInstance"].keys():
        endDateFilter = taskNameFilter["taskInstance"]["completedEndDate"]
    
    workFlowTaskStatusFilter = ""
    if 'workflowTaskStatus' in  taskNameFilter["taskInstance"].keys():
        workFlowTaskStatusFilter = taskNameFilter["taskInstance"]["workflowTaskStatus"]
    
    reviewedOnlyFilter = taskNameFilter["taskInstance"]["isReviewed"] == True
    
    # end of filters (we can expand as needed)
    
    taskInfoLs = [] # Response from CLIMB
    taskInfoReturnDictLs = { "taskInfo":[] } # What we return - a list of dictionaries
    
    call_header = {'Authorization' : 'Bearer ' + token()}
    try:
        # Start calls to CLIMB -- first are tasks
        endpointUrl = endpoint() +'/taskinstances?WorkflowTaskName=' + escapeHtmlCharacter(workFlowTaskName) + '&PageNumber=0&PageSize=2000'
        wgResponse = requests.get(endpointUrl, headers=call_header, timeout=60)
        taskInfoLs = wgResponse.json()
        taskInfoLs = taskInfoLs["data"]["items"]
        
        # Big loop: Remove tasks that fail the filter
        for taskinstance in reversed(taskInfoLs):
            # Are we filtering by status?
            if len(workFlowTaskStatusFilter) > 0 and taskinstance["taskStatus"] != workFlowTaskStatusFilter:
                taskInfoLs.remove(taskinstance)
                continue
            
            # Are we filtering by date complete?
            if startDateFilter != None:
                if taskinstance["dateComplete"] == '':
                    taskInfoLs.remove(taskinstance)
                    continue
                elif startDateFilter > taskinstance["dateComplete"]:
                    taskInfoLs.remove(taskinstance)
                    continue
                    
            if endDateFilter != None:
                if taskinstance["dateComplete"] == '':
                    taskInfoLs.remove(taskinstance)
                    continue
                elif endDateFilter < taskinstance["dateComplete"]:
                    taskInfoLs.remove(taskinstance)
                    continue
            
            # Are we filtering by reviewed only?
            isReviewed = (taskinstance["reviewedBy"] != None) and (taskinstance["reviewedBy"] != '') # some value for reviewedBy
            if isReviewed == False and reviewedOnlyFilter == True:
                    taskInfoLs.remove(taskinstance)
                    continue
        # End of loop
        
        for taskinstance in taskInfoLs:
        # Get the inputs
            endpointUrl = endpoint() +'/taskinstances/taskInputs?TaskInstanceKey=' + str(taskinstance["taskInstanceKey"]) + '&PageNumber=0&PageSize=200'
            wgResponse = requests.get(endpointUrl, headers=call_header, timeout=60)
            inputLs = wgResponse.json()
            inputsOnly = inputLs["data"]["items"]
            # clean up unwanted input objects
            inputsOnly = cleanupInputs(inputsOnly)
            taskinstance["inputs"] = inputsOnly
            
        # Get the outputs
            endpointUrl = endpoint() +'/taskinstances/taskOutputs?TaskInstanceKey=' + str(taskinstance["taskInstanceKey"]) + '&PageNumber=0&PageSize=200'
            wgResponse = requests.get(endpointUrl, headers=call_header, timeout=60)
            outputLs = wgResponse.json()
            outputsOnly = outputLs["data"]["items"]
            # clean up unwanted output objects
            outputsOnly = cleanupOutputs(outputsOnly)
            taskinstance["outputs"] = outputsOnly
            
            # List inside a dict inside a list
            taskInfoReturnDictLs["taskInfo"].append({'taskInstance' : [taskinstance]}) 
        # A list containing one element that is a dict that is a llst of taskInstances
 
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
    
    return taskInfoReturnDictLs

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

    """_
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


def getProceduresAndDataGivenName(procName):
    # Return a list of dictionaries where dictionary is a procedure with inputs and putputs
    return []

def getAnimalsGivenProcedureName(proName):
    # Return a list of dictionaries where each element is an animals with strain and genotype info
    return []
 
    
######## END OF USEFUL, SPECIAL CLIMB METHODS

#### CSV CSV #########################################
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
#######################################################

if __name__ == '__main__':
    setWorkgroup('KOMP-JAX Lab')
    setMyToken(getTokenEx('mike', '1banana1'))
    getProceduresGivenFilter(json.loads('{ "taskInstance": { "workflowTaskName": "Viability Primary Screen v2", "workflowTaskStatus":"Complete", "isReviewed": true}, "animal": "", "lines": [] }'))
    print("SUCCESS")
