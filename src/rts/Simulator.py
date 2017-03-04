#from Files import ScriptFile
import Files
import Timer
import Trigger
import RTSOptions
import Global
import CommandQueue
import SimDebugger
import Statistics
import DbgStub
#import profile
import ExpectList
import SystemParser
import Processors
import tpg
#import gc

capsuleStash = None # Needed for profiling to work within __main__ namespace
def runCapsule(capsule):
    try:
        #gc.set_debug(gc.DEBUG_LEAK)
        Global.topCapsule = capsule
        # process options
        if RTSOptions.options.dumpConnectors:
            capsule.dumpConnectors()
        # read in commands from list
        scriptCmds = Files.ScriptFile(Global.scriptFile).cmds()
        # rewrite and multiply destinations
        cmdList = []
        for cmd in scriptCmds:
            cmdList = cmdList + cmd.redirect(capsule) # this is where they can expand
        # send to queue
        CommandQueue.set(cmdList)
        CommandQueue.prePerform()
        resultFile = Files.ResultFile(Global.resFile)
        while CommandQueue.hasEntries():
            DbgStub.ping("simcycle")
            # pop and execute top command
            SimDebugger.interpret()
            cmd = CommandQueue.next()
            cmd.perform()
            Global.results.putInput(cmd) # TBD output handling 

            if not cmd.isDataPort: # This means dataports get some peace to do their initialisation
                Trigger.triggerList.checkTriggers()
                Timer.timeQueue.checkElapse()
            Statistics.SimCycles += 1
            #if Statistics.SimCycles > 1000: break
        ExpectList.checkEmpty()
        resultFile.putStatistics()
        if Global.failureExpected:
            if not Global.failure:
                print "!!!!!!!!FAILURE TO FAIL IN FAILURE TEST: TEST FAILED!!!!!!"
            elif Global.selfCongratulate:
                print "PASS : %s" % capsule.__class__.__name__            
        elif ExpectList.expectPassed and Global.selfCongratulate:
            print "PASS : %s" % capsule.__class__.__name__
    except tpg.Error, e:
        print "%s, line %s row %s : %s " % (Global.scriptFile, e.line, e.row, e.msg)
def run(capsule):
    global capsuleStash
    if not RTSOptions.options:
        RTSOptions.setOptions()
    if not SystemParser.processMapfile(): return
    if not SystemParser.processArchfile(): return
    capsule.M3setHierarchicalNames()
    #import pdb; pdb.set_trace()
    capsule.M3setProcessors(processorName='default')
    Processors.checkMappedCapsules()
    if Global.profile:
        capsuleStash = capsule
        print "profiling ..."
        #profile.run("import Simulator; Simulator.runCapsule(Simulator.capsuleStash)", "profile.dat")
    else:
        runCapsule(capsule)
