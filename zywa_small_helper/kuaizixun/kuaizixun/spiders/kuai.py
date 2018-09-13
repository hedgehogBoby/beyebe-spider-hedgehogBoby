# -*- coding: utf-8 -*-
import datetime
import json
import sys
import time
from urllib.parse import urlencode
sys.path.append("../../../")

import scrapy
from scrapy import Request
from pyquery import PyQuery as pq

from zywa_small_helper.kuaizixun.kuaizixun.items import KuaizixunItem


class KuaiSpider(scrapy.Spider):
    name = 'kuai'
    # allowed_domains = ['sh.qihoo.com/pc']
    # start_urls = [
    #     # 'https://sh.qihoo.com/pc/',
    #     "http://papi.look.360.cn/mlist?c=youlike&u=e90bc5f760e96470de94cc112f72fb07&uid=e90bc5f760e96470de94cc112f72fb07&sign=360dh&version=2.0&sqid=&device=2&market=pc_def&net=4&tj_cmode=pclook&where=list&pid=index&src=&v=1&sv=4&n=10&action=1&f=jsonp&stype=portal&newest_showtime=&oldest_showtime=&ufrom=2&scene=2",
    # ]
    sleep_time = 2

    def start_requests(self):
        # url = "http://papi.look.360.cn/mlist?c=topshare_random&u=c242645eb0fb019e904c76784c576d03&uid=c242645eb0fb019e904c76784c576d03&sign=360dh&version=2.0&sqid=&device=2&market=pc_def&net=4&tj_cmode=pclook&where=&v=1&sv=4&n=20&action=2&f=jsonp&stype=portal&callfrom=ndetail&newest_showtime=&oldest_showtime=&scene=7&_=1529979482375"
        url = "http://papi.look.360.cn/mlist?c=youlike&u=e90bc5f760e96470de94cc112f72fb07&uid=e90bc5f760e96470de94cc112f72fb07&sign=360dh&version=2.0&sqid=&device=2&market=pc_def&net=4&tj_cmode=pclook&where=list&pid=index&src=&v=1&sv=4&n=10&action=1&f=jsonp&stype=portal&newest_showtime=&oldest_showtime=&ufrom=2&scene=2"
        yield Request(url, callback=self.parse)

    def parse(self, response):
        try:
            page = response.text
            page = page[1:][:-2]
            r = json.loads(page)
            data = r["data"]["res"]
            for d in data:
                url = d["u"]
                tags = d.get("j").split(";")
                from_channel = tags[0]
                tag = tags[-1].split("|")
                api_info = {
                    "url": url,
                    "newsId": d.get("gnid"),
                    "titleInfo": d['t'],
                    "mediaName": d.get("zmt", {}).get("name", ''),
                    "mediaId": d.get("zmt", {}).get("id", ''),
                    "fromChannel": from_channel,
                    "tags": tag,
                    "fromSpider": "推荐流",
                    # "recalltype": d.get("recalltype"),  # "hot"
                    "type": d.get("type"),  # "topshare"  "newgood"
                    "api_all_info": d,
                }
                # pc_url = d['pcurl']

                yield Request(url, callback=self.parse_acticle, meta=api_info)

        finally:
            print("parse 正在添加新任务至队列头部")
            request = Request(url=response.url, callback=self.parse, dont_filter=True)
            yield request
            time.sleep(self.sleep_time)

    def parse_acticle(self, response):
        article_info = response.meta
        page = response.text
        e = pq(page)
        script = e("script")
        for i, s in enumerate(script.items()):
            if "data_new =" in s.text():
                data_new = s.text().split("data_new = ")[-1]
                data_new = data_new.split(";")[0]
                # print(data_new)
                data_new = json.loads(data_new)
                if response.meta["mediaName"] == "":
                    article_info["mediaName"] = data_new.get("src")
                    article_info["mediaId"] = data_new.get("src")
                if response.meta['newsId'] is None:
                    article_info["newsId"] = data_new.get("gnid", "")
                article_info["publishDate"] = data_new.get("pub_time")
                article_info["introduction"] = data_new.get("abstract", {}).get("digest", '')
                img = data_new.get("img_data")[0].get("img")
                imgs = [i.get("url") for i in img]
                article_info["imgUrls"] = imgs
                article_info["content"] = data_new.get("content")
                pub_time = data_new.get("pub_time")
                # 转换为datetime 格式
                pub_time = datetime.datetime.fromtimestamp(int(pub_time) / 1000)
                article_info["publishDate"] = pub_time
                article_info["articleAllInfo"] = data_new
                """
                评论数在另一个链接中
                http://u.api.look.360.cn/article/zc?f=jsonp&sv=4&version=&market=pc_def&device=2&net=4&stype=portal&scene=&sub_scene=&refer_scene=&refer_subscene=&tj_cmode=pclook&url=https%3A%2F%2Fwww.toutiao.com%2Fi6570897440621199879%2F                
                """
                d = {
                    "f": "jsonp",
                    "sv": "4",
                    "version": "",
                    "market": "pc_def",
                    "device": "2",
                    "net": "4",
                    "stype": "portal",
                    "scene": "sub_scene",
                    "refer_scene": "refer_subscene",
                    "tj_cmode": "pclook",
                    "url": data_new["rawurl"],
                }
                comment_url = "http://u.api.look.360.cn/article/zc?" + urlencode(d)
                yield Request(url=comment_url, callback=self.parse_comment, meta=article_info)

    def parse_comment(self, response):
        item = KuaizixunItem()
        item["createTime"] = datetime.datetime.now()
        meta = response.meta
        for field in item.fields:
            if field in meta.keys():
                item[field] = meta[field]
        page = response.text
        page = page[1:][:-2]
        r = json.loads(page)
        item["goodNum"] = r.get("data")[0].get("zan")
        item["unlikeNum"] = r.get("data")[0].get("cai")
        item["readNum"] = -1
        item["commentNum"] = -1
        item["shareNum"] = -1

        item["imgFileUrls"] = {'num': 0}
        item["videoFileUrls"] = {'num': 0}
        item["etc"] = {
            "type": meta["type"],
            "zan_url": response.url,
            "apAllInfo": meta["api_all_info"],
            "articleAllInfo": meta["articleAllInfo"],
        }
        item["fromType"] = 9
        yield item
