# -*- coding: utf-8 -*-
import scrapy


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanMovie'
    allowed_domains = ['movie.douban.com/top250']
    start_urls = ['http://movie.douban.com/top250/']

    def parse(self, response):
        pass
