from zywa_database_core.dao.mongo.mongoClientMyself import MongoClientMyself
from zywa_extract_helper.model.missionBean import MissionBean

if __name__ == '__main__':
    __mongoClient = MongoClientMyself(host="172.10.3.219", port=20000, db="xiaociwei", user="xiaociweiRWUser", password="zywaXIAOCIWEI@!!!")
    items = __mongoClient.selectAll(tableName='iqiyi_video')
    i = 0
    for item in items:

        missionBean = MissionBean('', 0, [])
        missionBean.__dict__ = item
        print(i)
        print(missionBean.title)
        redisLPush( 4 ,'data_clear_' + str(missionBean.type), missionBean.getRedisDict())
        i += 1
