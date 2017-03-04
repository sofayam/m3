import time
import Options
import Exceptions
import Errors
import relpath
import sys
#
# Cute option-driven features such as
# - stop on error (exception)
# - warnings on or off
# - info on or off
# - summary at end of compiler run
# - Emacs conformant 
# TBD
# - snippets from offending code

errors = 0
warnings = 0

class StdoutWrapper:
    def write(self, txt, traits = None):
        sys.stdout.write(txt)
     
outStream = StdoutWrapper() # TBD what reason to discriminate with stderr usw ?

def setOutStream(stream):
    global outStream
    outStream = stream
    
def getLocation(obj):
    if not obj:
        return (None,None)
    else:
        if hasattr(obj,"lineno"):
            lineno = obj.lineno
        else:
            lineno = "?"
        return (relpath.relcwd(obj.getTopNode().source), lineno)
    
def error(msg, obj=None, fileName=None, lineno=None, catastrophic=False, code=None):
    # Syntax errors don't get reported with an object because we couldn't build a tree
    # so we have a mongrel function here
    global errors
    res = "No Message"
    errors += 1
    if not (fileName and str(lineno)):
        fileName, lineno = getLocation(obj)
    if Options.options.errorTest and Errors.directive:
        Errors.checkDirective(lineno, code)
    if not Options.options.errorTest:
        res = message("ERROR",msg, fileName, lineno, traits="error")
    if Options.options.stoperror or catastrophic:
        reset()
        raise Exceptions.CompilerCatastrophic(res)
    return res
def warning(msg, obj=None):
    global warnings
    warnings += 1
    if not Options.options.nowarnings:
        fileName, lineno = getLocation(obj)
        message("WARNING",msg, fileName, lineno)
def info(msg, obj=None):
    if Options.options.info:
        fileName, lineno = getLocation(obj)
        message("INFO", msg, fileName, lineno)


def message(mtype, msg, fileName=None, lineno=None, traits="normal"):
    if fileName and lineno:
        location = "%s:%s:" % (fileName,lineno)
    else:
        location = ""
    res = "%s %s %s\n" % (location, mtype, msg)
    messageOut(res,traits) #OK
    return res

def messageOut(txt, traits="normal"):
    outStream.write(txt, traits)

def summary(name):
    import Options
    if Options.options.errorTest:
        if Errors.foundError:
            predicate = "Found" 
        else:
            predicate = "!!!!!Missed!!!!"
        outStream.write("%s Error %s\n" % (predicate, Errors.directive[1]))
    elif not Options.options.nosummarymessages:
      if Options.options.syntax_only:
          burden = "syntax only"
      else:
          burden = "%d Errors and %d Warnings" % (errors,warnings) 
      outStream.write("%s : %s (%s)\n" % (name,burden,time.asctime(), )) #OK
    reset()

def reset():
    global errors, warnings
    errors = 0
    warnings = 0

def hasErrors():
    return errors > 0
