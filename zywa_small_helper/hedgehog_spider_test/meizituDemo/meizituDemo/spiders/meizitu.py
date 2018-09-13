from bs4 import BeautifulSoup
from scrapy import Spider, Request


class Meizitu(Spider):
    name = 'meizituDemo'
    start_urls = ['http://www.meizitu.com']

    def parse(self, response):
        text = response.text
        soup = BeautifulSoup(text)
        for item in soup.select('img'):
            print(item['src'])

        for item in soup.select('a'):
            url = item['href']
            yield Request(url=url, callback=self.parse2)

    def parse2(self, response):
        text = response.text
        soup = BeautifulSoup(text)
        for item in soup.select('img'):
            print(item['src'])
