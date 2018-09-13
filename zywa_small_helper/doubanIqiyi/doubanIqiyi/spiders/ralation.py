# -*- coding: utf-8 -*-
import time

import scrapy
import json
from scrapy import Request
from pyquery import PyQuery as pq

from zywa_alarm_httpserver.cang_client.mongoClient import CangMongoClient


class RalationSpider(scrapy.Spider):
    """
    https://movie.douban.com/subject_search?search_text=孤独的美食家&cat=1002
    """
    name = 'ralation'
    db = CangMongoClient(db='xiaociwei', user='xiaociweiRWUser', password='zywaXIAOCIWEI@!!!').new_db
    write_db = CangMongoClient(db='xiaociwei', user='xiaociweiRWUser', password='zywaXIAOCIWEI@!!!').new_db
    count = 0
    not_exist_movie = []

    def start_requests(self):
        """
        前奏： 读取iqiyi库标题，匹配
        1. 读取库里所有的iqiyi标题
        2. 使用标题搜索，如果标题匹配入库， 否则第三条
        3. 抓取第一条
        4. 解析第一条的iqiyi链接地址是否对应，对应入库更新，否则结束
        """
        for index, res in enumerate(self.db.iqiyi_movie.find()):
            title = res.get("title")
            iqiyi_video_id = res.get("info").get("videoId")
            mongo_id = res.get("_id")
            iqiyi_info = {
                "title": title,
                "videoId": iqiyi_video_id,
                "mongoId": mongo_id,
                "mongoDBName": "xiaociwei",
                "tableName": "v_iqiyi_movie",
            }
            # 查豆瓣库看有多少匹配
            query = {
                "title": res.get("title"),
            }
            r = self.db.v_doubanMovie.find_one(query)
            if r is not None:
                # 名字和豆瓣库的匹配，入库，不发起搜索请求
                del r["_id"]
                query2 = {
                    "movieId": r["movieId"]
                }
                r['relation'] = iqiyi_info
                print("爱奇艺名字和豆瓣库的匹配, 正在入库", r)
                self.count += 1
                print("匹配成功总数", self.count)
                self.write_db.v_doubanMovie.update(query2, {"$set": r}, upsert=True)
            else:
                # url = "https://movie.douban.com/subject_search?search_text={}&cat=1002".format(title)
                url = "http://api.douban.com/v2/movie/search?q={}".format(title)
                request = Request(url, callback=self.parse)
                request.info = iqiyi_info
                yield request
            time.sleep(1)

    def parse(self, response):
        iqiyi_info = response.request.info
        page = response.text
        r = json.loads(page)
        first = r.get("subjects")[0]
        if first.get("title") == iqiyi_info.get("title"):
            # 匹配成功 入库
            query2 = {
                "movieId": first["id"]
            }
            insert = {
                'relation': iqiyi_info,
            }
            print("搜索结果第一个名字匹配成功，正在入库", first.get("title"))
            self.count += 1
            print("匹配成功总数", self.count)
            self.write_db.v_doubanMovie.update(query2, {"$set": insert}, upsert=True)
        else:
            url = first.get("alt")
            request = Request(url, callback=self.parse_sub)
            request.info = iqiyi_info
            request.doubanId = first.get("id")
            print("搜索结果第一个名字不匹配，正在发起请求", first.get("title"))
            yield request

    def parse_sub(self, response):
        iqiyi_info = response.request.info
        douban_id = response.request.doubanId
        page = response.text
        e = pq(page)
        gray_ad = e(".gray_ad li")
        # 是否存在爱奇艺的一个标识
        iqiyi = False
        for g in gray_ad.items():
            if "爱奇艺" in g.text():
                iqiyi_url = g("a").attr("href")
                print("详情页存在爱奇艺", g.text(), iqiyi_url, iqiyi_info)
                if iqiyi_url is not None:
                    tmp = iqiyi_url.split("%")
                    for t in tmp:
                        if "html" in t:
                            if t.split(".html")[0] == ("2F" + iqiyi_info.get("videoId")):
                                # 可以入库了
                                query = {
                                    "movieId": douban_id
                                }
                                insert = {
                                    'relation': iqiyi_info,
                                }
                                print("详情页，爱奇艺videoId 匹配成功，正在入库")
                                iqiyi = True
                                self.count += 1
                                print("匹配成功总数", self.count)
                                self.write_db.v_doubanMovie.update(query, {"$set": insert}, upsert=True)
        if not iqiyi:
            # 本条数据中没有匹配到爱奇艺
            self.not_exist_movie.append(iqiyi_info.get("title"))
            print("没有匹配到的爱奇艺电影有:", self.not_exist_movie)
            print("共:{}个".format(len(self.not_exist_movie)))
