import Files
import Global
import CapsuleMap
import SimDebugger
import Processors
import SystemParser
import optparse
import sys
import os

options = None

def setOptions():
    global options
    parser = optparse.OptionParser(usage="""
usage: %prog [options] model [testscenario [outputfilebasename]]
        """)
    parser.add_option("-a", "--ignore-assertfailures", action="store_true", default=0,
                      help="Do not raise exception when assert fails", 
                      dest='ignoreAssert')

    parser.add_option("-c", "--console-output", type="choice",
                      choices=('neither','pro','res'),
                      dest='txtsrc', default="neither",
                      help="output protocol (pro) or results (res) to console")
   
    parser.add_option("-d", "--debug", action="store_true",
                      dest='debug', default=0, help="enter debugger")
    parser.add_option("-D", "--dump-connectors", action="store_true",
                      dest='dumpConnectors', default=0, help="dump connector tables (for internal use)")

    parser.add_option("-f", "--failure-expected", action="store_true",
                      dest="failureExpected", default=0, help="expect the test to fail (for internal testing use)")
    
    parser.add_option("--debug-port", type="int", action="store", default=0,
                      dest='debugPort', help="port for graphical debug messages to server")

    parser.add_option("--gi", type="string",
                      dest='globalImplement', default="", help="set global implementations for capsule interfaces")
    parser.add_option("--ii", type="string",
                      dest='instanceImplement', default="", help="set instance implementations for capsule interfaces")

    parser.add_option("-i", "--invocations", action="store_true",
                      dest='traceInvocations', default="", help="trace all activity and transition invocations")
    parser.add_option("-m", "--system-mapping", type="string", default="",
                      dest="systemMapping", help="specify mapping file")
    parser.add_option("-p", "--processors", type="string", default="",
                      dest='processors', help="maps capsules to processors (simple string w. format cap=pro,*)")
    parser.add_option("--preprocess-only", action="store_true",
                      dest='preprocessOnly', default=0,
                      help="stop after preprocessing (macros for input)")
    parser.add_option("-P", "--profile", action="store_true", dest="profile", 
                      help="generate profile information")
    parser.add_option("-s", "--statistics", type="int", action="store", default=1,
                      dest='statistics', help="dump statistics in protocol 0=none;1=basic;2=detailed;3=gory")
    parser.add_option("--self-congratulate", action="store_true",
                      dest='selfCongratulate', help="print a message when expectations have been met (or have not been met but --fail was used too)")
    parser.add_option("--strict-states", action="store_true",
                      dest="strictStates", help="raise exception when message is not handled by a transition from current state")
    parser.add_option("--system-architecture", type="string", default="",
                      dest="systemArchitecture", help="specify system architecture file")
    parser.add_option("-r", "--results", default=0,
                      help="path for results subdirectory (defaults to res)", type="string",
                      dest='results')
    parser.add_option("--raw-python", action="store_true", dest="raw_python",
                      help="use raw python types")
    parser.add_option("-t", "--trace", action="store_true", dest="trace",
                      help="trace low level operations in results files")


    (options, args) = parser.parse_args()

    if options.txtsrc  == "pro":
        Files.dupeProtocol = True
    if options.txtsrc == "res":
        Files.dupeResults = True
        
    if options.debug:
        SimDebugger.activate()

    
    if options.trace:
        SimDebugger.t()

    if options.results:
        Global.outputPath = options.results + os.sep

    if options.ignoreAssert:
        Global.assertRaises = False


    Global.traceInvocations = options.traceInvocations

    Global.profile = options.profile

    Global.preprocessOnly = options.preprocessOnly

    Global.statistics = options.statistics

    Global.debugPort = options.debugPort

    Global.trace = options.trace

    Global.failureExpected = options.failureExpected

    Global.selfCongratulate = options.selfCongratulate

    Global.strictStates = options.strictStates

    if options.globalImplement:
        CapsuleMap.setGlobalMappingsFromOption(options.globalImplement)
    if options.instanceImplement:
        CapsuleMap.setInstanceMappingsFromOption(options.instanceImplement)

    Global.systemMapping = options.systemMapping
    Global.systemArchitecture = options.systemArchitecture
    
    if options.processors:
        SystemParser.setCapsuleProcessorMapFromOption(options.processors,options.systemArchitecture)


    if os.environ.has_key("RAW_PYTHON"):
        Global.raw_python = os.environ["RAW_PYTHON"] != ""
    else:
        Global.raw_python = options.raw_python

    if len(args) == 3:
        Global.sysFile = args[0]
        Global.scriptFile = args[1]
        Global.resFile = args[2]
    elif len(args) == 2:
        Global.sysFile = args[0]
        Global.scriptFile = args[1]
        Global.resFile = args[1]
    elif len(args) == 1:
        Global.sysFile = args[0]
        Global.scriptFile = args[0]
        Global.resFile = args[0]
    else:
        parser.print_help()
        sys.exit()

