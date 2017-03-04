import Global
import OutputFormatter
import types
import M3Types
import DbgStub
import ExpectList
import string
# Who created/sent this command ?

dbg = False

(dontCareSrc,
internalSrc,         # RTS (used for internal purposes (contElapse))
scriptSrc,           # the test script
triggerSrc,          # a trigger firing
timerSrc,            # a timer expiring
userSrc) = range(6)  # an explicit SEND in the model


def toDict(assocList):
    res = {}
    for key,val in assocList:
        res[key] = val
    return res

class CommandBase:
    def __init__(self):
        self.printable = False
        self.isScriptMsg = False
        self.isModelMsg = False
        self.isElapse = False
        self.isContElapse = False
        self.isElapsed = False
        self.isExpected = False
        self.isDataPort = False
        self.source = dontCareSrc
        self.resetPossible = False
        self.isUnlock = False
        self.isTestValue = False
    def image(self):
        return "command"

    def getLocalFun(self):
        portMsg = string.split(self.msgName, ".")
        if Global.raw_python:
            localFun = self.msgName
        if len(portMsg) == 1:
            localFun = self.msgName
        elif len(portMsg) == 2:
            localFun = portMsg[1]
        return localFun
    
    def executeLocalFunction(self):
        #print self.travelog.image()
        localFun = self.getLocalFun()
        if hasattr(self.target, localFun):
            m=getattr(self.target, localFun)
            if type(m) == types.MethodType:
                DbgStub.showActivity(self.target.__class__.__name__,localFun)
                if Global.traceInvocations:
                    print "INVOKE message:%s args:%s kwargs%s" % (localFun, self.args, self.kwargs)
                m(*self.args, **self.kwargs)
            else:
                raise "Compiler bug : message %s does not map to a function in %s" % (self.msgName, self.target)
        else:
            # TBD Commands with no target are simply sent to output, no matter what level, i.e. even if we
            # just plain forgot to connect them up FIXME

            # This is where you fix up the scaled integers (or any other info which may not be kept at run time)
            # and also where you do expectation testing.
#            if not Global.raw_python:
            self.fixArgTypesDict()
            expect = ExpectList.findExpectation(self.msgName, self.kwargs)
            Global.results.putOutput(self.msgName, *self.args, **self.kwargs)
            #else:
            #    Global.results.putOutput(self.msgName, *self.args, **self.kwargs)
                
            if Global.traceInvocations:
                print "NODEST message:%s args:%s kwargs%s" % (localFun, self.args, self.kwargs)

    def fixArgTypesDict(self):
        if Global.raw_python: return 
        paramDict = toDict(self.target.M3param_converters[self.msgName])
        for key,val in self.kwargs.items():
            if paramDict[key].isInteger: val.tipe = paramDict[key]
        for arg,(key,type) in zip(self.args, self.target.M3param_converters[self.msgName]): # convert the positionals to keyword
            if type.isInteger: arg.tipe = type
            self.kwargs[key] = arg
        self.args = []
            
    def prePerform(self):
        pass # this is currently just for expect's and elapsed's
    def isOutboundTopLevel(self):
        # quick hack to find out if this command is sent to the top level and outbound
        localFun = self.getLocalFun()
        return not (self.target.owningCapsule or hasattr(self.target,localFun))
    def perform(self):
        import Processors
        pname = self.target.M3ProcessorName
        if Processors.isLocked(pname) and not self.isOutboundTopLevel():
            if dbg: print "STORING", pname,self.image()
            Processors.store(pname,self)
        else:
            if dbg: print "PERFORMING",pname,self.image()
            self.executeLocalFunction()

class ScriptMsgCommand(CommandBase):
    def __init__(self, portName, msgName, inpLine, lastLine):
        CommandBase.__init__(self)
        self.printable = False
        self.isScriptMsg = True
        self.msgName = msgName
        self.portName = portName
        #print "port %s msg %s" % (portName,msgName)
        self.params = inpLine

        self.lastLine = lastLine
        self.source = scriptSrc
        #self.kwargs = self.params
        #self.args = []
    def redirect(self,capsule):

        #import pdb; pdb.set_trace()
        # rewrite message so that port is specified
        if self.portName:
            self.msgName = "%s.%s" % (self.portName, self.msgName)
        if not Global.raw_python:
            if (self.msgName in capsule.M3port_converters):
                self.msgName = capsule.M3port_converters[self.msgName]
#            else:
#                raise "bad message specification : %s is non-existent or ambiguous for capsule %s" % (self.msgName, capsule.__class__.__name__)
        # work out where this message ends up and rewrite it to that effect
        if hasattr(capsule, "M3param_converters"):
            self.convertM3params(capsule)
        else:
            self.convertPythonParams()

        dests = capsule.getDestinations(self.msgName, -1)
        cmdList = []
        for target, msgName, level, travelog in dests:
            smc = ScriptMsgCommand(self.portName, self.msgName, self.params, self.lastLine)
            smc.source = scriptSrc
            smc.target = target
            smc.msgName = msgName
            smc.level = level
            smc.travelog = travelog
            smc.text = self.text
            smc.args = self.args
            smc.kwargs = self.kwargs
            cmdList.append(smc)
        cmdList[0].printable = True
        return cmdList
    def convertM3params(self,capsule):
        # Now coerce the input data to the types of the message parameters
        typedParams = {}
        if self.msgName not in capsule.M3param_converters:
            raise "bad message specification : %s not understood by capsule %s" % (self.msgName, capsule.__class__.__name__)
        targTypes = toDict(capsule.M3param_converters[self.msgName]) # a dictionary containing the type of each parameter
        for k,v in self.params:
            if k not in targTypes:
                raise "bad input parameter %s" % k
            typedParams[k] = targTypes[k].coerce(v)
        self.params = typedParams
        self.kwargs = self.params
        self.args = []
    def convertPythonParams(self):
        self.args = []
        self.kwargs = {}
        for k,v in self.params:
            self.kwargs[k] = v
        self.params = self.kwargs 
    def image(self):
        return "Script Message " + self.msgName + " " + OutputFormatter.argsToString([],self.params)
    def resultsImage(self):
        return self.msgName + " " + OutputFormatter.argsToString([],self.params)
class ModelMsgCommand(CommandBase):
    def __init__(self, target, msgName, source, level, args, kwargs):
        CommandBase.__init__(self)
        self.resetPossible = True
        self.isModelMsg = True        
        self.target = target
        self.msgName = msgName
        self.args = args
        self.kwargs = kwargs
        self.source = source
        self.level = level
        self.printable = False
    def image(self):
        return "Model Message " + self.msgName + ":" + str(self.level) + " " + str(self.args) + str(self.kwargs)
    def redirect(self,capsule=None):
        if capsule == None: return [self]
        #print "redirect ", self.image()
        # work out where this message ends up and rewrite it to that effect
        cmdList = []
        
        dests = capsule.getDestinations(self.msgName, self.level)
        for target, msgName, level, travelog in dests:
            mmc = ModelMsgCommand(target,msgName,self.source,level,self.args,self.kwargs)
            cmdList.append(mmc)
        return cmdList
class TimerMsgCommand(ModelMsgCommand):
    def __init__(self, context, target, msgName, source, level, args, kwargs):
        ModelMsgCommand.__init__(self, target, msgName, source, level, args, kwargs)
        self.context = context
        self.redirected = False
        self.resetPossible = True
        self.printable = True
    def redirect(self):
        dests = self.target.getDestinations(self.msgName, self.level)
        cmdList = []
        for target, msgName, level, travelog in dests:
            tmc = TimerMsgCommand(self.context,target,msgName,self.source,level,self.args,self.kwargs)
            cmdList.append(tmc)
        return cmdList    
            
    def image(self):
        return "Timer Message " + self.msgName + ":" + str(self.level)  # + " " + str(self.target) + str(self.context) + " " + str(self.args) + str(self.kwargs)

class TriggerMsgCommand(ModelMsgCommand):
    def __init__(self, trigger, context,target, msgName, source, level, args, kwargs):
        ModelMsgCommand.__init__(self, target, msgName, source, level, args, kwargs)
        self.trigger = trigger
        self.context = context
        self.printable = True
        self.redirected = False
        self.resetPossible = True
    def redirect(self):
        # TBD currently command types redirected at different times
        dests = self.target.getDestinations(self.msgName, self.level)        
        cmdList = []
        for target, msgName, level, travelog in dests:
            tmc = TriggerMsgCommand(self.trigger,self.context,target,msgName,self.source,level,self.args,self.kwargs)
            cmdList.append(tmc)
        return cmdList    
    def image(self):
        return "Trigger Message from " + self.getTriggerName + " sending "  + self.msgName
    def getTriggerName(self):
        return self.trigger.runtimeName
        

class ElapseCommand(CommandBase):
    def __init__(self, quantity, factor, lastLine):
        CommandBase.__init__(self)
        self.isElapse = True        
        self.quantity = quantity
        self.factor = factor
        self.lastLine = lastLine
        self.source = scriptSrc
        self.level = -1
        self.printable = True
    def perform(self):
        #print "(elapse performed)"
        import Timer
        Timer.timeQueue.elapse(self.quantity, self.factor)
    def image(self):
        return "Elapse %s %s " % (self.quantity,self.factor)
    def redirect(self,_): return [self]
class ContElapseCommand(CommandBase):
    def __init__(self):
        CommandBase.__init__(self)
        self.isContElapse = True
        self.source = internalSrc
        self.level = 0
        # This makes sure that the command is inserted before all currently active model-generated commands (which start at 1)
        # but after all those generated by the script (which are at -1)
    def perform(self):
        import Timer
        Timer.timeQueue.contElapse()
    def image(self):
        return "ContElapse Command (Internal)"
    
class DataportSetCommand(CommandBase):
    def __init__(self, portName, value, lastLine):
        CommandBase.__init__(self)
        self.isDataPort = True
        self.portName = portName
        self.value = value
        self.lastLine = lastLine
        self.level = -1
    def image(self):
        return "Dataport set %s = %s" % (self.portName, self.value)
    def perform(self):
        self.capsule.setData(self.portName,self.value)
        Global.results.putDataport(self)
    def redirect(self,capsule):
        # don't redirect, but the capsule reference is useful
        self.capsule = capsule
        return [self]

class ElapsedCommand(CommandBase):
    def __init__(self, absTime, lastLine):
        CommandBase.__init__(self)
        self.isElapsed = True
        self.timeList = absTime
        self.lastLine = lastLine
        self.level = -1
    def image(self):
        return "Elapsed %s" % self.timeList
    def prePerform(self):
        #print "shifting time base"
        ExpectList.shiftTimeBase(self.timeList)    
    def perform(self):
        pass
    def redirect(self,capsule):
        return [self]

class ExpectCommand(CommandBase):
    def __init__(self, earliest, latest, portName, msgName, params, lastLine):
        def processTimeConstraint(tc):
            import Time
            if tc == "*":
                return tc
            elif tc == None:
                return 0
            else:
                return Time.makeTime(tc)
        CommandBase.__init__(self)
        self.isExpect = True
        self.earliest = processTimeConstraint(earliest)
        self.latest = processTimeConstraint(latest)
        self.params = params
        self.lastLine = lastLine
        if portName:
            self.fullName = "%s.%s" % (portName,msgName)
        else:
            self.fullName = msgName
        self.level = -1
    def image(self):
        return "Expect %s %s" % (self.fullName, self.params)
    def prePerform(self):
        #print "adding expectation"
        ExpectList.addExpectation(self)
    def perform(self):
        pass
    def redirect(self,capsule):
        return [self]

class TestValueCommand(CommandBase):
    def __init__(self,name,value,lastLine):
        CommandBase.__init__(self)
        self.name = name
        self.value = value
        self.lastLine = lastLine
        self.isTestValue = True
        self.printable = True
        self.level = -1        
    def image(self):
        return "TestValue %s %s" % (self.name, self.value)
    def perform(self):
        #import pdb; pdb.set_trace()
        self.actualValue = self.capsule.testValue(self.name,self.value)
    def redirect(self,capsule):
        self.capsule = capsule
        return [self]

class UnlockCommand(CommandBase):
    def __init__(self,processorName):
        CommandBase.__init__(self)
        self.processorName = processorName
        self.isUnlock = True
        self.level = 1000000
    def perform(self):
        import Processors
        Processors.unlock(self.processorName)
    def redirect(self):
        return [self]
    
class ChoiceHolder: 
    def assign(self, rhs):
        import pdb; pdb.set_trace()
    
class Any(ChoiceHolder):
    def doCoerce(self, coerce):
        import M3Objects
        return M3Objects.Any()
    def image(self):
        return "*"
    
class Range(ChoiceHolder):
    def __init__(self, small, large):
        self.small = small
        self.large = large
    def doCoerce(self, coerce):
        import M3Objects
        # ranges must be scalar and must have fitting types
        small = coerce(self.small,allowChoices=True)
        large = coerce(self.large,allowChoices=True)
        if not (small.isScalar() and large.isScalar()) :
            raise "Ranges only allowed on scalar types, you gave me %s %s", small, large
        if not small.tipe.fits(large.tipe):
            raise "Types in range are not compatible"
        return M3Objects.Range(small, large)
    def image(self):
        return "[[%s .. %s]]" % (self.small.image(), self.large.image())

class Alternatives(ChoiceHolder):
    def __init__(self, altList):
        self.altList = altList
    def doCoerce(self, coerce):
        import M3Objects
        objList = []
        for alt in self.altList:
            objList.append(coerce(alt,allowChoices=True))
        return M3Objects.Alternatives(objList)
    def image(self):
        return "[[ " + string.join([alt.image() for alt in self.altList],"; ") + " ]]" 

