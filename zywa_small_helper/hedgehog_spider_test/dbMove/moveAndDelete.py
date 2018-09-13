from zywa_database_core.dao.mongo.mongoClientMyself import getMongoMainClient

client = getMongoMainClient()
i = 0
for item in client.selectAll(tableName='r_toutiao_clear'):
    i = i + 1
    print(i)
    # print(item)
    if 'tags' in item:
        print("存在tags，保留")
        continue
    else:
        print("不存在tags，删除")
        print(client.remove(item, tableName='r_toutiao_clear'))
        continue
