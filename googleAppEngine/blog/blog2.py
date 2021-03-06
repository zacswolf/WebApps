import webapp2
import logging
import jinja2
import os
import re
import cgi
import hashlib
import hmac
import random
import string
import time

from datetime import datetime, timedelta
from google.appengine.ext import db

# Jinja Setup
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

class Users(db.Model):
	username = db.StringProperty()
	pw_hash = db.StringProperty()
	email = db.StringProperty()

class Handler(webapp2.RequestHandler):
	def write(self, *items):    
		self.response.write(" : ".join(items))

	def render_str(self, template, **params):
		tplt = JINJA_ENVIRONMENT.get_template('templates/'+template)
		return tplt.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def hash_str(self,s):
		return hmac.new("imsosecret",s).hexdigest()
	def make_secure_val(self, s):
		return "%s|%s" % (s, self.hash_str(s))
	def check_secure_val(self, h):
		array = h.split("|")
		if (self.hash_str(array[0]) == array[1]):
			return array[0]
	def make_salt(self):
		salt = ""
		for i in range(24):
			salt += random.choice(string.hexdigits)
		return salt
	def make_pw_hash(self, name,pw,salt=None):
		if not salt:
			salt = self.make_salt()
		return "%s|%s" % (self.hash_str(name + pw + salt), salt)
	def valid_pw(self, name,pw,h):
		array = h.split("|")
		if (self.make_pw_hash(name, pw, array[1]) == h): # WORK HERE
			return True
		return False
	def time_plus(self, time, timedelta): # Copied from online
		start = datetime(2000, 1, 1, hour=time.hour, minute=time.minute, second=time.second)
		end = start + timedelta
		return end.time()
	def checkCookieTampering(self):
		user_id = self.request.cookies.get('user_id')
		try:
			if not self.check_secure_val(user_id):
				self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
				return False
		except:
			self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
			return False
		array = user_id.split("|")
		return Users.get_by_id(long(array[0])).username
	def validateCreds(self):
		if not self.checkCookieTampering():
			self.redirect("/blog")
		else:
			return self.checkCookieTampering() #username


# Regex
USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^$|^\S+?@\S+?.\S+?$")

# Checking Regex
def valid_username(username):
		return USERNAME_RE.match(username)
def valid_password(password):
		return PASSWORD_RE.match(password)
def valid_email(email):
		return EMAIL_RE.match(email)
def escape_html(s):
	return cgi.escape(s, quote = True)


# Templates
def getForm(self,u="",p="",v="",e="",user="",passw="",ver="",ema=""):
	template_values = {"usernameError": escape_html(u), "passwordError": escape_html(p), "verifyError": escape_html(v), "emailError": escape_html(e), "username": escape_html(user), "password": "", "verify": "", "email": escape_html(ema)}
	template = JINJA_ENVIRONMENT.get_template('templates/base.html')
	self.response.write(template.render(template_values))
def getLoginForm(self,u="",user="",passw=""):
	template_values = {"Error": escape_html(u), "username": escape_html(user), "password": ""}
	template = JINJA_ENVIRONMENT.get_template('templates/login.html')
	self.response.write(template.render(template_values))
def getWelcome(self, name=""):
	template_values = {"name":escape_html(name)}
	template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
	self.response.write(template.render(template_values))



# Pages
class MainPage(Handler):   
		def get(self):
			logging.info("***** MainPage GET *****")
			self.response.headers['Content-Type']='text/html'  
			getForm(self) # write blank form
		def post(self):
			logging.info("***** TestHandler POST *****")
			# Getting info from form
			username = self.request.get("username")
			password = self.request.get("password")
			verify = self.request.get("verify")
			email = self.request.get("email")

			error = "That's not a valid "
			u = ""
			p = ""
			v = ""
			e = ""

			query = db.GqlQuery("SELECT * FROM Users WHERE username = '%s'" % username)
			logging.info("***** query.count() %s *****" % query.count())
			if not query.count() == 0:
				u = "That user already exist"
			elif not valid_username(username):
				u = error + "username."
			if not valid_password(password):
				p = error + "password."
			if password != verify:
				v = "Passwords do not match."
			if not valid_email(email):
				e = error + "email."

			if u+p+v+e=="":
				userInst = Users()
				userInst.username = username
				userInst.pw_hash = self.make_pw_hash(username, password)
				userInst.email = email
				userInst.put()
				time.sleep(0.2)
				val = self.make_secure_val(str(userInst.key().id()))
				user_id = self.request.cookies.get('user_id', val)
				self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % val)
				
				

				self.redirect("/blog/welcome")

			logging.info("*** username=" + str(username) + " type=" + str(type(username)))
			getForm(self,u,p,v,e,username,password,verify,email)


class LoginPage(Handler):   
		def get(self):
			logging.info("***** MainPage GET *****")
			self.response.headers['Content-Type']='text/html'  
			getLoginForm(self) # write blank form
		def post(self):
			logging.info("***** TestHandler POST *****")
			# Getting info from form
			username = self.request.get("username")
			password = self.request.get("password")
			
			error = "That's not a valid "
			u = ""
			

			query = db.GqlQuery("SELECT * FROM Users WHERE username = '%s'" % username)
			logging.info("***** query.count() %s *****" % query.count())
			logging.info("***** query.get() %s*****" % query.get())
			if not query.count() == 0 and self.valid_pw(username,password,query.get().pw_hash):
				val = self.make_secure_val(str(query.get().key().id()))
				user_id = self.request.cookies.get('user_id', val)
				self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % val)
				self.redirect("/blog/welcome")
			else:
				u = "Invalid Login"

			logging.info("*** username=" + str(username) + " type=" + str(type(username)))
			getLoginForm(self,u, "", "")


class WelcomePage(Handler):   
		def get(self):
			logging.info("***** MainPage GET *****")
			self.response.headers['Content-Type']='text/html'
			if not self.checkCookieTampering():
				self.redirect("/blog/login")
			else:
				getWelcome(self, self.checkCookieTampering())








class Post(db.Model):
	subject = db.StringProperty()
	content = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add=True)
	



# Pages
class MainBlogPage(Handler): 
	def render_blogs(self):
		user_id = self.request.cookies.get('user_id')
		self.checkCookieTampering()
		self.response.headers['Content-Type']='text/html'	
		posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC limit 10")
		self.render("posts.html", posts=posts, time_plus=self.time_plus, timedelta=timedelta)
	def get(self):
		logging.info("***** MainPage GET *****")
		self.response.headers['Content-Type']='text/html'  
		self.render_blogs()

class Newpost(Handler):
	def get(self):
		logging.info("***** Newpost GET *****")
		self.response.headers['Content-Type']='text/html'
		self.checkCookieTampering()
		self.validateCreds()
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

class ProductHandler(Handler):   
	def get(self, id):
		logging.info("***** ProjectHandler GET *****")
		self.response.headers['Content-Type']='text/html'
		self.checkCookieTampering()
		post = Post.get_by_id(int(id))
		self.render("permalink.html", Postnumber=id, post=post, time_plus=self.time_plus, timedelta=timedelta)





class LogoutPage(Handler):   
		def get(self):
			logging.info("***** LogoutPage GET *****")
			self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
			self.redirect("/blog/login")
			


# Web App Stuff
application = webapp2.WSGIApplication([ 
		(r'^/blog/newpost/?$', Newpost),
		(r'^/blog/(\d+)/?$', ProductHandler),
		(r'^/blog/signup/?$', MainPage),
		(r'^/?(?:blog/?)?$', MainBlogPage),
		(r'^/blog/login/?$', LoginPage),
		(r'^/blog/logout/?$', LogoutPage),
		(r'^/blog/welcome/?$', WelcomePage)

], debug=True)
