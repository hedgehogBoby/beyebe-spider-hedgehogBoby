# -*- coding:utf-8 -*-
from scrapy import cmdline  # 引入命令行

cmdline.execute('scrapy crawl sougou'.split())

'''
cd /root/zywa-spider-xiaociwei/zywa_small_helper/sougouTop/sougouTop
nohup python3 -u /root/zywa-spider-xiaociwei/zywa_small_helper/sougouTop/sougouTop/start.py &
'''
