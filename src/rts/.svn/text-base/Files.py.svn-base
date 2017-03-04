import types
import sys
import string
import os
import os.path
import time

import InputParser
import OutputFormatter
import Command 
#from   SimDebugger import trc
import Global
import Time
import Timer
import Statistics
import xmlrpclib

elapseOutputEnabled = True

dupeProtocol = False
dupeResults = False

com = "% "
comline = (com * 25) + "\n"


class ScriptFile:
    def __init__(self, fileName):
        self.fileName = fileName
        self.cmdlist = InputParser.parse(fileName) 
        prevLastLine = 0

        # drag the actual source text into the commands (including comments and formatting)
        for cmd in self.cmdlist:
            cmd.text = string.join(InputParser.inpLines[prevLastLine:cmd.lastLine],"")
            # precaution to stop last line w/o \n from messing up the protocol file
            if cmd.text[-1] != '\n': cmd.text += '\n'
            prevLastLine = cmd.lastLine

    def cmds(self):
        return self.cmdlist
    def __getitem__(self, i):
        return self.cmdlist[i]


class FileWrapper:
    def __init__(self, fileName, mode, dupe, createOnWrite=False):
        if createOnWrite:
            self.written = False
            self.fileName = fileName
            self.mode = mode
        else:
            self.fh = open(fileName, mode)
            self.written = True
        self.dupToConsole = dupe
    def write(self, txt):
        if not self.written:
            self.written = True
            self.fh = open(self.fileName, self.mode)            
        self.fh.write(txt)
        if self.dupToConsole:
            sys.stdout.write(txt)
    
class ResultFile:
    def __init__(self, fileName):
        try:
            if not (os.path.exists(Global.outputPath)):
                os.mkdir(Global.outputPath)
            self.results = FileWrapper(Global.outputPath
                                      + fileName + ".res", "w", dupeResults)
            self.protocol = FileWrapper(Global.outputPath
                                        + fileName + ".pro", "w", dupeProtocol)
            self.sequences = FileWrapper(Global.outputPath
                                        + fileName + ".seq", "w", False)
            self.failures = FileWrapper(Global.outputPath
                                        + fileName + ".fail", "w", False, createOnWrite=True)
            self.putProtocolHeader()
        except:
            raise
            print "Error opening Results Files for %s : %s" % (fileName, sys.exc_info()[0])
            sys.exit()
        self.elapsedNew = False
        Global.results = self

    def putUserMessage(self, outStr):
        txt = "% " + outStr + "\n"
        self.flushElapsed()
        self.results.write(txt)
        self.protocol.write(txt)

    def putUserMessageProtocol(self, outStr):
        txt = "% " + outStr + "\n"
        self.flushElapsed()
        self.protocol.write(txt)


    def putTrigger(self, cmd):
        txt = "* " + cmd.getTriggerName() + "\n"
        self.flushElapsed()
        self.protocol.write(txt)

    def putFailure(self, msg):
        Global.failure = True
        self.failures.write(msg + "\n")
        fullmsg = "%% FAILURE: %s\n" % msg
        self.protocol.write(fullmsg)
        self.results.write(fullmsg)
        if not (dupeResults or dupeProtocol):
            if not Global.failureExpected:
                sys.stdout.write(fullmsg)

                         
        
    def putInput(self, cmd):
        # Some tricky stuff here reflects the fact
        # that internally all commands are dealt with
        # together on one input queue
        # even though some of them do not come from the input file, and some
        # of them (i.e. timer elapse) have a special syntax
        # Here we add syntactic sugar to the output
        # to hide this fact
        if not cmd.printable: return 
        if self.checkElapse(cmd): return 
        if self.checkTrigger(cmd): return
        if self.checkTestValue(cmd): return
#        if self.checkSimCmd(cmd): return
#        if self.checkAnnCmd(cmd): return
        if cmd.isScriptMsg:
            pref = "> "
        else:
            return 
        txt = pref + cmd.resultsImage() + "\n"
        self.flushElapsed()
        self.results.write(cmd.text)
        self.protocol.write(cmd.text)
        #if trc(): print txt

    def putDataport(self, cmd):
        self.protocol.write(cmd.text)
        self.results.write(cmd.text)

#    def checkSimCmd(self, cmd):
#        if cmd.ctype != Command.simcmd: return False
#        self.putSimCmd(cmd)
#        return True

    def checkTrigger(self, cmd):
        if cmd.source != Command.triggerSrc: return False
        self.putTrigger(cmd)
        return True

    def checkElapse(self, cmd):
        if not cmd.isElapse: return False
        self.putElapse(cmd)
        return True

#    def checkAnnCmd(self, cmd):
#        if cmd.ctype != Command.anncmd: return False
#        self.putAnnounce(cmd)
#        return True

    def checkTestValue(self, cmd):
        if not cmd.isTestValue: return False
        #import pdb; pdb.set_trace()
        txt = "== " + string.join(cmd.name,".") + " " + cmd.actualValue.image() + "\n"
        self.results.write(txt)
        self.protocol.write(txt)
        
        
    def putCobegin(self):
        self.sequences.write("COBEGIN\n")
    def putCoend(self):
        self.sequences.write("COEND\n")
    def putSeqbegin(self):
        self.sequences.write("SEQBEGIN\n")
    def putSeqend(self):
        self.sequences.write("SEQEND\n")
        
    def putInternal(self, cmd, source, dests, args):
        if len(dests) > 1:
            deststr = "["
            for dest, port in dests:
                deststr += dest.label
            deststr += "]"
        else:
            deststr = dests[0][0].label
        #print source.container.isa()

        if (source.container.isa() == "Trigger") and (source.name != "triggeredPort"):
            pref = "<*> "
        else:
            pref = "<-> "
        payload = (pref,str(source),deststr,str(cmd),OutputFormatter.argsToString([],args))
        txt = ("%s%s -> %s : %s %s\n" % payload)
        self.protocol.write(txt)

    def putSequence(self, cmd, source, dests, args):
        for _,destport in dests:
            def shorten(label):
                return string.join((string.split(label,".")[1:]),".")
            def show(port):
                return port.name + "@" + shorten(port.container.label)
            payload = (show(source),show(destport),str(cmd),
                       OutputFormatter.argsToString([],args),
                       str(long(Timer.timeQueue.wallClock)))
            seqtxt = string.join(payload,'|')  + "\n"
            self.sequences.write(seqtxt)
            
    def putOutput(self, cmd, *args, **kwargs):
        txt = "< " + str(cmd) + " " + OutputFormatter.argsToString(args,kwargs) + "\n"
        self.flushElapsed()
        self.results.write(txt)
        self.protocol.write(txt)
        #if trc(): print txt

    def putTrace(self, txt):
        self.flushElapsed()
        txt = "%" + txt + "\n"
        self.protocol.write(txt)
        self.results.write(txt)        

    def putAssert(self, txt):
        self.flushElapsed()
        txt = "%" + txt + "\n"
        self.protocol.write(txt)
        self.results.write(txt)
    def putElapse(self, cmd):
        #txt = "? %d %s\n" % (cmd.quantity, cmd.factor)
        self.results.write(cmd.text)
        self.protocol.write(cmd.text)
        #if trc(): print txt
    
    def putElapsed(self, delta):
        txt = "! %s \n" % Time.timeString(delta)
        self.timeText = txt
        self.elapsedNew = True
        
    def flushElapsed(self):
        if self.elapsedNew:
            self.elapsedNew = False
            self.results.write(self.timeText)
            self.protocol.write(self.timeText)
            #if trc(): print self.timeText

    def putSimCmd(self, cmd):
        txt = "$ %s \n" % str(cmd)
        self.protocol.write(cmd.text)

    def putSimCmdOutput(self, cmd):
        txt = "# %s \n" % cmd
        self.protocol.write(txt)

    def putAnnCmdOutput(self, cmd):
        txt = "# %s \n" % cmd
        self.protocol.write(txt)
        self.results.write(txt)
        
    def putAnnounce(self, cmd):
        txt = ": %s \n" % cmd 
        self.results.write(txt)
        self.protocol.write(cmd.text)

    def putUserResults(self, txt):
        txt = "| " + txt
        self.results.write(txt)
        self.protocol.write(txt)

    def putUserProtocol(self, txt):
        txt = "| " + txt + "\n"
        self.protocol.write(txt)

    def putAssertFail(self, name, params):
        self.putAnnCmdOutput("Failed assert %s with params %s" % (name, params))

    def putAssertPass(self, name, params):
        self.protocol.write("# Passed assert %s with params %s" % (name, params))

    def putProtocolHeader(self):
        if os.environ.has_key('USER'):
            username = os.environ['USER']
        elif os.environ.has_key('USERNAME'):
            username = os.environ['USERNAME']
        else:
            username = "Anonymous User on Strange System"
        runtime = time.asctime(time.localtime())
        self.protocol.write(comline)
        self.protocol.write("%sProtocol %s\n" %
                            (com, Global.resFile + Global.protocolFileExtension))
        myargv = sys.argv[:]
        # manipulate the first arg of the command line so that it looks
        # like the actual invocation and is not too long.
        # Don't actually change argv just in case.
        enteredCommand = os.path.basename(myargv[0])
        enteredCommand = os.path.splitext(enteredCommand)[0]
        myargv[0] = enteredCommand
        self.protocol.write("%sCommand Line: '%s'\n" %
                            (com, string.join(myargv)))
        self.protocol.write("%sRun by user %s on %s\n" % (com, username, runtime))
        self.protocol.write("%sModel: %s\n" %
                            (com, Global.sysFile))
        self.protocol.write("%sInput file: %s\n" %
                            (com, Global.scriptFile + Global.inputFileExtension))
        self.protocol.write("%sResults file: %s\n" %
                            (com, Global.resFile + Global.resultFileExtension))
        self.protocol.write(comline)

    def putStatistics(self):
        self.protocol.write(comline)
        self.protocol.write(Statistics.report(Global.statistics))
        self.protocol.write(comline)

    def close(self):
        self.results.close()
        self.protocol.close()
        self.sequences.close()
    
