# -*- coding: utf-8 -*-
import datetime
import re
import sys
import time

import scrapy
import json
from scrapy import Request
from bs4 import BeautifulSoup as bs
from pyquery import PyQuery as pq

sys.path.append("../../../")
# from zywa_ippool_util.helper.iPPoolHelper import getRandomOneIP
from zywa_small_helper.douban.douban.items import DoubanItem


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanMovie'
    # allowed_domains = ['movie.douban.com/top250']
    start_urls = ['https://movie.douban.com/j/new_search_subjects?range=0,10&start=0']
    count = 500

    SLEEP = 0

    # ip_dict = getRandomOneIP()
    # ip_meta = {'proxy': 'http://' + ip_dict['ip'] + ':' + ip_dict['port']}

    def parse(self, response):
        r = response.text
        r = json.loads(r)
        data = r['data']
        # print(len(data))
        if len(data) > 0:
            for d in data:
                request = Request(url=d.get('url'), callback=self.parse_subject)
                request.info = d
                yield request
            self.count += 1
            url = 'https://movie.douban.com/j/new_search_subjects?range=0,10&start={}'.format(self.count * 20)
            yield Request(url=url, callback=self.parse)

    @staticmethod
    def parse_pub_date(pub_date, info):
        """
        把时间转换为date，同时保留时间描述信息
        :param pub_date: 传入的是一个列表
        :return: 返回一个包含列表的字典
        """
        for d in pub_date:
            new_d = d.split("(")
            new_pub = []
            if len(new_d) > 1:
                # 带描述信息
                new_date = new_d[0]
                if len(new_date) == 4:
                    # 兼容 1994 这种奇葩
                    new_date = datetime.datetime.strptime(new_date, '%Y')
                    # 兼容2000-07
                elif len(new_date) == 7:
                    new_date = datetime.datetime.strptime(new_date, '%Y-%m')
                else:
                    new_date = datetime.datetime.strptime(new_date, '%Y-%m-%d')
                description = new_d[1].split(")")[0]
                pub = {
                    "date": new_date,
                    "description": description
                }
                new_pub.append(pub)
            else:
                # 不带描述信息
                new_date = new_d[0]
                if len(new_date) == 4:
                    # 兼容 1994 这种奇葩
                    new_date = datetime.datetime.strptime(new_date, '%Y')
                elif len(new_date) == 7:
                    new_date = datetime.datetime.strptime(new_date, '%Y-%m')
                else:
                    new_date = datetime.datetime.strptime(new_date, '%Y-%m-%d')
                pub = {
                    "date": new_date,
                    "description": info.get("country")
                }
                new_pub.append(pub)
            return new_pub

    def parse_subject_one(self, page):
        tmp = bs(page, "html.parser")
        info = tmp.body.find('div', id='info').text

        info1 = info.split("\n")
        d = {}
        for i in info1:
            if "类型" in i:
                tags = i.split(": ")[-1].split(" / ")
                # print(tags)
                d['tags'] = tags
            if "制片国家/地区" in i:
                country = i.split(": ")[-1]
                # print(country)
                d['country'] = country
            if "语言" in i:
                movie_language = i.split(": ")[-1]
                d['movieLanguage'] = movie_language
            if ("首播" in i) or ("上映日期" in i):
                pub_date = i.split(": ")[-1]
                pub_date = pub_date.split(" / ")
                pub_date = self.parse_pub_date(pub_date, d)
                d['pubDate'] = pub_date
            if "单集片长" in i:
                runtime = i.split(": ")[-1]
                result = re.search(r'[1-9]\d*', runtime)
                runtime = result.group()
                runtime = int(runtime) * 60
                d['runtime'] = runtime
            if "又名" in i:
                title_others = i.split(": ")[-1]
                d['titleOthers'] = title_others
            if "IMDb链接" in i:
                IMDb_url = i.split(": ")[-1]
                d['IMDbUrl'] = "http://www.imdb.com/title/{}".format(IMDb_url)
        if "IMDb链接" not in info:
            IMDb_url = '0'
            d['IMDbUrl'] = IMDb_url
        if ("首播" not in info) and ("上映日期" not in info):
            d['pubDate'] = []
        return d

    def parse_subject(self, response):
        item = DoubanItem()
        api_info = response.request.info
        actors = response.css(".actor a::text").extract()
        page = response.text
        e = pq(page)
        link_report = e("#link-report").text()
        pic_url = e(".related-pic-bd a")
        related_pic = [p.attr("href") for p in pic_url.items()]
        rating_people = e(".rating_people span").text()
        # 解析页面 得到一个字典
        d = self.parse_subject_one(page)
        sub_info = {
            "title": api_info["title"],
            "movieId": api_info["id"],
            "directors": api_info["directors"],
            "casts": api_info["casts"],
            "actors": actors,
            "category": "电影",
            "coverUrl": api_info["cover"],
            "movieUrl": api_info["url"],
            "ratingValue": float(api_info["rate"]),
            "introduction": link_report,
            "ratingPeople": int(rating_people),
            "comments": {
                "shortComment": [],
                "longComment": [],
            },
            "commentStatus": {
                # 全部抓取完成设为 True
                "short": False,
                "long": False,
                "full": True,
            },
            "etc": {
                "relatedPictures": related_pic,
            }
        }
        sub_info = dict(d, **sub_info)
        movie_id = api_info["id"]
        # 短评
        short_url = "https://movie.douban.com/subject/{}/comments?start=0&limit=20&sort=new_score&status=P".format(
            movie_id)
        # request = Request(short_url, callback=self.parse_short, meta=self.ip_meta)
        request = Request(short_url, callback=self.parse_short)
        request.item = item
        request.info = sub_info
        yield request
        # 剧评
        long_url = "https://movie.douban.com/subject/{}/reviews?start=0".format(movie_id)
        request2 = Request(long_url, callback=self.parse_long)
        request2.info = sub_info
        request2.item = item
        yield request2
        time.sleep(self.SLEEP)

    @staticmethod
    def parse_short_one(c):
        comment_info = c('.comment-info')
        people_name = comment_info('a').text()
        people_id = comment_info('a').attr("href").split("/")[-2]
        # 评分 对应五颗星 力荐表示五星
        people_rating = comment_info(".rating").attr("title")
        comment_time = comment_info(".comment-time ").attr("title")
        comment_time = datetime.datetime.strptime(comment_time, '%Y-%m-%d %H:%M:%S')
        # 其他人对这个评论的标记 是否有用
        comment_vote = c(".votes").text()
        comment_content = c(".comment p").text()

        d = {
            "comment_content": comment_content,
            "people_name": people_name,
            "people_id": people_id,  # string 有的人可以自定义个人空间后缀的 https://www.douban.com/people/Wjiaer/
            "people_rating": people_rating,
            "comment_time": comment_time,
            "comment_vote": int(comment_vote),
        }
        return d

    def parse_short(self, response):
        item = response.request.item
        sub_info = response.request.info
        movie_id = sub_info.get("movieId")
        page = response.text
        e = pq(page)
        comment = e(".comment-item")
        # 包含一页的评论
        # comments = [self.parse_short_one(c) for c in comment.items()]
        for c in comment.items():
            one_comment = self.parse_short_one(c)
            sub_info["comments"]["shortComment"].append(one_comment)
        # 翻页
        # next_page = e('.next').attr("href")
        # if next_page is not None:
        #     next_url = "https://movie.douban.com/subject/{}/comments{}".format(movie_id, next_page)
        #     # request = Request(next_url, callback=self.parse_short, meta=self.ip_meta)
        #     request = Request(next_url, callback=self.parse_short)
        #     request.item = item
        #     request.info = sub_info
        #     yield request
        #     time.sleep(self.SLEEP)
        # else:
        #     print("短评最后一页了")
        # 这里改成只抓一页
        print("短评抓完了一页，", sub_info.get("title"))
        sub_info["commentStatus"]["short"] = True
        for field in item.fields:
            if field in sub_info.keys():
                item[field] = sub_info[field]
        if sub_info["commentStatus"]["short"] and \
                sub_info["commentStatus"]["long"] and \
                sub_info["commentStatus"]["full"]:
            yield item

    @staticmethod
    def parse_long_one(r):
        d = {}
        title_tmp = r(".main-bd h2 a")
        full_url = title_tmp.attr("href")
        title = title_tmp.text()
        d["full_url"] = full_url
        d["title"] = title
        author_info = r(".main-hd a")
        for index, info in enumerate(author_info.items()):
            # print(index, info)
            if index == 0:
                people_img = info("img").attr("src")
                d["people_img"] = people_img
                # print(people_img)
            if index == 1:
                people_name = info.text()
                people_id = info.attr("href").split("/")[-2]
                d["people_name"] = people_name
                d["people_id"] = people_id
        comment_id = r.attr("id")
        useful_count = r("#r-useful_count-" + comment_id).text()
        if useful_count == "":
            useful_count = 0
        else:
            useful_count = int(useful_count)
        useless_count = r("#r-useless_count-" + comment_id).text()
        if useless_count == "":
            useless_count = 0
        else:
            useless_count = int(useless_count)
        d["comment_id"] = comment_id
        d["useful_count"] = useful_count
        d["useless_count"] = useless_count
        return d

    def parse_long(self, response):
        item = response.request.item
        sub_info = response.request.info
        page = response.text
        e = pq(page)
        review = e(".review-item")
        # 这个里面对评论的投票没有抓，后面全文的时候一起合并
        # 这里的评论只是一页的
        comments = [self.parse_long_one(r) for r in review.items()]
        # 抓取第一个完整影评，剩下的让解析函数自己去发起请求
        # 因为后面的请求需要前面的数据
        # if len(comments) > 1:
        #     full_url = comments[0].get("full_url")
        #     request = Request(full_url, callback=self.parse_long_full)
        #     request.item = item
        #     request.allComments = comments
        #     request.currentComment = comments[0]
        #     request.status = {
        #         "index": 0,  # 现在是第几个
        #         "len": len(comments),  # 总长度
        #     }  # 判断长评论有没有抓完
        #     request.info = sub_info
        #     yield request

        # # 合并
        # sub_info["comments"]["longComment"].append(comments)

        # 翻页
        # movie_id = sub_info.get("movieId")
        # next_page = e('.next a').attr("href")
        # if next_page is not None:
        #     next_url = "https://movie.douban.com/subject/{}/reviews?start=20".format(movie_id)
        #     # request = Request(next_url, callback=self.parse_long, meta=self.ip_meta)
        #     request = Request(next_url, callback=self.parse_long)
        #     request.item = item
        #     request.info = sub_info
        #     yield request
        #     time.sleep(self.SLEEP)
        # else:
        #     print("影评最后一页了")
        # 这里改成只抓一页
        print("剧评(不含评论)抓完了一页，", sub_info.get("title"))
        for field in item.fields:
            if field in sub_info.keys():
                item[field] = sub_info[field]
        sub_info["commentStatus"]["long"] = True
        if sub_info["commentStatus"]["short"] and \
                sub_info["commentStatus"]["long"] and \
                sub_info["commentStatus"]["full"]:
            yield item

    def parse_long_full(self, response):
        item = response.request.item
        comments = response.request.allComments
        comment_now = response.request.currentComment
        status = response.request.status
        sub_info = response.request.info
        page = response.text
        e = pq(page)
        link_report = e("#link-report")
        comment_content = link_report.text()
        comment_now["comment_content"] = comment_content
        # 合并 也就是更新之前longComment 中存的值
        # comments[status.get("index")] = comment_now
        sub_info["comments"]["longComment"].append(comment_now)

        # if status.get("index") < status.get("len") - 1:
        #     # 这里表示长评论后面的没抓，产生一个新任务
        #     full_url = comments[status.get("index") + 1].get("full_url")
        #     # request = Request(full_url, callback=self.parse_long_full, meta=self.ip_meta)
        #     request = Request(full_url, callback=self.parse_long_full)
        #     request.item = item
        #     request.allComments = comments
        #     request.currentComment = comments[status.get("index") + 1]
        #     request.status = {
        #         "index": status.get("index") + 1,  # 现在是第几个
        #         "len": len(comments),  # 总长度
        #     }  # 用来判断长评论有没有抓完
        #     request.info = sub_info
        #     yield request
        #     time.sleep(self.SLEEP)

        # 判断是否是长评论最后一页的最后一个
        if sub_info["commentStatus"]["long"] and status.get("index") == status.get("len") - 1:
            print("完整剧评最后一页", sub_info.get("title"))
            sub_info["commentStatus"]["full"] = True
            for field in item.fields:
                if field in sub_info.keys():
                    item[field] = sub_info[field]

            if sub_info["commentStatus"]["short"] and \
                    sub_info["commentStatus"]["long"] and \
                    sub_info["commentStatus"]["full"]:
                yield item

# TODO 详情页有图片没有写  短评头像没有抓
