import os
import os.path
import os
import time
import stat
import string
import sys
import Options

def libFile(fileName):
    #import pdb; pdb.set_trace()
    res = string.join([os.environ['M3_HOME'], "lib", fileName], os.sep)
    return res
def createIfAbsent(fullFileName):
    wasMissing = False
    if not os.path.exists(fullFileName):
        wasMissing = True
        f = open(fullFileName,"w")
        f.write("created")
        f.close()
    return wasMissing
def modTime(fullFileName):
    return os.stat(fullFileName)[stat.ST_MTIME]
def buildCmdLine():
    if sys.platform == "win32":
        ext = "bat"
    else:
        ext = "sh"
    libfiles = libFile("*.i3")
    libm3lib = libFile("m3lib")
    return 'm3.%s "%s" --library="%s" --no-library-check' % (ext,libfiles,libm3lib)
    
def updateLib():
    if Options.options.noLibraryCheck:
        # this gets us out of endless recursion
        return
    updateNeeded = libFile("updateNeeded")
    lastUpdate = libFile("lastUpdate")
    lastUpdateWasMissing = createIfAbsent(lastUpdate)
    createIfAbsent(updateNeeded)
    if lastUpdateWasMissing or (modTime(updateNeeded) >= modTime(lastUpdate)):
        cmd = buildCmdLine()
        print "Updating library....."
        print os.popen(cmd).read()
        h = open(lastUpdate,"w")
        h.write("created")
        h.close()
                 

        
