import Statistics
#from Command import *
import CommandQueue
import Global
#from SimDebugger import trc
import TraceServerStub
import copy

triggerList = None

up, down = range(2)
class Trigger:
    def __init__(self, triggerBlock):
        self.triggerBlock = triggerBlock
        self.state = down
    def canRun(self):
        currentVal = self.triggerBlock.guardFunc()
        if not Global.raw_python:
            currentVal = currentVal.toBool()
        if currentVal:
            if self.state == down:
                self.state = up
                return True
            else:            
                return False
        else:
            self.state = down
            return False

class TriggerList:
    def __init__(self):
        self.triggers = []
    def addTrigger(self, triggerBlock):
        self.triggers.append(Trigger(triggerBlock))

    def checkTriggers(self):
        TraceServerStub.mute()
        trigs = [trig for trig in self.triggers if trig.canRun()]
        TraceServerStub.loud()
        #if len(trigs) > 1:
        #    self.system.warning("More than one trigger has become active at one time")
        #    TBD so much for this syndrome
        for trig in trigs:
            #if trc(): 
            #    print "pushed command from Trigger %s" % trig.name
            Statistics.TriggersActivated += 1
            # TBDXXX resolve connections and translate message first
            cmd = trig.triggerBlock.triggeredCommand
            if cmd:
                cmdList = cmd.redirect()
                for cmd in cmdList:
                    CommandQueue.insert(cmd)

triggerList = TriggerList()
