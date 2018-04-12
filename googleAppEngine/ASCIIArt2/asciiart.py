import webapp2
import logging
import re
import cgi
import jinja2
import os
import time

from google.appengine.api import memcache
from google.appengine.ext import db



## see http://jinja.pocoo.org/docs/api/#autoescaping
def guess_autoescape(template_name):
		if template_name is None or '.' not in template_name:
				return False
		ext = template_name.rsplit('.', 1)[1]
		return ext in ('html', 'htm', 'xml')

JINJA_ENVIRONMENT = jinja2.Environment(
		autoescape=guess_autoescape,     ## see http://jinja.pocoo.org/docs/api/#autoescaping
		loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
		extensions=['jinja2.ext.autoescape'])

def escape_html(s):
	 return cgi.escape(s, quote = True)

class Handler(webapp2.RequestHandler):
	 def write(self, *items):    
			self.response.write(" : ".join(items))

	 def render_str(self, template, **params):
			tplt = JINJA_ENVIRONMENT.get_template('templates/'+template)
			return tplt.render(params)

	 def render(self, template, **kw):
			self.write(self.render_str(template, **kw))


class Art(db.Model):
	 title = db.StringProperty()  
	 art = db.TextProperty()
	 created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
		def toparts(self, CacheUpdated = False):
			if CacheUpdated or not memcache.get("blog-post"):
				artQuery = db.GqlQuery("SELECT * FROM Art "
														 "ORDER BY created DESC "
														 "LIMIT 10" )
				logging.info(">>> DATABASE ACCESS <<<")
				memcache.set("blog-post",list(artQuery))
			else: 
				logging.info(">>> CASHE HIT <<<")
			return memcache.get("blog-post")

		def render_ascii(self, title="", art="", error="",_CacheUpdated=False):
			artList = self.toparts(CacheUpdated=_CacheUpdated)
			self.render("ascii.html", title=title, art=art, error=error, arts=artList)

		def get(self):
				logging.info("********** MainPage GET **********")
				self.render_ascii()

		def post(self):
				logging.info("********** MainPage POST *********")

				title = self.request.get("title")
				art   = self.request.get("art")
				
				if title and art:
					 a = Art(title=title,art=art)
					 a.put()
					 time.sleep(0.2)
					 self.render_ascii(_CacheUpdated=True)
					 logging.info("Just POSTED")
				else:
					 error = "we need both a title and some artwork!"
					 self.render_ascii(title, art, error)


application = webapp2.WSGIApplication([
		('/', MainPage)
], debug=True)
