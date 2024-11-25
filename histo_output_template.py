"""
    The list fo all suported Histopathology parameters supported by us. 
    
    I used the query 
    SELECT "{'outputKey' : ",_ClimbType_key, ", 'outputName' :'", ImpcCode, "', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'}," FROM komp.dccparameterdetails where _ClimbType_key > 0 AND ImpcCode LIKE '%_HIS_%' AND _DccType_key <> 7; -- AND ImpcCode IN (

     
    For those that we report on we will replace the None value with the actual value.   
"""


import mysql.connector
import json
import omero_api as omero

histo_items_ls = None

"""
EX  : [
{'outputKey' : 825, 'outputName' :'IMPC_HIS_117_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 824, 'outputName' :'IMPC_HIS_139_002', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
{'outputKey' : 1053, 'outputName' :'IMPC_HIS_140_001', 'outputValue' : None, 'collectedDate' :'2000-01-01', 'collectedBy' :'Kristy', 'modifiedBy' : 'Kristy', 'dateModified' : '2000-01-01', 'statusCode' : 'Parameter not measured - not in SOP'},
....
"""

# IMPC_HIS_177_001 - The images are store differently in CLIMB for Histo. Need kluge.
def build_histo_image(climbOutputLs:list) -> str:   
  image_dict = {}  
  # "Testis Images" : 977, "Epididymis images" : 978, "Ovary Images" : 1145, "Uterus Images" : 1146
  image_climb_keys = [ 1145, 1146, 978, 977]  # These are the keys in CLIMB for images.
  
  # The image values are stored as a string representation of a dict 
  # but refernce an image in the public facing OMERO database.
  # This method will :
  # 1. Find the image keys in the list of output keys listed in image_climb_keys[] .
  # 2. Convert the string representation of a dict to a dict.
  # 3. Convert the image values to a real dict.
  # 4. Convert the public facing OMERO value to the private facing OMERO id.
  # 5. Build a URL to the private facing OMERO image.
  
  filename = ''
  filename_ls = []  
  image_dict = {}
  
  private_omero_url_base= 'https://omeroweb.jax.org/webgateway/img_detail/'
  
  try:
    # Find the images in these outputs and build a list.
    for v in image_climb_keys:
        output = next((d for d in climbOutputLs if d.get("outputKey") == v), None)
        if output != None:
          if output["outputValue"] != None:
            filename = output["outputValue"]  # For histo this should be a string version of a dict
            filename = filename.replace("\'","\"")  # Convert the string to a dict.
            filename_dict = json.loads(filename)  # Convert the string to a dict.
            filename_ls.append(filename_dict["1"])  # The value is the public facing OMERO id.
            
    # filename_ls should now contain the public facing OMERO ids.    
    key = 1
    for filename in filename_ls:
      # Get the private URL given the public URL
      private_id = omero.get_omero_id_given_public_id(int(filename.split("-")[1]))
      image_dict[key] = private_omero_url_base + str(private_id)   
      key = key + 1
  except Exception as e:
    print(e)
  finally:
    return json.dumps(image_dict) 


def generate_histo_template():
  
  selectStmt = "SELECT _ClimbType_key, ImpcCode FROM KOMP.dccparameterdetails WHERE _ClimbType_key > 0 AND ImpcCode LIKE '%_HIS_%' AND _DccType_key <> 7 ORDER BY _DccType_key,ImpcCode"

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
  d = find_dict_by_key_value('outputKey', 977) 
  d = find_dict_by_key_value('outputKey', 978)  
  d = find_dict_by_key_value('outputKey', 1145)  
  d = find_dict_by_key_value('outputKey', 1146)  
  print(d)