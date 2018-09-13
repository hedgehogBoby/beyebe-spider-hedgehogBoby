# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from zywa_database_core.dao.mongo.mongoClientNew import db_spider


class WangyiyunPipeline(object):
    def process_item(self, item, spider):
        try:
            db_spider['music_163'].insert_one(dict(item))
        except:
            pass
        try:
            db_spider['music_total'].insert_one(dict(item))
        except:
            pass
        return item
