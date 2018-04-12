import webapp2
import logging
import jinja2
import os
import re
import cgi
import time
from datetime import datetime, timedelta
from google.appengine.ext import db


# Jinja Setup
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])





class Post(db.Model):
	subject = db.StringProperty()
	content = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add=True)


# Templates
class MyHandler(webapp2.RequestHandler):
	def write(self, *writeArgs):    
		self.response.write(" : ".join(writeArgs))

	def render_str(self, template, **params):
		tplt = JINJA_ENVIRONMENT.get_template('templates/'+template)
		return tplt.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def time_plus(self, time, timedelta): # Copied from online
		start = datetime(2000, 1, 1, hour=time.hour, minute=time.minute, second=time.second)
		end = start + timedelta
		return end.time()
	


# Pages
class MainPage(MyHandler): 
	def render_blogs(self):
		posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC limit 10")
		self.render("posts.html", posts=posts, time_plus=self.time_plus, timedelta=timedelta)

	def get(self):
		logging.info("***** MainPage GET *****")
		self.response.headers['Content-Type']='text/html'  
		self.render_blogs()



class Newpost(MyHandler):   
	def get(self):
		logging.info("***** Newpost GET *****")
		self.response.headers['Content-Type']='text/html'  
		self.render("newpost.html")
	def post(self):
		logging.info("***** Newpost POST *****")
		self.response.headers['Content-Type']='text/html'

		subject = self.request.get("subject")
		content = self.request.get("content")

		if (subject and content):
			postInst = Post()
			postInst.subject = subject
			postInst.content = content 
			postInst.put()
			time.sleep(0.2)
			postInst.key().id()
			self.redirect("/blog/%s" % postInst.key().id())

		else:
			self.render("newpost.html", ph_subject=subject, ph_content=content, 
				ph_error="Please provide both a subject and content")

class ProductHandler(MyHandler):   
	def get(self, id):
		logging.info("***** ProjectHandler GET *****")
		self.response.headers['Content-Type']='text/html'
		post = Post.get_by_id(int(id))
		self.render("permalink.html", Postnumber=id, post=post, time_plus=self.time_plus, timedelta=timedelta)

		 




# Web App Stuff
application = webapp2.WSGIApplication([
		('/', MainPage),
		(r'^/blog/?$', MainPage),   # maps the URL '/' to MainPage  
		(r'^/blog/newpost/?$', Newpost),
		(r'^/blog/(\d+)$', ProductHandler)
], debug=True)
