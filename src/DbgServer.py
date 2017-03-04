import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import sys
import Options
import traceback
import time

server = None
thread = None
quitFlag = False
tracehandler = None
muted = False
master = None
serverStarted = False

def ping(msg):
    print "++++ YOU pinged me with << %s >> ++++" % msg
    return True

def waitNext():
    tracehandler.nextFlag = False
    while not tracehandler.nextFlag:
        time.sleep(0.1)

def showActivity(capsuleName, actionName):
    #print "++++ EXECUTING %s in capsule %s ++++" % (actionName, capsuleName)
    master.after_idle(tracehandler.showActivity, capsuleName, actionName, "in")
    waitNext()
    master.after_idle(tracehandler.showActivity, capsuleName, actionName, "out")
    return True

def showTransition(capsuleName, transitionName, stateName):    
    #print "++++ TRANSITION %s from state %s in capsule %s ++++" % (transitionName, stateName, capsuleName)
    master.after_idle(tracehandler.showTransition, capsuleName, transitionName, stateName, "in")
    waitNext()
    master.after_idle(tracehandler.showTransition, capsuleName, transitionName, stateName, "out")
    return True

def showState(capsuleName, stateName):    
    #print "++++ TRANSITION %s from state %s in capsule %s ++++" % (transitionName, stateName, capsuleName)
    master.after_idle(tracehandler.showState, capsuleName, stateName)
    return True


def showAssignment(capsuleName, objectName, newValue):
    master.after_idle(tracehandler.showAssignment, capsuleName, objectName, newValue)
    waitNext()
    return True

def reloadCapsule(capsuleName):
    master.after_idle(tracehandler.reloadCapsule, capsuleName)
    return True
    

## def mute():
##     global muted
##     muted = True
##     return True

## def loud():
##     global muted
##     muted = False
##     return True

def shutdown():
     print "received a shutdown request"
     global quitFlag
     quitFlag = True
     return True

def selfShutdown():
    if serverStarted:
        s = xmlrpclib.Server("http://localhost:%s" % Options.options.debugPort)
        s.shutdown()
    
    
def serveTillDawn():
    global quitFlag
    while not quitFlag:
        server.handle_request()
    server.server_close()
    
def startServer(th,port=None,root=None):
    global server
    global tracehandler
    global master
    global serverStarted
    if Options.options.noXMLServer: return
    master=root
    tracehandler = th
    try:
        server = SimpleXMLRPCServer(("localhost", port or Options.options.debugPort))
        #    server.register_function(mute)
        #    server.register_function(loud)
        server.register_function(shutdown)
        server.register_function(ping)
        server.register_function(showActivity)
        server.register_function(showTransition)
        server.register_function(showState)
        server.register_function(showAssignment)
        server.register_function(reloadCapsule)        
        thread = threading.Thread(target=serveTillDawn)
        thread.start()
        serverStarted = True
    except:
        print "XMLRPC Server socket blocked: not started"
if __name__ == "__main__":
    # this is just for checking xmlrpclib sanity - you can ping it from a test client
    startServer(th=None,port=int(sys.argv[1]),root=None)
