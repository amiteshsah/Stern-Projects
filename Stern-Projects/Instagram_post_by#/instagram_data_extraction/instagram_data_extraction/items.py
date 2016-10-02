# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramDataExtractionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	Username=scrapy.Field()
	Date_posted=scrapy.Field()
	Post=scrapy.Field()
	Hashtag_list=scrapy.Field()
	Likes=scrapy.Field()
	Comments=scrapy.Field()
	image_urls=scrapy.Field()
	#image_location=scrapy.Field()
	Post_url=scrapy.Field()
	images = scrapy.Field()


