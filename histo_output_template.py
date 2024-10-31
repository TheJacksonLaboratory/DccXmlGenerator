"""
    The list fo all suported Histopathology parameters supported by us. 
    
    I used the query 
    SELECT "{'outputKey' : ",_ClimbType_key, ", 'outputName' :'", ImpcCode, "', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'}," FROM komp.dccparameterdetails where _ClimbType_key > 0 AND ImpcCode LIKE '%_HIS_%' AND _DccType_key <> 7; -- AND ImpcCode IN (

     
    For those that we report on we will replace the None value with the actual value.   
"""


import mysql.connector
import json

histo_items_ls = None

"""
EX  : [
{'outputKey' : 825, 'outputName' :'IMPC_HIS_117_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 824, 'outputName' :'IMPC_HIS_139_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 1053, 'outputName' :'IMPC_HIS_140_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
....
"""

# IMPC_HIS_177_001 - The iages are store differently in CLIMB for Histo. Need kluge.
def build_histo_image(climbOutputLs:list) -> str:   
  image_dict = {}  
  # "Testis Images" : 977, "Epididymis images" : 978, "Ovary Images" : 1145, "Uterus Images" : 1146
  image_climb_keys = [ 1145, 1146, 978, 977]  # These are the keys in CLIMB for images.
  
  idx = 0
  # Find the images an build a list.
  for v in image_climb_keys:
    output = next((d for d in climbOutputLs if d.get("outputKey") == v), None)
    if output != None:
      if output["outputValue"] != None:
        idx = idx + 1
        image_dict[str(idx)] = output["outputValue"] # This is the image name.
  
  if idx == 0:
    return None
  else:
    return json.dumps(image_dict)

def generate_histo_template():
  
  selectStmt = "SELECT _ClimbType_key, ImpcCode FROM KOMP.dccparameterdetails WHERE _ClimbType_key > 0 AND ImpcCode LIKE '%_HIS_%' AND _DccType_key <> 7 ORDER BY _DccType_key"

  histo_template = []
  histo_dict = {'outputKey' : 0, 'outputName' :'', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'}

  try:    
    mysqldb = mysql.connector.connect(host="rslims", user="dba", password="rsdba", database="komp")
        
    mysqlCursor = mysqldb.cursor()
    mysqlCursor.execute(selectStmt)
        
    for (_ClimbType_key, ImpcCode) in mysqlCursor:
      histo_dict['outputKey'] = _ClimbType_key
      histo_dict['outputName'] = ImpcCode
      histo_template.append(histo_dict)       
      histo_dict = {'outputKey' : 0, 'outputName' :'', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'}
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
  d = find_dict_by_key_value('outputKey', 1117) 
  d = find_dict_by_key_value('outputKey', 12050)  
  d = find_dict_by_key_value('outputKey', 12051)  
  d = find_dict_by_key_value('outputKey', 12052)  
  d = find_dict_by_key_value('outputKey', 12053)  
  print(d)