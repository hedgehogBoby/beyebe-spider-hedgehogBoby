import datetime
import json
import re
import traceback
from bs4 import BeautifulSoup

from zywa_database_core.bean.newsBean import NewsBean
from zywa_database_core.dao.mongo.mongoClientMyself import getMongoDownloadClient
import time
from scrapy.http import Request
from scrapy.spiders import Spider

from zywa_extract_helper.filter import daoFilterAndSave
from zywa_extract_helper.model.missionBean import MissionBean


class FishingSpider(Spider):
    # mongodb
    client = getMongoDownloadClient()
    # 不让scrapy处理任何异常
    handle_httpstatus_list = []
    for i in range(400, 600):
        handle_httpstatus_list.append(i)
    name = 'qutoutiao'
    baseUrl = 'http://api.1sapp.com/content/outList?cid=255&tn=1&page={page}&limit=10&user=temporary{timeNow}&show_time=&min_time=&content_type=1&dtu=200'
    TYPE_DICT = {17: ' 育儿', 6: ' 娱乐', 19: ' 游戏', 5: ' 养生', 18: ' 星座', 40: ' 新时代', 20: ' 天气', 13: ' 体育', 30: ' 收藏', 49: ' 世界杯', 14: ' 时尚', 8: ' 生活', 46: ' 摄影', 27: ' 三农', 1: ' 热点', 11: ' 情感', 9: ' 汽车', 3: ' 其他', 12: ' 美食', 16: ' 旅行',
                 4: ' 励志', 23: ' 历史', 7: ' 科技', 15: ' 军事', 42: ' 健康', 28: ' 国际', 29: ' 故事', 2: ' 搞笑', 25: ' 动漫', 45: ' 彩票', 10: ' 财经'}
    start_urls = []

    def start_requests(self):
        for i in range(1, 20):
            url = self.baseUrl.replace('{timeNow}', str(int(time.time()) * 1000)).replace('{page}', str(i))
            yield Request(url=url, dont_filter=True, priority=1)

    def parse(self, response):

        try:
            print(response.text)
            msgDict = json.loads(response.text)
            for data in msgDict['data']['data']:
                info = data
                info['fromSpider'] = '推荐流'
                request = Request(url=info['url'], priority=10, callback=self.parse_item)
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
        html = response.text
        bs4 = BeautifulSoup(html, "html.parser")
        content = bs4.select_one('div[class=\"content\"]').prettify()
        info['content'] = content
        missionBean = MissionBean(response.url, 1001, ['qutoutiao'])
        missionBean.info = info
        missionBean.html = html
        missionBean.title = info['title']
        # 组装正式版Bean
        newsBean = NewsBean()
        newsBean.titleInfo = info['title']
        newsBean.content = info['content']
        newsBean.url = response.url
        newsBean.newsId = info['id']
        newsBean.tags = info['tag']

        newsBean.etc = {'news_type': info['type']}
        newsBean.fromChannel = self.TYPE_DICT.get(int(info['type']), '其他')
        newsBean.fromSpider = '推荐流'
        newsBean.fromType = 8
        newsBean.goodNum = int(info['like_num'])
        newsBean.commentNum = int(info['comment_count'])
        newsBean.readNum = int(info['read_count'])
        newsBean.mediaName = info['source_name']
        newsBean.mediaId = info['source_name']
        newsBean.introduction = info['introduction']
        newsBean.imgUrls = info['cover']
        newsBean.shareNum = info['share_count']
        missionBean.info = newsBean.__dict__
        # 其中publishDate和createTime由于redis的格式问题
        # TODO 只能传递时间戳
        newsBean.publishDate = datetime.datetime.fromtimestamp(int(info['publish_time']) / 1000).timestamp()
        newsBean.createTime = newsBean.createTime.timestamp()
        daoFilterAndSave.MongoFilterSave(missionBean)

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
        time.sleep(0)
