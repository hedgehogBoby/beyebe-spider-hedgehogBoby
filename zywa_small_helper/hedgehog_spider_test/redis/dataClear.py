import json

import time

from zywa_database_core.dao.mongo.mongoClientMyself import MongoClientMyself

if __name__ == '__main__':
    __mongoClient = MongoClientMyself(host="172.10.3.219", port=20000, db="xiaociwei", user="xiaociweiRWUser", password="zywaXIAOCIWEI@!!!")
    for item in __mongoClient.db['gov_app_new_zhejiang'].find():
        item.pop('html')
        item['_id'] = str(item.get('_id'))
        item['missionCreateTime'] = time.mktime(item['missionCreateTime'].timetuple())
        redisLPush( 4 ,'data_clear', json.dumps(item))
        print(item['_id'] + " redis save success!")
