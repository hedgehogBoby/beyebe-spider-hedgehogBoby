import re
import redis
import threadpool
import demjson
import logging.handlers
import traceback
import urllib.request as request
from pymongo import MongoClient
from fdfs_client.client import *

"""
    资讯图片下载
    1、按日期查询已爬取的资讯内容
    2、解析内容中得图片地址
    3、下载图片并保存
"""


class DownImage:
    p = re.compile(r'//p[0-9a-zA-Z]+.pstatp.com/[a-zA-Z]+/[0-9a-zA-Z \- /]+')
    p1 = re.compile(r'//p[0-9a-zA-Z]+.pstatp.com/[a-zA-Z]+/\d{2,10}/\d{5,10}')
    MONGO_CONNECT_INFO = "mongodb://172.10.3.219:20000/"
    redis_client = redis.Redis("172.10.3.157", 16379)
    failed_url_key = 'toutiao_image_download_failed'
    img_url_list_key = 'toutiao_image_urls'

    # 日志初始化
    logging.config.fileConfig("logger.conf")
    logger = logging.getLogger("example02")

    def __init__(self):
        client = MongoClient(self.MONGO_CONNECT_INFO)
        # self.mongo_db = client.testdb
        self.mongo_db = client.news_toutiao
        self.mongo_db.authenticate("toutiaoRWUser", "zywaTOUTIAO@!!!")

        tracker = get_tracker_conf(conf_path='client.conf')
        self.client = Fdfs_client(tracker)

    def downAndSaveImage(self, url):
        try:
            socket.setdefaulttimeout(5)
            data_spl = str(url).split('?')
            #newsId image_url
            image_url, newsId = data_spl[0], data_spl[1]
            req = request.Request(image_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36')
            res = request.urlopen(req)
            if str(res.status) == '200':
                length = int(res.getheader("Content-Length"))
                if length < 16777216:
                    self.logger.info(url + "=================下载图片成功=====================")
                    print(url + "=================下载图片成功=====================")
                    imageType = res.getheader('Content-Type')
                    suffix = imageType[6:]
                    image_name = image_url.split('/')[-1] + '.' + suffix
                    image_collection = self.mongo_db.d_news_images
                    img_data = res.read()
                    res_upload = self.client.upload_by_buffer(filebuffer=img_data)
                    group_name = res_upload['Group name'].decode("utf-8")
                    remote_file_id = res_upload['Remote file_id'].decode("utf-8")
                    uploaded_size = res_upload['Uploaded size']
                    storage_ip = res_upload['Storage IP'].decode("utf-8")
                    image_dict = {'articleId': newsId, "imgUrl": image_url, "imgName": image_name, "imgType": imageType,
                                  'Group name': group_name, 'Remote file_id': remote_file_id,
                                  'Uploaded size': uploaded_size, 'Storage IP': storage_ip}

                    image_collection.insert(image_dict)

            else:
                self.logger.info(url + "=================下载图片失败=====================")
                faild_url = re.findall(self.p1, url)
                if not faild_url:
                    self.redis_client.sadd(self.failed_url_key, url)
        except Exception as e:
            exstr = traceback.format_exc()
            faild_url = re.findall(self.p1, url)
            if not faild_url:
                self.redis_client.sadd(self.failed_url_key, url)
            exinfo = '下载图片异常:{},url:{}'.format(exstr, url)
            self.logger.error(exinfo)

    def parseImageUrlbyNews(self):
        try:
            befor_date_str = '2017-11-17 00:00:00'
            last_date_str = '2017-11-17 23:59:59'
            news_collection = self.mongo_db.d_news_toutiao
            articleInfos = news_collection.find({"createTime": {"$gte": datetime.strptime(befor_date_str, '%Y-%m-%d %H:%M:%S'), "$lte": datetime.strptime(last_date_str, '%Y-%m-%d %H:%M:%S')}})
            # articleInfos = news_collection.find({"newsId":"6511815209957458440"})
            for articleInfo in articleInfos:
                if "publishDate" in articleInfo.keys():
                    newsId = articleInfo['newsId']
                    article = articleInfo['articleInfo']
                    pgcInfo = articleInfo['pgcInfo']
                    article = str(article).replace('\n', '')
                    urls = []
                    if not pgcInfo:
                        if '\\' in article or '\\\\' in article:
                            article = article.replace('\\', '').replace('\\\\', '')
                        sub_images = re.findall(r'"sub_images":(.+)"max_img_width":', article)
                        if sub_images:
                            imagestr = sub_images[0][:-1]
                            image_list = demjson.decode(imagestr)
                            if image_list:
                                for image in image_list:
                                    urls.append(image['url'])
                    else:
                        urls = re.findall(self.p, article)
                    if urls:
                        for url in urls:
                            if not url.startswith('http://') and not url.startswith("https://"):
                                url = 'https:{}?{}'.format(url, newsId)
                                self.redis_client.lpush("toutiao_history_image_urls", url)

        except Exception as e:
            exstr = traceback.format_exc()
            exinfo = '解析news_image图片url异常:{}'.format(exstr)
            self.logger.logging.error(exinfo)

    def download(self):
        try:
            pool = threadpool.ThreadPool(50)
            while True:
                url_list = []
                for i in range(100):
                    data = self.redis_client.brpop(self.img_url_list_key)
                    url_list.append(data[1].decode("utf-8"))
                requests = threadpool.makeRequests(self.downAndSaveImage, url_list)
                [pool.putRequest(req) for req in requests]
                pool.wait()
        except Exception as e:
            exstr = traceback.format_exc()
            exinfo = '获取news_image图片url异常:{}'.format(exstr)
            self.logger.error(exinfo)

    def main(self, *args):
        # self.download()
        # self.parseImageUrlbyNews()
        if args:
            self.img_url_list_key = args[0]
        self.download()


if __name__ == '__main__':
    down = DownImage()
    arg = sys.argv[1]
    down.main(arg)
