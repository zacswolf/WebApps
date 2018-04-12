import webapp2
import logging


form = """
<h1> Google </h1>
<form method="get" action="http://www.google.com/search">
<input name="q">
<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):   
    def get(self):
    	logging.info("***** MainPage GET *****")
        self.response.headers['Content-Type']='text/html'  
        self.response.write(form) # write blank form

application = webapp2.WSGIApplication([
    ('/', MainPage),   # maps the URL '/' to MainPage
], debug=True)
