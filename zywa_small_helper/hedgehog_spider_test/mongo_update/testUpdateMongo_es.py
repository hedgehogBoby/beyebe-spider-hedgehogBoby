

from zywa_database_core.dao.mongo.mongoClientMyself import MongoClientMyself

if __name__ == '__main__':
    __mongoClient = MongoClientMyself(host="172.10.3.219", port=20000, db="xiaociwei", user="xiaociweiRWUser", password="zywaXIAOCIWEI@!!!")
    items = __mongoClient.selectAll(tableName='train_hotword')
    for item in items:
        isIncludeNum = False
        for i in item['info']:
            if 'num' in i:
                isIncludeNum = True
                break
        if not isIncludeNum:
            print('news_type', item['info']['news_type'])
            print("发现需要更新的字段")
            item['info']['num'] = -1
            __mongoClient.update(item, tableName='train_hotword')
