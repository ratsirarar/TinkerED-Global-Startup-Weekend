import sys
sys.path.insert(0, 'libs')

import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from get_data import Startup

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

	def get(self):
		data = Startup.query()
		data = data.order(-Startup.vote)
		template_values = {
		'startups': data,
		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)