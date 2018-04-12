import urllib2
import json
#reddit_json = urllib2.urlopen("http://www.reddit.com/.json").read()
reddit_json = open("reddit.txt").read()
#print len(reddit_json)
r = json.loads(reddit_json)
r_data = r['data']
r_data_children = r_data['children']


downs=0
ups=0
difTitle = ""
maxUpsDown = 0
tornadoTitles = list()

for dic in r_data_children:
    downs+=dic["data"]["downs"]
    ups+=dic["data"]["ups"]
    if(dic["data"]["ups"]-dic["data"]["downs"]>maxUpsDown):
        difTitle = dic["data"]["title"]
        maxUpsDown = dic["data"]["ups"]-dic["data"]["downs"]
    if not (dic["data"]["title"].find("tornado") == -1):
        tornadoTitles.append(dic["data"]["title"])
#r_data_children0 = r_data_children[0]
print "ups: %d" % ups
print "downs: %d" % downs
print "Fastest riser up/down dif: %s" % maxUpsDown
print "Fastest riser: %s" % difTitle
print "Tornado Titles:"
print tornadoTitles
