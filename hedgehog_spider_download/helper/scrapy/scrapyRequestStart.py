# -*- coding:utf-8 -*-
import os

from scrapy import cmdline


# threading.Thread(target=webDownloadTest, args=('https://tv.sohu.com', 10102,), kwargs={'ippool': True}).start()

def scrapyDownloadstart():
    # current_path = os.path.dirname(__file__)
    # strCD = "cd " + current_path
    # cmdline.execute(strCD.split())

    cmdline.execute("scrapy crawl scrapy_download".split())


if __name__ == '__main__':
    scrapyDownloadstart()
