import threading
import traceback
from queue import Queue

from zywa_database_core.dao.mongo.mongoClientMyself import getMongoMainClient
from zywa_extract_helper.helper.downloadUtil.imgDownloadUtil import downloadImg

queue = Queue(10)


def deal():
    global queue
    while True:
        item = queue.get()
        try:
            imgUrl = item['info']['pic']
            images = downloadImg([imgUrl])
            item['info']['images'] = images
            client.update(item, tableName=tableName)
            print(item['info']['title'], ' finish')
        except:
            traceback.print_exc()


if __name__ == '__main__':

    # 从数据库中读取任务后,补充image标签进入数据
    client = getMongoMainClient()
    tableName = 'v_bilibili_movie_iqiyi'
    items = client.selectAll(tableName=tableName)
    for i in range(5):
        threading.Thread(target=deal, ).start()

    for i, item in enumerate(items):
        print(i, ':', item['info']['title'], str(item['_id']))
        queue.put(item)
