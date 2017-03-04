import m3
import string
verbose = True
Cmin,Cmout,Cmint = range(3)
class MessagePoint:
    def __init__(self,owner,name,type):
        self.owner = owner
        self.type = type
        self.name = str(name)
        print ">>>>",self.name
        self.next = None
        self.level = -1
    def setNext(self,next):
        if self.next:
            print "ambiguous routing for", self.image()
        self.next = next
    def setLast(self):
        self.last, self.level = self.lastConnection(self.owner.level)
        if verbose:
            if self.last != self:
                print "routed from %s to %s" % (self.image(),self.last.image())
    def lastConnection(self,level):
        if not self.next:
            return self, min(self.owner.level,level)
        else:
            # if this is an across connection then bump up the level
            if (self.next.type == Cmin) and  (self.type == Cmout):
                newlevel = min(self.owner.level-1,level)
            else:
                newlevel = min(self.owner.level,level)
            return self.next.lastConnection(newlevel)
    def image(self):
        return "messagepoint %s of owner %s with level %s" % (self.name, self.owner.name, self.level)
    def plainName(self):
        return string.split(self.name,".")[1]

class CapsuleEntity:
    def __init__(self,name,specnode,bodynode):
        self.name = name
        self.specnode = specnode
        self.bodynode = bodynode
        self.transitions = self.bodynode.gatherTransitions() # TBD dubious use of EditNodes functionality
        self.activities = self.bodynode.gatherActivities()
        self.internalNames = [avatar.name for avatar in self.transitions] + [avatar.name for avatar in self.activities]
    def elabChildren(self,level=1):
        children = []
        self.childEntities = {}
        self.level = level
        self.bodynode.collectCapsuleChildren(children)
        for childName, childType in children:
            # get the body and spec (TBD ignore alternative impls for now)
            bodyName = str(childType.node.modname.idname)
            #print "bodyName", bodyName
            childbody = m3.compile(bodyName + ".cm3o")
            # create the Entity
            self.childEntities[childName] = CapsuleEntity(self.name + "." + childName,
                                                          childType.node,
                                                          childbody)
        for entity in self.childEntities.values():
            entity.elabChildren(level=level+1)


    def createMessagePoints(self,top=False):
        self.inMessagePoints = {}
        self.outMessagePoints = {}
        self.internalPoints = {}
        for messageName in self.specnode.getType().inDict:
            self.inMessagePoints[messageName]= MessagePoint(self,messageName,Cmin)
        for messageName in self.specnode.getType().outDict:            
            self.outMessagePoints[messageName] = MessagePoint(self,messageName,Cmout)
            
        if verbose:    
            print self.name
            print [pt.name for pt in self.inMessagePoints.values()]
            print [pt.name for pt in self.outMessagePoints.values()]
        
        for entity in self.childEntities.values():
            entity.createMessagePoints()
        
    def installConnections(self):
        # find all connect statements
        conns = self.bodynode.block.connections
        if not conns.isNULL():
            connections = conns.connectionList.kidsNoSep()
            for connection in connections:
                connection.setMessages(self)
            
        for entity in self.childEntities.values():
            entity.installConnections()

    def findActivities(self):
        # follow through all the next pointers
        for point in self.inMessagePoints.values():
            point.setLast()
        for point in self.outMessagePoints.values():
            point.setLast()

        # and find the activities attached if the message is not routed further
        for point in self.inMessagePoints.values():
            if point.last == point:
                # print "should be an activity or transition at ", point.image()
                # look through the single connects for this
                if point.plainName() not in self.internalNames:
                    print "dead connection"
                else:
                    print "found connection for ", point.plainName()
        for entity in self.childEntities.values():
            entity.findActivities()
            
    def findPoint(self,start):
        child, msg = start
        if len(string.split(msg,".")) == 1:
            p = MessagePoint(self,msg,Cmint)
            self.internalPoints[msg] = p
            return p
        if child:
            tgt = self.childEntities[child]
        else:
            tgt = self
        if msg in tgt.inMessagePoints:
            return tgt.inMessagePoints[msg]
        elif msg in tgt.outMessagePoints:
            return tgt.outMessagePoints[msg]
        else:
            raise "cannot find point"
            
    # callbacks used for installing connections from down in the CGEn Nodes
    def connectToChild(self,startMsg,child,endMsg):
        print "connectToChild",self.name,startMsg,child,endMsg
        self.inMessagePoints[startMsg].setNext(self.childEntities[child].inMessagePoints[endMsg])
    def connectFromChild(self,child,startMsg,endMsg):
        print "connectFromChild",self.name,child,startMsg,endMsg
        self.childEntities[child].outMessagePoints[startMsg].setNext(self.outMessagePoints[endMsg])
    def connectChildren(self,child1,startMsg,child2,endMsg):
        print "connectChildren",self.name,child1,startMsg,child2,endMsg
        self.childEntities[child1].outMessagePoints[startMsg].setNext(self.childEntities[child2].inMessagePoints[endMsg])
    def addSingleConnection(self,start,end):
        # port is either childport or port
        # conn is either port to port or port to activity
        print "addSingleConn",start,end
        startPoint = self.findPoint(start)
        endPoint = self.findPoint(end)
        startPoint.setNext(endPoint)
        if not verbose: return
        # Now chatter on about what you have found
        if endPoint.internal:
            print "found a single connected activity", endPoint.image()


    def addTrigger(self,triggerName,end):
        pass
    def addTimer(self,timerName,end):
        pass
    
    def image(self):
        tabs = self.level
        res = (" "* tabs) + self.name + "\n" 
        def printMessagePoints(name,points):
            if not points: return "" 
            res = (" "* tabs) + name + "\n"
            for point in points.values():
                res +=  (" "*tabs) +  "   " +  point.image() + "\n"
            return res
        res += printMessagePoints("inMessagePoints",self.inMessagePoints)
        res += printMessagePoints("outMessagePoints",self.outMessagePoints)
        res += printMessagePoints("internalPoints",self.internalPoints)
        return res

    def printtree(self):
        print self.image()
        for entity in self.childEntities.values():
            entity.printtree()
                
        
