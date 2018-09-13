# -* - coding: UTF-8 -* -

from six.moves import configparser
#生成config对象
cf = configparser.ConfigParser()
cf.read("../../../configMyself.conf","utf-8")

db_host = cf.get("sysPath", "mac")
print('sections:', db_host)

secs = cf.sections()
print('sections:', secs)