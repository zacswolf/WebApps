import urllib2
from xml.dom import minidom

def get_coords(ip):
    page = urllib2.urlopen("http://www.freegeoip.net/xml/%s" % ip)
    x = minidom.parseString(page.read())
    lat = x.childNodes[0].getElementsByTagName("Latitude")[0].childNodes[0].nodeValue
    lon = x.childNodes[0].getElementsByTagName("Longitude")[0].childNodes[0].nodeValue
    coord = (lat, lon)
    if coord == ("0","0"):
        return None
    return coord
coord = get_coords("0.0.0.0")
print(coord)
