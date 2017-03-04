import Global
import xmlrpclib
import Timer
import Time
# TBD Why do we have to create a new server proxy for every call?

def getServer():
    return xmlrpclib.ServerProxy("http://localhost:%d" % Global.tracePort)


def traceMessage(port,label,actlabels):
    if Global.graphicalTrace:
        server=getServer()
        return server.traceMessage(port,label,actlabels,Time.timeString(Timer.timeQueue.wallClock))

def traceTransition(label,number):
    if Global.graphicalTrace:
        server=getServer()
        return server.traceTransition(label,number,Time.timeString(Timer.timeQueue.wallClock))

def mute():
    if Global.graphicalTrace and (Global.stepCommand == "STEP"):
        server=getServer()
        server.mute()

def loud():
    if Global.graphicalTrace and (Global.stepCommand == "STEP"):
        server=getServer()
        server.loud()
