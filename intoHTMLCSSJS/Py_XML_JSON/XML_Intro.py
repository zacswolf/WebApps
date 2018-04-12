import urllib2

response1 = urllib2.urlopen("http://www.example.com")
print response1.headers["Last-Modified"]

response2 = urllib2.urlopen("http://www.statesman.com")
print response2.headers["Server"]

response3 = urllib2.urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
print response3.headers["Age"]

