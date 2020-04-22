# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import json
client = MongoClient()
collection = client['jdbook']['book']

class JdbookPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'book':
            collection.insert(item)
        return item

class DangdangPipeline(object):
    def process_item(self,item,spider):
        if spider.name=='dangdang':
            with open('dangdang.tst','a',encoding='utf-8') as f:
                f.write(json.dumps(item,ensure_ascii=False,indent=2))
                print('\n')
        return item