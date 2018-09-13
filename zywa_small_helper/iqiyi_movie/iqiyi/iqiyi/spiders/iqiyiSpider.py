import datetime
import json
import re
import traceback

import requests
from bs4 import BeautifulSoup
from scrapy import Spider, Request
from scrapy.http import Response

from zywa_database_core.bean.newsBeanKafka import NewsBeanKafka
from zywa_database_core.dao.kafka.kafkaClient import producerVideo
from zywa_database_core.dao.mongo.mongoClientMyself import getMongoMainClient
from zywa_extract_helper.filter.daoFilterAndSave import MongoFilterSave
from zywa_extract_helper.helper.downloadUtil.imgDownloadUtil import downloadImg
from zywa_extract_helper.model.missionBean import MissionBean
from zywa_small_helper.iqiyi_movie.iqiyi.iqiyi.model.videoBean import VideoBean


class IqiyiSpider(Spider):
    name = 'iqiyi'
    URL_START = 'http://list.iqiyi.com/www/1/-------------4-1-1-iqiyi--.html'
    URL_START2 = 'http://www.iqiyi.com/lib/dianying/,,_11_1.html'
    num_total_movie = 0
    num_total_page = 0

    def start_requests(self):

        request = Request(url=self.URL_START, callback=self.parseReady, dont_filter=True)
        request.page = 1
        yield request
        request = Request(url=self.URL_START2, callback=self.parseReady, dont_filter=True)
        request.page = 1
        yield request

    # 处理频道页与渠道分发
    def parseReady(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.select('a'):
            try:
                # 分发渠道1标签
                if 'www/1/' in a['href'] and '1-1-iqiyi--.html' in a['href']:
                    URL_BASE = 'http://list.iqiyi.com'
                    urlNow = URL_BASE + a['href']
                    URL_BASE = urlNow.replace('1-1-iqiyi--.html', '{page}-1-iqiyi--.html')
                    request = Request(url=urlNow, callback=self.parsePage, dont_filter=True)
                    request.page = 1
                    request.URL_BASE = URL_BASE
                    yield request
                # 分发渠道2标签
                if 'lib/dianying/' in a['href'] and '_11_1.html' in a['href']:
                    URL_BASE = 'http://www.iqiyi.com/'
                    urlNow = URL_BASE + a['href']
                    URL_BASE = urlNow.replace('_11_1.html', '_11_{page}.html')
                    request = Request(url=urlNow, callback=self.parsePage, dont_filter=True)
                    request.page = 1
                    request.URL_BASE = URL_BASE
                    yield request
            except:
                pass

    # 处理翻页以及菜单
    def parsePage(self, response):
        print("当前页数:" + str(response.request.page))
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            for li in soup.select_one("div[class=\"wrapper-piclist\"]").select('li'):
                # print(li.prettify())

                videoBean = VideoBean()
                # 分数不一定有
                try:
                    scoreTag = li.select_one('span[class=\"score\"]')
                    scoreStr = scoreTag.text
                    videoBean.score = float(scoreStr)
                except:
                    videoBean.score = -1
                videoBean.url = li.select_one('a')['href']
                videoBean.imgMenuUrl = 'http:' + li.select_one('img')['src']
                videoBean.title = li.select_one('a')['title']
                # 检验数据库中是否存在该影片
                testItems = getMongoMainClient().find_one({'title': videoBean.title}, tableName='v_iqiyi_movie')
                if testItems is not None:
                    print("已经完成过下载,跳过任务")
                    continue
                # 跳转中间页
                if '/lib/m_' in videoBean.url:
                    request = Request(url=videoBean.url, callback=self.parseMiddleMovie, priority=4, dont_filter=True)
                    request.info = videoBean
                    yield request
                # 电影落地页
                if 'com/v_' in videoBean.url:
                    request = Request(url=videoBean.url, callback=self.parseMovie, priority=9, dont_filter=True)
                    request.info = videoBean
                    yield request
        finally:
            page = response.request.page + 1
            if page < 100:
                request = Request(url=response.request.URL_BASE.replace('{page}', str(page)), callback=self.parsePage, dont_filter=True)
                request.page = page
                yield request
            else:
                page = 1
                request = Request(url=response.request.URL_BASE.replace('{page}', str(page)), dont_filter=True)
                request.page = page
                yield request

    # 处理视频跳转中间页
    def parseMiddleMovie(self, response):
        # 只需要修改url即可
        info = response.request.info
        # response = Response().css()[0]
        url = response.css('a[id=\"j-album-play\"]::attr("href")').extract_first()
        request = Request(url=url, callback=self.parseMovie, priority=9)
        request.info = info
        self.num_total_movie = self.num_total_movie + 1
        print("潜在的落地页数量:" + str(self.num_total_movie))
        yield request

    # 处理落地页
    def parseMovie(self, response, **kwargs):
        if kwargs.get('html') is None:
            html = response.text
        else:
            html = kwargs.get('html')
        soup = BeautifulSoup(html, "html.parser")
        msgStr = re.search(":page-info='(.*?)'", html).group(1)
        msgStr2 = re.search(":video-info='(.*?)'", html).group(1)
        pageInfoDict = json.loads(msgStr)
        videoInfoDict = json.loads(msgStr2)
        videoBean = VideoBean()
        videoBean.title = pageInfoDict['albumName']
        # 检查数据库中是否存在 TODO
        item = getMongoMainClient().getClient(tableName='v_iqiyi_movie').find_one({'title': videoBean.title})

        if item is not None:
            print("库中已存在,跳过！", videoBean.title)
            return
        # 影片信息
        videoBean.videoId = re.compile('/(v_.*?).html').search(soup.select_one("meta[property=\"og:url\"]")['content']).group(1)
        videoBean.description = videoInfoDict['description']
        videoBean.areas = videoInfoDict['areas']
        videoBean.language = soup.select_one("meta[itemprop=\"inLanguage\"]")['content']
        videoBean.url = pageInfoDict['pageUrl']
        videoBean.runtime = videoInfoDict.get('duration', -1)
        # 主演\导演\编剧
        videoBean.writers = videoInfoDict['cast'].get('writers', [])
        videoBean.directors = videoInfoDict['cast'].get('directors', [])
        videoBean.mainActors = videoInfoDict['cast'].get('mainActors', [])

        # 分类标签
        videoBean.category = pageInfoDict['categoryName']
        videoBean.keywords = videoInfoDict['categories']
        videoBean.tags = pageInfoDict['categories'].split(',')
        # 时间信息
        videoBean.uploadDate = datetime.datetime.strptime(soup.select_one("meta[itemprop=\"uploadDate\"]")['content'], "%Y-%m-%d")
        videoBean.publishDate = datetime.datetime.strptime(soup.select_one("meta[itemprop=\"datePublished\"]")['content'], "%Y-%m-%d")
        # 其他
        videoBean.isVip = videoInfoDict['vip']
        videoBean.etc = pageInfoDict
        videoBean.etc2 = videoInfoDict
        # tid和vid
        tMsg = {}
        # 方法1
        try:
            tMsg['tid'] = soup.select_one('div[data-player-tvid]')['data-player-tvid']
            tMsg['vid'] = soup.select_one('div[data-player-videoid]')['data-player-videoid']
        except:
            # 方法2
            print("方法1无法获得tid和vid")
            # param['tvid'] = "96922900";
            # param['vid'] = "e250b51f481e48439159d437e94398ca";
            tMsg['tid'] = re.search("param..tvid.*?\"(.*?)\"", html).group(1)
            tMsg['vid'] = re.search("param..vid.*?\"(.*?)\"", html).group(1)
        videoBean.technologyMsg = tMsg
        # 获取图片
        print('抓取图片')
        imgUrlBase = soup.select_one("meta[property=\"og:image\"]")['content'].replace('.jpg', '{size}.jpg').replace('.jpeg', '{size}.jpeg').replace('.gif', '{size}.gif').replace('.webp', '{size}.webp')
        imgList = ['_180_236', '_440_608', '_480_270', '_260_360', '_180_236', '_1080_608']
        imgUrlList = []
        imgDict = {}
        for imgSize in imgList:
            url = imgUrlBase.replace('{size}', imgSize)
            imgUrlList.append(url)
        imgDownloadList = downloadImg(imgUrlList)
        for imgDownload in imgDownloadList:
            for imgStr in imgList:
                if imgStr in imgDownload['url']:
                    imgDict[imgStr] = imgDownload
                    break
        videoBean.imgs = imgDict
        # 获取图片完成
        missionBean = MissionBean(videoBean.url, 2001, ['v_iqiyi_movie'])
        missionBean.html = html
        missionBean.title = videoBean.title
        missionBean.info = videoBean.__dict__
        MongoFilterSave(missionBean)
        print("入库成功:", missionBean.title)
        producerVideo(self.getNewsBean(missionBean.info))
        print("入Kafka成功:", missionBean.title)

    def getNewsBean(self, info):
        print("测试:示范如何组装一个Video结果(方便你偷懒复制使用)")
        print("范例2:BiliBili影片《不愧是票房冠军!这个视频告诉你《捉妖记2》到底值不值得看!》")
        newsBean = NewsBeanKafka()
        # 时间相关
        import time
        newsBean.createTime = int(time.time())  # [必填秒级时间戳]抓取时间
        """
        从指定字符串格式转化为秒级时间戳
        """
        newsBean.publishDate = int(info['publishDate'])
        # 新闻内容
        newsBean.title = info['title']
        newsBean.newsId = info['videoId']
        newsBean.video = []
        # 没有缩略图不需要存储
        newsBean.thumbnails = info['imgs']
        newsBean.authorId = '爱奇艺'  # [字符串]媒体/作者唯一ID(若抓取源无该id则用作者名填充)
        newsBean.authorNickname = '爱奇艺'  # [字符串]作者名
        # 抓取新闻特征
        newsBean.url = "http://www.bilibili.com/video/av20131777"  # [必填字符串]抓取页地址
        newsBean.channel = info['category']  # [字符串]频道标签/一级标签(只允许有一个)
        newsBean.tags = info['tags']  # [字符串List]属性标签/二级标签
        # 补充新闻特征
        newsBean.mediaType = 1  # [必填整形int]新闻填写0,视频填写1
        newsBean.fromType = 11  # [必填整形int]代表抓取渠道(头条:0,前10都已使用2018/7/11,联系管理员领取)
        # 其他
        newsBean.etc = info  # [字典/Map]其他记录,其中log这个key保留记录错误信息,其他随意使用
        return newsBean


if __name__ == '__main__':
    clientNew = getMongoMainClient().getClient(tableName='v_iqiyi_movie')
    items = getMongoMainClient().getClient(tableName='v_iqiyi_movie').find()
    for i, item in enumerate(items):
        print('当前任务数:', i)
        try:
            itemTest = clientNew.find_one({'title': item['title']})
            if itemTest is not None:
                print("库中已存在,跳过！", item['title'])
                continue
            else:
                print("不存在,正在处理", item['title'], ' URL: ' + item['url'])
            # 处理该任务，伪造Response。
            url = item['url']
            response = Response(url=url)
            IqiyiSpider().parseMovie(response, html=requests.get(url).text)
        except:
            traceback.print_exc()
