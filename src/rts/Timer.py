import Statistics
from Time import *
import Command
import Global
import CommandQueue
import SimDebugger
from SimDebugger import trc

timeQueue = None          # TBD no longer hide the timeQueue inside system

class TimeQueue:
    """
    Start with a simple implementation - Timers are kept in a sorted list
    Later keep this as a list where each member only holds the time difference
    between itself and its predecessor
    """
    def __init__(self):
        global timeQueue
        SimDebugger.setTimeQueue(self)
        self.q = []
        self.mustElapse = 0
        self.wallClock = 0L
        self.stallElapse = 0
        self.timers = {}
        # The following is a special signal used to show that a set of timer triggered commands
        # have been completed. This is needed when several timers time out simultaneously
        # in order for the elapse checking to be stalled until they have all been processed
        self.contElapseCmd = Command.ContElapseCommand()
        timeQueue = self # TBD global time queue so that the blocks world can get at it
                                         
    def contElapse(self):
        #if trc(): print "TimeQueue.contElapse"
        self.stallElapse = 0

    def elapse(self, quantity, factor):
        #if trc(): print "TimeQueue.elapse"
        reqTicks = Time(quantity,factor).ticks
        if self.q == []:
            #if trc(): print "time queue empty"
            self.wallClock += reqTicks
            Global.results.putElapsed(self.wallClock)            
            return
        self.mustElapse = reqTicks

    def dumpTQ(self):
        print "Time Queue"
        for i in self.q:
            print "    " + str(i)
        print "wallClock: ", self.wallClock
        print "mustElapse: ", self.mustElapse
    def checkElapse(self):
        timedouttimers = []
        #if trc(): print "TimeQueue.checkElapse"
        # self.dumpTQ()
        if (not self.stallElapse) and self.mustElapse != 0:

            if self.q != []:
                front = self.q[0]
                if front.delta <= self.mustElapse: # tasks waiting and ready to time out
                    self.wallClock += front.delta
                    actuallyElapsed = front.delta
                    timeouts = self.multiTimeout()
                    if timeouts > 1:
                        warning = "More than one timer expired at once :"
                        for i in range(timeouts):
                            warning += " " + self.q[i].rtsObj.runtimeName
                        # self.system.warning(warning)
                    # push the special internal continuation command and stall all further elapse checking
                    #CommandQueue.push(self.contElapseCmd)
                    CommandQueue.insert(self.contElapseCmd) # TBDXXX
                    self.stallElapse = 1
                    for i in range(timeouts):
                        front = self.q[0]
                        Statistics.TimersElapsed += 1
                        #print self.wallClock
                        front.pushCommand()
                        timedouttimers.append(self.q[0])
                        self.q = self.q[1:]
                        
                    self.mustElapse = self.mustElapse - front.delta
                else: # tasks waiting but not yet ready - swallow complete elapse
                    self.wallClock += self.mustElapse
                    actuallyElapsed = self.mustElapse
                    self.mustElapse = 0
            else: # no tasks waiting - swallow complete elapse
                #print "!!!!!!!!!!!!!!!swallowing delay"
                self.wallClock += self.mustElapse
                actuallyElapsed = self.mustElapse
                self.mustElapse = 0
                
            # Now simulate the passing of time by reducing the wait time on the remaining timers 
            for i in self.q:
                #print i.delta
                i.delta = i.delta - actuallyElapsed
            Global.results.putElapsed(self.wallClock)

            # Deal with periodic timers which automatically reenter themselves 
            for i in timedouttimers:
                if i.periodic:
                    #if trc(): print "Inserted Periodic Timer %s " % i
                    self.insert(i.rtsObj) # TBD Inefficient double lookup
            
    def multiTimeout(self):
        #if trc(): print "TimeQueue.multiTimeout"
        timeouts = 1
        if self.q != []:
            front = self.q[0]
            rest = self.q[1:]
            while (rest != []) and (rest[0].delta == front.delta):
                timeouts += 1
                rest = rest[1:]
        return timeouts

    def change(self, name, newDelay):
        #if trc(): print "Timer.change"
        if name not in self.timers.keys():
            raise "NoSuchTimer %s" % name
        timer = self.timers[name]
        if not timer.changeable:
            raise "Timer %s is fixed" % name
        #(q, f) = newDelay
        timer.init = newDelay #convertToDelta(q, f)
        timer.changed = True

    def insert(self, name):
        #print "inserting %s" % name
        #if trc(): print "TimeQueue.insert"
        if name not in self.timers.keys():
            raise "NoSuchTimer %s" % name
        timer = self.timers[name]
        if timer.changeable and not timer.changed:
            raise "Attempt to start uninitialised timer %s" % name
        timer.delta = timer.init
        if timer in self.q:
            self.cancel(name)
            #raise "Timer %s already in queue" % name
        self.q.append(timer)
        self.q.sort(timer.ordered)

    def create(self, rtsTimer, delta, cmd, periodic, changeable):
        #if trc(): print "TimeQueue.create"
        timer = Timer(rtsTimer, delta, cmd, periodic, changeable)
        if rtsTimer in self.timers.keys():
            raise "Timer %s Defined Twice"  % name   # runtime errors
        self.timers[rtsTimer] = timer

    def deltaSeconds(self, timer):
        return float(self.timers[timer].init) / F_sec
        
    def cancel(self, t):
        #if trc(): print "TimeQueue.cancel"
        # delete timer from queue with name
        self.q = [timer for timer in self.q if timer.rtsObj is not t]

    def reset(self, runtimeName):
        # delete all timers whose name starts runtimeName and a "." separator
        leader = runtimeName + "."
        leaderLen = len(leader)
        def resettable(timerName):
            res = (len(timerName) > leaderLen) and (timerName[:leaderLen] == leader)
            if res:
                print "reset: kicking out %s" % timerName
            return res
        self.q = [timer for timer in self.q if not resettable(timer.rtsObj.runtimeName)]

timeQueue = TimeQueue()

class Timer:
    def __init__(self, timer, init, cmd, periodic, changeable):
        self.rtsObj = timer
        self.delta = None
        self.cmd = cmd
        self.init = init
        self.setRange = None
        self.periodic = periodic
        self.changeable = changeable
        self.changed = (init != 0)
    def pushCommand(self):
        cmdList = self.cmd.redirect() # need to do this now so that the level will be right when it is inserted
        for cmd in cmdList:
            CommandQueue.insert(cmd) 
    def ordered(self, x, y):
        if x.delta == y.delta:
            return 0
        elif x.delta < y.delta:
            return -1
        else:
            return 1
    def __repr__(self):
        return "%s %s %s %s" % (self.rtsObj.runtimeName, timeString(self.delta), str(self.cmd), self.setRange)

dummyctr = 0

class DummyM3Timer:
    def __init__(self,proc):
        global dummyctr
        dummyctr += 1
        self.runtimeName = "%s*%s" % (proc,dummyctr)  
    
def enterUnlock(processorName,howLong):
    #print "locking %s for %s" % (processorName,howLong)
    oneoff = DummyM3Timer(processorName)
    timeQueue.create(rtsTimer=oneoff,delta=howLong,
                     cmd=Command.UnlockCommand(processorName),periodic=None,changeable=None)
    timeQueue.insert(oneoff)

def insertAfter(after,cmd):
    oneoff = DummyM3Timer("SENDAFTER")
    timeQueue.create(rtsTimer=oneoff,delta=after,
                     cmd=cmd,periodic=None,changeable=None)
    timeQueue.insert(oneoff)
    
    
