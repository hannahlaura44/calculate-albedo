# coding: utf-8

# MODIS
# images the entire Earth every 1 to 2 days
# wikipedia: https://en.wikipedia.org/wiki/Moderate-resolution_imaging_spectroradiometer
# use to access images by supplying a date and location : https://api.nasa.gov/api.html#earth
# use image processing to calculate albedo based on pixel DN (digital number)
# if cloud score is high, throw out the image. or assing 
# API key: gzvu4msw4Lc4nCh3CJtFU5bZqPdN5MyE0KM3HVtt
# https://api.nasa.gov/planetary/earth/imagery?lon=100.75&lat=1.5&date=2014-02-01&cloud_score=True&api_key=gzvu4msw4Lc4nCh3CJtFU5bZqPdN5MyE0KM3HVtt
# MODIS albedo product only has resolution of 500m (not good enough for 1 acre which is 63m x 63m)
# resolution: Providing moderate-resolution imagery, from 15 meters to 100 meters, of Earth's land surface and polar regions, Landsat 8 operates in the visible, near-infrared, short wave infrared, and thermal infrared spectrum
	# OLI multispectral bands 1-7,9: 30-meters
	# OLI panchromatic band 8: 15-meters
	# TIRS bands 10-11: collected at 100 meters but resampled
	# to 30 meters to match OLI multispectral bands
# they are updated frequently, I obtained images of UCB campus taken as recently as July 29. They seem to be uploaded in real time.
# TODO (if time permits): make a timeseries of albedo at 3 locations.


# import requests
# r = requests.get("https://api.nasa.gov/planetary/earth/imagery?lon=38.0&lat=-120.0&date=2014-10-30&cloud_score=True&api_key=gzvu4msw4Lc4nCh3CJtFU5bZqPdN5MyE0KM3HVtt")
# print "status code: ", r.status_code
# print "headers: ", r.headers
# print "content: ", r.content



# function to save an image in the current directory given a request query QUERY and a filename FILENAME
import requests
from PIL import Image
from StringIO import StringIO
import urllib, cStringIO
def saveImage(query, filename):
	print "accessing", query, "..."
	r = requests.get(query)
	imgURL = getImageURL(r)
	if imgURL:
		file = cStringIO.StringIO(urllib.urlopen(imgURL).read())
		img = Image.open(file)
		img.save(filename,'PNG')
		print "image successfully saved in current directory as ", filename
	if not imgURL:
		print "error: did not find requested image."
	# open("foo.jpg", "w").write(img)

# function to get image url from Response contents
def getImageURL(r):
	i = 0
	j = 0
	foundurl = False
	while i < len(r.content):
		# beginning of url
		if r.content[i:i+3] == "url":
			i = i + 7 # move forward past these characters --> url": "
			j = i
			while j < len(r.content):
				if r.content[j] == '"': # end of url
					foundurl = True
					break
				j=j+1
		if foundurl:
			print "information about the image: ", r.content
			return r.content[i:j]
			break
		i = i+1
	if  not foundurl:
		print "error: ", r.content
	return
# print "imageURL: ", getImageURL(r)

# Tests
#note: in order to complete this query, you will have to register for a nasa API key here: https://api.nasa.gov/index.html#apply-for-an-api-key
# and replace the api_key in the query below.
imageFileName = ""
def test1(): # ucb campus
	query = "https://api.nasa.gov/planetary/earth/imagery?lon=-122.257813&lat=37.872003&date=2016-08-15&cloud_score=True&api_key=gzvu4msw4Lc4nCh3CJtFU5bZqPdN5MyE0KM3HVtt"
	imageFileName = "ucb campus"
	saveImage(query,imageFileName)
def test2(): # Anderson Almonds (Almond Orchard in Hilmar, CA)
	query = "https://api.nasa.gov/planetary/earth/imagery?lon=-120.897293&lat=37.380056&date=2016-08-15&cloud_score=True&api_key=gzvu4msw4Lc4nCh3CJtFU5bZqPdN5MyE0KM3HVtt"
	imageFileName = "Anderson Almonds"
	saveImage(query,"Anderson Almonds")
def test3(): # UCB campus
	query = "https://api.nasa.gov/planetary/earth/imagery?lon=-122.257813&lat=37.872003&date=2016-08-9&cloud_score=True&api_key=gzvu4msw4Lc4nCh3CJtFU5bZqPdN5MyE0KM3HVtt"
	saveImage(query,"pic3")

def test4(): 
	query = "https://api.nasa.gov/planetary/earth/imagery?lon=38.0&lat=-120.0&date=2014-10-30&cloud_score=True&api_key=gzvu4msw4Lc4nCh3CJtFU5bZqPdN5MyE0KM3HVtt"
	saveImage(query,"pic4")

def test5(): 
	query = "https://api.nasa.gov/planetary/earth/imagery?lon=38.0&lat=-120.0&date=2014-10-30&cloud_score=True&api_key=gzvu4msw4Lc4nCh3CJtFU5bZqPdN5MyE0KM3HVtt"
	saveImage(query,"pic5")

# main
#UCB campus is test 1
# test1()
# Anderson Almonds is test 2
test2()
# test3()
# test4()
# test5()



# see DN-to-albedo

