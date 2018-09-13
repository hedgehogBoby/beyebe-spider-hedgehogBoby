# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class DoubanItem(scrapy.Item):
    movieId = Field()  # 电影id
    movieUrl = Field()  # 电影链接
    title = Field()  # 电影名      string
    ratingValue = Field()  # 评分 string
    ratingPeople = Field()  # 评分人数   int
    directors = Field()  # 导演  list
    casts = Field()  # 编剧  list
    coverUrl = Field()  # 封面地址 string
    actors = Field()  # 主演  list
    category = Field()  # 一级分类  影视
    tags = Field()  # 二级分类  list
    country = Field()  # 制片国家/地区
    movieLanguage = Field()  # 语言
    pubDate = Field()  # 发布日期  数组 因为有的会有中国和其它国家的发布日期
    runtime = Field()  # 电影时长 int 秒
    titleOthers = Field()  # 又名
    IMDbUrl = Field()  # IMDb 链接
    introduction = Field()  # 简介
    won = Field()  # 获奖情况
    comments = Field()  # 影评  作者 + 影评链接
    etc = Field()  # 其它字段  dict
