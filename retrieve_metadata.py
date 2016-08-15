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


# test
# run_script('landsat search --lat 37.872003 --lon -122.257813 --start "July 27 2016"')

# download this file.
# sceneID = 'LC80440342016211LGN00' # whatever the sceneID from the file was.
# command = 'landsat download ' + sceneID
# run_script(command) # this saves the files in ~/landsat

# get the MTL file





