

from zywa_database_core.dao.mongo.mongoClientMyself import MongoClientMyself

if __name__ == '__main__':
    __mongoClient = MongoClientMyself(host="172.10.3.219", port=20000, db="xiaociwei", user="xiaociweiRWUser", password="zywaXIAOCIWEI@!!!")
    items = __mongoClient.selectAll(tableName='train_rank')
    for item in items:
        if item['info'].get('tag') == 'ad':
            print('删除一个广告')
            __mongoClient.remove(item, tableName='train_rank')
