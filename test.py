import requests
import os
from datetime import datetime
import pytz
import json


if __name__ == '__main__':
    
    response = requests.get('https://api.mousephenotype.org/validation/status?u=spikemcfarland&s=glpat-k1zZWp2-yT1pAHXB2tFm')
    if response.status_code != 200:
        print('>>>>>> RESPONSE CONTENT TYPE <<<<<<')
        type(response.content)
        if response.content is not None:
            print('>>>>>> RESPONSE CONTENT <<<<<<')
            print(response.content)
            myContent = response.content.decode('utf8')
            if 'error' in myContent and 'error_description' in myContent:
                raise Exception(myContent['error'], myContent['error_description'])
            else:
                raise Exception("Response content is empty. Status code is {0}.".format(response.status_code))
    else:
        print(response.content)
            
