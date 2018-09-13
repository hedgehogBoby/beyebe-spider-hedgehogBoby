# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class MusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    musicId = Field()  # 音乐ID string
    title = Field()  # 歌曲名 string
    singers = Field()  # 歌手 list
    fromType = Field()  # int 千千-1 网易云音乐-2
    album = Field()  # 专辑名 可以为null
