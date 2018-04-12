import urllib2
from xml.dom import minidom
response = urllib2.urlopen("http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")

x = minidom.parseString(response.read())
print("There are %d items\n" % len(x.getElementsByTagName("item")))

for item in x.getElementsByTagName("item"):
	print(item.getElementsByTagName("title")[0].childNodes[0].nodeValue+"\n")

