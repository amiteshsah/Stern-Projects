# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZapposWebdataExtractionItem(scrapy.Item):
    # define the fields for your item here like:
	name = scrapy.Field()
	brand=scrapy.Field()
	price=scrapy.Field()
	rating=scrapy.Field()
	review=scrapy.Field()
	five_star_per=scrapy.Field()
	four_star_per=scrapy.Field()
	three_star_per=scrapy.Field()
	two_star_per=scrapy.Field()
	one_star_per=scrapy.Field()
	item_information=scrapy.Field()

	image_urls = scrapy.Field()
	images = scrapy.Field()


# class ZapposWebdataExtractionItem2(scrapy.Item):
# 	name=scrapy.Field()
# 	womens_width=scrapy.Field()
# 	styles=scrapy.Field()
# 	heel_height=scrapy.Field()
# 	heel_style=scrapy.Field()
# 	occasion=scrapy.Field()
# 	color=scrapy.Field()
# 	brand=scrapy.Field()
# 	toe_style=scrapy.Field()
# 	materials=scrapy.Field()
# 	insole=scrapy.Field()
# 	theme=scrapy.Field()
# 	pattern=scrapy.Field()
# 	accents=scrapy.Field()
