# -*- coding: utf-8 -*-
import sys
import re

from bs4 import BeautifulSoup

# from zywa_ippool_util.helper.iPPoolHelper import getRandomOneIP


sys.path.append("../../../")
import json
import time
from datetime import datetime

from scrapy import Request
from scrapy.spiders import Spider

from zywa_small_helper.sougouTop.sougouTop.items import SougoutopItem
from pyquery import PyQuery as pq


class SougouSpider(Spider):
    name = 'sougou'

    # 不让scrapy处理任何异常
    handle_httpstatus_list = []
    for i in range(400, 600):
        handle_httpstatus_list.append(i)
    # allowed_domains = ['top.sogou.com/hot/shishi_1.html?fr=tph_righ']
    start_urls = [
        # 搜狗实时热词
        "http://top.sogou.com/hot/shishi_1.html",
        "http://top.sogou.com/hot/shishi_2.html",
        "http://top.sogou.com/hot/shishi_3.html",
        # 搜狗七日热点
        "http://top.sogou.com/hot/sevendsnews_1.html",
        "http://top.sogou.com/hot/sevendsnews_2.html",
        "http://top.sogou.com/hot/sevendsnews_3.html",

        # sina
        "http://news.sina.com.cn/hotnews/",

        # tencent
        "http://news.qq.com/articleList/ranking/",

        # 凤凰网
        "http://news.ifeng.com/hotnews/",

        # 人民网
        "http://news.people.com.cn/GB/28053/",

        # 整合
        'http://s.weibo.com/top/summary?cate=realtimehot',
        'http://s.weibo.com/top/summary?cate=socialevent',
        # 'http://top.baidu.com/buzz?b=341',
        # 'http://news.163.com/rank/',
        #
        # 天涯社区
        # 家庭生活
        "http://bbs.tianya.cn/list.jsp?item=934&sub=2&order=1",
        # 恋爱感悟
        "http://bbs.tianya.cn/list.jsp?item=feeling&sub=2",
        # 单身男女
        "http://bbs.tianya.cn/list.jsp?item=feeling&sub=4",
        # 八卦江湖
        "http://bbs.tianya.cn/list.jsp?item=funinfo&sub=2",
        # 搞笑图片
        "http://bbs.tianya.cn/list.jsp?item=14&sub=2",
    ]
    allowed_domains = ["sina", "sogou"]
    avg_sleep = 10
    baidu_mainurl = 'http://top.baidu.com'

    def start_requests(self):
        for url in self.start_urls:
            # ip_dict = getRandomOneIP()
            # ip_meta = {'proxy': 'http://' + ip_dict['ip'] + ':' + ip_dict['port']}
            u = url.split(".")
            if "sogou" in u:
                yield Request(url, callback=self.parse_sougou, dont_filter=True)
            elif "sina" in u:
                yield Request(url, callback=self.parse_sina, dont_filter=True)
            elif "qq" in u:
                yield Request(url, callback=self.parse_tencent, dont_filter=True)
            elif "ifeng" in u:
                yield Request(url, callback=self.parse_ifeng, dont_filter=True)
            elif "people" in u:
                yield Request(url, callback=self.parse_people, dont_filter=True)
            elif "tianya" in u:
                yield Request(url, callback=self.parse_tianya, dont_filter=True)
            elif "weibo" in u:
                yield Request(url, callback=self.parse_weibo, dont_filter=True)
            elif "baidu" in u:
                yield Request(url, callback=self.parse_baidu, dont_filter=True)

    def parse_sougou(self, response):
        try:
            url = response.url
            t = url.split("?")

            item = SougoutopItem()
            if len(t) == 2:
                # 实时热点
                item['type'] = 550
                info = {
                    "news_type": "搜狗实时热点",
                }
                item["info"] = info
            elif len(t) == 1:
                # 七日热点
                item['type'] = 551
                info = {
                    "news_type": "搜狗七日热点",
                }
                item["info"] = info
            item['url'] = url
            item["missionCreateTime"] = datetime.now()
            e = pq(response.text)
            li = e("ul li")
            li_list = [l for i, l in enumerate(li.items())]
            li_list = li_list[11:]
            for li in li_list:
                self._parse_li(item, li)
                yield item

            # self.start_requests()
        finally:
            print("正在添加新任务至队列头部")
            request = Request(url=response.url, callback=self.parse_sougou, dont_filter=True)
            yield request
            time.sleep(self.avg_sleep)

    def _parse_li(self, item, li):
        rank = li("span i").text()
        a = li("span p a")
        num = li(".s3").text()
        info = {
            "index": rank,
            "title": a.text(),
            "url": a.attr("href"),
            "num": int(num),
            "resource": "搜狗",
        }
        item["info"] = dict(item["info"], **info)

    '''
    下面是 sina 解析部分
    '''

    def parse_sina(self, response):
        try:
            e = pq(response.text)
            loopblk = e(".loopblk")
            for i, div in enumerate(loopblk.items()):
                if i == 1 or i == 2:
                    # 去掉图片排行和视频排行
                    pass
                else:
                    """
                    1. 拿到这个 div 是干什么的 如：新闻总排行
                    2. 拿到数据很简单，重点是判断它是属于什么排行 --点击量排行，评论量排行，分享数排行
                    """
                    rank_name = div(".lbti h2").text()
                    cons = div(".Cons")
                    for index, c in enumerate(cons.items()):
                        # 只要前三个
                        if index == 3 or index == 4:
                            pass
                        else:
                            # self.test(i, c, rank_name, url, item)
                            # self.parse_cons(i, c, rank_name, url, item)
                            # ----------------------------test----------------------------
                            # print("parsing sina")
                            """
                            :param url: 拿到这些信息的 url
                            :param rank_name: 排行榜的名字
                            :param i: i==0 -->点击量排行， i==1 -->评论数排行， i==2 -->分享数排行
                            :param c: 要抓的最小单位
                            :return:
                            """
                            # item = SougoutopItem()
                            info = {}
                            if index == 0:
                                info['news_type'] = "新浪" + rank_name + "点击量排行"
                            elif index == 1:

                                info['news_type'] = "新浪" + rank_name + "评论数排行"
                            elif index == 2:
                                info['news_type'] = "新浪" + rank_name + "分享数排行"

                            script = c("script")
                            item = SougoutopItem()
                            item['url'] = response.url
                            item["missionCreateTime"] = datetime.now()
                            item["info"] = info
                            for a, s in enumerate(script.items()):
                                if a == 0 and index < 2:
                                    pass
                                    # print(i, a, s)
                                    # print(i, a, "dududu", s.attr("src"))
                                    url = s.attr("src")
                                    request = Request(url, callback=self._parse_script, dont_filter=True)
                                    request.item = item
                                    yield request
                                    # yield Request("http://www.baidu.com", callback=self.parse_sougou)

                                if index == 2 and a == 1:
                                    # pass
                                    # print(i, a, "总有奇葩", s.attr("src"))
                                    url = s.attr("src")
                                    request = Request(url, callback=self._parse_script, dont_filter=True)
                                    request.item = item
                                    yield request
                            # ----------------------------test----------------------------
        finally:
            print("sina 正在添加新任务至队列头部")
            request = Request(url=response.url, callback=self.parse_sina, dont_filter=True)
            yield request
            time.sleep(self.avg_sleep)

    def _parse_script(self, response):
        """
        这里拿到了 一个伪json数据，解析一下
        info = {
            "up_or_down"
            "index": rank,
            "title": a.text(),
            "url": a.attr("href"),
            "num": int(num),
        }
        """
        item = response.request.item
        page = response.text
        # e = pq(page)
        # body = e("body").text()
        data = page.split("=", 1)[-1]
        data = data.split(";", 1)[0]
        d = json.loads(data)
        for i, l in enumerate(d["data"]):
            info = {
                "upOrDown": -1,
                "index": i + 1,
                "title": l.get("title"),
                "url": l.get("url"),
                "num": int(l.get("top_num").replace(",", "")),
                "author": l.get("author"),
                "scriptUrl": response.url,
                "resource": "新浪",
            }
            item["info"] = dict(item["info"], **info)
            yield item

    '''
    下面是腾讯新闻排行榜解析
    '''

    def parse_tencent(self, response):
        # page = response.text
        # print(response.text)
        try:
            item = SougoutopItem()
            # e = pq(response.text)
            url = response.url
            item["url"] = url
            item["missionCreateTime"] = datetime.now()
            # 从 module 中拿到每个新闻 13个 module
            module = response.css(".module")
            sub_title = ['新闻', '时政', '国际', '财经', '体育', '娱乐', '时尚', '汽车', '房产', '游戏', '社会', '教育', '旅游']
            for i, m in enumerate(module):
                # sub_title = response.css(".subTit::text").extract_first()

                ul = m.css(".tab ul")
                for u in ul:
                    li = u.css("li")
                    for j, l in enumerate(li):
                        a = l.css(".info p a")
                        num = l.css(".heatIndex::text").extract_first()
                        print(num)
                        # if "评论数" in num:
                        #     num = -1
                        # else:
                        result = re.search(r'[1-9]\d*|0', num, re.M | re.I)
                        num = result.group()
                        # print("index", index, "u", u, "j", j, "li", l, "tab_title", tab_title)
                        info = {
                            "news_type": "腾讯" + sub_title[i],
                            "upOrDown": -1,
                            "index": l.css(".top::text").extract_first(),
                            "title": a.css("::text").extract_first(),
                            "url": a.css("::attr(href)").extract_first(),
                            "origin": l.css(".origin::text").extract_first(),
                            "num": int(num),
                            "resource": "腾讯",
                        }
                        item["info"] = info
                        yield item
        finally:
            print("parse_tencent 正在添加新任务至队列头部")
            request = Request(url=response.url, callback=self.parse_tencent, dont_filter=True)
            yield request
            time.sleep(self.avg_sleep)

    '''
    凤凰网
    '''

    def parse_ifeng(self, response):
        try:
            item = SougoutopItem()
            url = response.url
            item["url"] = url
            item["missionCreateTime"] = datetime.now()
            box_tab = response.css(".boxTab")
            for box in box_tab:
                sub_title = {}
                tit = box.css(".tit span::text").extract_first()
                li = box.css(".label_01 li")
                for i, l in enumerate(li):
                    sub_title[i] = l.css("::text").extract_first()
                table = box.css(".conTab .tab_01")
                for index, t in enumerate(table):
                    for i, tr in enumerate(t.css("tr")):
                        if i == 0:
                            continue
                        td = tr.css("td")

                        info = {
                            "news_type": "凤凰网" + tit + sub_title[index],
                            "upOrDown": -1,
                            "index": td[0].css("::text").extract_first(),
                            "title": td[1].css("h3 a::text").extract_first(),
                            "url": td[1].css("h3 a::attr(href)").extract_first(),
                            "num": int(td[2].css("::text").extract_first()),
                            "resource": "凤凰网",
                            "news_date": td[3].css("::text").extract_first(),
                        }
                        item["info"] = info
                        yield item
        finally:
            print("parse_tencent 正在添加新任务至队列头部")
            request = Request(url=response.url, callback=self.parse_ifeng, dont_filter=True)
            yield request
            time.sleep(self.avg_sleep)

    '''
    人民网
    '''

    def parse_people(self, response):
        try:
            item = SougoutopItem()
            url = response.url
            item["url"] = url
            item["missionCreateTime"] = datetime.now()
            tr = response.css("tr tr table tr")
            tr = tr[:51]
            # print(len(tr.extract()), tr.extract())
            for i, t in enumerate(tr):
                if i == 0:
                    continue
                td = t.css("td")
                index = td[0].css("td::text").extract_first()
                a = td[1].css("td a")
                info = {
                    "news_type": "人民网",
                    "upOrDown": -1,
                    "index": int(index),
                    "title": a.css("::text").extract_first(),
                    "url": a.css("::attr(href)").extract_first(),
                    "origin": td[2].css("::text").extract_first(),
                    "num": -1,
                    "resource": "人民网",
                }
                item["info"] = info
                yield item
        finally:
            print("parse_tencent 正在添加新任务至队列头部")
            request = Request(url=response.url, callback=self.parse_people, dont_filter=True)
            yield request
            time.sleep(self.avg_sleep)

    '''
    微博
    '''

    def parse_weibo(self, response):
        try:
            item = SougoutopItem()
            url = response.url
            item["url"] = url
            item["missionCreateTime"] = datetime.now()

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
                if 'realtimehot' in response.url:
                    dictInfo["news_type"] = '微博热搜'
                if 'socialevent' in response.url:
                    dictInfo["news_type"] = '微博新时代'
                item["info"] = dictInfo
                yield item
        finally:
            print("parse_tencent 正在添加新任务至队列头部")
            request = Request(url=response.url, callback=self.parse_weibo, dont_filter=True)
            yield request
            time.sleep(self.avg_sleep)

    '''
    百度
    '''
    def parse_baidu(self, response):
        modes = response.xpath('//div[@class="hblock"]/ul/li/a/@href').extract()
        for mode in modes[1:]:
            news_type = response.xpath(
                '//div[@class="hblock"]/ul/li[{}]/a/@title'.format(str(1 + modes.index(mode)))).extract_first()
            yield Request(url=self.baidu_mainurl + mode[1:], callback=self.parse_item, dont_filter=True,
                          meta={'news_type': news_type}, priority=2)

    def parse_item(self, response):
        item = SougoutopItem()
        url = response.url
        item["url"] = url
        item["missionCreateTime"] = datetime.now()
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
                item['info'] = items
        print('本次抓取个数{}'.format(i))
        yield item
        #   print response.meta['news_type'].encode('gb18030'),num,title.encode('gb18030'),href

    '''
    天涯
    '''

    def parse_tianya(self, response):
        try:
            url = response.url
            item = SougoutopItem()
            item["url"] = url
            item["missionCreateTime"] = datetime.now()
            page = response.text
            e = pq(page)
            trs = e("tr")
            for i, tr in enumerate(trs.items()):
                if i != 0:
                    type_list = e(".type-list")
                    type_list("a").remove()
                    news_type = type_list.text().replace("\\", "").replace(" ", "")
                    info = {
                        "news_type": "天涯社区" + news_type,
                        "upOrDown": -1,
                        "resource": "天涯社区",
                        "index": i,
                    }
                    title = tr(".td-title a")
                    title_url = "http://bbs.tianya.cn" + title.attr("href")
                    info["title"] = title.text()
                    info["url"] = title_url
                    td = tr("td")
                    for j, t in enumerate(td.items()):
                        if j == 2:
                            # 点击
                            info["num"] = int(t.text())
                        if j == 3:
                            # 评论
                            info["num1"] = int(t.text())

                    item["info"] = info
                    yield item
        finally:
            print("parse_tencent 正在添加新任务至队列头部")
            request = Request(url=response.url, callback=self.parse_tianya, dont_filter=True)
            yield request
            time.sleep(self.avg_sleep)

