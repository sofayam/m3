# A functional interface to capsule editor objects, used by Test Scripts

import CapsuleEditor
import Connection
import Tkinter
import Options
import time
import LoadSrc
ce = None
allDrawings = {}
turboMode = False
editorRunning = False

def setEditorRunning():
    global editorRunning
    editorRunning = True

def start():
    global ce
    if editorRunning:
        ce = CapsuleEditor.ce
        CapsuleEditor.root.mainloop()
    else:
        Options.setOptions()
        ce = CapsuleEditor.CapsuleEditor(Tkinter.Toplevel())

def open(capsuleName):
    cd = ce.openCapsule(capsuleName)
    allDrawings[capsuleName] = cd
    setFocus(capsuleName)
    
def setFocus(capsuleName):
    global currentDrawing
    currentDrawing = allDrawings[capsuleName]
    currentDrawing.makeTop()
#    currentDrawing.root.wait_visibility()
    
def goNewActMode():
    currentDrawing.goNewActMode(scr=True)

def goNewDataMode():
    currentDrawing.goNewDataMode(scr=True)    

def goNewStateMode():
    currentDrawing.goNewStateMode(scr=True)    

def goNewDataFlowMode():
    currentDrawing.goNewDataFlowMode(scr=True)    

def goMoveMode():
    currentDrawing.goMoveMode(scr=True)

def doSave():
    currentDrawing.doSave()

def setGeom(geom):
    currentDrawing.setGeom(geom)
    pause()

def setZoom(setting):
    currentDrawing.setZoom(setting)
    pause()
    
class PseudoEvent:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def ev(x,y):
    return PseudoEvent(x,y)

def msedwn(x,y,dl={}):
#    print "msedwn",x,y
    currentDrawing.msedwn(ev(x,y),dl)
    pause()
    
def msemv(x,y,dl={}):
#    print "msemv",x,y    
    currentDrawing.msemv(ev(x,y),dl)
    pause()
    
def mseup(x,y,dl={}):
#    print "mseup",x,y        
    currentDrawing.mseup(ev(x,y),dl)
    pause()
    
def msedbl(x,y,dl={}):
    currentDrawing.msedbl(ev(x,y),dl)
    pause()

def pause():
    if not turboMode:
        currentDrawing.root.update()    
        time.sleep(0.1)
        currentDrawing.makeTop()
#---------------------------------

def setTurbo(setting=True):
    global turboMode
    turboMode = setting
    LoadSrc.setTurbo(setting)

def connect(fromAvatar,toAvatar):
    conn = Connection.makeIfLegal(fromAvatar, toAvatar, currentDrawing)
    if conn:
        conn.createSource()
        conn.draw()

def activities():
    return currentDrawing.activities

def datastores():
    return currentDrawing.datastores


    
