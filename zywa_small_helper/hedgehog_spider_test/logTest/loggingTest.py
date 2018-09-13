# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 10:32:50 2018

@author: Administrator
"""

import traceback

import numpy as np
# from MongoDBHelper import MongoDB
# from ES_Delete import deleteES
# from ESHelper import Elastic_search
import sys

import logging
import datetime

import math
import platform
import jieba

k, v = platform.architecture()

if 'Linux' in platform.platform(True):
    #    sys.path.append("../")
    logPath = '/root/logs'
    stopword_path = "stopword.txt"
elif 'Darwin' in platform.platform(True):

    logPath = '/Users/magic/Desktop/logs'
    stopword_path = "stopword.txt"
else:
    import os

    os.chdir("D:\\pySourceCode\\recommend-hot")
    logPath = './logs'
    stopword_path = "stopword.txt"

logfilename = sys.argv[0].split("/")[-1][:-3]
indexTime = datetime.datetime.now().strftime('%Y%m%d_%H')
loggerfilename = logPath + "/{0}_{1}.log".format(logfilename, indexTime)

FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'

handler = logging.FileHandler(loggerfilename, mode='a+', encoding="utf-8", delay=False)

# logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%a, %d %b %Y %H:%M:%S', filename=loggerfilename,filemode='w')

logging.basicConfig(level=logging.WARNING, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S', handlers=[handler])

logging.info("---------------info---------------------")
logging.debug("---------------debug---------------------")
logging.warning("---------------warning---------------------")
