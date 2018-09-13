import platform

import sys

import time
from six.moves import configparser

# 生成config对象

cf = configparser.ConfigParser()
cf.read("../../../configMyself.conf", "utf-8")
try:
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
except:
    sys.path.append('../../')
