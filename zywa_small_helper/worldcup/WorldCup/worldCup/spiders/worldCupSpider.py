import datetime
import json
from time import sleep

import pymongo
import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from zywa_database_core.dao.redis.redisTest import redisDownloadSaveDb3, redisGet
from zywa_extract_helper.model.missionBean import MissionBean
from zywa_small_helper.worldcup.WorldCup.worldCup.filter.blackFilter import filterContent


class SohuWorldCupSpider(scrapy.Spider):
    name = 'worldCup'
    # urls = ['http://sports.163.com/special/000598SP/worldcup2018_newsdata_index.js']

    urls = ['http://v2.sohu.com/feed-service/server/wcup/feeds?suv=18060517245668F2&size=200&target=2018世界杯&exposed=&type=',
            'http://v2.sohu.com/feed-service/server/wcup/feeds?suv=18060517245668F2&size=200&target=2018世界杯&exposed=&type=',
            'http://v2.sohu.com/feed-service/server/wcup/feeds?suv=18060517245668F2&size=200&target=2018世界杯&exposed=&type=',
            'http://v2.sohu.com/feed-service/server/wcup/feeds?suv=18060517245668F2&size=200&target=2018世界杯&exposed=&type=',
            'http://v2.sohu.com/feed-service/server/wcup/feeds?suv=18060517245668F2&size=200&target=2018世界杯&exposed=&type=',
            'http://v2.sohu.com/feed-service/server/wcup/feeds?suv=18060517245668F2&size=200&target=2018世界杯&exposed=&type=',
            'http://interface.sina.cn/pc_zt_api/pc_zt_press_news_doc.d.json?subjectID=189082&cat=all&size=1000&page=1&channel=sports',
            'http://sports.163.com/special/000598SP/worldcup2018_newsdata_index.js',
            'http://sports.163.com/special/000598SP/worldcup2018_newsdata_index_02.js',
            'http://sports.163.com/special/000598SP/worldcup2018_newsdata_index_03.js',
            'http://sports.163.com/special/000598SP/worldcup2018_newsdata_index_04.js',
            ]
    start_urls = []
    for i in range(99999):
        start_urls.extend(urls)

    # 不让scrapy处理任何异常
    handle_httpstatus_list = []
    for i in range(400, 600):
        handle_httpstatus_list.append(i)

    # 线上环境
    MONGO_CONNECT_INFO = {
        "host": '172.10.3.219',
        "port": 20000,
        "db": 'news_toutiao',
        "user": 'toutiaoRWUser',
        "password": 'zywaTOUTIAO@!!!',
    }
    # 测试环境
    # MONGO_CONNECT_INFO = {
    #     "host": '172.10.4.106',
    #     "port": 32001,
    #     "db": 'tcpg',
    #     "user": 'paigu',
    #     "password": 'its123',
    # }
    DEEP_DOWNLOAD = 6
    FILE_KEY_DOWNLOAD = 'request_common_file'
    TYPE_DOWNLOAD = 7000

    def __init__(self):
        self.new_client = pymongo.MongoClient(self.MONGO_CONNECT_INFO['host'], self.MONGO_CONNECT_INFO['port'])
        self.new_db = self.new_client[self.MONGO_CONNECT_INFO['db']]
        self.new_db.authenticate(self.MONGO_CONNECT_INFO["user"], self.MONGO_CONNECT_INFO["password"])

    def parse(self, response):
        try:
            # 4 搜狐 5 新浪 6 163
            if 'v2.sohu.com' in response.url:
                jsonObject = json.loads(response.text)
                print(jsonObject)
                for dictNow in jsonObject:
                    print(dictNow)
                    dictNow['name'] = self.name
                    if '视频' in dictNow['title'] or '高清' in dictNow['title'] or '组图' in dictNow['title']:
                        print('不抓取图片视频,跳过')
                        continue

                    # request = Request(url='http:' + dictNow['url'] + '?timer=123', callback=self.parseSohu, priority=2)
                    request = Request(url='http:' + dictNow['url'], callback=self.parseSohu, priority=2)
                    request.msgDict = dictNow
                    yield request
            if 'interface.sina.cn' in response.url:
                # http://interface.sina.cn/pc_zt_api/pc_zt_press_news_doc.d.json?subjectID=189082&cat=all&size=1000&page=1&channel=sports
                str = response.text
                jsonObject = json.loads(str)
                print(jsonObject)
                for dictNow in jsonObject['result']['data']:
                    print(dictNow)
                    request = Request(url=dictNow['url'], callback=self.parseSina, priority=3)
                    request.msgDict = dictNow
                    yield request

            if '163' in response.url:
                content = response.text
                content = content.replace('data_callback(', '')
                content = content[0:len(content) - 1]
                jsonObject = json.loads(content)
                print(jsonObject)
                for dictNow in jsonObject:
                    print(dictNow)
                    dictNow['name'] = self.name
                    request = Request(url=dictNow['docurl'], callback=self.parse163, priority=3)
                    request.msgDict = dictNow
                    yield request
        finally:
            yield Request(url=response.url, dont_filter=True, priority=1)

    def parseSohu(self, response):
        bs4 = self.__getSoup(response)
        [s.extract() for s in bs4('a[id=\"backsohucom\"]')]
        bs4Content = bs4.select_one('article[class=\"article\"]')
        title = bs4.select_one('meta[property=\"og:title\"]')['content']
        content = bs4Content.prettify()
        content = filterContent(content)
        msgDict = response.request.msgDict
        dictInsert = {}
        dictInsert['url'] = response.url
        dictInsert['newsId'] = str(msgDict['id'])
        dictInsert['titleInfo'] = title
        dictInsert['fromType'] = 4
        dictInsert['fromChannel'] = '世界杯'
        dictInsert['content'] = content
        dictInsert['createTime'] = datetime.datetime.now()
        dictInsert['publishDate'] = datetime.datetime.fromtimestamp(int(msgDict['publishTime']) / 1000)

        imageTags = bs4Content.select('img')
        lstImage = []
        for tag in imageTags:
            lstImage.append(tag['src'])

        self.__waitforImgs(lstImage, dictInsert['newsId'])
        dictInsert['images'] = json.dumps(lstImage)
        dictInsert['thumbnail'] = msgDict["images"]
        self.new_db['d_news_toutiao'].save(dictInsert)
        print(msgDict)
        sleep(2)

    def parseSina(self, response):
        bs4 = self.__getSoup(response)
        [s.extract() for s in bs4('a')]
        bs4Content = bs4.select_one('div[id=\"artibody\"]')
        content = bs4Content.prettify()
        content = filterContent(content)
        msgDict = response.request.msgDict
        dictInsert = {}
        dictInsert['url'] = response.url
        dictInsert['newsId'] = str(msgDict['id'])
        dictInsert['titleInfo'] = msgDict['title']
        dictInsert['fromType'] = 5
        dictInsert['fromChannel'] = '世界杯'
        dictInsert['content'] = content
        dictInsert['createTime'] = datetime.datetime.now()
        dictInsert['publishDate'] = datetime.datetime.fromtimestamp(int(msgDict['createtime']))
        imageTags = bs4Content.select('img')
        lstImage = []
        for tag in imageTags:
            lstImage.append(tag['src'])  # 回调图片
        # 下载图片,入表，可能的话还会对图片url做清洗
        self.__waitforImgs(lstImage, dictInsert['newsId'])
        dictInsert['images'] = json.dumps(lstImage)
        dictInsert['thumbnail'] = msgDict["img"]
        self.new_db['d_news_toutiao'].save(dictInsert)
        print(msgDict)
        sleep(2)

    def parse163(self, response):
        bs4 = self.__getSoup(response)
        bs4Content = bs4.select_one('div[class=\"post_text\"]')
        content = bs4Content.prettify()
        content = filterContent(content)
        msgDict = response.request.msgDict
        dictInsert = {}
        dictInsert['url'] = response.url
        pp = response.url.split('/')
        dictInsert['newsId'] = pp[len(pp) - 1].replace('.html', '')
        dictInsert['titleInfo'] = str(bs4.select_one('h1').text)
        dictInsert['fromType'] = 6
        dictInsert['fromChannel'] = '世界杯'
        dictInsert['content'] = content
        dictInsert['createTime'] = datetime.datetime.now()
        import time
        timeArray = time.strptime(msgDict['time'], "%m/%d/%Y %H:%M:%S")
        dictInsert['publishDate'] = datetime.datetime.fromtimestamp(int(time.mktime(timeArray)))
        imageTags = bs4Content.select('img')
        lstImage = []
        for tag in imageTags:
            lstImage.append(tag['src'])  # 回调图片
        # 下载图片,入表，可能的话还会对图片url做清洗
        self.__waitforImgs(lstImage, dictInsert['newsId'])
        dictInsert['images'] = json.dumps(lstImage)
        dictInsert['thumbnail'] = msgDict["imgurl"]

        self.new_db['d_news_toutiao'].save(dictInsert)
        print(msgDict)
        sleep(2)

    def __getSoup(self, response):
        bs4 = BeautifulSoup(response.text, 'html.parser')
        [s.extract() for s in bs4('iframe')]
        [s.extract() for s in bs4('script')]
        [s.extract() for s in bs4.select('div[class=\"ep-source cDGray\"]')]

        return bs4

    def __waitforImgs(self, urlImgList, newsId):
        """
        对一组图片进行下载，只要有一个失败，就报异常
        :param urlImgList:
        :param newsId:
        :return:
        """
        urlImgListAfterFilter = []
        for img in urlImgList:
            if img[0:2] == '//':
                img = 'http:' + img
            urlImgListAfterFilter.append(img)
            missionBean = MissionBean(img, 7000, [])
            missionBean.isFileTag = True
            missionBean.downloadCallback = 'set'
            redisDownloadSaveDb3(str(self.DEEP_DOWNLOAD) + '_' + self.FILE_KEY_DOWNLOAD, missionBean.getRedisDict())
        for url in urlImgListAfterFilter:
            timeStart = datetime.datetime.now().timestamp()
            while True:
                # 下载超时30秒
                if datetime.datetime.now().timestamp() - timeStart > 30:
                    raise Exception('图片下载超时')

                msgStr = redisGet(3, self.FILE_KEY_DOWNLOAD + '_callback_' + str(self.TYPE_DOWNLOAD) + ':' + url)
                if msgStr is None:
                    sleep(1)
                    continue
                else:
                    dictMsg = json.loads(msgStr)
                    print('图片下载成功,正在存储')
                    dictInsert = {}
                    fileUrl = dictMsg['fileUrl']
                    fileSome = fileUrl.split('/')
                    urlSome = img.split('/')
                    lstTag = ['.jpg', '.jpeg', '.gif', '.bmp', '.png']
                    for tag in lstTag:
                        if tag in fileUrl:
                            dictInsert['fileUrl'] = 'testFileName' + tag
                            break
                        dictInsert['fileUrl'] = 'testFileName.jpg'
                    dictInsert['Uploaded size'] = dictMsg['info']['file']['size']
                    dictInsert['Storage IP'] = fileSome[2]
                    dictInsert['Remote file_id'] = fileUrl.split(fileSome[2] + '/')[1]
                    dictInsert['imgUrl'] = dictMsg['url']
                    dictInsert['imgName'] = urlSome[len(urlSome) - 1]
                    dictInsert['Group name'] = fileSome[3]
                    dictInsert['articleId'] = newsId
                    self.new_db['d_news_images'].save(dictInsert)
                    break
