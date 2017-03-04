import PSUtils
import Colors
import LoadSrc
import Exceptions
import Message
import DiagMaths
import string


def setAllInvisible(allConnections):
    for conn in allConnections:
        conn.setInvisible()
def setAllVisible(allConnections):
    for conn in allConnections:
        conn.setVisible()

    
def createCameoConnectionsPS(drawing, parentDrawing, childAvatar,psfile):
    capOutline=parentDrawing.capsule.outline
    constraints=childAvatar.outline
    for connection in parentDrawing.connections:
        outline = DiagMaths.constrain(connection.xsandys(), capOutline, constraints)
        psfile.write("gsave %s setrgbcolor newpath %s 1 5 7 arrow stroke grestore\n" % (
            connection.setPSColor(), PSUtils.arrayAsString(outline)))
    
def createCameoConnections(drawing, parentDrawing, childAvatar):
    import Avatars
    cameos = []
    capOutline=parentDrawing.capsule.outline
    constraints=childAvatar.outline
    for connection in parentDrawing.connections:
        if connection.__class__.__name__ == "ConnectPortConnection":
            arrows=connection.calcArrow()
        else:
            arrows="last"
        cameos.append(Avatars.Cameo(drawing,connection,
                                    parentDrawing,
                                    childAvatar,
                                    drawing.create_line(
            DiagMaths.constrain(connection.xsandys(), capOutline, constraints), arrow=arrows, fill=connection.getColor()),
                                    cameoType=Avatars.Cameo.connection))
    return cameos
class Connection:
    def __init__(self, start, end, drawing):
        #print "connection init",start,end, self.__class__.__name__
        self.start = start
        self.end = end
        self.drawing = drawing
        self.visible = True
        self.labels = []
        end.addConnections(self)
        start.addConnections(self)
        #allConnections.append(self)
    def setVisible(self):
        self.drawing.config(self.line,fill=self.getColor())
        self.drawing.lift(self.line)
        for label in self.labels:
            label.setVisible()
    def setInvisible(self):
        self.drawing.config(self.line,fill=Colors.cancolor)
        self.drawing.lower(self.line)        
        for label in self.labels:
            label.setInvisible()
    def getColor(self):
        return self.connColor()
    def connColor(self):
        return "black"
    def xsandys(self):
        fromx,fromy = self.start.edge(self.end.middle())
        tox,toy = self.end.edge(self.start.middle())
        return (fromx,fromy,tox,toy)
    def move(self):
        self.drawing.coords(self.line,self.xsandys())
    def connectionType(self):
        return self.__class__.__name__
    def setPSColor(self):
        return PSUtils.makeColor(self.connColor())
    def getPostscript(self,f):
        xsandys = self.xsandys()
        f.write("gsave %s setrgbcolor newpath %s 1 5 7 arrow stroke grestore\n" % (
            self.setPSColor(), PSUtils.arrayAsString(self.xsandys())))
    def addLabel(self,connLabels): pass

    def createSourceHelper(self, connectionType):
        connectToken = {'cmc': '->', 'cpc': '<=>'}[connectionType]
        def addMessage(conn):
            # Compensate the fact that messages are no longer graphically shown
            # by asking for them afterwards if the user has pointed to a port
            if connectionType == 'cmc':
                if conn.node.__class__.__name__ == "PortNode":
                    x,y = conn.middle()
                    msg = self.drawing.chooseMessage(conn.node.getType(),x,y)
                    return ".%s" % msg
                else:
                    return ""
            else:
                return ""
        sourceMsg = self.start.name + addMessage(self.start)
        destMsg = self.end.name + addMessage(self.end)
        topNode = self.drawing.capsule.node
        # does this guy even have a connect node ?
        if topNode.block.connections.isNULL():
            connNode = LoadSrc.compileFragment('Connections', "\n  CONNECT\n    %s %s %s;" % (sourceMsg,connectToken,destMsg))
            #print connNode.regen()
            topNode.appendConnectionSection(connNode)
        else:
            connNode = LoadSrc.compileFragment('AnyConnection', "\n  %s %s %s" % (sourceMsg,connectToken,destMsg))
            sepNode = LoadSrc.compileFragment('tokSEMI', ";")
            topNode.appendConnection(connNode,sepNode)


class DataFlowConnection(Connection):
    def __init__(self, start, end, drawing):
#        import pdb; pdb.set_trace()
        Connection.__init__(self,start,end,drawing)
    def connColor(self):
        return Colors.dataflowcolor
    def getPov(self,f):
        f.write("Arrow (%s,%s,%s,%s, Grey)\n" % tuple(DiagMaths.flipYCoords(self.xsandys())))
    def draw(self):
        self.line = self.drawing.create_line(self.xsandys(),arrow="last", fill=self.getColor())
    def createSource(self):
        startRole = self.start.avatarType()
        endRole = self.end.avatarType()
        if (startRole == "DataStore") and ((endRole == "Activity") or (endRole == "Transition")):
            depInfo = self.createDependencyInfo("READS",self.start.name,self.end)
        elif (endRole == "DataStore") and ((startRole == "Activity") or (startRole == "Transition")):
            depInfo = self.createDependencyInfo("WRITES",self.end.name,self.start)
        else:
            print "***********Not implemented" #OK
    def createDependencyInfo(self,dir,name,insTarget):
        depInfo = LoadSrc.compileFragment('Decl', '\n    %s %s ;' % (dir, name))
        sepNode = LoadSrc.compileFragment('tokSEMI', ";")
        insTarget.node.appendDependencyInfo(depInfo,sepNode)
        
class CallConnection(Connection):
    def connColor(self):
        return Colors.callcolor

    def getPov(self,f):
        f.write("Arrow (%s,%s,%s,%s, Green)\n" % tuple(DiagMaths.flipYCoords(self.xsandys())))
    def draw(self):
        self.line = self.drawing.create_line(self.xsandys(),arrow="last", fill=self.getColor())
    def addLabel(self,connLabels):
        import Avatars
        if self.end.avatarType() in ["Port", "ChildPort"]:
            cl = Avatars.ConnLabel("*CallLabel*" + self.start.name + "*" + string.join(self.message,"."), None)
            x,y = DiagMaths.middle(self.xsandys())
            cl.create(x,y)
            cl.setPorts(self.start,self.end)
            cl.setWords([self.message[-1]])
            connLabels.append(cl)
            self.labels.append(cl)
    def setMessage(self,message):
        #print "setting message", message
        self.message = message
    def createSource(self):
        self.createSourceHelper('cmc')
class MessageConnection(Connection):
    def connColor(self):
        return Colors.messagecolor
    def getPov(self,f):
        f.write("Arrow (%s,%s,%s,%s, Red)\n" % tuple(DiagMaths.flipYCoords(self.xsandys())))

    def draw(self):
        self.line = self.drawing.create_line(self.xsandys(),arrow="last", fill=self.getColor())



class ConnectMessageConnection(MessageConnection):
    def createSource(self):
        self.createSourceHelper('cmc')

class ConnectPortConnection(MessageConnection):
    def connColor(self):
        return self.color
    def __init__(self, start, end, drawing):
        MessageConnection.__init__(self, start, end, drawing)
        self.setColor(self.start,self.end)
    def createSource(self):
        self.createSourceHelper('cpc')
    def calcArrow(self):
        last = self.start.getMessagesFor(self.end)
        first = self.end.getMessagesFor(self.start)
        if first and last:
            return "both"
        elif first:
            return "first"
        elif last:
            return "last"
        else:
            return "none"
    def draw(self):
        self.line = self.drawing.create_line(self.xsandys(), arrow=self.calcArrow(), fill=self.getColor(), width=2)
        # TBD tailor arrow ends to protocol direction(s)
    def addLabel(self,connLabels):
        import Avatars
        # one for each direction
        x,y = DiagMaths.middle(self.xsandys())
        for a,b in ((self.start, self.end), (self.end, self.start)):
            cl = Avatars.ConnLabel("*ConLabel" + a.name + "*" + b.name,None)
            cl.create(x,y)
            cl.setPorts(a,b)

            cl.setWords(a.getMessagesFor(b))
            connLabels.append(cl)
            self.labels.append(cl)
    def setColor(self,a,b):
        synch1 = a.getSynchFor(b)
        synch2 = b.getSynchFor(a)
        if synch1 and synch2:
            self.color = Colors.callcolor
        else:
            self.color = Colors.messagecolor

class MessageToMessageConnection(ConnectPortConnection):
    def __init__(self, start, end, drawing):
        MessageConnection.__init__(self, start, end, drawing)
        if end.avatarType() == "Procedure":
            self.color = Colors.callcolor 
        else:
            self.color = Colors.messagecolor
    def setStartEndMessages(self, start, end):
        self.startMessage = start
        self.endMessage = end
    def addLabel(self, connLabels):
        import Avatars
        x,y = DiagMaths.middle(self.xsandys())
        cl = Avatars.ConnLabel("*MsgMsgLabel*" + self.startMessage + "*" + self.endMessage, None)
        cl.create(x,y)
        cl.setPorts(self.start,self.end)
        if self.end.avatarType() in ["Port", "ChildPort"]:
            end = " -> %s" % self.endMessage
        else:
            end = ""
        cl.setWords(["%s%s" % (self.startMessage, end)])
        connLabels.append(cl)
        self.labels.append(cl)
    def draw(self):
        self.line = self.drawing.create_line(self.xsandys(),arrow="last", fill=self.color)
        
class SendsMessageConnection(MessageConnection):
    def createSource(self):
        sendsNode = LoadSrc.compileFragment('Decl', '\n    SENDS %s;' % self.end.name)
        self.start.node.appendSendsDecl(sendsNode)
    def addLabel(self,connLabels):
        import Avatars
        x,y = DiagMaths.middle(self.xsandys())
        cl = Avatars.ConnLabel("*SendsMessageLabel*" + self.start.name + "*" + self.end.name + "*" + self.message, None)
        cl.create(x,y)
        cl.setPorts(self.start,self.end)
        cl.setWords([self.message])
        connLabels.append(cl)
        self.labels.append(cl)
    def setMessage(self,message):
        self.message = message
    
def ImplicitConnection(port, avatar, drawing):
    if avatar.avatarType() == "Activity":
        return MessageConnection(port,avatar,drawing)
    elif avatar.avatarType() == "Procedure":
        return CallConnection(port,avatar,drawing)
    else:
        raise "WTF ", avatar.avatarType()
    
class TransitionConnection(Connection):
    def connColor(self):
        return Colors.statecolor

    def getPov(self,f):
        f.write("Arrow (%s,%s,%s,%s, Blue)\n" % tuple(DiagMaths.flipYCoords(self.xsandys())))
    def draw(self):
        self.line = self.drawing.create_line(self.xsandys(),arrow="last", fill=self.getColor())
    def createSource(self):
        # Source is only created for the connection leading away from the transition towards the new state
        if self.start.avatarType() != "Transition":
            Message.info("source is not a transition")
            return
        nextNode = LoadSrc.compileFragment('NextSt', "\n      NEXT %s" % self.end.name)
        sepNode1 = LoadSrc.compileFragment('tokSEMI', ";")
        sepNode2 = LoadSrc.compileFragment('tokSEMI', ";")
        self.start.node.appendNext(nextNode, sepNode1, sepNode2)


class NoteConnection(Connection):
    def createCameoConnectionsPS(drawing, parentDrawing, childAvatar,psfile): pass
    def createCameoConnections(drawing, parentDrawing, childAvatar): pass
    def connColor(self):
        return Colors.notecolor
    def draw(self):
        self.line = self.drawing.create_line(self.xsandys(),arrow="last", fill=self.getColor(), width=4)
    def createSource(self):
        pass


class LegalityTable:
    def __init__(self,sets):
        self.startEndTypes = sets
    def makeIfLegal(self, start, end, drawing, startHint, endHint):
        if startHint:
            startRole = startHint
        else:
            startRole = start.avatarType()
        if endHint:
            endRole = endHint
        else:
            endRole = end.avatarType()
        #print "iflegal",startRole,endRole
        for legalStart, legalEnd, connectionClass in self.startEndTypes:
            if (startRole == legalStart) and (endRole == legalEnd):
                return connectionClass(start,end,drawing)
        return False

# Overlap MSG/DAT with Timer -> Activity has been decided for MSG
# DAT dependencies can only be derived from the source
# see file connections.txt in doc directory for explanation of the following

dfc = DataFlowConnection
cmc = ConnectMessageConnection
cpc = ConnectPortConnection
smc = SendsMessageConnection
tc = TransitionConnection
nc = NoteConnection
cc = CallConnection
mmc = MessageToMessageConnection
connectionCheck = LegalityTable([
                                 ("Port", "Activity", cmc),
                                 ("ChildPort", "Activity", cmc),                                 
                                 ("Port", "TransitionProxy", cmc),
                                 ("ChildPort", "TransitionProxy", cmc),                                 
                                 
                                 ("Activity", "Port", smc),
                                 ("Activity", "ChildPort", smc),                                                                  
                                 ("Activity", "Activity", smc),
                                 ("Activity", "TransitionProxy", smc),
                                 ("Activity", "DataStore",dfc),                                 
                                 ("Activity", "Timer",dfc),

                                 ("DataStore", "Activity",dfc),
                                 ("DataStore", "Trigger",dfc),
                                 ("DataStore", "Transition",dfc),

                                 ("Port", "Port", cpc),
                                 ("ChildPort", "ChildPort", cpc),
                                 ("Port", "ChildPort", cpc),
                                 ("ChildPort", "Port", cpc),

                                 ("Timer", "Port", cmc),
                                 ("Timer", "ChildPort", cmc),                                 
                                 ("Timer", "Activity", cmc),
                                 ("Timer", "TransitionProxy", cmc),

                                 ("Trigger", "Port", cmc),
                                 ("Trigger", "ChildPort", cmc),                                 
                                 ("Trigger", "Activity", cmc),
                                 ("Trigger", "TransitionProxy", cmc),
                                 
                                 ("Transition", "Port", smc),
                                 ("Transition", "ChildPort", smc),                                 
                                 ("Transition", "Activity", smc),     
                                 ("Transition", "DataStore", dfc),                                 
                                 ("Transition", "State", tc),
                                 ("Transition", "TransitionProxy", smc),

                                 ("State", "Transition", tc),
                                 ("State", "State", tc),                              
                                 ("Start", "State", tc),

                                 ("Note", "NoteArrow", nc),

                                 ("Port", "Procedure", cc),

                                 ("Message", "Message", mmc),
                                 ])

def makeIfLegal(start,end,drawing):
    return connectionCheck.makeIfLegal(start,end,drawing,None,None)
def make(start,end,drawing,startHint=None,endHint=None):
    # hacked this so that message to message exists even if there are no avatars
    #print "start,end", start, end
    res = connectionCheck.makeIfLegal(start,end,drawing,startHint,endHint)
    if not res:
        message = "Illegal Connection between %s and %s" % (start.name, end.name)
        Message.error(message)
        raise Exceptions.EditorError(message)
    return res
def makeDataFlowConnection(start,end,drawing):
    return DataFlowConnection(start,end,drawing)
