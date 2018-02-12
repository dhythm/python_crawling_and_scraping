# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from pymongo import MongoClient

class MyprojectPipeline(object):
    def process_item(self, item, spider):
        return item

class ValidationPipeline(object):
    # Item を検証する Pipeline
    def process_item(self, item, spider):
        if not item['title']:
            raise DropItem('Missing title')
        return item

class MongoPipeline(object):
    # Item を MongoDB に保存する Pipeline
    def open_spider(self, spider):
        # MongoDB に接続する
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['scraping-book']
        self.collection = self.db['items']

    def close_spider(self, spider):
        # MongoDB の接続を切断する
        self.client.close()

    def process_item(self, item, spider):
        # Item をコレクションに追加
        self.collection.insert_one(dict(item))
        return item
