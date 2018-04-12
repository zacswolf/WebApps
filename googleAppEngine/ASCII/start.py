import webapp2
import logging
import re
import jinja2
import os
import time
from google.appengine.ext import db

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])


class Art(db.Model):
	title = db.StringProperty()
	art = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add=True)

CACHE = {} 
cacheUpdated = 0
class MyHandler(webapp2.RequestHandler):
	def write(self, *writeArgs):    
		self.response.write(" : ".join(writeArgs))

	def render_str(self, template, **params):
		tplt = JINJA_ENVIRONMENT.get_template('templates/'+template)
		return tplt.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
	def top_arts(self):
		global CACHE
		global cacheUpdated
		if not cacheUpdated:
			CACHE = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC Limit 10")
			cacheUpdated = 1
		return CACHE

class MainPage(MyHandler):
	def render_ascii(self, title="", art="", error=""):
		arts = self.top_arts()
		self.render("ascii.html", title=title, art=art, error=error, arts=arts)

	def get(self):
		logging.info("********** MainPage GET **********")
		self.render_ascii()

	def post(self):
		global cacheUpdated
		title = self.request.get("title")
		art = self.request.get("art")
		python_dictionary = {}
		if (not (title and art)):
			python_dictionary["title"] = title
			python_dictionary["art"] = art
			python_dictionary["error"] = "Need both a title and some artwork!"   # creating a new dictionary
		else:
			artInst = Art()
			artInst.title = title
			artInst.art = art 
			artInst.put()
			time.sleep(0.2)
			cacheUpdated = 0
		self.render_ascii(**python_dictionary)

class FavoritePage(MyHandler):
	def render_ascii(self, title="", art="", error=""):
		arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC ")
		self.render("ascii.html", title=title, art=art, error=error, arts=arts)

	def render_favorite_ascii(self, title="", art="", error=""):
		art = Art.get_by_id(5275456790069248)
		self.render("favorite.html", title=art.title, art=art.art)

	def get(self):
		logging.info("********** MainPage GET **********")
		self.render_favorite_ascii()


application = webapp2.WSGIApplication([
	('/', MainPage),
	('/favorite', FavoritePage)

], debug=True)
