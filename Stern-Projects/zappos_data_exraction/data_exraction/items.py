# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html



# import scrapy
# class DataExractionItem(scrapy.Item):
# 	ATTRIBUTE_MAPPINGS={"Women's Size":"womens_size", "Women's Width":"womens_width",'Styles':"styles",'Heel Height':"heel_height",'Heel Style':"heel_style", 'Occasion':"occasion", 'Color':"color", 'Price':"price",'Brand':"brand",'Toe Style':"toe_style", 'Materials':"materials", 'Insole':"insole", 'Theme':"theme",'Pattern':"pattern",'Accents':"accents"}
# 	category=scrapy.Field()
# 	name=scrapy.Field()
# 	womens_size=scrapy.Field()
# 	womens_width=scrapy.Field()
# 	styles=scrapy.Field()
# 	heel_height=scrapy.Field()
# 	heel_style=scrapy.Field()
# 	occasion=scrapy.Field()
# 	color=scrapy.Field()
# 	price=scrapy.Field()
# 	brand=scrapy.Field()
# 	toe_style=scrapy.Field()
# 	materials=scrapy.Field()
# 	insole=scrapy.Field()
# 	theme=scrapy.Field()
# 	pattern=scrapy.Field()
# 	accents=scrapy.Field()
# 	Others=scrapy.Field()

from scrapy.item import Item, Field
class DataExractionItem(Item):
	def __setitem__(self, key, value):
		if key not in self.fields:
			self.fields[key] = Field()
		self._values[key] = value