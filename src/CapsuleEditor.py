import time
import threading
import re
import sys
import os
import string
from Tkinter import *
import Options
Options.setOptions()
import Message
from CapsuleDrawing import CapsuleDrawing
from SourceEditor import SourceEditor
import tkFileDialog
import m3
import ScriptRecorder
import TestScript
import MessageWindow
import Dialogs
import tkMessageBox
from Message import error, info, warning, messageOut
import Project
import traceback
import Exceptions
import DbgServer
import UnitCache
class ModuleSession:
    def __init__(self, capsuleDrawing, sourceEditor, specFileName, bodyFileName, specSource, bodySource):
        self.capsuleDrawing = capsuleDrawing
        self.sourceEditor = sourceEditor
        self.specFileName = specFileName
        self.bodyFileName = bodyFileName
        self.history = []
        self.redoList = []
        self.oldSpecSource = specSource
        self.oldBodySource = bodySource
    def update(self,specSource,bodySource,saveOutput=False):
        self.updateHelper(specSource,bodySource,saveOutput)
        self.history.append((self.oldSpecSource,self.oldBodySource))
        self.oldSpecSource = specSource
        self.oldBodySource = bodySource
        self.redoList = []
    def updateHelper(self,specSource,bodySource,saveOutput):
        try:
            # recompile the two sets of sources
            specTopNode = m3.compile(src=specSource, patchFileName=self.specFileName, mainProg=True, saveOutput=saveOutput)
            bodyTopNode = m3.compile(src=bodySource, patchFileName=self.bodyFileName, mainProg=True, saveOutput=saveOutput)
            # and resupply the nodes to the two editors
            self.capsuleDrawing.rescueResources()
            self.capsuleDrawing.show(specTopNode,bodyTopNode)
            self.capsuleDrawing.clearSelector()
            self.sourceEditor.show(specTopNode,bodyTopNode)
        except Exceptions.CompilerCatastrophic, res:
            messageOut("Catastrophic Compiler Error\n")
        else:
            traceback.print_exc() #OK
    def undo(self):
        if self.history :
            self.redoList.append((self.oldSpecSource,self.oldBodySource))
            self.oldSpecSource,self.oldBodySource = self.history.pop()
            self.updateHelper(self.oldSpecSource,self.oldBodySource,False)
    def redo(self):
        if self.redoList:
            self.oldSpecSource,self.oldBodySource = self.redoList.pop()
            self.updateHelper(self.oldSpecSource,self.oldBodySource,False)
    def redraw(self):
        self.capsuleDrawing.doRedraw()
    def save(self):
        self.capsuleDrawing.doSave()
    def lockGraphics(self):
        self.capsuleDrawing.lock()
    def unlockGraphics(self):
        self.capsuleDrawing.unlock()
    def setChanged(self):
        self.capsuleDrawing.setDirty()
    def showError(self,unitType,lineNo):
        self.sourceEditor.showError(unitType,lineNo)
    def genScene(self):
        self.capsuleDrawing.genPov()
    def screenshot(self):
        self.capsuleDrawing.doScreenshot()
    def printQuit(self):
        self.capsuleDrawing.doPrint()

    def reload(self):
        print "reloading %s %s " % (self.specFileName, self.bodyFileName)
        UnitCache.flush()
        self.update(open(self.specFileName).read(), open(self.bodyFileName).read())
class CapsuleEditor:
    def showActivity(self, capsuleName, actionName, phase):
        self.openCapsule(capsuleName)
        self.modules[capsuleName].capsuleDrawing.showActivity(actionName,phase)
    def showTransition(self, capsuleName, transitionName, stateName,phase):
        self.openCapsule(capsuleName)
        self.modules[capsuleName].capsuleDrawing.showTransition(transitionName,stateName,phase)
    def showAssignment(self,capsuleName,objectName,newValue):
        self.openCapsule(capsuleName)
        self.modules[capsuleName].capsuleDrawing.showAssignment(objectName,newValue)
    def showState(self,capsuleName,stateName):
        self.openCapsule(capsuleName)
        self.modules[capsuleName].capsuleDrawing.showState(stateName)
    def reloadCapsule(self,capsuleName):
        # called from emacs
#        print "SOOOOO you want to reload %s do you ?" % capsuleName
        self.openCapsule(capsuleName)
        self.reload(capsuleName)
    def update(self, capName, specSource, bodySource,saveOutput):
        # calls for non existent modules may get through when we are doing cameos
        if capName in self.modules:
            self.modules[capName].update(specSource,bodySource,saveOutput)
    def undo(self,capName):
        self.modules[capName].undo()
    def redo(self,capName):
        self.modules[capName].redo()
    def reload(self,capName):
        self.modules[capName].reload()
    def lockGraphics(self,capName):
        self.modules[capName].lockGraphics()        
    def unlockGraphics(self,capName):
        self.modules[capName].unlockGraphics()
    def setChanged(self, capName):
        self.modules[capName].setChanged()
    def showDiagram(self, name):
        self.modules[name].capsuleDrawing.makeTop()
    def showError(self, errorTxt):
        match = re.compile(r'(\w*)\.(.)3\:(\w*)\:').match(errorTxt)
        if match:
            moduleName, unitType, lineNo = match.groups()
            self.modules[moduleName].showError(unitType,lineNo)
        else:
            print "no match"
    def __init__(self,root):
        self.modules={}
        self.root = root
        self.project = None
        self.nextFlag = False
    def doQuit(self):
        if self.project:
            self.project.save()
        dirtyModules = []
        for module in self.modules.values():
            if module.capsuleDrawing.dirty():
                dirtyModules.append(module)
        dirtyCount = len(dirtyModules)
        if dirtyCount > 0:
            dirtyModuleNames = [module.capsuleDrawing.name for module in dirtyModules]
            if dirtyCount == 1:
                verb = " has"
                pron = " it"
            else:
                verb = " have"
                pron = " them"
            quit = 'Quit anyway'
            saveQuit = 'Save' + pron + ' and then quit'
            carryOn = 'Carry on editing'
            answer = Dialogs.askQuestion(string.join(dirtyModuleNames," + ") +
                                         verb + " been changed, what shall I do?",
                                         (quit, saveQuit, carryOn))
            if answer == quit:
                self.lastThings()
            elif answer == saveQuit:
                for module in dirtyModules:
                    module.save()
                self.lastThings()                    
            else:
                pass # carry on without doing anything
        else:
            self.lastThings()

    def doRedrawAll(self):
        for module in self.modules.values():
            module.redraw()

    def getFile(self):
        fn = tkFileDialog.askopenfilename(initialdir=os.getcwd(),
                                      parent=self.root, title="Open Capsule file",
                                      filetypes=[("Capsule files", ".m3")],
                                      defaultextension='.m3')
        return fn
    def saveAll(self):
        for module in self.modules.values():
            module.save()

    def newCapsule(self):
        res = Dialogs.askString(self.root, "New Capsule", None)
        if not res: return
        self.openCapsule(res)
            
    def openCapsule(self,fn=None):
        # finds both the spec and the body
        # if necessary creates them
        # compiles them
        # creates a new capsule drawing and source editor
        capsuleDrawing = None
        if not fn:
            fn = self.getFile()
        if not fn: return
        capName = os.path.splitext(os.path.basename(fn))[0]
        if capName in self.modules:
            #Message.info("module %s already loaded" % capName)
            capsuleDrawing = self.modules[capName].capsuleDrawing
            capsuleDrawing.makeTop()
        else:
            specFileName,bodyFileName = makeSkeletonsIfNeeded(fn)
            try:
                specTopNode = m3.compile(fileName=specFileName, mainProg=True)
                bodyTopNode = m3.compile(fileName=bodyFileName, mainProg=True)
            except:
                Message.reset()
                raise
                return None
            if Message.errors:
                print "module contains errors : no visual editing possible" #OK
                Message.reset()
            elif bodyTopNode.isEditable():
                sourceEditor = SourceEditor(central=self, name=capName, specTopNode=specTopNode, bodyTopNode=bodyTopNode)
                capsuleDrawing = CapsuleDrawing(central=self, name=capName, sourceEditor=sourceEditor)
                try:
                    capsuleDrawing.show(specTopNode, bodyTopNode)
                except:
                    traceback.print_exc() #OK

                capsuleDrawing.makeTop()
                self.modules[capName] = ModuleSession(capsuleDrawing,sourceEditor,
                                                      specFileName,bodyFileName,
                                                      specTopNode.regen(),bodyTopNode.regen())
                Message.info("module %s loaded" % fn)
            else:
                Message.info("module is not editable")
        ScriptRecorder.write("open('%s')" % fn)
        if self.project:
            self.project.addCapsule(capsuleDrawing.name)
        return capsuleDrawing # TBD why are we returning anything

    def setProject(self,project):
        self.project = project

    def genScene(self):
        for module in self.modules.values():
            module.genScene()

    def screenshot(self):
        for module in self.modules.values():
            module.screenshot()
    def printQuit(self):
        for module in self.modules.values():
            module.printQuit()


    def lastThings(self):
        DbgServer.selfShutdown()
        sys.exit()

    def doNext(self):
        self.nextFlag = True
        

    def doRun(self, name, inpFile, debug=False):
        self.saveAll()
        runcapSrc = os.environ["M3_HOME"] + os.sep + "src" + os.sep + "runcap.py"
        if debug:
            dbgString = "--debug-port=%s" % Options.options.debugPort
        else:
            dbgString = ""
        cmdString = 'python -u "%s" -cres %s %s %s' % (runcapSrc, name, inpFile, dbgString)
        print "Starting command <%s>" % cmdString
        fi,foe = os.popen4(cmdString)
        def showOutput():
            ch = True
            while ch:
                ch = foe.read(1)
                #print "character from pruefling<%s>" % ch
                Message.messageOut(ch,"dbg")
        thread = threading.Thread(target=showOutput)
        thread.start()
        
    
def makeSkeletonsIfNeeded(fn):
    # make sure we have two files standing where we want them to be
    basename = os.path.basename(fn)
    modname = os.path.splitext(basename)[0]
    truncfilename = os.path.splitext(fn)[0]
    bodyFileName = truncfilename + ".m3"
    specFileName = truncfilename + ".i3"
    bodysrc = """CAPSULE %s ;
IMPORT Timer;
BEGIN

END %s.
""" % (modname, modname)

    specsrc = """CAPSULE INTERFACE %s ;
PORT p1 : PROTOCOL
END;
END %s.
"""  % (modname, modname)
    if  not os.path.exists(bodyFileName):  
        f = open(bodyFileName,"w")
        f.write(bodysrc)
        f.close()
    if  not os.path.exists(specFileName):      
        f = open(specFileName,"w")
        f.write(specsrc)
        f.close()
    return  specFileName, bodyFileName,


if __name__ == "__main__":
    try:

        Options.options.info = True
        ScriptRecorder.startScripting() # TBD maybe use an option for this
        TestScript.setEditorRunning()
        root = Tk()
        ce = CapsuleEditor(root)
        DbgServer.startServer(th=ce,root=root) # TBD where and how do we decide on port ?
        def closeCallBack():
            if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
                ce.doQuit()
        root.protocol("WM_DELETE_WINDOW", closeCallBack)
        MessageWindow.start(ce)
        Button(root,text="New", command=ce.newCapsule).pack()
        Button(root,text="Open",command=ce.openCapsule).pack()
        Button(root,text="Save All",command=ce.saveAll).pack()
        Button(root,text="Quit",command=ce.doQuit).pack()
        Button(root,text="Next", command=ce.doNext).pack()
        root.geometry('100x150+0+0')
        if len(Options.args):
            fn=Options.args[0]
            p = Project.isProject(fn)
            if p:
                ce.setProject(p)
                capsules = p.capsules
            else:
                capsules = Options.args
            for capsule in capsules:
                ce.openCapsule(fn=capsule)
            if Options.options.genSceneOnly:
                ce.genScene()
                ce.lastThings()
#            if Options.options.screenshot:
#                ce.screenshot()
#                ce.lastThings()
            if Options.options.printQuit:
                print "Printing and quitting"
                ce.printQuit()
                ce.lastThings()
        root.mainloop()
    except Exceptions.Exception, cc:
        Message.info("Exception " +  cc.cause)
        
        
        
