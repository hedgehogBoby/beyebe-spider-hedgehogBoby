import time

from hedgehog_base_core.dao.redis.redisTest import poolList, redisLPush
from hedgehog_spider_download.downloadDealImp import DownloadDealImp
from hedgehog_spider_download.helper.scrapy.scrapyRequestStart import scrapyDownloadstart


class ScrapyDealImp(DownloadDealImp):
    def __init__(self):
        scrapyDownloadstart()

    def deal(self, url):
        redisLPush(1, 'hedgehog_scrapy:strat_urls', url)

    def version(self):
        return super().version()


if __name__ == '__main__':
    while True:
        print('add_One')
        ScrapyDealImp().deal("http://www.baidu.com")
        time.sleep(0.1)
