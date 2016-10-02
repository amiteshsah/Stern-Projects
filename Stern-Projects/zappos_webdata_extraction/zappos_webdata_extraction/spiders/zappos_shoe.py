# -*- coding: utf-8 -*-
#scraps each product information in detail, e.g. name, price, rating, brand, review, product information and images
#Another program zappos_data_extracttion is responsible for extracting all the product name .
import scrapy
import urlparse
from zappos_webdata_extraction.items import ZapposWebdataExtractionItem

a=['five_star_per','four_star_per','three_star_per','two_star_per','one_star_per']

class MySpider(scrapy.Spider):
	name = "zapposshoe"
	allowed_domains = ["zappos.com"]
	start_urls =[
		"http://www.zappos.com/womens-heels~Nk"
		]
	base_url="http://www.zappos.com"
	seen_urls=[]
	
	list_names=[]

	#def __init__(self,  *args, **kwargs):
	#	super(MySpider, self).__init__(*args, **kwargs)
	#	self.total_names = 



	def parse(self, response):
		urls = response.xpath('//div[@id="searchResults"]/a/@href').extract()
		
		#print cat
				#yield{'URLS':urls}
		#item=ZapposWebdataExtractionItem()
		#N_product=len(urls)
		#print "Total number of product :"+str(N_product)
		for url in urls:
			#yield{'Url':url}
			self.list_names.append(url)
			absolute_url = response.urljoin(url)
			request = scrapy.Request(absolute_url, callback=self.parse_eachshoe)
			yield request

		# process next page
		next_page_url = response.xpath(u'//a[contains(text(),"\u00bb")]/@href').extract_first()
		absolute_next_page_url = response.urljoin(next_page_url)
		request = scrapy.Request(absolute_next_page_url)
		yield request



	def parse_eachshoe(self, response):
		#name = response.xpath(
		#	'//div[@class="mapContainer"]/@data-name').extract_first()
		item=ZapposWebdataExtractionItem()
		path_product=response.xpath('/html/head/meta[8]/@content').extract_first()
		item['name']=path_product.split('http://www.zappos.com')[1]
		item['rating'] = response.xpath('//a[@href="#productReviews"]/meta[@itemprop="ratingValue"]/@content').extract_first()
		for i in range(1,6):
			item[a[i-1]]=response.xpath('//*[@id="reviewSummary"]/ul/li[%d]/span[2]/text()'%i).extract()
		# item['four_star_per']=response.xpath(
		# 	'//*[@id="reviewSummary"]/ul/li[2]/span[2]/text()').extract()
		# item['three_star_per']=response.xpath(
		# 	'//*[@id="reviewSummary"]/ul/li[3]/span[2]/text()').extract()
		# item['two_star_per']=response.xpath(
		# 	'//*[@id="reviewSummary"]/ul/li[4]/span[2]/text()').extract()
		# item['one_star_per']=response.xpath(
		# 	'//*[@id="reviewSummary"]/ul/li[5]/span[2]/text()').extract()
		item['review']= response.xpath('//a[@href="#productReviews"]//span[@itemprop="reviewCount ratingCount"]/text()').extract_first()
		item['price'] = response.xpath('//div[@id="priceSlot"]/span/text()').extract()
		item['brand']=response.xpath('///h1[@class="banner"]/a[@href]/text()').extract()
		item['item_information']=response.xpath('//*[@id="productDescription"]/div/div/ul//li/text()').extract()

		#Total 7 images link
		#item['image_urls'] = link1[0]+str(response.xpath('//div[@id="angles-vertical"]/ul/li/a[@id]/@href').extract_first())
		

		#url = response.xpath('//div[@id="angles-vertical"]/ul/li/a[@id]/@href').extract_first()
		#item['image_urls']  = urlparse.urljoin(self.base_url, url)
		#print item['image_urls']
		
		

		#link=str(response.xpath('//div[@id="angles-vertical"]/ul/li/a[@id]/@href').extract_first())
		#item['image_urls'] = ['http://www.zappos.com' + link]
		#if (not link in self.seen_urls):
		#	self.seen_urls.append(link) 
		#	yield


		images = response.xpath('//div[@id="angles-vertical"]/ul/li/a[@id]/@href').extract()
		item['image_urls'] = ['http://www.zappos.com' + str(image) for image in images]

		#longitude = response.xpath(
		#	'//div[@class="mapContainer"]/@data-lng').extract_first()
#		shoe = {
#			'Rating': rating
#			'5star':five_star_per,
#			'4star':four_star_per,
#			'3star':three_star_per,
#			'2star':two_star_per,
#			'1star':one_star_per,
#			'Reviews': reviews,
#			'Price': price,
#			'Brand':brand,
#			'name': response.url
#			}
#		yield shoe
		yield item

