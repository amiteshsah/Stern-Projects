# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
from scrapy.pipelines.images import ImagesPipeline
import sqlite3 as lite
from instagram_data_extraction import settings
from instagram_data_extraction import items
con = None

class InstagramDataExtractionPipeline(ImagesPipeline):
    def set_filename(self, response):
        return 'instagram_images_rich/{0}.jpg'.format(response.meta['title'][0])

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'title': item['title']})

    def get_images(self, response, request, info):
        for key, image, buf in super(ZapposWebdataExtractionPipeline, self).get_images(response, request, info):
            key = self.set_filename(response)
        yield key, image, buf
