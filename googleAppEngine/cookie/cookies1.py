import webapp2
import logging
import re
import cgi
import jinja2
import os
import hashlib
import hmac

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

class MainPage(Handler):   
	def get(self):
		logging.info("********** MainPage GET **********")
		self.response.headers['Content-Type'] = 'text/plain'
		##1 Assign the variable 'visits' to the value of the 'visits' 
		##1 cookie obtained from the browsers HTTP response. If the cookie 
		##1 does not exist, set the variable 'visits' to '0'

		visits = self.request.cookies.get('visits', self.make_secure_val("0"))

		##2 If the variable visits is an integer (i.e. use str.isdigit())
		##2 increment visits by 1
		##2 else set visits to 0

		if visits.split("|")[0].isdigit() and self.check_secure_val(visits):
			visits = self.make_secure_val(str(int(visits.split("|")[0])+1))
			self.response.headers.add_header('Set-Cookie', 'visits=%s' % visits)
			if int(visits.split("|")[0]) >10000:
				self.write("Congratulations, you have no life")
			else:
				self.write("You have been here %s times!" % visits.split("|")[0])
		else:
			self.write("You can't hack me")
			self.response.headers.add_header('Set-Cookie', 'visits=%s' % self.make_secure_val("0"))



		##3 Add the 'Set-Cookie:' header with the value set to the 
		##3 variable 'visits' to the HTTP response

		

		##4 if visits > 10000, 
		##4   write out a congratulations message
		##4 else
		##4   write out a message stating how many times the user has visited
		
		

	def post(self):
		logging.info("DBG: MainPage POST")

application = webapp2.WSGIApplication([
	('/', MainPage)
], debug=True)
