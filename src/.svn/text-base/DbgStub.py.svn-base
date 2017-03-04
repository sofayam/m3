import Global	
import xmlrpclib


def getServer():
    return xmlrpclib.ServerProxy("http://localhost:%d" % Global.debugPort)

def ping(msg):
    return
    if Global.debugPort:
        server = getServer()
        server.ping(msg)

def showActivity(capsuleName, activityName):
    if Global.debugPort:
        server = getServer()
        server.showActivity(capsuleName, activityName)

def showTransition(capsuleName, transitionName, stateName):
    if Global.debugPort:
        server = getServer()
        server.showTransition(capsuleName, transitionName, stateName)

def showState(capsuleName,stateName):
    if Global.debugPort:
        server = getServer()
        server.showState(capsuleName,stateName)

def showAssignment(capsuleName, objectName, newValue):
    if Global.debugPort:
        server = getServer()
        server.showAssignment(capsuleName, objectName, newValue)
    
def mute():
    if Global.graphicalTrace and (Global.stepCommand == "STEP"):
        server=getServer()
        server.mute()

def loud():
    if Global.graphicalTrace and (Global.stepCommand == "STEP"):
        server=getServer()
        server.loud()
