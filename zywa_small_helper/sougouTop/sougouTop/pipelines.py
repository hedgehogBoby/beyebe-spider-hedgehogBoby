# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys

# sys.path.append("../../../")
from zywa_alarm_httpserver.cang_client.mongoClient import CangMongoClient


class SougoutopPipeline(object):

    def open_spider(self, spider):
        self.client = CangMongoClient(db='xiaociwei', user='xiaociweiRWUser', password='zywaXIAOCIWEI@!!!')
        self.db = self.client.new_db

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db["train_hotword"].insert(dict(item))
        return item
