import os
import os.path
import sys
import time
import traceback
from Tkinter import *
from ResourceFile import ResourceFile
from ZoomDrawing import ZoomDrawing
import Avatars
import Dialogs
import FileUtils
import Options
import ScriptRecorder
import Connection
import UnitCache
import Message
import DiagMaths
import Colors
import DocuDumper
import CompOrder
import InputFile
minSelect = 5

def uniquify(list):
    res = []
    for item in list:
        if item not in res:
            res.append(item)
    return res

class CapsuleDrawing(ZoomDrawing):
    def __init__(self,central,name,sourceEditor):
        try:
            self.inputFile = False
            self.geomSet = False
            self.textDirty = False
            self.drawingDirty = False
            self.cameoObservers = []
            self.central = central
            self.name = name
            self.sourceEditor = sourceEditor
            self.selectHandle = None
            self.inpFile = name 
            ZoomDrawing.__init__(self, name) 
            self.resource = ResourceFile(name,read=True)
            res = (not Options.options.ignoreGeometry) and self.resource.read("**capsuleDrawing")
            if res:
                #print "setting geometry from resource"
                magscale, geom = res
                self.setGeom(geom)
                self.setZoom(magscale)

            res = (not Options.options.ignoreGeometry) and self.resource.read("**sourceEditor")
            if res:
                self.sourceEditor.setGeom(res)
            self.goMoveMode(scr=True) # Don't script this
        except:
            traceback.print_exc() #OK

    def addCameoObserver(self,observer):
        self.cameoObservers.append(observer)

    def deleteCallBack(self):
        self.central.doQuit()

    def lock(self):
        self.textDirty = True
    def unlock(self):
        self.textDirty = False
    def rescueResources(self):
        for avatar in self.allAvatars():
            res = avatar.getResource()
            if res:
                self.resource.write(avatar.name,res)
            self.oldTarget = None
        cdResource = self.rescueResource()
        self.resource.write("**capsuleDrawing",cdResource)
        seResource = self.sourceEditor.rescueResource()
        self.resource.write("**sourceEditor",seResource)
        
    def show(self,specTopNode,bodyTopNode):
        self.clear()
        self.oldTarget = None
        self.bodyTopNode = bodyTopNode
        self.specTopNode = specTopNode
        self.setupAvatars()
        self.setupConnections()
        self.setupConnLabels()
        self.setupPortLabels()
        if Options.options.ignoreGeometry and not self.geomSet:
            _,_,maxX, maxY = self.minMaxXY()
            if (maxX < 1000) and (maxY < 800):
                geom = "%dx%d+0+0" % (maxX+64, maxY+20)
                self.setGeom(geom)
            self.geomSet = True
    def showActivity(self,activityName,phase):
        avatar = self.existsAvatar(withName=activityName)
        if avatar:
            self.makeTop()
            avatar.Highlight(phase)
        else:
            print "+++++++++++avatar %s not found++++++++++++++" % activityName
    def showTransition(self, transitionName, stateName,phase):
        avatarName = "%s:%s" % (stateName,transitionName)
        avatar = self.existsAvatar(avatarName)
        if avatar:
            self.makeTop()
            avatar.Highlight(phase)
        else:
            print "+++++++++++avatar %s not found++++++++++++++" % avatarName
    def showAssignment(self, objectName, newValue):
        #print "show Assignment objectName %s, newValue %s" % (objectName, newValue)
        avatar = self.existsAvatar(withName=objectName)
        if avatar:
            avatar.HighlightValue("%s" % newValue)
    def showState(self, stateName):
        avatar = self.existsAvatar(withName=stateName)
        if avatar:
            print "highlightexclusive"
            avatar.HighlightExclusive()
        
    def update(self, saveOutput=False):
        self.central.update(self.name,self.specTopNode.regen(),self.bodyTopNode.regen(),saveOutput=saveOutput)
                
#    def doScreenshot(self):
#        self.canvas.update()
#        ps = self.canvas.postscript()
#        psfile = open("%sshot.ps" % self.name,"w")
#        psfile.write(ps)
#        psfile.close()

    def genPov(self):
        povProlog = os.environ['M3_HOME'] + os.sep + "lib" + os.sep + "avatars.pov"
        prolog = open(povProlog).read()
        _,_,maxX, maxY = self.minMaxXY()
        prolog = prolog.replace("<<maxX>>","%d" % maxX)
        prolog = prolog.replace("<<maxY>>","%d" % maxY)
        f = open("%s.pov" % self.name,"w")
        f.write(prolog)
        DiagMaths.setYFlip(maxY) 
        for avatar in self.allAvatars():
            avatar.getPov(f)
        for connection in self.connections:
            connection.getPov(f)
        f.close()
        
    def dirty(self):
        return self.drawingDirty or self.textDirty

    def setDirty(self):
        self.drawingDirty = True
        self.updateTitle()
    def setClean(self):
        self.drawingDirty = False
        self.updateTitle()

    def updateTitle(self):
        dirtyFlag = ""
        if self.dirty(): dirtyFlag = "*"
        self.setTitle(self.name + dirtyFlag + " [" + self.modeString + "]")

    def nothing(self): pass

    def doDebug(self):
        self.central.doRun(self.name, self.inpFile, debug=True)

    def doOptions(self):
        dict = Dialogs.askOptions(self.root, {'cameos': Options.options.cameos, 'arrows': not Options.options.arrowsOff})
        Options.options.cameos = dict['cameos']
        Options.options.arrowsOff = not dict['arrows']
        self.central.doRedrawAll()
        print dict

    def doRun(self):
        self.central.doRun(self.name, self.inpFile)
        
    def addPopup(self, root):

        self.popup = Menu(root,tearoff=0)

        self.popup.add_command(label="dismiss",     command=self.nothing)
        DocuDumper.startDoc("rightMouse.inc")
        DocuDumper.addGroup("The first group covers mode changes (see more on modes below)")
        self.popup.add_command(label="move",        command=self.goMoveMode)
        DocuDumper.addItem("move", "Go into move mode")
        self.popup.add_command(label="select",      command=self.goSelectMode)
        DocuDumper.addItem("select", "Go into select mode")
        self.popup.add_command(label="new object",  command=self.goNewObjectMode)
        DocuDumper.addItem("new object", "Go into new object mode")
        self.popup.add_command(label="connect",     command=self.goNewConnectionMode)
        DocuDumper.addItem("connect", "Go into connect mode")
        self.popup.add_command(label="align",       command=self.goAlignMode)
        DocuDumper.addItem("align", "Go into align mode")

        self.popup.add_command(label="locate",      command=self.goLocateMode)
        DocuDumper.addItem("locate", "Go into locate mode")
        self.popup.add_command(label="explain",      command=self.goExplainMode)
        DocuDumper.addItem("explain", "Go into explain mode")

        DocuDumper.endGroup()
        DocuDumper.addGroup("The second group covers printing")
        self.popup.add_command(label="print",       command=self.doPrint) #OK
        DocuDumper.addItem("print", "Generate scaled postscript and png of the complete design canvas (works on capsules of arbitrary size and complexity)")
#        self.popup.add_command(label="screenshot",  command=self.doScreenshot) #OK
#        DocuDumper.addItem("screenshot", "Low level tkinter screenshot of the current design canvas")
        self.popup.add_command(label="gen scene",   command=self.genPov)
        DocuDumper.addItem("gen scene", "generate a povray scene file, only interesting" +
                           "if you have Povray installed on your computer and you want to impress people with three dimensional models")
        DocuDumper.endGroup()
        DocuDumper.addGroup("Finally we have some other functions")
        self.popup.add_command(label="open",        command=self.central.openCapsule)
        DocuDumper.addItem("open", "Open a new or existing capsule")
        self.popup.add_command(label="save",        command=self.doSave)
        DocuDumper.addItem("save", "save and generate code for current capsule")
        self.popup.add_command(label="undo",        command=self.doUndo)
        DocuDumper.addItem("undo", "undo the last change to the model text (graphics-only changes not included)")
        self.popup.add_command(label="redo",        command=self.doRedo)
        DocuDumper.addItem("redo", "redo what was undone")
        self.popup.add_command(label="redraw",      command=self.doRedraw)
        DocuDumper.addItem("redraw", "reparse and redraw the current capsule")
        self.popup.add_command(label="reload",      command=self.doReload)
        DocuDumper.addItem("reload", "reload the source files of the current capsule (e.g. if they have been edited by another tool)")
        self.popup.add_command(label="test",        command=self.doTest)
        DocuDumper.addItem("test", "dump a list of avatars to console (for internal test purposes)")
        self.popup.add_command(label="run",       command=self.doRun)
        DocuDumper.addItem("run", "run the system with the default input file")
        self.popup.add_command(label="debug",       command=self.doDebug)
        DocuDumper.addItem("debug", "start a debug run (see section on debugging below)")
        self.popup.add_command(label="options",       command=self.doOptions)
        DocuDumper.addItem("options", "change various options at run time (instead of using command line)")
        self.popup.add_command(label="input",       command=self.doInput)
        DocuDumper.addItem("input", "edit and manage the input file used for a test run")

        DocuDumper.endGroup()
        DocuDumper.endDoc()
        self.popup.add_command(label="quit",        command=self.central.doQuit)
        root.bind('<Button-3>', self.popupMenu)

    def popupMenu(self,event):
        self.popup.post(event.x_root, event.y_root)

    def chooseMessage(self, portType, x, y):
        messageList = portType.protocol.messages
        if len(messageList) == 0:
            Dialogs.complain("Port %s has no messages" % (portType.name))
            return ""
        elif len(messageList) == 1:
            return messageList[0].name
        else:
            sd = Dialogs.chooseMessage(self.root, [message.name for message in messageList])
            return sd['message']

    def doInput(self):
        if self.inputFile:
            return # TBD highlight the input window
        else:
            self.inputFile = InputFile.InputFile(self)

    def setInpFile(self,inpFile):
        self.inpFile = inpFile

    def addHandlers(self, canvas):
        Widget.bind(canvas, "<Button-1>", self.msedwn)
        Widget.bind(canvas, "<Button1-Motion>", self.msemv)
        Widget.bind(canvas, "<Button1-ButtonRelease>", self.mseup)
        Widget.bind(canvas, "<Double-Button-1>", self.doubleClick)
        Widget.bind(canvas, "<Motion>", self.motion)
    def allAvatars(self):
        # The smallest and most dependent first : useful for searching on mouse posn.
        # NB activities at the front so they get caught first when drawing message connections
        # labels at the end so that you dont drag them inadvertently while trying to sort out lost resources
        all = self.noteArrows + self.activities + self.messages + self.childPorts + (
            self.datastores + self.triggers + self.childCapsules + self.procedures + (
            self.timers + self.states + self.transitions + self.transitionProxies + self.notes + (
            self.portLabels + self.connLabels + self.ports)))
        if self.start:
            all.append(self.start)
        all.append(self.capsule)
        return all
    def allignableAvatars(self):
        return self.activities + self.datastores + self.triggers + self.childCapsules + self.procedures +  (
            self.transitions + self.states + self.timers)
    def allAvatarsReversed(self):
        # The heaviest and most inclusive first : useful for drawing with fill
        res = self.allAvatars()
        res.reverse()
        return res

    def minMaxXY(self,ignoreCapsule=False):
        maxx = 0
        maxy = 0
        minx = None
        miny = None
        for avatar in self.allAvatars():
            if (avatar == self.capsule) and ignoreCapsule: continue
            sx,sy,ex,ey = avatar.outline
            maxx = max(maxx, ex)
            maxy = max(maxy, ey)
            if minx == None:
                minx = sx
            else:
                minx = min(minx, sx)
            if miny == None:
                miny = sy
            else:
                miny = min(miny, sy)

        return minx,miny,maxx, maxy

    def unitCacheChanged(self):
        self.update()

    def portWithName(self,name):
        for port in self.ports:
            if port.name == name:
                return port
    
    def setupAvatars(self):
        self.connLabels = []
        self.portLabels = []
        self.noteArrows = []
        self.capsule = self.bodyTopNode.gatherCapsule()
        self.datastores = self.bodyTopNode.gatherDataStores()
        self.triggers = self.bodyTopNode.gatherTriggers()
        self.childCapsules = self.bodyTopNode.gatherChildCapsules()
        self.activities = self.bodyTopNode.gatherActivities()
        self.timers = self.bodyTopNode.gatherTimers()
        self.states = self.bodyTopNode.gatherStates()
        self.transitions = self.bodyTopNode.gatherTransitions()
        self.ports = self.specTopNode.gatherPorts()
        self.childPorts = self.gatherChildPorts()
        self.procedures = self.bodyTopNode.gatherProcedures()
        self.start = self.bodyTopNode.gatherStart()
        self.transitionProxies = self.bodyTopNode.gatherTransitionProxies(self.transitions)
        for port in self.ports:
            port.setCapsule(self.capsule)
        self.notes = self.createNotes()

        # Register as a listener for all changes to units on which you depend (so that when they change you will be
        # sent the unitCacheChanged message)
        
        CompOrder.grabDB()

        depUnitIFs = [CompOrder.makeSpec(unit) for unit in (self.bodyTopNode.getDependencies() +
                          self.specTopNode.getDependencies())]
        #Message.info(str(depUnitIFs))

        for depUnitIF in depUnitIFs:
            UnitCache.addListener(depUnitIF,self)


        # Now derive all the message avatars from their ports
        self.messages = []

        for avatar in self.allAvatarsReversed():
            r = self.resource.read(avatar.name)
            if r and not Options.options.ignoreResources:
                avatar.setResource(r)
            else:
                avatar.setRandom()
                
        for avatar in self.allAvatars():
            avatar.setCanvas(self)

        for avatar in self.allAvatarsReversed():
            avatar.draw()

        if Options.options.cameos:
            for childAvatar in self.childCapsules:
                # open the capsule corresponding to the child (if not already the case)
                capsule = self.central.openCapsule(childAvatar.capName())
                
                childAvatar.createCameos(parentDrawing=capsule, childAvatar=childAvatar)
                capsule.addCameoObserver(childAvatar)
                
        for avatar in self.allAvatars():
            avatar.move(0,0) # give everything a little joggle to make the constraints kick in
            
    def gatherChildPorts(self):
        res = []
        for child in self.childCapsules:
            res += child.createChildPorts()
        return res
    def setupConnections(self):
        self.connections = []
        self.setupDataDependencies(self.connections)
        self.setupTransitions(self.connections)
        self.setupMessageConnections(self.connections)
        self.setupNoteArrows(self.connections)
        self.setupCalls(self.connections)
    def setupConnLabels(self):
        for connection in self.connections:
            connection.addLabel(self.connLabels)

        for connLabel in self.connLabels:
            r = self.resource.read(connLabel.name)
            if r and not Options.options.ignoreResources:
                connLabel.setResource(r)
            connLabel.setCanvas(self)
            connLabel.draw()
    def setupPortLabels(self):
        def makePortLabel(dir, messNameList, port):
            pl = Avatars.PortLabel("*PortLabel" + dir + "*" + port.name, None)
            pl.setPort(port,dir)
            pl.setWords(messNameList)
            self.portLabels.append(pl)
            x,y = port.middle()
            x = x-50
            pl.create(x,y)
            r = self.resource.read(pl.name)
            if r and not Options.options.ignoreResources:
                pl.setResource(r)
            pl.setCanvas(self)
            pl.draw()
            port.addPortLabel(pl)
            
        for port in self.ports:
            inMess = [] ; outMess = []
            for message in port.node.getType().protocol.messages:
                if message.dir == "INCOMING":
                    inMess.append(message.name)
                else:
                    outMess.append(message.name)
            #import pdb; pdb.set_trace()
            makePortLabel("INCOMING", inMess, port)
            makePortLabel("OUTGOING", outMess, port)            
            
    def setupDataDependencies(self,connections):
        for avatar in self.allAvatars():
            readWriteDeps = []
            # These two have nodes further up the tree, data connections are denoted by their children only
            if avatar.avatarType() in ["State","Capsule"]: continue
            if not avatar.node: continue
            avatar.node.getReadWriteDependencies(readWriteDeps)
            for mode,dep in readWriteDeps:
                otherAvatar = self.existsAvatar(dep)
                if otherAvatar:
                    if mode == "READS":
                        conn = Connection.makeDataFlowConnection(otherAvatar, avatar, self)
                    elif mode == "WRITES":
                        conn = Connection.makeDataFlowConnection(avatar,otherAvatar,self)
                    else:
                        raise "bad mode"
                    connections.append(conn)
                    conn.draw()
                else:
                    print "%s is a bogus avatar : TBD check for this in compiler" % dep # OK

    def setupTransitions(self,connections):
        for transition in self.transitions:
            # Draw conn from state to trans box
            conn = Connection.make(transition.owningState,transition,self)
            connections.append(conn)
            conn.draw()
            # and conn from trans box to next state 
            self.makeNextTransitions(connections,fromAvatar=transition)
        # and then from the start thingie
        if self.start:
            self.makeNextTransitions(connections,fromAvatar=self.start)
                
    def makeNextTransitions(self, connections, fromAvatar):
        nexts = fromAvatar.node.gatherNexts()
        for nextState in nexts:
            state = self.existsAvatar(withName=nextState)
            #print "state",state
            if (not state) or (state.avatarType() != "State"):
                print "bad next state %s" % nextState # OK
            else:
                conn = Connection.make(fromAvatar, state, self)
                connections.append(conn)
                conn.draw()


    def findMessageDestAvatar(self,idList):
        #import pdb; pdb.set_trace()
        #print "############findAvatar %s" % str(idList)
        avatar = None
        if len(idList) == 1:
            id = idList[0]
            avatar = self.existsAvatar(id)
            # if it is a message then use the port
            if not avatar:
                port = self.capsule.node.getType().getPortOfMessage(id)
                if port:
                    portName = port.name
                else:
                    raise "unique message %s not found" % id
                avatar = self.existsAvatar(portName)
        elif len(idList) == 2:

            # first try the easy one: childName.portName
            avatar = self.existsAvatar("%s.%s" % tuple(idList))

            if not avatar:
                # then try to find the port for
                # childName.messageName

                child =  self.existsAvatar(idList[0])
                if child and child.__class__.__name__ == "Child":
                    #print child.specNode
                    port = child.specNode.getType().getPortOfMessage(idList[1])
                    if port:
                        avatar = self.existsAvatar("%s.%s" % (idList[0],port.name))
                if not avatar:
                # finally try for 
                # portName.messageName
                    port = self.existsAvatar(idList[0])
                    if port and port.__class__.__name__ == "Port":
                        avatar = port 


        elif len(idList) == 3:
            # childCapsuleName.portName.messageName
            # avatar is just the childCapsuleName.portName
            avatar =  self.existsAvatar("%s.%s" % (idList[0], idList[1]))
        else:
            problem = "idList too long %s" % str(idList)
            raise problem
        #print "avatar is",idList,avatar
        return avatar


    def setupCalls(self, connections):
        for avatar in self.procedures + self.activities + self.transitions:
            if not avatar.node: continue
            calls = []
            avatar.node.getCalls(calls)
            for call in calls:
                if type(call) == type([]):
                    destAvatar = self.findMessageDestAvatar(call)
                else:
                    destAvatar = self.existsAvatar(call)
                    call = [call]
                if destAvatar:
                    conn = Connection.CallConnection(avatar, destAvatar, self)
                    conn.setMessage(call)
                    connections.append(conn)
                    conn.draw()
                else:
                    print "%s is a bogus avatar : TBD check for this in compiler" % call # OK                    


    def setupMessageConnections(self,connections):
        conns = self.bodyTopNode.gatherConnectMessageConnections()

        for connType,start,end in conns:
            #print "conns",connType,start,end
            a1 = self.findMessageDestAvatar(start)
            #print "A1!!!!!!!!!!",a1
            a2 = self.findMessageDestAvatar(end)
            #print "A2!!!!!!!!!!",a2
            if Options.options.hideports:
                return
            if connType == "MC":
                # we have to cheat here because we are reusing the port avatar as a physical connector
                # because the logical connector (message) does not exist as an avatar in the drawing
                conn = Connection.make(a1,a2,self,"Message","Message")
                conn.setStartEndMessages(start[-1],end[-1]) 
            else:
                conn = Connection.make(a1,a2,self)
            connections.append(conn)
            conn.draw()
            
        for sender in self.activities + self.transitions:
            sends = uniquify(sender.node.gatherSendMessageConnections())
            for send in sends:
                end = self.findMessageDestAvatar(send)
                conn = Connection.make(sender,end,self)
                conn.setMessage(send[-1])
                connections.append(conn)
                conn.draw()
                
        if not Options.options.noImplicit:
            for avatar in self.activities + self.procedures:
                for message in self.capsule.node.getType().spec.uniqueMessages:
                    if avatar.name == message:
                        portName = self.capsule.node.getType().getPortOfMessage(message).name
                        port = self.portWithName(portName)
                        conn = Connection.ImplicitConnection(port, avatar, self)
                        connections.append(conn)
                        conn.draw()

                    
    def setupNoteArrows(self,connections):
        self.noteArrows = []
        for note in self.notes:
            for x, y in note.arrowCoords:
                na = Avatars.NoteArrow("**Arrow%s" % time.time(), None)
                na.create(x,y)
                note.addArrow(na)
                self.noteArrows.append(na)
                nc = Connection.make(note,na,self)
                connections.append(nc) 
                nc.draw()
                
    def createNotes(self):
        noteDict = self.resource.getNotes()
        notes = []
        for name in noteDict:
            note = Avatars.Note(name,None)
            notes.append(note)
        return notes
            
    def findTarget(self,x,y,choiceList=None):
        if not choiceList:
            choiceList = self.allAvatars()
        for avatar in choiceList:
            if avatar.isUnder(x,y):
                return avatar


    def doPrint(self,scr=False):
        if not scr:
            ScriptRecorder.write("doPrint()")
        psprocs = open(os.environ['M3_HOME'] + os.sep + "lib" + os.sep + "psprocs.ps").read()
        fn = self.name + ".ps"
        fnpng = self.name + ".png"        
        f = open(fn,"w")
        minx,miny,maxx,maxy = self.minMaxXY()

        # only scale if it is too broad
        if maxx > 500:
            scale = 500.0/maxx
        else:
            scale = 1
        # now scale everything

        maxx *= scale
        maxy *= scale
        minx *= scale
        miny *= scale
        
        f.write(psprocs)
        f.write("10 %s translate\n" % - int(maxy + miny))
        f.write("%s %s scale\n" % (scale, scale))
        for avatar in self.allAvatarsReversed():
            avatar.getPostscript(f)
        for connection in self.connections:
            connection.getPostscript(f)
        if Options.options.cameos:
            for childAvatar in self.childCapsules:
                capsule = self.central.openCapsule(childAvatar.capName())
                childAvatar.createCameosPS(parentDrawing=capsule, childAvatar=childAvatar,psfile=f)
        f.close()

        if sys.platform == "win32":
            gscommand = "gswin32c"
        else:
            gscommand = "gs"
        ptFactor = 4
        pngBound = 10

        # generate bbox
        commandLine = '%s -q -dBATCH -dNOPAUSE -sDEVICE=bbox %s -c showpage' % (gscommand, fn)
        (stdin, sdout, stderr) = os.popen3(commandLine)
        bbox = stderr.read()
        if bbox.find("BoundingBox") != -1:
            nochmal = open(fn).read()
            f = open(fn,"w")
            f.write(bbox + nochmal)
            f.close()
        else:
            Dialogs.complain("Problem calculating bounding box : %s" % bbox)

        # generate png        
        commandLine = '%s -g%sx%s -q -dBATCH -dNOPAUSE -sDEVICE=png16m -r%s -sOutputFile=%s %s -c showpage' % (
            gscommand, int(maxx+pngBound)*ptFactor, int(maxy+pngBound)*ptFactor, 70*ptFactor, fnpng, fn)
        #print commandLine
        (stdin, stdout, stderr) = os.popen3(commandLine)
        errtxt = stderr.read()
        if errtxt != "":
            Dialogs.complain("%s is not on your path or has failed in some way : failure %s" % (gscommand, errtxt))
    def doUndo(self):
        self.central.undo(self.name)
    def doRedo(self):
        self.central.redo(self.name)
    def doRedraw(self):
        self.clearSelector()
        self.update()
    def doReload(self):
        UnitCache.flush()
        self.central.reload(self.name)        
    def doSave(self,scr=False):
        self.clearSelector()
        if self.textDirty:
            self.sourceEditor.accept()
        self.rescueResources()
        self.resource.flush()
        def saveSourceFile(fn,txt):
            FileUtils.makebackup(fn)
            f = open(fn,"w")
            # the lack of a trailing cr was causing recognition problems in emacs (I think)
            if txt[-1:] != "\n": txt += "\n"
            f.write(txt)
            f.close()
        if not scr:
            ScriptRecorder.write("doSave()")
        spec, body = self.sourceEditor.getSource()
        saveSourceFile(self.specTopNode.source, spec)

        saveSourceFile(self.bodyTopNode.source, body)
        # fully compile and codegen if it will work at all
        self.central.update(self.name,spec,body,saveOutput=True)
        self.setClean()
        Message.info(self.name + " saved")
        # and have a try at generating code too
    def doTest(self):
        for avatar in self.allAvatars():
            print avatar.name, avatar #OK
        #sys.stdout = 0
        import pdb; pdb.set_trace()
    def existsAvatar(self,withName):
        #print "existsAvatar:", withName
        for avatar in self.allAvatars():
            #print avatar.name
            if avatar.name == withName:
                return avatar
        return False
    def dupeCheck(self,name):
        if self.existsAvatar(name):
            Dialogs.complain("Object %s already exists" % name)
            return True
        else:
            return False
    # TBD refactor this lot using closures (or would it make it harder to read?)

    def goMoveMode(self,scr=False):
        self.modeString = "move"
        self.updateTitle()
        self.root.configure(cursor="fleur")
        self.mouseHandler = MoveHandler(self)
        if not scr:
            ScriptRecorder.write("goMoveMode()")

    def goAlignMode(self,scr=False):
        self.modeString = "align"
        self.updateTitle()
        self.root.configure(cursor="left_side")
        self.mouseHandler = AlignHandler(self)
        if not scr:
            ScriptRecorder.write("goAlignMode()")

    def goSelectMode(self,scr=False):
        self.modeString = "select"
        self.updateTitle()
        self.root.configure(cursor="icon")
        self.mouseHandler = SelectHandler(self)
        if not scr:
            ScriptRecorder.write("goSelectMode()")


    def goNewObjectMode(self,scr=False):
        self.modeString = "new object"
        self.updateTitle()
        self.root.configure(cursor="dotbox")
        self.mouseHandler = NewObjectHandler(self)
        if not scr:
            ScriptRecorder.write("goNewObjectMode()")

    def goNewConnectionMode(self, scr=False):
        self.modeString = "new connection"
        self.updateTitle()
        self.root.configure(cursor="sb_h_double_arrow")
        self.mouseHandler = NewConnectionHandler(self)
        if not scr:
            ScriptRecorder.write("goNewConnectionMode()")
        
    def goLocateMode(self, scr=False):
        self.modeString = "locate"
        self.updateTitle()
        self.root.configure(cursor="question_arrow")
        self.mouseHandler = LocateHandler(self)
        if not scr:
            ScriptRecorder.write("goLocateMode()")

    def goExplainMode(self, scr=False):
        self.modeString = "explain"
        self.updateTitle()
        self.root.configure(cursor="question_arrow")
        self.mouseHandler = ExplainHandler(self)
        if not scr:
            ScriptRecorder.write("goExplainMode()")

        
    def checkLock(self):
        if self.textDirty:
            Dialogs.complain("Graphic Editing Locked, abort or accept your text edit changes before you can continue")
        return self.textDirty

    def msedwn(self,event,sd=None):
        if self.checkLock(): return 
        x,y = self.translateEvent(event)
        #print "pressed at",x,y
        self.mouseHandler.msedwn(x,y,sd,event)
    def msemv(self,event,sd=None):
        if self.checkLock(): return         
        x,y = self.translateEvent(event)
        #print "moved at",x,y
        self.mouseHandler.msemv(x,y,sd)        
    def mseup(self,event,sd=None):
        if self.checkLock(): return 
        x,y = self.translateEvent(event)
        #print "up at",x,y
        self.mouseHandler.mseup(x,y,sd)
    def doubleClick(self,event,sd=None):
        x,y = self.translateEvent(event)
        #print "double at",x,y        
        self.mouseHandler.msedbl(x,y,sd)
    def motion(self,event):
        x,y = self.translateEvent(event)
        #print x,y
        self.target = self.findTarget(x,y)
        if self.target:
            self.target.heat(x,y)
        if self.target == self.oldTarget:
            pass
        else:
            if self.oldTarget:
                #print "old", self.oldTarget
                self.oldTarget.cool()
            if self.target:
                self.target.heat(x,y)
            #print "new", self.target
            self.oldTarget = self.target
    def drawSelector(self,coords):
        if not self.selectHandle:
            self.selectHandle = self.create_rectangle(coords,outline=Colors.select)
        self.coords(self.selectHandle, coords)
    def moveSelector(self, dx, dy):
        self.selectCoords = DiagMaths.addOffset(self.selectCoords,dx,dy)
        self.coords(self.selectHandle, self.selectCoords)
    def setSelector(self, coords):
        self.selectCoords = coords
    def clearSelector(self):
        if self.selectHandle:
            self.delete(self.selectHandle)
            self.selectHandle = None
            
class Handler:
    def __init__(self,drawing):
        self.target=None
        self.drawing=drawing
    def msedbl(self,x,y,sd):
        self.target = self.drawing.findTarget(x,y)
        if self.target:
            avType = self.target.avatarType()
            if avType == "Child":
                self.drawing.central.openCapsule(self.target.capName())
            elif avType == "Note":
                sd = Dialogs.askNote(self.drawing.root, text=self.target.words)
                if sd:
                    self.target.words = sd['text']
                    self.drawing.setDirty()
                    self.drawing.update()
            else:
                self.drawing.sourceEditor.showSource(self.target.node)
    def msemv(self,x,y,sd):
        pass
    def mseup(self,x,y,sd):
        pass

DocuDumper.startDoc("modeDetails.inc")
DocuDumper.addGroup("The modes and their effects are as follows")
DocuDumper.addItem("Move", "The default mode, you can move objects by dragging them around the window or "+
                   "you can resize them if you click over a corner of an object while it is red")
class MoveHandler(Handler):
    def msedwn(self,x,y,sd,event):
        def kickDependentPorts(avatars): # this stops ports in a selection from getting two bashes at moving when all avatars are told to move
            deps = []
            for child in avatars:
                if child.avatarType == "Child":
                    for port in child.childPorts:
                        if port in avatars:
                            deps.append(port)
            return [avatar for avatar in avatars if not avatar in deps] 
        def kickLabels(avatars): # this filters out the connection labels
            return [avatar for avatar in avatars if not avatar.avatarType() in ["ConnLabel","PortLabel"]]
                        
        if not sd:
            ScriptRecorder.write("msedwn(%s,%s)" % (x,y))
        if self.drawing.selectHandle and DiagMaths.isUnder(x,y,self.drawing.selectCoords):
            self.select = True
            self.targets = kickDependentPorts([avatar for avatar in self.drawing.allAvatars() if avatar.isInside(self.drawing.selectCoords)])
            self.targets = kickLabels(self.targets)
        else:
            self.select = False
            avatars = self.drawing.allAvatars()
            if Options.options.arrowsOff:
                avatars = kickLabels(avatars)
            self.targets = [self.drawing.findTarget(x,y,avatars)]
        #if self.target == self.drawing.capsule:
        #    self.target = None # Don't just let him move the capsule around
        self.startx = x
        self.starty = y
    def msemv(self,x,y,sd):
        # print x,y
        if self.targets:
            if not sd:
                if Options.options.animate:
                    ScriptRecorder.write("msemv(%s,%s)" % (x,y))
            dx = x - self.startx
            dy = y - self.starty
            self.drawing.setDirty()
            for target in self.targets:
                if target:
                    target.move(dx,dy)
                    if target.__class__.__name__ == "Child":
                        target.updateCameos()
            if self.select:
                self.drawing.moveSelector(dx,dy)
            for observer in self.drawing.cameoObservers:
                observer.updateCameos()
            self.startx = x
            self.starty = y

    def mseup(self,x,y,sd):
        if not sd:
            ScriptRecorder.write("msemv(%s,%s)" % (x,y))
            ScriptRecorder.write("mseup(%s,%s)" % (x,y))
        self.targets=None

DocuDumper.addItem("Select", "In this mode you can drag to create a box around items which you can then either move as a group in move mode"
                   " or manipulate in other useful ways together in align mode")

class SelectHandler(Handler):
    def msedwn(self,x,y,sd,event):
        if not sd:
            ScriptRecorder.write("msedwn(%s,%s)" % (x,y))
        self.startx = x
        self.starty = y
        self.drawing.drawSelector((x,y,x,y))
    def msemv(self,x,y,sd):
        self.drawing.drawSelector((self.startx, self.starty, x,y))
    def mseup(self,x,y,sd):
        self.endx = x
        self.endy = y
        if (abs(self.endx-self.startx) < minSelect) or (abs(self.endy-self.starty) < minSelect):
            self.drawing.clearSelector()
        else:
            self.drawing.setSelector((min(self.startx, self.endx), min(self.starty,self.endy),
                                      max(self.startx, self.endx), max(self.starty,self.endy)))
        if not sd:
            ScriptRecorder.write("msemv(%s,%s)" % (x,y))
            ScriptRecorder.write("mseup(%s,%s)" % (x,y))

DocuDumper.addItem("Align", "Acts on the currently selected set of objects and allows you to line them up, evenly distribute them or make them all the same size")

class AlignHandler(Handler):
    def msedwn(self,x,y,sd,event):
        if not sd:
            ScriptRecorder.write("msedwn(%s,%s)" % (x,y))
        if not (self.drawing.selectHandle and DiagMaths.isUnder(x,y,self.drawing.selectCoords)):
            return 
        self.leader = self.drawing.findTarget(x,y)
        if not self.leader:
            return 
        self.followers = [avatar for avatar in self.drawing.allignableAvatars()
                          if avatar.isInside(self.drawing.selectCoords) and avatar != self.leader]
        for follower in self.followers:
            follower.outline = list(follower.outline) # some of these were tuples, which we couldnt change
        self.x = x
        self.y = y
        newmenu = Menu(self.drawing.root, tearoff=0)
        newmenu.add_command(label="dismiss",     command=self.doNothing)
        newmenu.add_command(label="flush left",      command=self.flushLeft)
        newmenu.add_command(label="flush right",     command=self.flushRight)
        newmenu.add_command(label="align width",     command=self.alignWidth)
        newmenu.add_command(label="flush top",       command=self.flushTop)
        newmenu.add_command(label="flush bottom",    command=self.flushBottom)
        newmenu.add_command(label="align height",    command=self.alignHeight)
        newmenu.add_command(label="same width",    command=self.sameWidth)
        newmenu.add_command(label="same height",    command=self.sameHeight)
        newmenu.add_command(label="same width and height",  command=self.sameWidthHeight)
        newmenu.add_command(label="distribute vertical",  command=self.distributeVertical)
        newmenu.add_command(label="distribute horizontal",  command=self.distributeHorizontal)
        newmenu.post(event.x_root, event.y_root)

    def doNothing(self): pass

    
    def redraw(self, follower):
        follower.setShape()
        follower.move(0,0)
    
    def flushLeft(self):
        for follower in self.followers:
            diff = self.leader.outline[0] - follower.outline[0]
            follower.outline[0] += diff
            follower.outline[2] += diff
            self.redraw(follower)

    def flushRight(self):
        for follower in self.followers:
            diff = self.leader.outline[2] - follower.outline[2]
            follower.outline[0] += diff
            follower.outline[2] += diff
            self.redraw(follower)            

    def alignWidth(self):
        self.flushLeft()
        self.flushRight()
    
    def flushTop(self):
        for follower in self.followers:
            diff = self.leader.outline[1] - follower.outline[1]
            follower.outline[1] += diff
            follower.outline[3] += diff
            self.redraw(follower)                        

    def flushBottom(self):
        for follower in self.followers:
            diff = self.leader.outline[3] - follower.outline[3]
            follower.outline[1] += diff
            follower.outline[3] += diff
            self.redraw(follower)                                    

    def alignHeight(self):
        self.flushTop()
        self.flushBottom()

    def sameWidth(self):
        leaderWidth = self.leader.outline[2] - self.leader.outline[0]
        for follower in self.followers:
            follower.outline[2] = follower.outline[0] + leaderWidth
            self.redraw(follower)                                    
        
    def sameHeight(self):
        leaderHeight = self.leader.outline[3] - self.leader.outline[1]
        for follower in self.followers:
            follower.outline[3] = follower.outline[1] + leaderHeight
            self.redraw(follower)                                            

    def sameWidthHeight(self):
        self.sameWidth()
        self.sameHeight()

    

    def distribute(self,idx):
        all = self.followers + [ self.leader ]
        if len(all) < 3:
            print "three or more needed for a distribution"
            return
        def cmpy(a,b):
            if a.outline[idx] < b.outline[idx]:
                return -1
            elif a.outline[idx] == b.outline[idx]:
                return 0
            else:
                return 1
        all.sort(cmpy)
        minavatar = all[0]
        maxavatar = all[-1]

        distance = maxavatar.outline[idx] - minavatar.outline[idx]
        step = distance / (len(all) - 1)
        ctr = 0
        for avatar in all[1:-1]:
            ctr += 1
            offset = minavatar.outline[idx] + (step * ctr)
            height = avatar.outline[idx+2] - avatar.outline[idx]
            avatar.outline[idx] = offset
            avatar.outline[idx+2] = offset + height
            self.redraw(avatar)
            
    def distributeVertical(self):
        self.distribute(1)
    
    def distributeHorizontal(self):
        self.distribute(0)

DocuDumper.addItem("New Object", "Create new objects, for each left click a menu of possible objects is shown, once a selection has been made" +
                   " a dialog is presented asking for the necessary details")

class NewObjectHandler(Handler):
    def doNothing(self): pass
    def msedwn(self,x,y,sd,event):
        self.x = x
        self.y = y
        self.sd = sd
        self.dialPos = "+%d+%d" % (event.x_root, event.y_root) # so we can position dialogs ergonomically
        newmenu = Menu(self.drawing.root, tearoff=0)
        newmenu.add_command(label="dismiss",     command=self.doNothing)
        newmenu.add_command(label="new activity",command=self.newActivity)
        newmenu.add_command(label="new procedure",command=self.newProcedure)
        newmenu.add_command(label="new message", command=self.newMessage)
        newmenu.add_command(label="new data",    command=self.newData)
        newmenu.add_command(label="new trigger", command=self.newTrigger)
        newmenu.add_command(label="new timer",   command=self.newTimer)
        newmenu.add_command(label="new state",   command=self.newState)
        newmenu.add_command(label="new child",   command=self.newChild)
        newmenu.add_command(label="new port",    command=self.newPort)
        newmenu.add_command(label="new note",    command=self.newNote)
        newmenu.post(event.x_root, event.y_root)

    def newActivity(self):
        if not self.sd:
            self.sd = Dialogs.askActNamePortName(self.drawing.root,self.dialPos,[port.name for port in self.drawing.ports])
            if not self.sd: return # he canceled
            ScriptRecorder.write("msedwn(%s,%s,%s)" % (self.x,self.y,str(self.sd)))
        actName = self.sd['name']
        portName = self.sd['port']
        if self.drawing.dupeCheck(actName): return
        port = self.drawing.existsAvatar(portName)
        if not port:
            Dialogs.complain("%s does not exist" % portName)    
            return
        elif port.avatarType() != "Port":
            Dialogs.complain("%s is not a port but a %s" % (portName,port.avatarType()))   
            return
        newact = Avatars.Activity(actName,None)
        newact.setXY(self.x,self.y)
        self.drawing.bodyTopNode.appendActivity(actName,self.drawing.specTopNode,self.sd)
        self.drawing.activities.append(newact)
        self.drawing.setDirty()
        self.drawing.update()


    def newProcedure(self):
        if not self.sd:
            self.sd = Dialogs.askProcNamePortName(self.drawing.root,self.dialPos,[port.name for port in self.drawing.ports])
            if not self.sd: return # he canceled
            ScriptRecorder.write("msedwn(%s,%s,%s)" % (self.x,self.y,str(self.sd)))
        procName = self.sd['name']
        portName = self.sd['port']
        if self.drawing.dupeCheck(procName): return
        port = self.drawing.existsAvatar(portName)
        if not port:
            Dialogs.complain("Port %s does not exist" % portName)    
            return
        elif port.avatarType() != "Port":
            Dialogs.complain("%s is not a port but a %s" % (portName,port.avatarType()))   
            return
        newproc = Avatars.Procedure(procName,None)
        newproc.setXY(self.x,self.y)
        self.drawing.bodyTopNode.appendProcedure(procName,self.drawing.specTopNode,self.sd)
        self.drawing.setDirty()
        self.drawing.update()


    def newMessage(self):
        if not self.sd:
            self.sd = Dialogs.askMessage(self.drawing.root, self.dialPos, [port.name for port in self.drawing.ports])
            if not self.sd: return
        messageName = self.sd["name"]
        # TBD check for dupes
        #newmess = Avatars.Message(messageName,None)
        self.drawing.specTopNode.appendMessage(self.sd)
        #self.drawing.messages.append(newmess)
        self.drawing.setDirty()
        self.drawing.update()
        
    def newData(self):
        if not self.sd:
            self.sd = Dialogs.askData(self.drawing.root,self.dialPos)
            if not self.sd: return             
            ScriptRecorder.write("msedwn(%s,%s,%s)" % (self.x,self.y,str(self.sd)))
        name = self.sd['name']
        type = self.sd['type']
        if self.drawing.dupeCheck(name): return 
        newdata = Avatars.DataStore(name,None)
        newdata.setXY(self.x,self.y)
        self.drawing.bodyTopNode.appendDataStore(name,type)
        self.drawing.datastores.append(newdata)
        self.drawing.setDirty()
        self.drawing.update()        

    def newState(self):
        if not self.sd:
            self.sd = Dialogs.askState(self.drawing.root,self.dialPos)
            if not self.sd: return             
            ScriptRecorder.write("msedwn(%s,%s,%s)" % (self.x,self.y,str(self.sd)))
        name = self.sd['name']
        if self.drawing.dupeCheck(name): return 
        newstate = Avatars.State(name,None)
        newstate.setXY(self.x,self.y)
        self.drawing.bodyTopNode.appendState(name)
        self.drawing.states.append(newstate)
        
        if len(self.drawing.states) == 1:
            start = Avatars.Start('*start*',None)
            start.setXY(self.x+100,self.y+100)
            self.drawing.bodyTopNode.appendStart(startState=name)
            self.drawing.start = start
        self.drawing.setDirty()
        self.drawing.update()        

    def newTrigger(self):
        if not self.sd:
            self.sd = Dialogs.askTrigger(self.drawing.root,self.dialPos)
            if not self.sd: return             
            ScriptRecorder.write("msdwn(%s,%s,%s)" % (self.x,self.y,str(self.sd)))
        name = self.sd['name']
        if self.drawing.dupeCheck(name): return 
        newtrigger = Avatars.Trigger(name,None)
        newtrigger.setXY(self.x,self.y)
        self.drawing.bodyTopNode.appendTrigger(name,dialDict=self.sd)
        self.drawing.triggers.append(newtrigger)
        self.drawing.setDirty()
        self.drawing.update()        

    def newTimer(self):
        if not self.sd:
            self.sd = Dialogs.askTimer(self.drawing.root,self.dialPos)
            if not self.sd: return 
            ScriptRecorder.write("msdwn(%s,%s,%s)" % (self.x,self.y,str(self.sd)))
        name = self.sd['name']
        if self.drawing.dupeCheck(name): return 
        newtimer = Avatars.Timer(name,None)
        newtimer.setXY(self.x,self.y)
        self.drawing.bodyTopNode.appendTimer(name,dialDict=self.sd)
        self.drawing.timers.append(newtimer)
        self.drawing.setDirty()
        self.drawing.update()

    def newChild(self):
        if not self.sd:
            self.sd = Dialogs.askChild(self.drawing.root,self.dialPos)
            if not self.sd: return 
            ScriptRecorder.write("msdwn(%s,%s,%s)" % (self.x,self.y,str(self.sd)))
        childname = self.sd['childname']
        capsulename = self.sd['capsulename']
        if self.drawing.dupeCheck(childname): return 
        cd = self.drawing.central.openCapsule(capsulename + ".m3") # TBD
        newchild = Avatars.Child(childname,None)
        newchild.setXY(self.x,self.y)
        self.drawing.bodyTopNode.appendChild(childname,capsulename)
        self.drawing.childCapsules.append(newchild)
        self.drawing.setDirty()
        self.drawing.update()                

    def newPort(self):
        if not self.sd:
            self.sd = Dialogs.askPort(self.drawing.root,self.dialPos)
            if not self.sd: return 
            ScriptRecorder.write("msdwn(%s,%s,%s)" % (self.x,self.y,str(self.sd)))
        portname = self.sd['name']
        child = self.drawing.findTarget(self.x,self.y)
        if child and (child.avatarType() == "Child"):
            raise "not implemented"
        else:
            if self.drawing.dupeCheck(portname): return 
            newport = Avatars.Port(portname,None)
            newport.setXY(self.x,self.y)
            self.drawing.specTopNode.appendPort(portname)
        self.drawing.ports.append(newport)
        self.drawing.setDirty()
        self.drawing.update()
        
    def newNote(self):
        if not self.sd:
            self.sd = Dialogs.askNote(self.drawing.root,self.dialPos)
            if not self.sd: return             
            ScriptRecorder.write("msdwn(%s,%s,%s)" % (self.x,self.y,str(self.sd)))
        text = self.sd['text']
        name = "**Note%s" % time.time()
        self.drawing.resource.writeNote(name,text, (self.x,self.y), [])
        # poke this into the resources and then wait for the big redraw
        self.drawing.setDirty()
        self.drawing.update()

DocuDumper.addItem("Locate", "clicking on any graphical item will highlight its source in the text window")
        
class LocateHandler(Handler):
    def msedwn(self,x,y,sd,event):
        self.target = self.drawing.findTarget(x,y)
        #print "locating", target, target.node, target.node.lineno
        if self.target:
            self.drawing.sourceEditor.showSource(self.target.node)
    def mseup(self,x,y,sd):
        if self.target:
            self.drawing.sourceEditor.coolSource()

DocuDumper.addItem("Explain", "selectively show and hide connections from all or selected avatars")            

class ExplainHandler(Handler):
    def doNothing(self): pass
    
    def msedwn(self,x,y,sd,event):
        self.x = x
        self.y = y
        self.sd = sd
        self.dialPos = "+%d+%d" % (event.x_root, event.y_root) # so we can position dialogs ergonomically
        newmenu = Menu(self.drawing.root, tearoff=0)
        newmenu.add_command(label="dismiss",     command=self.doNothing)
        newmenu.add_command(label="hide",        command=self.hide)
        newmenu.add_command(label="show",        command=self.show)
        newmenu.add_command(label="show only",   command=self.showOnly)        
        newmenu.add_command(label="hide all",    command=self.hideAll)
        newmenu.add_command(label="show all",    command=self.showAll)
        newmenu.post(event.x_root, event.y_root)
        self.target = self.drawing.findTarget(x,y)

    def hide(self):
        if self.target:
            if self.target.avatarType() == "Child":
                for target in self.target.childPorts:
                    for conn in target.connections:
                        conn.setInvisible()
            else:
                for conn in self.target.connections:
                    conn.setInvisible()
    def show(self): 
        if self.target:
            if self.target.avatarType() == "Child":
                for target in self.target.childPorts:
                    for conn in target.connections:
                        conn.setVisible()
            else:
                for conn in self.target.connections:
                    conn.setVisible()
    def hideAll(self):
        import Connection
        Connection.setAllInvisible(self.drawing.connections)
    def showAll(self):
        import Connection
        Connection.setAllVisible(self.drawing.connections)        
    def showOnly(self):
        self.hideAll()
        self.show()
DocuDumper.addItem("New Connection", "Create new connections: simply drag from the source object to the target object, the tool will guess what you want to do")

            
class NewConnectionHandler(Handler):
    def msedwn(self,x,y,sd,event):
        self.updated = False
        self.fromTarget = self.drawing.findTarget(x,y)
        self.dialPos = "+%d+%d" % (event.x_root, event.y_root) # so we can position dialogs ergonomically        
        if self.fromTarget:
            if not sd:
                ScriptRecorder.write("msedwn(%s,%s)" % (x,y))
            self.fromx, self.fromy = x,y
            self.line = self.drawing.create_line((self.fromx, self.fromy, self.fromx, self.fromy), arrow="last")                    
    def msemv(self,x,y,sd):
        if self.fromTarget:
            if not sd:
                if Options.options.animate:
                    ScriptRecorder.write("msemv(%s,%s)" % (x,y))
            self.drawing.coords(self.line, (self.fromx, self.fromy, x, y))                    
    def mseup(self,x,y,sd):
        if self.fromTarget:
            if self.fromTarget.avatarType() == "Note":
                self.handleNoteConnection(x,y,sd)
                return 
            if self.fromTarget.avatarType() == "State":
                self.handleStateConnection(x,y,sd)
                return 
            if not sd:
                ScriptRecorder.write("mseup(%s,%s)" % (x,y))
            self.toTarget = self.drawing.findTarget(x,y)
            if self.toTarget and (self.toTarget != self.fromTarget):
                conn = Connection.makeIfLegal(self.fromTarget, self.toTarget, self.drawing)
                if conn:
                    conn.createSource()
                    self.drawing.setDirty()
                    self.drawing.update()
                    self.updated = True
                else:
                    Message.info("bad connection")
            if not self.updated:
                self.drawing.delete(self.line)
            self.updated = False
            self.fromTarget=None

    def handleStateConnection(self,x,y,sd):
        self.toTarget = self.drawing.findTarget(x,y)
        stateToOpen = self.toTarget == self.drawing.capsule
        stateToState = self.toTarget and (
            self.toTarget.avatarType() == "State") and (
            self.toTarget != self.fromTarget)
        # only do this either if you have raised the mouse in the middle of the background capsule
        # or on another state
        if stateToOpen or stateToState:
            if not sd:
                sd = Dialogs.askTransition(self.drawing.root,self.dialPos, [port.name for port in self.drawing.ports])
                if not sd: return 
                ScriptRecorder.write("mseup(%s,%s,%s)" % (x,y,str(sd)))
            name = self.fromTarget.name + ":" + sd['name']
            if self.drawing.dupeCheck(name):
                self.drawing.delete(self.line)
                return 
            if stateToState:
                # plant the transition between the two states
                x,y = self.toTarget.between(self.fromTarget)
            newtrans = Avatars.Transition(name,None)
            newtrans.setXY(x,y)
            transNode = self.drawing.bodyTopNode.appendTransition(
                self.drawing.specTopNode,self.fromTarget,sd)
            newtrans.node = transNode # TBD messy hack FIXME
            self.drawing.transitions.append(newtrans)
            newtrans.setOwningState(self.fromTarget)
            self.drawing.delete(self.line)
            conn1 = Connection.make(self.fromTarget,newtrans,self.drawing)
            if stateToState:
                conn2 = Connection.make(newtrans,self.toTarget,self.drawing)
                conn2.createSource()
            self.fromTarget=None
            self.drawing.setDirty()
            self.drawing.update()


    def handleNoteConnection(self,x,y,sd):
        self.fromTarget.addArrowXY(x,y)
        self.drawing.setDirty()
        self.drawing.update()

DocuDumper.endGroup()
DocuDumper.endDoc()

if __name__ == "__main__":
    root = Tk()
    foo = CapsuleDrawing(None,None)
    root.mainloop()
