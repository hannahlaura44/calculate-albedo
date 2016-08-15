
# ------------------------------------------------------------------------
# ------------------------FUNCTIONS & CLASSES-----------------------------
# ------------------------------------------------------------------------

import math
from PIL import Image
import numpy as num
import subprocess
from os.path import expanduser

# The Scene class represents an area of land which is defined by it's name, id, and bounding box coordinates (longitude, latitude)
class Scene:
    # set scene name, ID, and boundaries of box
    def __init__(self, sceneName):
        self.sceneName = sceneName

        if sceneName == "Anderson Almond Orchard in Hilmar, CA":
            self.sceneID = 'LC80430342016220LGN00'
            self.max_lon = -120.896773 # boundaries of box with area ~= 1 acre.
            self.min_lon = -120.897449
            self.max_lat = 37.380461 
            self.min_lat = 37.379967

        elif sceneName == "Spottswoode Winery in St. Helena, CA":
            self.sceneID = 'LC80430342016220LGN00'
            self.max_lon = -122.479728 # boundaries of box with area ~= 1 acre.
            self.min_lon = -122.481176
            self.max_lat = 38.500404
            self.min_lat = 38.500303

        elif sceneName == "Forest in Tahoe":
            self.sceneID = 'LC80430332016220LGN00'
            self.max_lon = -120.047328 # boundaries of box with area ~= 1 acre.
            self.min_lon = -120.048658
            self.max_lat = 38.828116
            self.min_lat = 38.827255

        else: 
            print "sorry we do not have data on that farm name yet."

# function to run a command-line SCRIPT from a python program.
def run_script(script, stdin=None):
    # """Returns (stdout, stderr), raises error on non-zero return code"""
    import subprocess
    # Note: by using a list here (['bash', ...]) you avoid quoting issues, as the 
    # arguments are passed in exactly this order (spaces, quotes, and newlines won't
    # cause problems):
    proc = subprocess.Popen(['bash', '-c', script],
        # stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    # if proc.returncode:
        # raise ScriptException(proc.returncode, stdout, stderr, script)
    return stdout, stderr

class ScriptException(Exception):
    def __init__(self, returncode, stdout, stderr, script):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        Exception.__init__('Error in script')



