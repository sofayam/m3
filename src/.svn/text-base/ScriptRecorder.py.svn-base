import FileUtils
import time
import Options
import os.path
f = None

def startScripting():
    global f
    fn = Options.options.script_output
    if not fn:
        fn = "SessionScript.py"
    else:
        fn = os.path.splitext(fn)[0] + ".py"
    FileUtils.makebackup(fn)        
    f = open (fn,"w")    
    f.write("# ---- Script for session on %s ----\n" % time.asctime(time.localtime()))
    f.write("#\n")
    f.write("from TestScript import *\n")
    f.write("start()\n")
    
def write(txt):
    if f:
        f.write(txt + "\n")
    
