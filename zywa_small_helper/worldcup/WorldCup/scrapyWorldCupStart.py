# -*- coding:utf-8 -*-

from scrapy import cmdline
import __init__

# threading.Thread(target=webDownloadTest, args=('https://tv.sohu.com', 10102,), kwargs={'ippool': True}).start()
cmdline.execute("scrapy crawl worldCup".split())
