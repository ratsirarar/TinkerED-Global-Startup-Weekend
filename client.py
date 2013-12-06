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