# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UptodownItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    android_html = scrapy.Field()
    detail_html = scrapy.Field()
    android_url = scrapy.Field()
    android_download_url = scrapy.Field()
    description = scrapy.Field()
    title = scrapy.Field()
    description_article = scrapy.Field()
    search_app_name = scrapy.Field()
    app_name = scrapy.Field()
    logo_url = scrapy.Field()
    app_size = scrapy.Field()
    app_version = scrapy.Field()
    app_publish_date = scrapy.Field()
    app_developer = scrapy.Field()
    app_download_capacity = scrapy.Field()
    short_description = scrapy.Field()
    app_url = scrapy.Field()
    apk_download_url = scrapy.Field()
    app_category = scrapy.Field()
    app_sub_category = scrapy.Field()
    app_detailed_category = scrapy.Field()
    pass
