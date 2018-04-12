import webapp2
import logging
import jinja2
import os
import re
import cgi


# Jinja Setup
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

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
def getWelcome(self, name=""):
	template_values = {"name":escape_html(name)}
	template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
	self.response.write(template.render(template_values))


# Globals
name = ""

# Pages
class MainPage(webapp2.RequestHandler):   
		def get(self):
			logging.info("***** MainPage GET *****")
			self.response.headers['Content-Type']='text/html'  
			getForm(self) # write blank form
		def post(self):
			global name
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

			if not valid_username(username):
				u = error + "username."
			if not valid_password(password):
				p = error + "password."
			if password != verify:
				v = "Passwords do not match."
			if not valid_email(email):
				e = error + "email."

			if u+p+v+e=="":
				name = username
				self.redirect("/welcome")

			logging.info("*** username=" + str(username) + " type=" + str(type(username)))
			getForm(self,u,p,v,e,username,password,verify,email)


class WelcomePage(webapp2.RequestHandler):   
		def get(self):
			global name
			logging.info("***** MainPage GET *****")
			self.response.headers['Content-Type']='text/html'  
			getWelcome(self, name)


# Web App Stuff
application = webapp2.WSGIApplication([
		('/', MainPage),   # maps the URL '/' to MainPage  
		("/welcome", WelcomePage)
], debug=True)
