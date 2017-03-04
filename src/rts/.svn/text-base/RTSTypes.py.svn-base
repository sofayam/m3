import types
import Command
import Global
import CommandQueue
import Statistics
import DbgStub
import Processors
import string
class Travelog:
    # A record of all the connections and capsules used by a command
    def __init__(self):
        self.tour = []
    def addHop(self, capsule,msgName,context):
        self.tour.append((capsule,msgName,context))
    def image(self):
        return [(cap.__class__.__name__, msgName, context and context.__class__.__name__) for cap, msgName,context in self.tour]

class M3CapsuleRuntimeType(Statistics.Gatherer):
#    def __setattr__(self,name,value):
#        if name == "runtimeName":
#            print "set runtimeName", value
#            raise "hell"
#            if name == "top": raise "hell"
#        self.__dict__[name] = value

    def __init__(self,level):
        Statistics.Gatherer.__init__(self,"Capsule")
        self.runtimeName = "top"
        self.M3ProcessorName = "default"
        self.__level = level
        self.dispatchTable = {}
        self.M3startCapsule()
        self.owningCapsule = None
    def M3LockProcessor(self,howLong):
        import Timer
        Processors.lock(self.M3ProcessorName)
        # TBD enter a timer to unlock the processor after howLong (scaled according to processor speed)
        howLong = howLong / Processors.getSpeed(self.M3ProcessorName)
        Timer.enterUnlock(self.M3ProcessorName,howLong)
    def M3TransitionCallHook(self,transitionName,stateName):
        DbgStub.showTransition(self.__class__.__name__,transitionName,stateName)
    def M3TransitionFinishedHook(self,stateName):
        DbgStub.showState(self.__class__.__name__,stateName)
    def M3NoTransitionForMessageInState(self,message,state):
        if Global.strictStates:
            raise "NoTransitionForMessage%sInState%s" % (message,state)
    def M3startCapsule(self):
        #print "calling default capsule start code"
        #This is overrun by capsules which have a START clause
        pass
    def connect(self,context,srcMsg,destMsg,destObj,level):
        #print "Called connect with srcMsg %s destMsg %s destObj %s" % (srcMsg,destMsg,destObj)
        if srcMsg not in self.dispatchTable:
            self.dispatchTable[srcMsg] = []
            #raise "compiler bug: duplicate name %s in dispatch table" % srcMsg
        self.dispatchTable[srcMsg].append((destMsg, destObj, level, context))
    def getDestinations(self, msgName, oldlevel, travelog=None,context=None):
        #print "getDestination",self,msgName,oldlevel
        if not travelog:
            travelog = Travelog()
        travelog.addHop(self,msgName,context)
        if msgName not in self.dispatchTable:
            # Add the current capsule as a destination if you can find no routing 
            newlevel = min(self.__level,oldlevel)
            return [(self, msgName, newlevel, travelog)]
        else:
            dests = []
            #import pdb; pdb.set_trace()
            # Add the current capsule as a destination if you find a corresponding attribute
            shortName = string.split(msgName,".")[-1]
            if hasattr(self,shortName) and (type(getattr(self,shortName)) == types.MethodType):
                newlevel = min(self.__level,oldlevel)
                dests = [(self, msgName, newlevel, travelog)]
            for destMsg, destObj, level, context in self.dispatchTable[msgName]:
                newlevel = min(oldlevel, level)
                dests += destObj.getDestinations(destMsg, newlevel,travelog,context)
            return dests

    def call(self, msgName, *args, **kwargs):
        # this is mapped from an M3 CALL statement
        cmd = Command.ModelMsgCommand(target=self,
                                      msgName=msgName,
                                      source=Command.userSrc,
                                      level=0,
                                      args=args,
                                      kwargs=kwargs)
        #print "level of send",level
        cmdList = cmd.redirect(self)
        DbgStub.ping("call")
        for cmd in cmdList:
            cmd.perform()
            
    def send(self, originator, level, msgName, *args, **kwargs):
        self.sendAfter(originator, level, msgName, 0, *args, **kwargs)
        
    def sendAfter(self, originator, level, msgName, after, *args, **kwargs):        
        import Timer        
        # this is mapped from an M3 SEND statement
        if not Global.raw_python:
            args = [ arg.dupe() for arg in args ]
            for key in kwargs: kwargs[key] = kwargs[key].dupe()
        cmd = Command.ModelMsgCommand(target=self,
                                      msgName=msgName,
                                      source=Command.userSrc,
                                      level=level,
                                      args=args,
                                      kwargs=kwargs)
        #print "SENDING",level
        #import pdb; pdb.set_trace()
        cmdList = cmd.redirect(self)
        DbgStub.ping("send") # this is not right for send after's

        for cmd in cmdList:
            # calculate the link overhead if present
            linkCost = Processors.getLinkCost(self.M3ProcessorName,cmd.target.M3ProcessorName)
            if after or linkCost:
                # divide by performance factor if present, then add link cost
                speed = Processors.getSpeed(self.M3ProcessorName)
                Timer.insertAfter((after / speed) + linkCost, cmd)
            else:
                CommandQueue.insert(cmd)
            

    def M3setHierarchicalNames(self,ind=0,pref="top"):
        if pref != "": pref += "."
        for name in dir(self):
            obj = getattr(self,name)
            if type(obj) == types.InstanceType:
                # christen everything which is an object
                obj.runtimeName = pref + name 
                #print "  " * ind, obj.runtimeName
                if M3CapsuleRuntimeType in obj.__class__.__bases__:
                    # and start the whole thing over with everything which is a capsule
                    obj.M3setHierarchicalNames(ind=ind+1,pref=pref + name)
                # and give all capsule level objects a reference to their owner
                obj.owningCapsule = self
        return self
    
    def M3setProcessors(self,processorName):
        if self.runtimeName == "top":
            self.M3ProcessorName = processorName
        else: 
            if self.runtimeName[0:4] != "top.":
                raise "bad runtime name %s" % self.runtimeName
            cname = self.runtimeName[4:] # snip off "top." because users do not use this in specifying capsules
            if cname in Processors.capsuleProcessorMap:
                processorName = Processors.capsuleProcessorMap[cname]
                Processors.addMappedCapsule(cname)
            self.M3ProcessorName = processorName
        #print "set processor", self.runtimeName, processorName            
        for name in dir(self):
            if name == "owningCapsule": continue
            obj = getattr(self,name)
            if (type(obj) == types.InstanceType) and (M3CapsuleRuntimeType in obj.__class__.__bases__):
                obj.M3setProcessors(processorName)
        
    def dumpConnectors(self):
        print self.runtimeName, ":"
        for connect in self.dispatchTable:
            print "  ", connect, "->", self.dispatchTable[connect]
        for name in dir(self):
            obj = getattr(self,name)
            if name == "owningCapsule": continue
            if M3CapsuleRuntimeType in obj.__class__.__bases__: 
                obj.dumpConnectors()

    def M3Reset(self, levelsUp = 0):
        if (levelsUp > 0) and self.owningCapsule:
            self.owningCapsule.M3Reset(levelsUp - 1)
        else:
            import Timer
            # delete all pending model-generated command queue entries for this capsule and subcapsules
            CommandQueue.reset(self.runtimeName)
            # delete all timers from this capsule and subcapsules
            Timer.timeQueue.reset(self.runtimeName)

    def setData(self, dataPort, value):
        if len(dataPort) == 1:
            dataPort = dataPort[0]
            if hasattr(self,dataPort):
                dp = getattr(self,dataPort)
                if (type(dp) == types.InstanceType) and hasattr(dp,"tipe"):
                    dp.assign(dp.tipe.coerce(value))
                else:
                    raise "%s is not a valid capsule entity" % dataPort
            else:
                raise "unknown data port %s" % dataPort
        else:
            nextcap = dataPort[0]
            restcap = dataPort[1:]
            if hasattr(self,nextcap):
                child = getattr(self,nextcap)
                if M3CapsuleRuntimeType in child.__class__.__bases__:
                    child.setData(restcap, value)
                else:
                    raise "error in path to data port: %s is not a child of capsule %s"  % (nextcap, self)                    
            else:
                raise "error in path to data port: child %s not found in capsule %s"  % (nextcap, self)

    def testValue(self, dataPort, value):
        if len(dataPort) == 1:
            dataPort = dataPort[0]
            if hasattr(self,dataPort):
                dp = getattr(self,dataPort)
                if (type(dp) == types.InstanceType) and hasattr(dp,"tipe"):
                    actualType = dp.tipe
                    if value:
                        expectedValue = actualType.coerce(value,allowChoices=True)
                        if not expectedValue.equals(dp).toBool():
                            Global.results.putFailure("Datastore %s : - value expected %s, value found %s " %  (
                                dataPort, expectedValue.image(),
                                dp.image()))
                    # TBD make sure that this displays "== name v a l u e"  in the res and pro files
                    #dp.assign(dp.tipe.coerce(value))
                    #raise "hell"
                    return dp
                else:
                    raise "%s is not a valid capsule entity" % dataPort
            else:
                raise "unknown data port %s" % dataPort
        else:
            nextcap = dataPort[0]
            restcap = dataPort[1:]
            if hasattr(self,nextcap):
                child = getattr(self,nextcap)
                if M3CapsuleRuntimeType in child.__class__.__bases__:
                    return child.testValue(restcap, value)
                else:
                    raise "error in path to data port: %s is not a child of capsule %s"  % (nextcap, self)                    
            else:
                raise "error in path to data port: child %s not found in capsule %s"  % (nextcap, self)

            
class M3TimerRuntimeType(Statistics.Gatherer):
    def __init__(self, delay, periodic, changeable):
        Statistics.Gatherer.__init__(self,"Timer")
        if delay:
            if type(delay) in [types.IntType, types.LongType]: # for use directly from python
                self.delay = delay
            else:
                self.delay = delay.val
        else:
            self.delay = 0 # This means uninitialised !!!
        self.periodic = periodic
        self.changeable = changeable
        if (not self.delay) and (not self.changeable): raise "compiler bug : inconsistent timer"
        #print "creating a type with delay %s  " % self.delay
    def createObject(self):
        return M3TimerRuntimeObject(self, self.periodic, self.changeable)
        #print "creating a timer object with type %s  " % self


tctr = 1
class M3TimerRuntimeObject(Statistics.Gatherer):
    def __init__(self,type,periodic,changeable):
        self.type = type
        self.created = False
        self.connected = False
        self.periodic = periodic
        self.changeable = changeable
        # self.runtimeName is allocated at runtime, after the capsule tree has been built, by setHierarchicalNames
    def connect(self,context,srcMsg,destMsg,destObj,level) :
        if self.connected:
            raise "RTS restriction : timer can only have one connection"
        #print "timerconnected"
        self.msgName = destMsg
        self.target = destObj 
        self.connected = True
        self.level = level
        self.context = context # this is the capsule I am in
    def create(self):
        global tctr
        if not self.connected:
            raise "Attempt to use timer with no connection"
        import Timer
        expireCmd = Command.TimerMsgCommand(context=self.context,
                                            target=self.target,
                                            msgName=self.msgName,
                                            source=Command.timerSrc,
                                            level=self.level,
                                            args=[],
                                            kwargs={})
        #print "creating timer with name %s" % self.runtimeName
        Timer.timeQueue.create(rtsTimer=self,
                               delta=self.type.delay,
                               cmd=expireCmd,
                               periodic=self.periodic,
                               changeable=self.changeable) 
        self.created = True
    def start(self):
        import Timer
        if not self.created:
            self.create()
        Timer.timeQueue.insert(self)
    def change(self, newDelay):
        import Timer
        if not self.created:
            self.create()
        if not type(newDelay) in [types.IntType, types.LongType]: # can also be used directly from python
            newDelay = newDelay.val
        Timer.timeQueue.change(self,newDelay)
    def stop(self):
        import Timer
        if not self.created:
            self.create()
        Timer.timeQueue.cancel(self)

class M3TriggerType(Statistics.Gatherer):
    def __init__(self, proc):
        import Trigger
        Statistics.Gatherer.__init__(self,"Timer")
        self.guardFunc = proc
        Trigger.triggerList.addTrigger(self)
        self.triggeredCommand = None
    def connect(self, context, dummy, msgName,target,level):
        self.triggeredCommand = Command.TriggerMsgCommand(trigger=self,
                                                          context=context,
                                                          target=target,
                                                          msgName=msgName,
                                                          source=Command.triggerSrc,
                                                          level=level,
                                                          args=[],
                                                          kwargs={})

        
# There is no trigger object defined here because trigger objects contain code and are
# generated by the compiler as needed

class M3RunTimeCallBackType:
    def __init__(self, owningCapsule, port):
        self.owningCapsule = owningCapsule
        self.port = port
    def handlerFunctionClosure(self,name):
        def handlerFunction(*args,**kwargs):
            msgName = "%s.%s" % (self.port,name)
            #import pdb; pdb.set_trace()
            self.owningCapsule.sendAfter(None,
                                         -1,
                                         msgName,
                                         0,
                                         *args,
                                         **kwargs)
        return handlerFunction
    def dupe(self): return self # this is always called in parameters
    def __getattr__(self,name):
        return self.handlerFunctionClosure(name)

