import json
import threading
from queue import Queue
from urllib.parse import quote

import pymongo
import requests

i = 0
q = Queue(200)
# client = pymongo.MongoClient("mongodb://172.10.3.157:27017")
# db = client['lichangjian']


def deal(item):
    global i, db
    try:
        i = i + 1
        # if i < 51910:
        #     print('跳过' + str(i))
        #     return None
        urlEncode = quote(item['img'])
        url = 'http://172.10.3.101:4567/utils/qrcode/url.go?url={}'.format(urlEncode)
        session = requests.session()
        try:
            strReq = session.get(url, timeout=20).text
        finally:
            session.close()
        jsonObj = json.loads(strReq)
        print(str(i) + "  " + str(jsonObj))
        if not 'data' in jsonObj or len(jsonObj['data']) == 0:
            print('url:' + item['img'])
            return None
        else:
            print('二维码解析成功,正在入库')
            item['qrDecode'] = jsonObj['data']
            db['gov_img_qrDecode'].insert(item)
    except Exception as err:
        print('ERROR' + str(err))
        print('url:' + item['img'])


def dealForever():
    global i
    while True:
        item = q.get()
        deal(item)


def produceForever():
    global db
    imgTags = db['gov_img_new'].find()
    # imgTags = db['gov_img_new'].find().skip(52910).limit(100)
    for item in imgTags:
        q.put(item)


if __name__ == '__main__':
    threading.Thread(target=produceForever, args=()).start()
    for i in range(30):
        threading.Thread(target=dealForever, args=()).start()
