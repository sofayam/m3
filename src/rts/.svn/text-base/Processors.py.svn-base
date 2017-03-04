import string

dbg = False

linksSet = False

locked = {}

capsuleProcessorMap = {}

processorLocked = {}

processorSpeed = {}

commandQueues = {}

mappedCapsules = []

class CommandQueue:
    def __init__(self):
        self.entries = []
    def isEmpty(self):
        return self.entries == []
    def store(self,command):
        for idx,entry in enumerate(self.entries):
            if entry.level < command.level:
                self.entries = self.entries[0:idx] + [command] + self.entries[idx:]
                return
        self.entries.append(command)
    def fetch(self):
        if self.isEmpty():
            return False
        else:
            if dbg: print "FETCHING"
            res = self.entries[0]
            self.entries = self.entries[1:]
        return res
    def image(self):
        res = "Processor Command Queue:"
        if self.isEmpty():
            res += " empty"
        for entry in self.entries:
            res +=  "\n  " + entry.image()
        return res
    
    
def setCapsuleProcessorMap(map):
    global capsuleProcessorMap
    capsuleProcessorMap = map
    #print capsuleProcessorMap

def setSpeeds(speeds):
    global processorSpeed
    processorSpeed = speeds

def getSpeed(processor):
    if processor == "default":
        return 1.0
    else:
        return processorSpeed[processor]

def setLinkCosts(costs):
    # dictionary of the form {"source->dest":
    global linkCosts, linksSet
    linkCosts = costs
    linksSet = True
    
def getLinkCost(source,dest):
    if not linksSet:
        return 0
    if (source == "default") or (dest == "default"):
        return 0
    else:
        key = "%s->%s" % (source,dest)
        if key not in linkCosts:
            raise "send %s attempted where no link exists" % key
        return linkCosts[key]

def isLocked(processor):
    return processor in processorLocked and processorLocked[processor]

def lock(processor):
    if dbg: print "LOCKING"
    processorLocked[processor] = True
    if processor not in commandQueues:
        commandQueues[processor] = CommandQueue()
    

def unlock(processor):
    if dbg: print "UNLOCKING"
    processorLocked[processor] = False
    # and flush out as much of the stuff that has been waiting as you can
    cq = commandQueues[processor]
    if dbg: print cq.image()
    while not (isLocked(processor) or cq.isEmpty()):
        #import pdb; pdb.set_trace()
        cmd = cq.fetch()
        if cmd:
            cmd.perform()

def store(processor, command):
    commandQueues[processor].store(command)
    
def fetch(processor):
    return commandQueue[processor].fetch()

def addMappedCapsule(capsuleName):
    mappedCapsules.append(capsuleName)

def checkMappedCapsules():
    for capsule in capsuleProcessorMap:
        if capsule not in mappedCapsules:
            print "WARNING : capsule %s was mapped but does not exist in the system under test" % capsule # OK
