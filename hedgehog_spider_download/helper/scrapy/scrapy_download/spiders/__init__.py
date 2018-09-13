# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import configparser
import platform

import sys

import os

current_path = os.path.dirname(__file__)
current_path = current_path[:current_path.find('beyebe-spider-xiaociwei')+len('beyebe-spider-xiaociwei')]
cf = configparser.ConfigParser()
cf.read(current_path+"/configMyself.conf", "utf-8")
if 'Linux' in platform.system():
    sysPath = cf.get("sysPath", "linux")
    sys.path.append(sysPath)
    print("sysPath setting ok in linux")
elif 'Windows' in platform.system():
    sysPath = cf.get("sysPath", "windows")
    sys.path.append(sysPath)
    print("sysPath setting ok in Windows")
else:
    sysPath = cf.get("sysPath", "mac")
    sys.path.append(sysPath)
    print("sysPath setting ok in mac")
