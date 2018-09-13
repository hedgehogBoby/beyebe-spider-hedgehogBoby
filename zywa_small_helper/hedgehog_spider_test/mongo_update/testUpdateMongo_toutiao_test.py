import traceback
from datetime import datetime

import pymongo

if __name__ == '__main__':
    MONGO_CONNECT_INFO = {
        "host": '172.10.4.106',
        "port": 32001,
        "db": 'tcpg',
        "user": 'paigu',
        "password": 'its123',
    }
    new_client = pymongo.MongoClient(MONGO_CONNECT_INFO['host'], MONGO_CONNECT_INFO['port'])
    new_db = new_client[MONGO_CONNECT_INFO['db']]
    new_db.authenticate(MONGO_CONNECT_INFO["user"], MONGO_CONNECT_INFO["password"])

    # mongodbIp = 172.10.3.219
    # mongodbPort = 20000
    # mongodbDatabase = news_toutiao
    # mongodbUserName = toutiaoRWUser
    # mongodbPassWord = zywaTOUTIAO @!!!

    MONGO_CONNECT_INFO2 = {
        "host": '172.10.3.219',
        "port": 20000,
        "db": 'news_toutiao',
        "user": 'toutiaoRWUser',
        "password": 'zywaTOUTIAO@!!!',
    }
    new_client2 = pymongo.MongoClient(MONGO_CONNECT_INFO2['host'], MONGO_CONNECT_INFO2['port'])
    new_db2 = new_client2[MONGO_CONNECT_INFO2['db']]
    new_db2.authenticate(MONGO_CONNECT_INFO2["user"], MONGO_CONNECT_INFO2["password"])

    i = 0
    items = new_db['d_news_toutiao'].find()
    for item in items:
        # 存储到线上服务器
        try:
            datetimeNow = datetime.fromtimestamp(1528711200)
            item.pop('_id')
            item['createTime'] = datetimeNow
            new_db2['d_news_toutiao'].insert(item)
            i = i + 1
            print('新闻插入成功!', i)
        except:
            traceback.print_exc()

    # i = 0
    # items = new_db['d_news_images'].find()
    # for item in items:
    #     # 存储到线上服务器
    #     try:
    #         item.pop('_id')
    #         new_db2['d_news_images'].insert(item)
    #         i = i + 1
    #         print('图片插入成功!', i, ' 总共:', len(items))
    #     except:
    #         traceback.print_exc()

    # lstTag = ['.jpg', '.jpeg', '.gif', '.bmp', '.png']
    #                   for tag in lstTag:
    #                       if tag in fileUrl:
    #                           dictInsert['fileUrl'] = 'testFileName' + tag
    #                           break
    #                       dictInsert['fileUrl'] = 'testFileName.jpg'

    # i = 0
    # items = new_db['d_news_images'].find()
    # for item in items:
    #     # 存储到线上服务器
    #     fileName = item['imgName']
    #
    #     try:
    #         new_db2['d_news_images'].update({'_id', item['_id']}, item)
    #         i = i + 1
    #         print('图片更新成功!', i, ' 总共:', len(items))
    #     except:
    #         traceback.print_exc()
