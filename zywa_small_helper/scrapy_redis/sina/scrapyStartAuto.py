# -*- coding:utf-8 -*-
import __init__
from scrapy import cmdline

if __name__ == '__main__':
    # cmdline.execute("scrapy crawl sina".split())
    cmdline.execute("scrapy runspider /Users/magic/PycharmProjects/beyebe-spider-xiaociwei/zywa_small_helper/scrapy_redis/sina/sinaNews/spiders/SinaSpider.py".split())

