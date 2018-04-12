import webapp2
import logging

from random import *

num = 0

def randNum():
    global num
    num = randint(1,100)
    return num

def form(_num):
    formA = """
    <style>
        body{
            text-align: center;
            background-color: rgb("""
    formB = "%d,%d,%d" % (2*_num,3*_num,4*_num)
    formC = """);
        }
        h1{
            color: blue;
        }
        p{
            color: green;
        }
        div {
            position: relative;
            top: 50%;
            transform: translateY(-50%);
            border: 5px solid yellow;
            border-radius: 5px
        }
        h3{
            color: red;
        }
    </style>
    <div>
        <h1> Good luck </h1>
        <form method="post" action="/">
        <p>Enter Guess:</p> <input name="q">
        <br>
        <input type="submit">
        </form>
        <br>
    """
    form = formA+formB+formC
    return form




class MainPage(webapp2.RequestHandler):   
    def get(self):
        global num 
        randNum()
    	logging.info("***** MainPage GET *****")
        self.response.headers['Content-Type']='text/html'  
        self.response.write(form(num) + """<h3> Random Number = %d </h3>
            </div>""" % num) # write blank form

    def post(self):
        global num
        logging.info("***** TestHandler POST *****")
        q = self.request.get("q")  # get 'q' from request

        try:
            if(int(q) == num):
                s = "<h1> Congrats your guess is perfect </h1>"
                randNum()
            elif(int(q) > num):
                s = "<h1> Your guess is too high </h1>"
            elif(int(q) < num):
                s = "<h1> Your guess is too low </h1>"
            self.response.write(form(num) + """<h3> Random Number = %d </h3>
                <h3> Guess Number = %d </h3>
                %s
                </div>""" % (num,int(q),s)) # write blank form
        except:
            self.response.write(form(num) + """<h3> Random Number = %d </h3>
            <h1> Your guess is not a number </h1>
            </div>""" % num) # write blank form

        #logging.info("*** q=" + str(q) + " type=" + str(type(q)))
        #logging.info("*** s=" + str(s) + " type=" + str(type(s)))


        


application = webapp2.WSGIApplication([
    ('/', MainPage),   # maps the URL '/' to MainPage  
], debug=True)

