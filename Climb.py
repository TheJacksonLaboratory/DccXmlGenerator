#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import NullHandler
import requests
import sys
import json
import datetime
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
        print(token)
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
    taskNames = ['Eye Morphology', 'Body Weight', 'First Body Weight', 'Open Field', 'Grip Strength', 'Light/Dark', 'Holeboard', 'EKGv3', 'GTT', 'Body Composition', 'Heart Weight', 'Clinical Blood Chemistry', 'Hematology', 'SHIRPA', 'Startle/PPI', 'Dysmorphology', 'ABR', 'ERGv2']
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
        print(endpoint() +'/taskAnimalInfo')
        print(json.dumps(taskInfoFiler))
        print(call_header)
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

def getMinMaxFromOutput(key):
    min = None
    max = None
    
    return min, max
    
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
    setMyToken(getTokenEx('mike', '1banana1'))
    setWorkgroup('KOMP-JAX Lab')
    setMyToken(getTokenEx('mike', '1banana1'))
    #userDictLs = getClimbUsers()
    #print(json.dumps(userDictLs, indent=4, sort_keys=True))
    #createUserCsv(userDictLs)
    
    
    print("SUCCESS")
