# TBD this "queue" is actually a stack for the time being
# one day it should be a set of queues distributed per-capsule
# or some other possibly pluggable mechanism
cmdQueue = None

def set(queue):
    global cmdQueue
    cmdQueue = queue

def prePerform():
    for command in cmdQueue:
        command.prePerform()

def hasEntries():
    return cmdQueue

def next():
    global cmdQueue
    cmd = cmdQueue[0]
    cmdQueue = cmdQueue[1:]
    #print "grabbing command with level ", cmd.level
    return cmd

def insert(cmd):
    #print "pushing command with level ", cmd.level, cmd.image()
    #
    # Insert in front of the first entry with a level lower than that of cmd
    #
    global cmdQueue
    #dump()
    for idx,entry in enumerate(cmdQueue):
        if entry.level < cmd.level:
            cmdQueue = cmdQueue[0:idx] + [cmd] + cmdQueue[idx:]
            return
    cmdQueue = cmdQueue + [cmd]

def dump():
    for cmd in cmdQueue:
        print cmd.image()

def reset(runtimeName):
    global cmdQueue
    # look at the targets of all commands - if they are at or under the capsule runtimeName
    leader = runtimeName + "."
    leaderLen = len(leader)
    def resettable(cmd):
        res = False
        if cmd.resetPossible: # not all of them make sense
            tgtName = cmd.target.runtimeName
            res = (tgtName == runtimeName) or (tgtName[:leaderLen] == leader)
            if res:
                print "reset : kicking out cmd %s" % cmd.image()
        return res
    cmdQueue = [cmd for cmd in cmdQueue if not resettable(cmd)]

