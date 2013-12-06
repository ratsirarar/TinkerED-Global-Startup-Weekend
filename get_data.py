import sys
sys.path.insert(0, 'libs')

import webapp2
from google.appengine.ext import ndb

import urllib3
from bs4 import BeautifulSoup

class Scrap(object):
	def __init__(self, url=None):
		self.url = url

	def connect_to_page(self, url=None, action='GET'):
		self.url = url if url else self.url
		http = urllib3.PoolManager()
		response = http.request(action, self.url)
		self.response_status = response.status
		self.page_data = response.data
		return self.response_status

	def get_parsed_page(self):
		if self.response_status == 200:
			return BeautifulSoup(self.page_data)
		return


def startup_key(startup_name):
    """Constructs a Datastore key for a Startup entity with startup_name."""
    return ndb.Key('Startup', startup_name)

class Startup(ndb.Model):
	name = ndb.StringProperty(indexed=True)
	img = ndb.StringProperty(indexed=False)
	vote = ndb.IntegerProperty()

class StoreDataPage(webapp2.RequestHandler):

	def get(self):
		self.names = []
		for i in range(1, 24):
			#run scrap multiple times, to mitigate randomness from pool
			for a in range(4):
				scrapper = Scrap("http://globalstartupbattle.agorize.com/en/juries/10/votables?page={0}".format(i))
				scrapper.connect_to_page()
				if scrapper.response_status == 200:
					parsed_data = scrapper.get_parsed_page()
					list_startup_per_page = parsed_data.find_all('div', {'class': 's-votable s-vote-team-box'})
					self._parse_and_store_individual_startup(list_startup_per_page)

		self.response.write("Number of Names: {0}".format(len(self.names)))

	def _parse_and_store_individual_startup(self, startups):
		for startup in startups:
			name = startup.find('span', {"class": "s-votable-name"}).get_text()
			if name not in self.names:
				vote = int(startup.find('div', {"class": "s-vote-count"}).get_text().strip('\n')) 
				img = startup.find('img')['src']
				s = Startup.query(Startup.name==name)
				startup = s.get()
				if startup:
					startup.vote = vote
				else:
					startup = Startup(parent=startup_key(name))
					startup.name=name
					startup.img=img
					startup.vote=vote
				startup.put()
				self.names.append(name)


	


application = webapp2.WSGIApplication([
    ('/tasks/get_data', StoreDataPage),
], debug=True)