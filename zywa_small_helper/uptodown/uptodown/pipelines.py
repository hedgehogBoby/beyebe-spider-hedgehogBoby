# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from zywa_alarm_httpserver.cang_client.mongoClient import CangMongoClient


class MongoPipeline(object):

    def open_spider(self, spider):
        self.client = CangMongoClient(db='xiaociwei_parse', user='xiaociweiparseRWUser', password='zywaXIAOCIWEI@!!!')
        self.db = self.client.new_db

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db["uptodown_info"].insert(dict(item))
        return item
