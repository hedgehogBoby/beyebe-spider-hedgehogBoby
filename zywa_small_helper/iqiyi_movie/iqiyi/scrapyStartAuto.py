# -*- coding:utf-8 -*-
import __init__
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl iqiyi".split())
