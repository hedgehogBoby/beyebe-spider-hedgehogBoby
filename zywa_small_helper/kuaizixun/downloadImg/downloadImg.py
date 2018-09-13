import json
import requests
import redis
import config
from fdfs_client.client import *
from mongoClient import CangMongoClient
from multiprocessing import Pool, Process


class DownloadImg(object):
    def __init__(self):
        pool = redis.ConnectionPool(host=config.redis_host, port=config.redis_port, db=config.redis_db)
        self.r = redis.Redis(connection_pool=pool)
        client = CangMongoClient(
            host=config.mongoDB_host,
            port=config.mongoDB_port,
            db=config.mongoDB_dbName,
            user=config.mongoDB_user,
            password=config.mongoDB_password)
        self.db = client.new_db

    def start(self):
        """
        当 redis 队列不为空时一直调用， 队列为空时等待
        """
        while True:
            redis_len = self.r.llen(config.redis_name)
            if redis_len > 0:
                self.get_redis()
            else:
                print("redis无任务，正在等待……")

    @staticmethod
    def parse_file_size(size):
        if 'KB' in size:
            s = size.split("KB")[0]
            s = float(s)
            s = s * 1024
            return int(s)
        if 'MB' in size:
            s = size.split("MB")[0]
            s = float(s)
            s = s * 1024 * 1024
            return int(s)

    def get_redis(self):
        item = self.r.lpop(config.redis_name)
        item = json.loads(item)
        img_urls = item.get("imgUrls")
        img_list = []
        for url in img_urls:
            res_upload = self.download_img(url, item)
            item['etc']['fileSystemInfo'] = res_upload
            file_size = res_upload["Uploaded size"]
            size = self.parse_file_size(file_size)
            file_urls = {
                'imgName': url.split(".")[-1],
                "imgUrl": url,
                "fileUrl": "http://172.10.3.161/{}".format(res_upload["Remote file_id"].decode('utf-8')),
                "fileSize": size,
            }
            print("file_urls", file_urls)
            img_list.append(file_urls)
        item["imgFileUrls"] = {
            "num": len(img_list),
            "imgList": img_list,
        }

        # 存库
        self.db[config.mongoDB_tableName].insert(item)

    def download_img(self, url, item):
        s = requests.Session()
        print("正在下载..", url)
        r = s.get(url)
        while r.status_code != 200:
            r = s.get(url)
        res_upload = self.storage_to_system(r.content, item)
        return res_upload

    def storage_to_system(self, content, item):
        print("正在存储进文件系统")
        tracker = get_tracker_conf(conf_path='client.conf')
        client = Fdfs_client(tracker)
        try:
            res_upload = client.upload_by_buffer(content)  # 流上传
            if res_upload["Status"] == 'Upload successed.':
                print("存储成功", res_upload)
                return res_upload
            else:
                print("我不知道文件系统还会返回什么，反正不是成功标识", res_upload)
                # 把数据放回去
                print("正在把数据放回redis,")
                try:
                    self.r.lpush(item)
                except Exception as err:
                    print("插回redis失败", err)
        except Exception as err:
            print("存储文件系统遇到未知问题", err)
            # 把数据放回去
            print("正在把数据放回redis,")
            try:
                self.r.lpush(item)
            except Exception as err:
                print("插回redis失败", err)

    def test(self):
        print("test")


def test():
    print("test")


if __name__ == '__main__':
    d = DownloadImg()
    # for i in range(4):
    # p = Process(name="test", target=d.get_redis(), args=())
    # p.start()
    #

    ps = Pool(5)
    for i in range(10):
        # ps.apply(worker,args=(i,))          # 同步执行
        ps.apply_async(d.start(), args=())  # 异步执行
        # ps.apply_async(d.test(), args=())

    # 关闭进程池，停止接受其它进程
    ps.close()
    # 阻塞进程
    ps.join()
    print("主进程终止")

    # pool = redis.ConnectionPool(host=config.redis_host, port=config.redis_port, db=config.redis_db)
    # r = redis.Redis(connection_pool=pool)
    # print(r.keys())
    # print(len(r.keys()))
    # print(r.type(config.redis_name))
    # print(r.lpop(config.redis_name))
