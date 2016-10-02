import scrapy
import json
from selenium import webdriver
import time
import pickle
import re
import os.path as op
import os
from selenium.webdriver.support.ui import WebDriverWait
# check if directory exists, if not, make it
# directory='instagram_images/'
# if not op.exists(directory):
#     os.makedirs(directory)
import urllib

from instagram_data_extraction.items import InstagramDataExtractionItem

username_list=[]
class Instagram_spider(scrapy.Spider):
	name="instagram"
	allowed_domains = ["instagram.com"]
	# start_urls =[
	# 	"https://www.instagram.com/explore/tags/nomoney/"
	# 	]
	start_urls=["https://www.instagram.com/explore/tags/rich/"]
	seen_urls=[]
	
	list_names=[]


	def __init__(self):
		#self.driver = webdriver.Firefox()
		self.driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
		#self.driver = webdriver.PhantomJS()
		self.driver.set_window_size(1200,800)
		self.PAUSE=2
		self.count=7000
		self.count=0


	def parse(self, response):
		self.driver.get('https://www.instagram.com/explore/tags/rich/')
    #driver.get('https://www.instagram.com/explore/tags/nomoney/')
		all_data_links=[]

# 		#load_link_element=driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div/a').click()
# 		#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 		#time.sleep(5)
# 		#scroll_to_bottom = get_scroll_count(self.count)
# 		element = self.driver.find_element_by_css_selector('a._oidfu')
# 		self.driver.implicitly_wait(self.PAUSE)
# 		element.click()


# 		pause = 0.2
# 		lastHeight = self.driver.execute_script("return document.body.scrollHeight")
# 		print "last:"+str(lastHeight)
# 		i = 0
# 		n=0
# 		#browser.get_screenshot_as_file("test03_1_"+str(i)+".jpg")
# 		while True:
# 			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 			time.sleep(pause)
# 			newHeight = self.driver.execute_script("return document.body.scrollHeight")
# 			print "New:"+str(newHeight)+":"+str(i)
# 			num_link=len(self.driver.find_elements_by_xpath("//*[@id]/section/main/article/div/div/div/a"))
# 			print "Number of link:"+str(num_link)
# 			time.sleep(0.2)
# #			if newHeight == lastHeight:
# #				self.driver.execute_script("window.scrollTo(0, 0);")
# #				time.sleep(5)

# 			# 	break
# 			n=0
# 			while (newHeight == lastHeight):
# 					self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 					time.sleep(0.2)
# 					self.driver.execute_script("window.scrollTo(0, 0);")
# 					time.sleep(0.2)
# 					n=n+1
# 					newHeight = self.driver.execute_script("return document.body.scrollHeight")
# 					if n==25 or n==45:
# 						time.sleep(4)
# 						self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 						time.sleep(4)
# 						self.driver.execute_script("window.scrollTo(0, 0);")
# 						time.sleep(0.2)
# 						self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 						time.sleep(0.2)
# 						self.driver.implicitly_wait(10)
# 					newHeight = self.driver.execute_script("return document.body.scrollHeight")
# 					if n==50:
# 						break
# 			if n==50:
# 				break
			
# 			lastHeight = newHeight
# 			i += 1
# 			if num_link>=6000:
# 				break

# 			#alternative way to scroll
# 		# for y in range(int(scroll_to_bottom)):
# 		# 	self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#   #   		time.sleep(0.2)
#   #   		self.driver.execute_script("window.scrollTo(0, 0);")
#   #   		time.sleep(0.2)
		    

# 		video_links=[]    
# 		try:    
# 			video_links=self.driver.find_elements_by_xpath("//a[.//*[@class='_1lp5e']]").get_attribute('href')
# 			#print video_links
# 		except Exception: 
# 			pass
# 		#print video_links
# 		for link in self.driver.find_elements_by_xpath("//*[@id]/section/main/article/div/div/div/a"):
# 			url=link.get_attribute('href')
# 			if url not in video_links:
# 				all_data_links.append(url)

# 		print "\nTotal image link:\n"+str(len(all_data_links))
		
# 		file = open('link_list3.txt', 'w')
# 		pickle.dump(all_data_links, file)
# 		file.close()

#line 44 to 125 is made comment and line 129 to 134 is added to read the link_list1.txt

		friend=[]
		file = open("link_list3.txt", "r")
		friend = pickle.load(file)
		file.close()
		all_data_links=friend[:]

		crawl_urls=all_data_links[:]
		for link in all_data_links:
			yield scrapy.Request(link,meta={'link':link}, callback=self.each_user_data)
			#yield scrapy.Request(crawl_urls.pop(0),meta={'link':link}, callback=self.each_user_data)
				

	def each_user_data(self,response):
		link=response.request.meta['link']
		self.driver.get(link)
		self.count+=1
		print "Counting: "+str(self.count)
		username_element=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div/a')
		username=username_element.text
		if username not in username_list:
		#if True:
			username_list.append(username)

			date_element=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/a/time')
			date=date_element.get_attribute('datetime')

			post_element=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/ul/li[1]/h1/span')
			post=post_element.text

			tag_list=[]
			hashtag_element=self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/ul/li[1]/h1/span/a')
			for tag_element in hashtag_element:
				tag=tag_element.text
				if tag_element.get_attribute('class')!='notranslate':
					tag_list.append(tag)
	        
			try:
				likes_element=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/div/span[@class]/span')
				likes=likes_element.text
			except:
				likes_element_list=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div/section[1]/div/a').text
				likes=str(len(likes_element_list))

	        #like_view_element=driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/div/span/text()')
	        #like_view=like_view_element.text

			comments={}
			comment_expansion=[]
			try:
				comment_expansion=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/ul/li[2]/button')
			except Exception: 
				pass
			if comment_expansion:
				self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/ul/li[2]/button').click();
			comment_element_list=self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/ul/li/span')
			for k,comment_element in enumerate(comment_element_list):
				comments[k+1]=comment_element.text


			#download images
			image_link_element=self.driver.find_element_by_xpath('//div/img[@class]')
			image_link=image_link_element.get_attribute('src')
			# photo_url=image_link
			# photo_url = photo_url.replace('\\', '')
			# photo_url = re.sub(r'/s\d+x\d+/', '/', photo_url)
			# photo_url = re.sub(r'/\w+\.\d+\.\d+\.\d+/', '/', photo_url)
			# photo_url=photo_url.split('?')[0]
			# photo_basename = op.basename(photo_url)
			#photo_name = op.join(directory, photo_basename)
			#urllib.urlretrieve(link, photo_name)

			#image location in directory
			#image_location=photo_name

			item1= yield_data(username,date,post,tag_list,likes,comments,image_link,link)
			#print "\nItem list:"+str(item1)
			yield item1

def yield_data(username,date,post,tag_list,likes,comments,image_link,link):
	item=InstagramDataExtractionItem()
	item['Username']=username
	item['Date_posted']=date
	item['Post']=post
	item['Hashtag_list']=tag_list
	item['Likes']=likes
	item['Comments']=comments
	item['image_urls']=[image_link]
	#item['image_location']=image_location
	item['Post_url']=link
	return item

# def scroll_page(self):
#     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(0.05)
#     self.driver.execute_script("window.scrollTo(0, 0);")
#     time.sleep(0.05)

def get_scroll_count(count):
	return (int(count) - 24) / 12 + 1






