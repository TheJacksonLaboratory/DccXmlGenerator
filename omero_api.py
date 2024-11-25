
"""
omero_api.py

This module provides functions to interact with the OMERO server to retrieve image file paths and IDs.
It includes functions to initialize and close connections to the OMERO server, as well as to fetch
image file paths given an image ID or URL.

Dependencies:
- ezomero
- secret
- requests

Author: Michael McFarland
Date: 11/14/2024 
"""

import ezomero
import secret
import requests
import jaxlims_api
import json

conn = None

GATES_PUBLIC_PRJ_ID=1301
GATES_PRJ_ID=1356
GATES_PRJ_NAME='Gates Foundation'

KOMP_EYE_PRJ_NAME='KOMP_eye'
KOMP_EYE_PRJ_ID=203

KOMP_ULOAD_SFTP_SERVER = 'sftp://bhjlk02lp.jax.org/images/'

def getAllImportedOmeroImagesGivenImageId(image_id):
    
    """
    Given a connection object and an image id, return the full original pathname

    Returns:
        str: Original file path of the image    
    """
    orig_file_path = ''
    global conn
    try:
        if conn == None:
            omero_init(KOMP_EYE_PRJ_NAME)  # Name doesn't really matter
        conn.connect()
        orig_file_path_ls = ezomero.get_original_filepaths(conn,image_id)
        orig_file_path_ls = orig_file_path_ls[0].split('/')
        orig_file_path = orig_file_path_ls[len(orig_file_path_ls)-1]  # list should alway be onet']])
    except Exception as e:
        print(e)    
    finally:
        omero_close()
    
    return orig_file_path


def omero_init(group_name):
    """
    Initialize the OMERO connection using credentialis from the secret module
    """
    
    global conn
    if conn is None:
        conn = ezomero.connect(user=secret.OMERO_USER, 
                               password=secret.OMERO_PASSWORD, 
                               host=secret.OMERO_HOST, 
                               group=group_name, 
                               port=secret.OMERO_PORT, 
                               secure=True, config_path='.ezomero')
    return conn 


def omero_close():
    """
    Close the OMERO connection

    Returns:
        None: conn will be None after this call   
    """
    global conn
    if conn is not None:
        conn.close()
        conn = None
    return conn 

"""
Project         203=KOMP, 1356=Gates Foundation 
    Dataset     (stock numer for KOMP) (marker+jr) for Gates3523=KOMP, 35575=Gates Foundation
        Image
'"""

def get_omero_id_given_public_id(public_id):
    # Disover the proivate image id given the public image id
    session = requests.Session()
    
    web_host="http://images.jax.org"
    api_url = '%s/api/' % web_host
    r = session.get(api_url, verify=True)
    
    map_url = "https://images.jax.org/webclient/api/annotations/?type=map&image=%s" % public_id
    map_json = session.get(map_url).json()
    
    if 'annotations' not in map_json:  # dict
        print("No annotations found for image %s" % public_id)  
        print(map_json) 
        return None
    
    # Find the list we need
    annotations = map_json['annotations'] # List
    for annotation in annotations:
        if 'values' in annotation:
            for value in annotation['values']:
                if value[0] == 'origin_image_id':
                    return int(value[1])

    print("No origin_image_id found for image %s" % public_id)  
    print(json.dumps(map_json, indent=4, sort_keys=True))   
    return None
    
# This is the entry point for this module.  It is called from the XML generation module when the 
# Return empty string on error
def get_upload_image_filename(image_url:str) -> str:
    
    filename = ''   
    image_id = None
    
    # If this is an image stored on the public site
    # then we need to get the full path to the imagewe have a different way to get the image name
    if 'images.jax.org' in image_url:  # Public site 
        image_id = int(image_url.split('-')[-1]) # ex: http://images.jax.org/webclient/?show=image-356646     
        image_id = get_omero_id_given_public_id(image_id) # Pass in public get back private
    else:
        image_id = int(image_url.split('/')[-1])    # ex: 'https://omeroweb.jax.org/webgateway/img_detail/69844'
    
    if image_id is not None:
        filename = getAllImportedOmeroImagesGivenImageId(image_id)  
    return filename

def is_omero_url(url:str) -> bool:
    return ('omeroweb.jax.org' in url) or ('images.jax.org' in url)    


def create_imagefileuploadstatus_record(omero_url:str, impc_code:str) -> None:
    """
    Update the image file upload status in the database

    Args:
        image_url (str): The image URL
        status (str): The status to update the image to
    """
    try:
        # Get the source filename
        filename = get_upload_image_filename(omero_url)
        # Create the destination filename
        filename = KOMP_ULOAD_SFTP_SERVER + filename    
        jaxlims_api.recordMediaSubmission(omero_url, filename, 0, impc_code)    
    except Exception as e:
        print(e)
        print("Error in create_imagefileuploadstatus")
        print(omero_url)
        print(impc_code)
        print(filename) 
        

     
if __name__ == "__main__":
    histo_image_url = ['https://images.jax.org/webclient/?show=image-187928',
    'https://images.jax.org/webclient/?show=image-187934',
    'https://images.jax.org/webclient/?show=image-187952',
    'https://images.jax.org/webclient/?show=image-187958',
    'https://images.jax.org/webclient/?show=image-187964',
    'https://images.jax.org/webclient/?show=image-188254',
    'https://images.jax.org/webclient/?show=image-188257',
    'https://images.jax.org/webclient/?show=image-188266',
    'https://images.jax.org/webclient/?show=image-188287',
    'https://images.jax.org/webclient/?show=image-188299',
    'https://images.jax.org/webclient/?show=image-188464',
    'https://images.jax.org/webclient/?show=image-188482',
    'https://images.jax.org/webclient/?show=image-188497',
    'https://images.jax.org/webclient/?show=image-188503',
    'https://images.jax.org/webclient/?show=image-188506',
    'https://images.jax.org/webclient/?show=image-188605',
    'https://images.jax.org/webclient/?show=image-188614',
    'https://images.jax.org/webclient/?show=image-188623',
    'https://images.jax.org/webclient/?show=image-188626',
    'https://images.jax.org/webclient/?show=image-188629',
    'https://images.jax.org/webclient/?show=image-188804',
    'https://images.jax.org/webclient/?show=image-188819',
    'https://images.jax.org/webclient/?show=image-188822',
    'https://images.jax.org/webclient/?show=image-188825',
    'https://images.jax.org/webclient/?show=image-188837',
    'https://images.jax.org/webclient/?show=image-360119',
    'https://images.jax.org/webclient/?show=image-360131',
    'https://images.jax.org/webclient/?show=image-360152',
    'https://images.jax.org/webclient/?show=image-360164',
    'https://images.jax.org/webclient/?show=image-360170',
    'https://images.jax.org/webclient/?show=image-360486',
    'https://images.jax.org/webclient/?show=image-360511',
    'https://images.jax.org/webclient/?show=image-360514',
    'https://images.jax.org/webclient/?show=image-360517',
    'https://images.jax.org/webclient/?show=image-360529',
    'https://images.jax.org/webclient/?show=image-188061',
    'https://images.jax.org/webclient/?show=image-188094',
    'https://images.jax.org/webclient/?show=image-188115',
    'https://images.jax.org/webclient/?show=image-188136',
    'https://images.jax.org/webclient/?show=image-188172',
    'https://images.jax.org/webclient/?show=image-188647',
    'https://images.jax.org/webclient/?show=image-188650',
    'https://images.jax.org/webclient/?show=image-188662',
    'https://images.jax.org/webclient/?show=image-188669',
    'https://images.jax.org/webclient/?show=image-188708',
    'https://images.jax.org/webclient/?show=image-188855',
    'https://images.jax.org/webclient/?show=image-188876',
    'https://images.jax.org/webclient/?show=image-188942',
    'https://images.jax.org/webclient/?show=image-188996',
    'https://images.jax.org/webclient/?show=image-189071',
    'https://images.jax.org/webclient/?show=image-189074',
    'https://images.jax.org/webclient/?show=image-355972',
    'https://images.jax.org/webclient/?show=image-355988',
    'https://images.jax.org/webclient/?show=image-356006',
    'https://images.jax.org/webclient/?show=image-356009',
    'https://images.jax.org/webclient/?show=image-356159',
    'https://images.jax.org/webclient/?show=image-356420',
    'https://images.jax.org/webclient/?show=image-356429',
    'https://images.jax.org/webclient/?show=image-356505',
    'https://images.jax.org/webclient/?show=image-356529',
    'https://images.jax.org/webclient/?show=image-356613',
    'https://images.jax.org/webclient/?show=image-356646',
    'https://images.jax.org/webclient/?show=image-356675',
    'https://images.jax.org/webclient/?show=image-356714',
    'https://images.jax.org/webclient/?show=image-356738',
    'https://images.jax.org/webclient/?show=image-356762',
    'https://images.jax.org/webclient/?show=image-356813',
    'https://images.jax.org/webclient/?show=image-356998',
    'https://images.jax.org/webclient/?show=image-357025',
    'https://images.jax.org/webclient/?show=image-357073',
    'https://images.jax.org/webclient/?show=image-357076',
    'https://images.jax.org/webclient/?show=image-357103',
    'https://images.jax.org/webclient/?show=image-357187',
    'https://images.jax.org/webclient/?show=image-357190',
    'https://images.jax.org/webclient/?show=image-357253',
    'https://images.jax.org/webclient/?show=image-357280',
    'https://images.jax.org/webclient/?show=image-357292',
    'https://images.jax.org/webclient/?show=image-357298',
    'https://images.jax.org/webclient/?show=image-357313',
    'https://images.jax.org/webclient/?show=image-357382',
    'https://images.jax.org/webclient/?show=image-357445',
    'https://images.jax.org/webclient/?show=image-357488',
    'https://images.jax.org/webclient/?show=image-357655',
    'https://images.jax.org/webclient/?show=image-357701',
    'https://images.jax.org/webclient/?show=image-357731',
    'https://images.jax.org/webclient/?show=image-357746',
    'https://images.jax.org/webclient/?show=image-357758',
    'https://images.jax.org/webclient/?show=image-357810',
    'https://images.jax.org/webclient/?show=image-357822',
    'https://images.jax.org/webclient/?show=image-357858',
    'https://images.jax.org/webclient/?show=image-357894',
    'https://images.jax.org/webclient/?show=image-357939',
    'https://images.jax.org/webclient/?show=image-357960',
    'https://images.jax.org/webclient/?show=image-358066',
    'https://images.jax.org/webclient/?show=image-358090',
    'https://images.jax.org/webclient/?show=image-358166',
    'https://images.jax.org/webclient/?show=image-358217',
    'https://images.jax.org/webclient/?show=image-358259',
    'https://images.jax.org/webclient/?show=image-358262',
    'https://images.jax.org/webclient/?show=image-358319',
    'https://images.jax.org/webclient/?show=image-358349',
    'https://images.jax.org/webclient/?show=image-358355',
    'https://images.jax.org/webclient/?show=image-359018',
    'https://images.jax.org/webclient/?show=image-359021',
    'https://images.jax.org/webclient/?show=image-359036',
    'https://images.jax.org/webclient/?show=image-359075',
    'https://images.jax.org/webclient/?show=image-359198',
    'https://images.jax.org/webclient/?show=image-359323',
    'https://images.jax.org/webclient/?show=image-359350',
    'https://images.jax.org/webclient/?show=image-359371',
    'https://images.jax.org/webclient/?show=image-359407',
    'https://images.jax.org/webclient/?show=image-359437',
    'https://images.jax.org/webclient/?show=image-359910',
    'https://images.jax.org/webclient/?show=image-359946',
    'https://images.jax.org/webclient/?show=image-359979',
    'https://images.jax.org/webclient/?show=image-360015',
    'https://images.jax.org/webclient/?show=image-360058',
    'https://images.jax.org/webclient/?show=image-187928',
    'https://images.jax.org/webclient/?show=image-187934',
    'https://images.jax.org/webclient/?show=image-187952',
    'https://images.jax.org/webclient/?show=image-187958',
    'https://images.jax.org/webclient/?show=image-187964',
    'https://images.jax.org/webclient/?show=image-188254',
    'https://images.jax.org/webclient/?show=image-188257',
    'https://images.jax.org/webclient/?show=image-188266',
    'https://images.jax.org/webclient/?show=image-188287',
    'https://images.jax.org/webclient/?show=image-188299',
    'https://images.jax.org/webclient/?show=image-188464',
    'https://images.jax.org/webclient/?show=image-188482',
    'https://images.jax.org/webclient/?show=image-188497',
    'https://images.jax.org/webclient/?show=image-188503',
    'https://images.jax.org/webclient/?show=image-188506',
    'https://images.jax.org/webclient/?show=image-188605',
    'https://images.jax.org/webclient/?show=image-188614',
    'https://images.jax.org/webclient/?show=image-188623',
    'https://images.jax.org/webclient/?show=image-188626',
    'https://images.jax.org/webclient/?show=image-188629',
    'https://images.jax.org/webclient/?show=image-188804',
    'https://images.jax.org/webclient/?show=image-188819',
    'https://images.jax.org/webclient/?show=image-188822',
    'https://images.jax.org/webclient/?show=image-188825',
    'https://images.jax.org/webclient/?show=image-188837',
    'https://images.jax.org/webclient/?show=image-360119',
    'https://images.jax.org/webclient/?show=image-360131',
    'https://images.jax.org/webclient/?show=image-360152',
    'https://images.jax.org/webclient/?show=image-360164',
    'https://images.jax.org/webclient/?show=image-360170',
    'https://images.jax.org/webclient/?show=image-360486',
    'https://images.jax.org/webclient/?show=image-360511',
    'https://images.jax.org/webclient/?show=image-360514',
    'https://images.jax.org/webclient/?show=image-360517',
    'https://images.jax.org/webclient/?show=image-360529',
    'https://images.jax.org/webclient/?show=image-188076',
    'https://images.jax.org/webclient/?show=image-188079',
    'https://images.jax.org/webclient/?show=image-188106',
    'https://images.jax.org/webclient/?show=image-188112',
    'https://images.jax.org/webclient/?show=image-188184',
    'https://images.jax.org/webclient/?show=image-188672',
    'https://images.jax.org/webclient/?show=image-188687',
    'https://images.jax.org/webclient/?show=image-188693',
    'https://images.jax.org/webclient/?show=image-188753',
    'https://images.jax.org/webclient/?show=image-188789',
    'https://images.jax.org/webclient/?show=image-188924',
    'https://images.jax.org/webclient/?show=image-188933',
    'https://images.jax.org/webclient/?show=image-188993',
    'https://images.jax.org/webclient/?show=image-189020',
    'https://images.jax.org/webclient/?show=image-189044',
    'https://images.jax.org/webclient/?show=image-189113',
    'https://images.jax.org/webclient/?show=image-356030',
    'https://images.jax.org/webclient/?show=image-356060',
    'https://images.jax.org/webclient/?show=image-356147',
    'https://images.jax.org/webclient/?show=image-356159',
    'https://images.jax.org/webclient/?show=image-356162',
    'https://images.jax.org/webclient/?show=image-356438',
    'https://images.jax.org/webclient/?show=image-356453',
    'https://images.jax.org/webclient/?show=image-356465',
    'https://images.jax.org/webclient/?show=image-356523',
    'https://images.jax.org/webclient/?show=image-356541',
    'https://images.jax.org/webclient/?show=image-356607',
    'https://images.jax.org/webclient/?show=image-356657',
    'https://images.jax.org/webclient/?show=image-356678',
    'https://images.jax.org/webclient/?show=image-356696',
    'https://images.jax.org/webclient/?show=image-356801',
    'https://images.jax.org/webclient/?show=image-356804',
    'https://images.jax.org/webclient/?show=image-357013',
    'https://images.jax.org/webclient/?show=image-357019',
    'https://images.jax.org/webclient/?show=image-357028',
    'https://images.jax.org/webclient/?show=image-357046',
    'https://images.jax.org/webclient/?show=image-357142',
    'https://images.jax.org/webclient/?show=image-357163',
    'https://images.jax.org/webclient/?show=image-357205',
    'https://images.jax.org/webclient/?show=image-357226',
    'https://images.jax.org/webclient/?show=image-357232',
    'https://images.jax.org/webclient/?show=image-357268',
    'https://images.jax.org/webclient/?show=image-357400',
    'https://images.jax.org/webclient/?show=image-357433',
    'https://images.jax.org/webclient/?show=image-357472',
    'https://images.jax.org/webclient/?show=image-357484',
    'https://images.jax.org/webclient/?show=image-357506',
    'https://images.jax.org/webclient/?show=image-357631',
    'https://images.jax.org/webclient/?show=image-357643',
    'https://images.jax.org/webclient/?show=image-357658',
    'https://images.jax.org/webclient/?show=image-357704',
    'https://images.jax.org/webclient/?show=image-357707',
    'https://images.jax.org/webclient/?show=image-357834',
    'https://images.jax.org/webclient/?show=image-357870',
    'https://images.jax.org/webclient/?show=image-357900',
    'https://images.jax.org/webclient/?show=image-357927',
    'https://images.jax.org/webclient/?show=image-357945',
    'https://images.jax.org/webclient/?show=image-357966',
    'https://images.jax.org/webclient/?show=image-358009',
    'https://images.jax.org/webclient/?show=image-358057',
    'https://images.jax.org/webclient/?show=image-358157',
    'https://images.jax.org/webclient/?show=image-358253',
    'https://images.jax.org/webclient/?show=image-358289',
    'https://images.jax.org/webclient/?show=image-358307',
    'https://images.jax.org/webclient/?show=image-358310',
    'https://images.jax.org/webclient/?show=image-358331',
    'https://images.jax.org/webclient/?show=image-358343',
    'https://images.jax.org/webclient/?show=image-359093',
    'https://images.jax.org/webclient/?show=image-359132',
    'https://images.jax.org/webclient/?show=image-359141',
    'https://images.jax.org/webclient/?show=image-359156',
    'https://images.jax.org/webclient/?show=image-359189',
    'https://images.jax.org/webclient/?show=image-359254',
    'https://images.jax.org/webclient/?show=image-359278',
    'https://images.jax.org/webclient/?show=image-359281',
    'https://images.jax.org/webclient/?show=image-359320',
    'https://images.jax.org/webclient/?show=image-359383',
    'https://images.jax.org/webclient/?show=image-359901',
    'https://images.jax.org/webclient/?show=image-359931',
    'https://images.jax.org/webclient/?show=image-359940',
    'https://images.jax.org/webclient/?show=image-359970',
    'https://images.jax.org/webclient/?show=image-359994' ]
    private_id = 0
    with open('omero_api_test.log', 'w') as f:
        f.write("Starting\n")               
        for filename in histo_image_url:
            filename = get_upload_image_filename(filename)
            f.write(filename + '\t' + str(private_id) + filename + '\n')
    print("Done")