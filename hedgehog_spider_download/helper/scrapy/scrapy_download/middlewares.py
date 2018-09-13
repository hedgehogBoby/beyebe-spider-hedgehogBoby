# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import ssl
import traceback
import time
from scrapy import signals, Request
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import Response
from zywa_database_core.dao.redis.redisTest import redisGetBiggetDeepKey, redisRPop, redisConut, redisErrorSend
from zywa_extract_helper.model.missionBean import MissionBean
from zywa_ippool_util.helper.iPPoolHelper import getRandomOneIP
import json
import random
from scrapy.http import HtmlResponse


class ScrapyDwonloadSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyDwonloadDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpiderMyselfMiddleware(object):

    def __getMissionBeanFromRedis(self, requestKeys):
        random.shuffle(requestKeys)  # 随机乱序
        for redisKey in requestKeys:
            keyNow = redisGetBiggetDeepKey(3, redisKey)
            if keyNow is None:
                print(redisKey + '_redis 无任务(不存在任何key)')
                time.sleep(1)
                return None

            strMissionBean = json.loads(redisRPop(3, keyNow))
            # 下载队列为空
            if strMissionBean is None:
                print(redisKey + '_redis 无任务(key中不存在missionBean)')
                return None

            missionBean = MissionBean("", 0, [])
            missionBean.__dict__ = strMissionBean
            missionBean.downloadMethod = redisKey
            return missionBean

    def process_request(self, request, spider):
        requestKeys = []
        if spider.method == 'request':
            # requestKeys = ['request_outside']  # TEST
            requestKeys = ['request_common', 'request_ippool', 'request_outside']
        if spider.method == 'webdriver':
            requestKeys = ['webdriver_common', 'webdriver_ippool']
        # 获取missionBean,并按照redis打上标签
        missionBean = self.__getMissionBeanFromRedis(requestKeys)
        if missionBean is None:
            return Response('http://www.noMission__test.com', status=404)
        url = missionBean.url
        print("成功消费任务:" + missionBean.url)
        # 设置IP
        if 'ippool' in missionBean.downloadMethod:
            ipDict = getRandomOneIP()
            request.meta["proxy"] = 'http://' + ipDict['ip'] + ':' + ipDict['port']
        if 'outside' in missionBean.downloadMethod:
            request.meta["proxy"] = 'http://198.15.135.26:8090'

        if 'webdriver' in missionBean.downloadMethod:
            missionBean.downloadMethod = 'webdriver'

        request.__dict__['missionBean'] = missionBean
        request.priority = missionBean.deep
        request._set_url(url)
        request.dont_filter = True
        redisConut(missionBean.type, 'total')
        return None

    def process_exception(self, request, exception, spider):
        errMsg = traceback.format_exc()
        print("parse ERROR:" + errMsg)
        missionBean = request.missionBean
        redisErrorSend(missionBean.type, errMsg)
        url = 'http://www.a3__test.com?id=' + str(int(time.time()))
        return Request(url=url, dont_filter=True)


class MyUserAgentMiddleware(UserAgentMiddleware):
    """
    设置User-Agent
    """

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        if request.missionBean.headers is None:
            agent = random.choice(self.user_agent)
            request.headers['User-Agent'] = agent
        else:
            agent = random.choice(self.user_agent)
            request.headers['User-Agent'] = request.missionBean.headers.get('User-Agent', agent)


class PhantomJSMiddleware(object):
    count = 0
    driver = None

    @classmethod
    def process_request(cls, request, spider):
        ssl._create_default_https_context = ssl._create_unverified_context
        if spider.method == 'webdriver':
            try:
                if 'actionBeanList' in spider.__dict__:
                    actionBeanList = spider.actionBeanList
                else:
                    actionBeanList = request.missionBean.actionBeanList
                content = webDriverPhantomJSGet(request.missionBean.url, action=actionBeanList)
                return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

            except:
                errMsg = traceback.format_exc()
                print("parse PhantomJS ERROR:" + errMsg)
                missionBean = request.missionBean
                redisErrorSend(missionBean.type, errMsg)
                url = 'http://www.a3__test.com?id=' + str(int(time.time()))
                return Response(url, status=404)

        else:
            return None

    @classmethod
    def __doAction(cls, driver, actionBeanList):
        # action具有很大的不稳定性,但是是很重要的操作,请自行处理异常

        for actionNow in actionBeanList:
            if not type(actionNow) == type({}):
                actionNow = actionNow.__dict__
            tStart = int(time.time())
            # actionNow转对象
            print(actionNow)
            if actionNow['name'] == 'waitfor':
                print('[INFO]执行waitfor操作')
                while True:
                    if int(time.time()) - tStart > actionNow['timeout']:
                        print('[WARNING]执行waitfor操作超时')
                        break
                    if actionNow['msg'] in driver.page_source:
                        break
                time.sleep(0.01)
            if actionNow['name'] == 'delay':
                print('[INFO]执行delay操作')
                time.sleep(actionNow['timeout'])
            if actionNow['name'] == 'pushdown':
                print('[INFO]执行pushdown操作')
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(0.1)
            if actionNow['name'] == 'js':
                driver.execute_script(actionNow['msg'])
                time.sleep(actionNow['timeout'])

    def process_exception(self, request, exception, spider):
        errMsg = str(exception)
        print("PhantomJS ERROR:" + errMsg)

        missionBean = request.missionBean
        redisErrorSend(missionBean.type, errMsg + '\nurl: ' + missionBean.url)

        url = 'http://www.a3__test.com?id=' + str(int(time.time()))
        return Request(url=url, dont_filter=True)
