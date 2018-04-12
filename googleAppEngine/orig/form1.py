import webapp2
import logging


form = """
<form method="post" action="/testform">
<input name="q">
<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):   
    def get(self):
    	logging.info("***** MainPage GET *****")
        self.response.headers['Content-Type']='text/html'  
        self.response.write(form) # write blank form

class TestHandler(webapp2.RequestHandler):
    def post(self):
        logging.info("***** TestHandler POST *****")
        q = self.request.get("q")  # get 'q' from request
        logging.info("*** q=" + str(q) + " type=" + str(type(q)))
        self.response.write(q)     # write the 'q' value

application = webapp2.WSGIApplication([
    ('/', MainPage),   # maps the URL '/' to MainPage
    ('/testform', TestHandler),   
], debug=True)
