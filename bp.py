from pyquery import PyQuery as pq
import urllib2

def getListings(url):
	response = urllib2.urlopen(url).read()
	d = pq(response)
	rows = d(".dataTable tr")
	listings = []
	for row in rows:
		tds = row.findall("td")
		listing = []
		
		listings.append([d(tds[0]).text(),d(tds[1]).text(),d(tds[2]).text(),d(tds[3]).text()])

	return listings

url = "http://www.imdb.com/title/tt0098904/tvschedule"
listings = getListings(url)
print listings