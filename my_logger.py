"""
        This module handles the logging for dcc_xml generator
"""

import read_config as cfg
import logging
from logging.handlers import TimedRotatingFileHandler
import re

import argparse
from datetime import datetime

g_logger = None

def init():
    mycfg = cfg.parse_config(path="config.yml")
    # Setup properties for loggng
    log_dir = mycfg['directories']['xml_log_path']
    filename = mycfg['filenames']['dcc_xml_logfile_name']
    log_file = log_dir + filename
    
    global g_logger
    g_logger = logging.getLogger(__name__)
    date = datetime.now().strftime("%B-%d-%Y")
    #FORMAT = "[%(asctime)s->%(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
    FORMAT = "[%(asctime)s]%(levelname)s: %(message)s"
    logging.basicConfig(format=FORMAT, filemode="w", level=logging.DEBUG, force=True)
    handler =TimedRotatingFileHandler(f"{log_file}_{date}.log" , when="midnight", backupCount=10)
    handler.setFormatter(logging.Formatter(FORMAT))
    handler.suffix = "%Y%m%d"
    handler.extMatch = re.compile(r"^\d{8}$")
    g_logger.addHandler(handler)
    
    g_logger.info('Logger has been created')

def info(message):
    if g_logger == None:
        init()
        
    g_logger.info(message)
    

def debug(message):
    if g_logger == None:
        init()
        
    g_logger.debug(message)