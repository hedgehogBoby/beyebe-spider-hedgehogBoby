import json
import traceback
from urllib import parse
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from zywa_database_core.dao.mongo.mongoClientMyself import getMongoDownloadClient
import time
from scrapy.http import Request
from scrapy.spiders import Spider

from zywa_extract_helper.model.missionBean import MissionBean


class HotwordSpider(Spider):
    # mongodb
    client = getMongoDownloadClient()
    # 不让scrapy处理任何异常
    handle_httpstatus_list = []
    for i in range(400, 600):
        handle_httpstatus_list.append(i)
    name = 'hotword'
    allowed_domains = ['baidu.com', 'weibo.com', '163']
    # start_urls = ['http://news.163.com/rank/']
    start_urls = ['http://s.weibo.com/top/summary?cate=realtimehot',
                  'http://top.baidu.com/buzz?b=341',
                  'http://s.weibo.com/top/summary?cate=socialevent',
                  'http://news.163.com/rank/',
                  'http://api.1sapp.com/content/outList?cid=255&tn=1&page={page}&limit=100&user=temporary{timeStamp}&content_type=1&dtu=200']
    baidu_mainurl = 'http://top.baidu.com'

    def start_requests(self):
        for url in self.start_urls:
            if 'api.1sapp' in url:
                for i in range(10):
                    urlNow = url.replace('{page}', str(i + 1)).replace('{timeStamp}', str(int(time.time() * 1000)))
                    request = Request(url=urlNow)
                    request.info = {'page': i}
                    yield request
                continue
            yield Request(url=url)

    def parse(self, response):
        try:

            if 'top.baidu' in response.url:
                modes = response.xpath('//div[@class="hblock"]/ul/li/a/@href').extract()
                for mode in modes[1:]:
                    news_type = response.xpath('//div[@class="hblock"]/ul/li[{}]/a/@title'.format(str(1 + modes.index(mode)))).extract_first()
                    yield Request(url=self.baidu_mainurl + mode[1:], callback=self.parse_item, dont_filter=True, meta={'news_type': news_type}, priority=2)
            if 'weibo' in response.url:
                rhtml = response.xpath('//script/text()').extract()  # 变量瞎定义的，大家将就着看，获取整个页面的script的字符串信息。
                htm = rhtml[8]  # 获取目标ID为realtimehot的Table的脚本信息，为什么是8呢？我在页面数的。
                start = htm.find("(")
                substr = htm[start + 1:-1]  # 截取脚本里面的json串信息。
                html = json.loads(substr)['html']
                bs4 = BeautifulSoup(html, 'html.parser')
                trTags = bs4.select('tr[action-type=\"hover\"]')
                print("发现潜在词数量", len(trTags))
                for trTag in trTags:
                    dictInfo = {}
                    dictInfo['index'] = trTag.find('em').string

                    dictInfo['title'] = trTag.find('p', class_='star_name').a.string
                    dictInfo['url'] = trTag.find('p', class_='star_name').a.get('href')
                    dictInfo['resource'] = '微博'
                    try:
                        dictInfo['num'] = int(trTag.find('p', class_='star_num').span.string)
                    except:
                        dictInfo['num'] = -1
                    missionBean = MissionBean(dictInfo['url'], 501, ['train_hotword'])
                    missionBean.title = str(dictInfo['title'])
                    if 'realtimehot' in response.url:
                        missionBean.info = {'news_type': '微博热搜'}
                    if 'socialevent' in response.url:
                        missionBean.info = {'news_type': '微博新时代'}
                    missionBean.info.update(dictInfo)
                    print(missionBean.title)
                    self.client.save(missionBean)
            if 'news.163' in response.url:
                typeName0 = '163'
                bs4 = BeautifulSoup(response.text, "html.parser")
                items = bs4.select_one("div[class=\"area areabg1\"]")
                i = 0
                for titleBarTag in items.select("div[class=\"titleBar\"]"):
                    # 这个网站比较奇怪，是并列关系，第n个titleBar对应第n个left和right
                    typeName1 = titleBarTag.select_one("h2").get_text()  # 分类名
                    """
                    左侧分类【点击榜】
                    """
                    areaLeftTag = items.select('div[class=\"area-half left\"]')[i]
                    typeName2 = areaLeftTag.select_one("h2").get_text()
                    liTags = items.select("div[class=\"title-tab\"]")[i].select('li')
                    j = 0
                    for li in liTags:
                        typeName3 = li.get_text()
                        # print(str(areaLeftTag))
                        tableTag = areaLeftTag.select('table')[j]
                        for newsTag in tableTag.select("tr"):
                            # 标题行不抓取
                            if "标题" in newsTag.get_text():
                                continue
                            infoDict = {}
                            infoDict['title'] = newsTag.select_one('a').get_text()
                            infoDict['index'] = int(newsTag.select("td")[0].select_one("span").get_text())
                            infoDict['num'] = int(newsTag.select("td")[1].get_text())
                            infoDict['upOrDown'] = -1
                            infoDict['url'] = newsTag.select_one('a')['href']
                            infoDict['news_type'] = typeName0 + typeName1 + typeName2 + typeName3
                            infoDict['resource'] = '163'
                            missionBean = MissionBean(response.url, 510, ['train_hotword'])
                            missionBean.info = infoDict
                            self.client.save(missionBean)
                        j = j + 1
                    """
                    右侧分类【跟帖榜】
                    """
                    areaLeftTag = items.select('div[class=\"area-half right\"]')[i]
                    typeName2 = areaLeftTag.select_one("h2").get_text()
                    liTags = items.select("div[class=\"title-tab\"]")[i].select('li')
                    j = 0
                    for li in liTags:
                        typeName3 = li.get_text()
                        # print(str(areaLeftTag))
                        tableTag = areaLeftTag.select('table')[j]
                        for newsTag in tableTag.select("tr"):
                            # 标题行不抓取
                            if "标题" in newsTag.get_text():
                                continue
                            infoDict = {}
                            infoDict['title'] = newsTag.select_one('a').get_text()
                            infoDict['index'] = int(newsTag.select("td")[0].select_one("span").get_text())
                            infoDict['num'] = int(newsTag.select("td")[1].get_text())
                            infoDict['upOrDown'] = -1
                            infoDict['url'] = newsTag.select_one('a')['href']
                            infoDict['news_type'] = typeName0 + typeName1 + typeName2 + typeName3
                            infoDict['resource'] = '163'
                            missionBean = MissionBean(response.url, 511, ['train_hotword'])
                            missionBean.info = infoDict
                            self.client.save(missionBean)
                        j = j + 1
                    i = i + 1
            if 'api.1sapp' in response.url:
                jsonBean = json.loads(response.text)
                print(jsonBean)
                for i, news in enumerate(jsonBean['data']['data']):
                    items = {}
                    parseUrl = urlparse(response.url)
                    strParseQs = parseUrl[4]
                    res = parse.parse_qs(strParseQs)
                    pageNum = int(res.get('page')[0])
                    limitNum = int(res.get('limit')[0])
                    items['index'] = i + 1 + (pageNum - 1) * limitNum
                    items['title'] = news['title']
                    items['news_type'] = '趣头条推荐流'
                    items['url'] = news['url']
                    items['num'] = 10000 - items['index']
                    items['num1'] = int(news['read_count'])
                    items['num2'] = int(news['share_count'])
                    items['resource'] = '趣头条'
                    missionBean = MissionBean(items['url'], 500, ['train_hotword'])
                    missionBean.title = items['title']
                    missionBean.info = items
                    self.client.save(missionBean)
        except:
            traceback.print_exc()
        finally:
            print("正在添加新任务至队列头部")
            request = Request(url=response.url, dont_filter=True)
            yield request

    def parse_item(self, response):
        i = 0
        bodys = response.xpath('//table[@class="list-table"]/tr')
        for body in bodys:
            if body.xpath('.//td[@class="first"]').extract():
                items = {}
                num = body.xpath('.//td[@class="first"]/span/text()').extract_first()
                title = body.xpath('.//td[@class="keyword"]/a/text()').extract_first()
                href = body.xpath('.//td[@class="keyword"]/a/@href').extract_first()
                focus_num = body.xpath('.//td[@class="last"]/span/text()').extract_first()
                items['index'] = num
                items['title'] = title
                items['news_type'] = '百度' + response.meta['news_type']
                items['url'] = href
                items['num'] = int(focus_num)
                items['focus_num'] = focus_num
                items['resource'] = '百度'
                print(items)
                i = i + 1
                try:
                    missionBean = MissionBean(href, 500, ['train_hotword'])
                    missionBean.title = title
                    missionBean.info = items
                    self.client.save(missionBean)

                except:
                    print("存储数据库出现异常")
                    traceback.print_exc()
        print('本次抓取个数{}'.format(i))
        self.sleepMyself()
        #   print response.meta['news_type'].encode('gb18030'),num,title.encode('gb18030'),href

    def sleepMyself(self):
        print('休息一分钟')
        time.sleep(2)
