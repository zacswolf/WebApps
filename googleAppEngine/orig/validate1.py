import webapp2
import logging
import cgi

form = """
<h1>What is your birthday?</h1>
<form method="post" action="/">
	<label>Month</label>
	<input type="text" name="Month" value="%(month)s">
	<label>Day</label>
	<input type="text" name="Day" value="%(day)s">
	<label>Year</label>
	<input type="text" name="Year" value="%(year)s"><br><br>
	<div style="color: red">%(error)s</div>
	<input type="submit">
</form>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

def valid_month(_month):
	month_list = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
	return (_month[:3].lower() in month_list)

def valid_day(_day):
	try:
		return (int(_day) >= 1 and int(_day) <= 31)
	except:
		return False

def valid_year(_year):
	try:
		return (int(_year) >= 1900 and int(_year) <= 2017)
	except:
		return False

def write_form(self, error="", month="", day="", year=""):
    self.response.write(form % {"error": error, "month": month, "day": day, "year": year})

class Success(webapp2.RequestHandler):   
    def get(self):
        self.response.write("Thanks! That's a totally valid day !!!")

class MainPage(webapp2.RequestHandler):   
    def get(self):
        self.response.headers['Content-Type']='text/html'  
        write_form(self)
    def post(self):
    	logging.info("***** POST *****")
        month = self.request.get("Month")
        day = self.request.get("Day")
        year = self.request.get("Year")
        logging.info("*****" + month[:3].lower() +"\t"+ day +"\t"+ year + "*****")
        if (valid_month(month) and valid_day(day) and valid_year(year)):
        	self.redirect("/success")
        else:
        	write_form(self, "That is not correct", escape_html(month), escape_html(day), escape_html(year))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/success', Success),
], debug=True)
