import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
import sys
import Global
import traceback

server = None
thread = None
quitFlag = False
tracehandler = None
muted = False

def traceMessage(port,srclabel,destlabels,timeString):
    if muted: return True
    try:
        tracehandler.showHalos(port,srclabel,destlabels,timeString)
    except:
        traceback.print_exc()
    return tracehandler.stepCommand

def traceTransition(diagram, transnr,timeString):
    if muted: return True
    try:
        tracehandler.showTransition(diagram, transnr, timeString)
    except:
        traceback.print_exc()
    return tracehandler.stepCommand

def shutdown():
    print "received a shutdown request"
    global quitFlag
    quitFlag = True
    return True

def mute():
    global muted
    muted = True
    return True

def loud():
    global muted
    muted = False
    return True

def serveTillDawn():
    global quitFlag
    while not quitFlag:
        server.handle_request()

def startServer(th):
    global server
    global tracehandler
    tracehandler = th
    server = SimpleXMLRPCServer(("localhost", Global.tracePort))
    server.register_function(traceMessage)
    server.register_function(traceTransition)
    server.register_function(mute)
    server.register_function(loud)
    server.register_function(shutdown)
    thread = threading.Thread(target=serveTillDawn)

    print "starting thread"
    thread.start()


if __name__ == "__main__":
    startServer()
