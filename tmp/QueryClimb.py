#

import json


def getTaskAnimalDataFilter():
    return ''' {"taskInstance": 
               {"completed_start_date": "","completed_end_date": "","due_start_date": "","due_end_date": "",
                  "workflow_task_key": 0,"workflow_task_name": "","workflow_task_status": "", 
                   "material_key": 0,"isReviewed": false},
               "animals": [{"animalId": 0,"animalName": "","materialKey": 0,"generation": ""}],
               "lines": [{"lineKey": 0,"lineName": "","stock": ""}]} '''
  
  
if __name__ == '__main__':
    print(getTaskAnimalDataFilter())
    print(json.loads(getTaskAnimalDataFilter()))