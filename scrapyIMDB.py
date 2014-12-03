from scrapy import Spider, Item, Field
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log

class Listing(Item):
    date = Field()
    time = Field()
    station = Field()
    info = Field()

class ImdbSpider(Spider):
	name, start_urls = 'imdbspider', ['http://www.imdb.com/title/tt0098904/tvschedule']

	def parse(self, response):
		rows = response.css(".dataTable tr")
		myListings = []
		for index, tr in enumerate(rows):
			listing = tr.css('td a::text').extract()
			listingClass = Listing(date=listing[0],time=listing[1],station=listing[2],info=listing[3])
			myListings.append(listingClass)

		return myListings
