import traceback

from zywa_database_core.dao.mongo.mongoClientMyself import MongoClientMyself

__mongoClient = MongoClientMyself(host="172.10.3.219", port=20000, db="xiaociwei", user="xiaociweiRWUser", password="zywaXIAOCIWEI@!!!")
for item in __mongoClient.select(tableName='government'):
    try:
        print("work,encode:" + item['respEncoding'])
        # print(item)
        h5old = item['html']
        h5mid = item['html'].encode(item['respEncoding'])
        h5 = item['html'].encode(item['respEncoding']).decode('utf-8')
        # h5 = gzip.decompress(h5).decode(item['respEncoding'])
    except Exception as err:
        traceback.print_exc()
        # html = h5.decode('utf8')
    print('h5.old', h5old)
    print('h5.decode', h5)
    print('-------')
