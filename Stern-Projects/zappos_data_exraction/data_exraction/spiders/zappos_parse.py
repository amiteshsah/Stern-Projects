#responsible for extracting all the product name , each category and subcategory that it belongs to.
import scrapy
import urlparse
from data_exraction.items import DataExractionItem
from scrapy.loader import ItemLoader
from scrapy.signalmanager import SignalManager
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import json
import itertools

dict1={}
item2=DataExractionItem()
item2['listings']={}
class MySpider(scrapy.Spider):
	name = "zappos"
	allowed_domains = ["zappos.com"]
	start_urls =[
		"http://www.zappos.com/womens-heels~Nk"
		]

	def __init__(self,  *args, **kwargs):
		super(MySpider, self).__init__(*args, **kwargs)
		self.categorys = []#['womens_size','womens_width','styles','heel_height','heel_style','occasion','color','price','brand','toe_style','materials','insole','theme','pattern','accents']
		self.subcat_name='abc'
		self.list12 = []
		SignalManager(dispatcher.Any).connect(self.closed_handler, signal=signals.spider_closed)
		



	def parse(self,response):
		cat = response.xpath('//div[@id="naviCenter"]/h4[@class="stripeOuter navOpen"]/text()[2]').extract()
		cat=[x.strip() for x in cat]
		dict1={key: None for key in cat}
		self.categorys=cat
		length=len(self.categorys)
		
		for i in range(1,16):#16
			crawl_urlslist = [response.urljoin(subcat) for subcat in response.xpath('//div[@id="naviCenter"]/div[@id][%d]/a/@href' % i).extract()]
			#subcat_list=[''.join(map(str,response.xpath('//div[@id="naviCenter"]/div[@id][%d]/a[%d]/text()[1]'%(i,index+1)).extract())).encode('utf-8').strip() for index in range(len(crawl_urlslist))]
			subca=[response.xpath('//div[@id="naviCenter"]/div[@id][%d]/a[%d]/text()[1]'%(i,index+1)).extract() for index in range(len(crawl_urlslist))]
			merged_list = list(itertools.chain.from_iterable(subca))
			subcat_list=[m.strip().encode('utf-8') for m in merged_list]
			#print "The dictionary sublist :"+str(subcat_list)

			dict1[self.categorys[i-1]]={key: [] for key in subcat_list}

		for i in range(1,16):#16
			item=DataExractionItem()
			item[self.categorys[i-1]]={}

			crawl_urls = [response.urljoin(subcat) for subcat in response.xpath('//div[@id="naviCenter"]/div[@id][%d]/a/@href' % i).extract()]
			# print '\nCrawl URL:'+str(crawl_urls)
			# subcat_list=[''.join(map(str,response.xpath('//div[@id="naviCenter"]/div[@id][%d]/a[%d]/text()[1]'%(i,index+1)).extract())).strip() for index in range(len(crawl_urls))]
			# print '\nSubcategory list:'+str(subcat_list)

			#self.list12=[[] for i in range(len(subcat_list))]

			for index, sub_cat in enumerate(response.xpath('//div[@id="naviCenter"]/div[@id][%d]/a/@href' % i).extract()):
				sub_name=response.xpath('//div[@id="naviCenter"]/div[@id][%d]/a[%d]/text()[1]'%(i,index+1)).extract()
				#sub_name_string=''.join(map(str, sub_name))
				self.subcat_name=[m.strip().encode('utf-8') for m in sub_name][0]
				#self.subcat_name=sub_name_string.strip() 
				absolute_url=response.urljoin(sub_cat)
				
				yield scrapy.Request(crawl_urls.pop(0),meta={'item':item,'item2':item2,'category':self.categorys[i-1],'sub_category':self.subcat_name,'dict1':dict1}, callback=self.parse_eachcategory)
				#request.meta['item'] = item
				#yield request
				#print "\ncategory :"+str(self.categorys[i-1])+" , subcat_name54:"+str(self.subcat_name)+", length:"+str(item[self.categorys[i-1]])
		
		#print "The final item:"+str(dict1)
		item2['listings']=dict1.copy()
		yield item2



	def parse_eachcategory(self,response):
		item=response.request.meta['item']
		item2=response.request.meta['item2']
		category=response.request.meta['category']
		sub_category=response.request.meta['sub_category']
		dict1=response.request.meta['dict1']

		cat1=str(category)
		subcat1=str(sub_category).strip('[]')
		name_url=response.xpath('//div[@id="searchResults"]/a/@href').extract()

		dict1[cat1][subcat1].extend(list(name_url))
		#print "\n Category:"+str(cat1)+",subcat:"+str(subcat1)+"\nlength in one loop:"+str(len(name_url))+",total lengthloop:"+str(len(dict1[cat1][subcat1]))

		# Check if there is a 'Next' link
		xpath_Next_Page = u'//a[contains(text(),"\u00bb")]/@href'
		if response.xpath(xpath_Next_Page):
		# No need to calculate offset values. Just take the link ...
			next_page_href = response.xpath(xpath_Next_Page).extract_first()
			url_next_page = response.urljoin(next_page_href)
		# ... build the request ...
			request = scrapy.Request(url_next_page,meta={'item':item,'item2':item2,'category':category,'sub_category':sub_category,'dict1':dict1}, callback=self.parse_eachcategory)
			# ... and add the item with the collected values to the request
			yield request

	def closed_handler(self, spider):
		# Open a file for writing
		out_file = open("test_data1.json","w")

		# Save the dictionary into this file
		# (the 'indent=4' is optional, but makes it more readable)
		json.dump(item2['listings'],out_file, indent=4)                                    

		# Close the file
		out_file.close()
		#print "Found details:"+str(item2)
		