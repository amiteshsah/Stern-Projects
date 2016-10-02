# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
import sqlite3 as lite

from data_extraction import settings
from data_extraction import items
con=None

class DataExractionPipeline(ImagesPipeline):
    #def process_item(self, item, spider):
    #   return item

	def set_filename(self, response):
        return 'full/{0}.jpg'.format(response.meta['title'][0])

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'title': item['title']})

    def get_images(self, response, request, info):
        for key, image, buf in super(ZapposWebdataExtractionPipeline, self).get_images(response, request, info):
            key = self.set_filename(response)
        yield key, image, buf

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter

# class CSVPipeline(object):

#   def __init__(self):
#     self.files = {}

#   @classmethod
#   def from_crawler(cls, crawler):
#     pipeline = cls()
#     crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
#     crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
#     return pipeline

#   def spider_opened(self, spider):
#     file = open('%s_items.csv' % spider.name, 'w+b')
#     self.files[spider] = file
#     self.exporter = CsvItemExporter(file)
#     self.exporter.fields_to_export = [list with Names of fields to export - order is important]
#     self.exporter.start_exporting()

#   def spider_closed(self, spider):
#     self.exporter.finish_exporting()
#     file = self.files.pop(spider)
#     file.close()

#   def process_item(self, item, spider):
#     self.exporter.export_item(item)
#     return item