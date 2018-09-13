import re
import traceback
from bs4 import BeautifulSoup
from zywa_database_core.dao.mongo.mongoClientMyself import getMongoMyselfClient
import time
from scrapy.http import Request
from scrapy.spiders import Spider

from zywa_extract_helper.model.missionBean import MissionBean


class FishingSpider(Spider):
    # mongodb
    client = getMongoMyselfClient()
    # 不让scrapy处理任何异常
    handle_httpstatus_list = []
    for i in range(400, 600):
        handle_httpstatus_list.append(i)
    name = 'fishing'
    # allowed_domains = ['pearvideo']
    baseUrl = 'http://www.pearvideo.com/search_loading.jsp?start={startNum}&k=钓鱼&sort='
    start_urls = []
    for i in range(100):
        start_urls.append(baseUrl.replace('{startNum}', str((i + 1) * 9)))

    def parse(self, response):

        try:
            bs4 = BeautifulSoup(response.text, 'html.parser')
            for li in bs4.select('li'):
                info = {}
                info['url'] = 'http://www.pearvideo.com/' + li.select_one("a")['href']
                info['thumbnail'] = li.select_one("img")['src']
                info['title'] = li.select_one("h2").text
                info['vdo-time'] = li.select_one("div[class=\"vdo-time\"]").text
                info['publish-time'] = li.select_one("div[class=\"publish-time\"]").text
                info['cont'] = li.select_one("div[class=\"cont\"]").text
                info['i-icon_col-name'] = li.select_one("a[class=\"i-icon col-name\"]").text
                info['i-icon_like-num'] = li.select_one("span[class=\"i-icon like-num\"]").text

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
        info = response.request.info
        html = response.body.decode()
        match = self.get_addr(html)
        if len(match) > 0:
            info['videoUrl'] = match[0]
        else:
            return
        bs4 = BeautifulSoup(response.text, 'html.parser')
        info['img'] = bs4.select_one("div[id=\"poster\"]").select_one('img')['src']
        missionBean = MissionBean(response.url, 3, ['fishing_new'])
        missionBean.html = html
        missionBean.title = info['title']
        missionBean.info = info
        self.client.save(missionBean)

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
        time.sleep(1)
