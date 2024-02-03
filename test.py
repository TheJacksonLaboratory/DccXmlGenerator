import requests
import os
from datetime import datetime
import csv
import json
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

"""Note:	
   JR18558	is	UCD-10916A-F3-1-1
	JR21753	is	PH21753
"""

if __name__ == '__main__':
   """ 
   url = "https://www.ebi.ac.uk/mi/impc/solr/experiment/select?q=colony_id:PH21753&fl=colony_id,external_sample_id,sex,zygosity,experiment_source_id,procedure_stable_id&rows=25000"
   response = requests.get(url, timeout=15)
   responseJson = response.json()
   
   docs = responseJson["response"]["docs"]
   print(len(docs))
   new_ls = [dict(t) for t in {tuple(d.items()) for d in docs}]
   print(len(new_ls))
   {
   "external_sample_id":"C5673",
   "experiment_source_id":"Histopathology (2+2) - C5673 - 87337",
   "sex":"male",
   "zygosity":"heterozygote"}
   try:
      #sqlStmt = INSERT INTO komp.ebi_procedures (organism_name, experiment_name, sex, JRNumber, zygosity, IMPC_CODE)
      #VALUES( '{0}', '{1}', '{2}', '{3}', '{4}', '{5}') ;
      
      mysqldb = mysql.connector.connect(host='rslims.jax.org', user='dba', password='rsdba', database='komp')
      #mysqldb.cursor().executemany(sqlStmt, new_ls)
      for d in new_ls:
         if 'external_sample_id' not in d:
            d['external_sample_id'] = 'none'
         
         mysqldb.cursor().execute(sqlStmt.format(d["external_sample_id"],
                                       d["experiment_source_id"],d["sex"],
                                       d["colony_id"],d["zygosity"],d["procedure_stable_id"]))
      mysqldb.commit()
      mysqldb.cursor().close()
      mysqldb.close()
   except Exception:
      print ("Caught exception.")
    """
    
    