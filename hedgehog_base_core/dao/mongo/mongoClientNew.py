import configparser

import os
import pymongo
from pymongo.errors import DuplicateKeyError

current_path = os.path.dirname(__file__)
current_path = current_path[:current_path.find('beyebe-spider-xiaociwei')+len('beyebe-spider-xiaociwei')]
cf = configparser.ConfigParser()
cf.read(current_path+"/configMyself.conf", "utf-8")
# [mongoDB]
# ip=192.168.10.9
# port=27017
# database=hedgehog_spider
# user=fangnan
# password=Fang135

MONGODB_IP = cf.get("mongoDB", "ip")
MONGODB_PORT = cf.get("mongoDB", "port")
MONGODB_USER = cf.get("mongoDB", "user")
MONGODB_PASSWORD = cf.get("mongoDB", "password")
MONGODB_DATABASE = cf.get("mongoDB", "database")

db_spider = pymongo.MongoClient(MONGODB_IP, int(MONGODB_PORT))[MONGODB_DATABASE]
db_spider.authenticate(MONGODB_USER, MONGODB_PASSWORD)


def saveToDownloadTable(missionBean):
    if '_id' in missionBean.__dict__:
        missionBean.__dict__.pop('_id')
    try:
        tableName = 'download_all_xiaociwei'
        dictNow = missionBean.getDataBaseDict()
        tS = db_spider[tableName].insert(dictNow)
        missionBean._id = str(dictNow['_id'])
        missionBean.downloadId = str(dictNow['_id'])
        return tS
    except DuplicateKeyError:
        pass
    except Exception as err:
        print("[ERROR]数据库入库错误")
        traceback.print_exc()
        missionBean._id = 'error_datebase_insert'
        missionBean._mongoErrMsg = str(err)
