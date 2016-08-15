# -*- coding: utf-8 -*- 

# This is the main file which calculates the albedo for three, 1-acre areas of land in CA.

# I use landsat-util (a command line utility that makes it easy to search, download, and process Landsat imagery). 
# In order to run this script you will need to download this utility. info below:
    # Github: https://github.com/developmentseed/landsat-util
    # full documentation: https://pythonhosted.org/landsat-util/
    # installation: https://pythonhosted.org/landsat-util/installation.html

# I use landsat 8 satellite images and metadata to calculate the albedo following the method cited in this paper:
    # Smith, R.B. 2010. “The heat budget of the earth’s surface deduced from space” available at http://yceo.yale.edu/sites/default/files/files/Surface_Heat_Budget_From_Space.pdf
    # The implementation is further described here: http://landsat.usgs.gov/Landsat8_Using_Product.php

# Overview of method to calculate Albedo of an area of land from Landsat 8 satellite data.
    # The structure of the flow diagram below is:
    # given
    #   |
    #   | equation
    #   v
    # output

    # Compute albedo given pixel values (Qcal) and metadata (Mρ,Aρ,θSE):
    # ------------------------------------------------------------
    #  Qcal,Mρ,Aρ,θSE
    # 	|
    # 	|	ρλ' = Mρ * Qcal + Aρ
    # 	v
    #  ρλ' (TOA reflectance, without correction for solar angle) 
    # 	|
    # 	|	ρλ =	ρλ' / sin(θSE)
    # 	v
    #  ρλ (TOA reflectance corrected for solar angle)
    # 	|
    # 	|	a = ((0.356*ρλ1) + (0.130*ρλ3) + (0.373*ρλ4) + (0.085*ρλ5) + (0.072*ρλ7) -0.018) / 1.016
    # 	|	note that band 2, the green part of the spectrum, is not used because ____
    # 	v
    # 	a (Albedo : the weighted average over the measured band reflectances)
    # 	|
    # 	|	If i had more time, I would:
    # 	|	correct for terrain slopes (decrease the albedo estimate for a brightly illuminated hill slope and increase it for a pixel in shadow)
    #   |   I would use the formula provided in Smith, R.B. 2010
    # 	v
    # 	a (Albedo corrected for terrian slopes)
    # 
    # 
    # where
    # Mρ          = Band-specific multiplicative rescaling factor from the metadata (REFLECTANCE_MULT_BAND_x, where x is the band number)
    # Aρ          = Band-specific additive rescaling factor from the metadata (REFLECTANCE_ADD_BAND_x, where x is the band number)
    # Qcal        = Quantized and calibrated standard product pixel values (DN)
    # θSE         = Local sun elevation angle. The scene center sun elevation angle in degrees is provided in the metadata (SUN_ELEVATION).


# ------------------------------------------------------------------------
# --------------- **** ACTION REQUIRED **** ------------------------------
# TO DO: uncomment location of interest to calculate the albedo for this location.
# sceneName = "Anderson Almond Orchard in Hilmar, CA"
sceneName = "Spottswoode Winery in St. Helena, CA"
# sceneName = "Forest in Tahoe"
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------



# -------------nothing needs to be changed below here.--------------------

import math
from PIL import Image
import numpy as num
import subprocess
from os.path import expanduser
from calc_albedo_classes_functions import Scene, run_script

# ------------------------------------------------------------------------
# Look-up scene ID for each location. (already completed)
# --------------------
# I ran the folllowing search commands to look up the sceneID for the farm of interest. (in the future you could automate extraction of sceneID)
# note: landsat 8 circumvents the earth every 16 days, hence I used a search period of the past two weeks to acquire as close to real-time data as possible.

# Anderson Almond Orchard in Hilmar, CA
# searchCommand = 'landsat search --lon -120.897293 --lat 37.380056 --start "July 28 2016" --end "August 15 2016"'
# run_script(searchCommand)

# Spottswoode Winery in St. Helena, CA
# searchCommand = 'landsat search --lon -122.480176 --lat 38.500303 --start "July 28 2016" --end "August 15 2016"'
# run_script(searchCommand)

# Forest in Tahoe
# searchCommand = 'landsat search --lon -120.047328 --lat 38.828116 --start "July 28 2016" --end "August 15 2016"'
# run_script(searchCommand)
# ------------------------------------------------------------------------

# create an instance of this scene (location). Refer to Scene class at the end of this file.
s = Scene(sceneName)

# ------------------------------------------------------------------------
# Download the images (bands 1,4,5,6,7) and metadata file. Clip the area to the size of ~1 acre. Process the image.
# To improve image quality: add option "--pansharpen". requires more memory
downloadCommand = 'landsat download ' + s.sceneID + ' --bands 13457 --process --clip='+str(s.min_lon)+','+str(s.min_lat)+','+str(s.max_lon)+','+str(s.max_lat)
run_script(downloadCommand) # this saves the files in ~/landsat
# ------------------------------------------------------------------------
# Open image files for bands 1,3,4,5, and 7. Convert image file to an array and get the average DN (digital number) for each image.
# See README for wavelength range of each band.
user = expanduser('~')

img = Image.open(user + "/landsat/downloads/" + s.sceneID + "/clipped/" + s.sceneID + "_B1.TIF", "r")
imarray=num.array(img)
avg_DN_B1 = num.average(imarray)

img = Image.open(user + "/landsat/downloads/" + s.sceneID + "/clipped/" + s.sceneID + "_B3.TIF", "r")
imarray=num.array(img)
avg_DN_B3 = num.average(imarray)

img = Image.open(user + "/landsat/downloads/" + s.sceneID + "/clipped/" + s.sceneID + "_B4.TIF", "r")
imarray=num.array(img)
avg_DN_B4 = num.average(imarray)

img = Image.open(user + "/landsat/downloads/" + s.sceneID + "/clipped/" + s.sceneID + "_B5.TIF", "r")
imarray=num.array(img)
avg_DN_B5 = num.average(imarray)

img = Image.open(user + "/landsat/downloads/" + s.sceneID + "/clipped/" + s.sceneID + "_B7.TIF", "r")
imarray=num.array(img)
avg_DN_B7 = num.average(imarray)

# print the number of pixels in the image.
# note: this information can be used to assess how suspectible the image is to bias. 
# e.g. statistically, the more pixels you average over, the more accurate the average should be.
print "Image has", imarray.size, "pixels"

# ------------------------------------------------------------------------
# open the metadata file for the scene.
metadataFile = open(user + "/landsat/downloads/" + s.sceneID + "/clipped/" + s.sceneID + "_MTL.txt", "r")

# get band-specific multiplicative rescaling factors from metadata file (MTL file)
for line in metadataFile:
    if "REFLECTANCE_MULT_BAND_1" in line:
    	M_1 = float(line[30:-1])
    if "REFLECTANCE_MULT_BAND_3" in line:
    	M_3 = float(line[30:-1])
    if "REFLECTANCE_MULT_BAND_4" in line:
    	M_4 = float(line[30:-1])
    if "REFLECTANCE_MULT_BAND_5" in line:
    	M_5 = float(line[30:-1])
    if "REFLECTANCE_MULT_BAND_7" in line:
    	M_7 = float(line[30:-1])
# print M_1, M_3, M_4, M_5, M_7
metadataFile.close()

# 	get band-specific additive rescaling factors from metadata file (MTL file)
metadataFile = open(user + "/landsat/downloads/" + s.sceneID + "/" + s.sceneID + "_MTL.txt", "r")
for line in metadataFile:
    if "REFLECTANCE_ADD_BAND_1" in line:
    	A_1 = float(line[29:-1])
    if "REFLECTANCE_ADD_BAND_3" in line:
    	A_3 = float(line[29:-1])
    if "REFLECTANCE_ADD_BAND_4" in line:
    	A_4 = float(line[29:-1])
    if "REFLECTANCE_ADD_BAND_5" in line:
    	A_5 = float(line[29:-1])
    if "REFLECTANCE_ADD_BAND_7" in line:
    	A_7 = float(line[29:-1])
# print A_1, A_3, A_4, A_5, A_7
metadataFile.close()

# ------------------------------------------------------------------------
# calculate TOA reflectance for band 1,3,4,5,7
# --------------------
# recall: TOA_reflectance_x = M_x * Qcal + A_x
    # where
    # M_x = band-specific multiplicative rescaling factor
    # Qcal = quantized and calibrated standard product pixel values (DN)
    # A_x = band-specific additive rescaling factor
TOA_reflectance_B1 = M_1 * avg_DN_B1 + A_1
TOA_reflectance_B3 = M_3 * avg_DN_B3 + A_3
TOA_reflectance_B4 = M_4 * avg_DN_B4 + A_4
TOA_reflectance_B5 = M_5 * avg_DN_B5 + A_5
TOA_reflectance_B7 = M_7 * avg_DN_B7 + A_7
print "TOA_reflectance for bands 1,3,4,5,7: ", TOA_reflectance_B1, TOA_reflectance_B3, TOA_reflectance_B4, TOA_reflectance_B5, TOA_reflectance_B7
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# correct for solar angle
# --------------------
# TOA_reflectance_corrected_B1 = TOA_reflectance_B1 / sin(θSE)
metadataFile = open(user + "/landsat/downloads/" + s.sceneID + "/" + s.sceneID + "_MTL.txt", "r")
for line in metadataFile:
    if "SUN_ELEVATION" in line:
    	sun_angle = math.radians(float(line[29:-1]))
# print sun_angle

TOA_reflectance_corrected_B1 = TOA_reflectance_B1 / (math.sin(sun_angle))
TOA_reflectance_corrected_B3 = TOA_reflectance_B1 / (math.sin(sun_angle))
TOA_reflectance_corrected_B4 = TOA_reflectance_B1 / (math.sin(sun_angle))
TOA_reflectance_corrected_B5 = TOA_reflectance_B1 / (math.sin(sun_angle))
TOA_reflectance_corrected_B7 = TOA_reflectance_B1 / (math.sin(sun_angle))
print "TOA reflectance corrected for solar angle for bands 1,3,4,5,7: ",TOA_reflectance_corrected_B1, TOA_reflectance_corrected_B3, TOA_reflectance_corrected_B4, TOA_reflectance_corrected_B5, TOA_reflectance_corrected_B7
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
# calculate albedo
# --------------------
# a = ((0.356*ρλ1) + (0.130*ρλ3) + (0.373*ρλ4) + (0.085*ρλ5) + (0.072*ρλ7) -0.018) / 1.016
albedo = ((0.356*TOA_reflectance_corrected_B1) + (0.130*TOA_reflectance_corrected_B3) + (0.373*TOA_reflectance_corrected_B4) + (0.085*TOA_reflectance_corrected_B5) + (0.072*TOA_reflectance_corrected_B7) -0.018) / 1.016
print "albedo of",sceneName, "is", albedo


# END OF MAIN SCRIPT
print "finished"


