# MODIS
# images the entire Earth every 1 to 2 days
# wikipedia: https://en.wikipedia.org/wiki/Moderate-resolution_imaging_spectroradiometer
# use to access images by supplying a date and location : https://api.nasa.gov/api.html#earth
# use image processing to calculate albedo based on pixel RGB value
# if cloud score is high, throw out the image.
# API key: gzvu4msw4Lc4nCh3CJtFU5bZqPdN5MyE0KM3HVtt
# https://api.nasa.gov/planetary/earth/imagery?lon=100.75&lat=1.5&date=2014-02-01&cloud_score=True&api_key=gzvu4msw4Lc4nCh3CJtFU5bZqPdN5MyE0KM3HVtt
# MODIS albedo product only has resolution of 500m (not good enough for 1 acre which is 63m x 63m)

import requests
r = requests.get("https://api.nasa.gov/planetary/earth/imagery?lon=38.0&lat=40.0&date=2014-10-01&cloud_score=True&api_key=gzvu4msw4Lc4nCh3CJtFU5bZqPdN5MyE0KM3HVtt")
#print "status code: ", r.status_code
#print "headers: ", r.headers
# print "content: ", r.content

from PIL import Image
from StringIO import StringIO

# s = StringIO(r.content)
# img = Image.open(s)
# img.save('pic','PNG')
# open("foo.jpg", "w").write(img)

import urllib, cStringIO

file = cStringIO.StringIO(urllib.urlopen("https://earthengine.googleapis.com/api/thumb?thumbid=283832cff020a0a5f527221e359847fe&token=de36c5c4d067147f79ddeba6ef6e7075").read())
img = Image.open(file)
img.save('pic','PNG')

