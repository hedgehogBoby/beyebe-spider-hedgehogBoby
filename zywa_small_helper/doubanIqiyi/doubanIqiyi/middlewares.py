# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging

import redis
from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware


class DoubaniqiyiSpiderMiddleware(object):
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


class DoubaniqiyiDownloaderMiddleware(object):
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


import time
import uuid


def random_up():
    a = str(uuid.uuid1()).replace("-", "").upper()
    b = str(uuid.uuid1()).replace("-", "")
    return a[:8] + b[:8] + a[:8] + b[:8]


def random_cookie():
    uid1 = str(uuid.uuid1()).replace("-", "")  # 3
    uid2 = str(uuid.uuid1()).replace("-", "")  # 2
    uid2 = uid2.upper()
    uid3 = str(uuid.uuid1()).replace("-", "")[:16]  # 0
    # print(uid2)
    now = int(time.time())  # 1
    r = """
    ll="118282"; bid={4}; _pk_id.100001.4cf6={0}.{1}.1.{1}.{1}.; _pk_ses.100001.4cf6=*; __utma=30149280.1471161558.{1}.{1}.{1}.1; __utmb=30149280.0.10.{1}; __utmc=30149280; __utmz=30149280.{1}.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1872923760.{1}.{1}.{1}.1; __utmb=223695111.0.10.{1}; __utmc=223695111; __utmz=223695111.{1}.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=IsRMbZ9APKLegaDZfiR1BZRLnqa2GlDJ; _vwo_uuid_v2={2}|{3}
    """.format(uid3, now, uid2, uid1, random_up()[4:15], random_up())
    return r


# Redis
class RedisProxyCommonMiddleware(HttpProxyMiddleware):
    # 对发起的请求进行预处理
    def process_request(self, request, spider):

        REDIS_CONNECT_INFO = {
            "host": "172.10.3.157",
            "port": 16379,
            "password": "",
            "db": 3,
        }
        self.r = redis.Redis(host=REDIS_CONNECT_INFO['host'], port=REDIS_CONNECT_INFO['port'],
                             db=REDIS_CONNECT_INFO['db'],
                             password=REDIS_CONNECT_INFO['password'])

        self.json_ip = self.r.lpop("ippool_2")
        # self.r.rpush('ippool_2', self.json_ip)
        if self.json_ip:
            self.json_ip = self.json_ip.decode("utf-8")
            self.long_ip = json.loads(self.json_ip)
            self.ip = self.long_ip['ip']
            self.port = self.long_ip['port']
            if 'https' in str(request.url):
                logging.info("-------------------" + "使用https  ip请求:" + self.ip + "----------------------")
                request.meta['proxy'] = "https://" + self.ip + ":" + self.port
                request.meta['Cookie'] = random_cookie()
                logging.info('--------------------切换代理成功--------------------')
            else:
                logging.info("-------------------" + "使用http ip请求:" + self.ip + "----------------------")
                request.meta['proxy'] = "http://" + self.ip + ":" + self.port
                request.meta['Cookie'] = random_cookie()
                logging.info('--------------------切换代理成功--------------------')
        else:
            logging.info("--------------------代理池为空--------------------")
            request.meta['proxy'] = None
        return None

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        logging.info("-------------------" + str(response.status) + "状态" + "--------------------------")
        if response.status != 200:
            logging.info("------------------------已删除失效IP:" + self.ip + "----------------------")
            self.json_ip = self.r.lpop("ippool_2")
            # self.r.rpush('ippool_2', self.json_ip)
            if self.json_ip:
                self.json_ip = self.json_ip.decode("utf-8")
                self.long_ip = json.loads(self.json_ip)
                self.ip = self.long_ip['ip']
                self.port = self.long_ip['port']
                if 'https' in str(request.url):
                    request.meta['Cookie'] = random_cookie()
                    request.meta['proxy'] = "https://" + self.ip + ":" + self.port
                    logging.info("------------------------已重新切换IP:" + self.ip + "----------------------")
                else:
                    request.meta['Cookie'] = random_cookie()
                    request.meta['proxy'] = "http://" + self.ip + ":" + self.port
                    logging.info("------------------------已重新切换IP:" + self.ip + "----------------------")

                return request
            else:
                logging.info("--------------------切换时代理池为空--------------------")
                return response

        else:
            self.r.rpush('ippool_2', self.json_ip)
            return response

    # 对错误的请求进行再处理
    def process_exception(self, request, exception, spider):
        logging.info("------------------------已删除失效IP:" + self.ip + "----------------------")
        self.json_ip = self.r.lpop("ippool_2")
        # self.r.rpush('ippool_2', self.json_ip)
        if self.json_ip:
            self.json_ip = self.json_ip.decode("utf-8")
            self.long_ip = json.loads(self.json_ip)
            self.ip = self.long_ip['ip']
            self.port = self.long_ip['port']
            if 'https' in str(request.url):
                request.meta['Cookie'] = random_cookie()
                request.meta['proxy'] = "https://" + self.ip + ":" + self.port
                logging.info("------------------------已重新切换IP:" + self.ip + "----------------------")
            else:
                request.meta['Cookie'] = random_cookie()
                request.meta['proxy'] = "http://" + self.ip + ":" + self.port
                logging.info("------------------------已重新切换IP:" + self.ip + "----------------------")
            return request
        else:
            logging.info("--------------------切换时代理池为空--------------------")
            time.sleep(2)
            request.meta['Cookie'] = random_cookie()
            request.meta['proxy'] = None
            return request
