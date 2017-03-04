import string
import sys
import types
from Command import *
import Global
import MacroProcessor
from SimDebugger import trc

import compileCommandReader
compileCommandReader.metaCompile()

from CommandReader import Cmd

lineno = 1
inpLines = []

    
def parse(inpfileBase):
    global inpLines
    inpfile = inpfileBase + Global.inputFileExtension
    inpLines = open(inpfile).readlines()
    inpLines = MacroProcessor.process(inpLines)
    if Global.preprocessOnly:
        preproFile = open(inpfileBase + Global.preproFileExtension,"w")
        for i in inpLines:
            preproFile.write(i)
        preproFile.close()
        print "...Just preprocessing, look in .pre file for results"
        sys.exit()
    inp = string.join(inpLines)

    cmd = Cmd()
    cmds = cmd(inp)
    return cmds


if __name__ == "__main__":
    doit('test1')
