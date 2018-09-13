import re
import traceback
from bs4 import BeautifulSoup
from scrapy.conf import settings

from zywa_database_core.dao.mongo.mongoClientMyself import getMongoMyselfClient
import time
from scrapy.http import Request
from scrapy.spiders import Spider


class FishingSpider(Spider):
    # mongodb
    client = getMongoMyselfClient()
    # 不让scrapy处理任何异常
    handle_httpstatus_list = []
    for i in range(400, 600):
        handle_httpstatus_list.append(i)
    name = 'ydzx'
    # allowed_domains = ['pearvideo']
    baseUrl = 'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=hot&cstart=220&cend=230&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1529563944929'
    start_urls = []
    cookie = settings['COOKIE']
    for i in range(100):
        start_urls.append(baseUrl.replace('{startNum}', str((i + 1) * 9)))

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, cookies=self.cookie)

    def parse(self, response):

        try:
            print(response.text)
            bs4 = BeautifulSoup(response.text, 'html.parser')

            for li in bs4.select('li'):
                info = {}
                # 发布新任务
                request = Request(url=info['url'], callback=self.parse_item, priority=3)
                request.info = info
                yield request
        except:
            traceback.print_exc()
        finally:
            print("正在添加新任务至队列头部")
            request = Request(url=response.url, dont_filter=True)
            yield request
            self.sleepMyself()

    def parse_item(self, response):
        pass

    def get_addr(self, html):
        addr_regex = re.compile(r'''((http://|https://).*?(\.avi|\.wmv|\.mpeg|\.mp4|\.mov|\.mkv|\.flv|\.f4v|\.m4v|\.rmvb|\.rm|\.3gp|\.dat|\.ts|\.mts|\.vob))''', re.VERBOSE)  # 匹配网址，
        matchs = []
        for groups in addr_regex.findall(html):
            matchs.append(groups[0])
        if len(matchs) == 0:
            print('没有网址')
        return matchs

    def sleepMyself(self):
        print('休息一分钟')
        time.sleep(60)
