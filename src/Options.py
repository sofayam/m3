# TBD add some differentiated handling for sharing/differentiating options depending on caller

import optparse

options = None
args = None

def setOptions():
    global args, options
    parser = optparse.OptionParser(usage="usage: %prog <filename> [options]")
    parser.add_option("--animate-script", dest="animate", action="store_true",
                      help="record details of movement during scripting")
    parser.add_option("-a", "--arrows-off", dest="arrowsOff", action="store_true",
                      help="switch off dataflow labels and arrows")
    parser.add_option("-c", "--ccode", dest="ccode", action="store_true",
                      help="generate c code")
    parser.add_option("-C", "--draw-cameos", dest="cameos", action="store_true",
                      help="draw miniature capsule representation in each child")
    parser.add_option("--closure", dest="closure", action="store_true",
                      help="automatically compile all obsolete units needed to build this unit (see also --force-compile-closure)")
    parser.add_option("-d", "--dump-LUT", dest="dumpLUT", action="store_true",
                      help="dump Lookup Tables")
    parser.add_option("--debug-port", dest="debugPort", type="int", action="store", default=6666,
                      help="port used by capsule editor to serve graphical debugger requests"),
    
    parser.add_option("-e", "--stop-on-error", dest="stoperror", action="store_true",
                      help="stop on error (rather than just complain and go on)")
    parser.add_option("-E", "--error-test", dest="errorTest", action="store_true",
                      help="run in error testing mode (internal magic)")
    parser.add_option("-f", "--force-compile-closure", dest="forceCompile", action="store_true",
                      help="force recompilation of all needed units")
    parser.add_option("-g", "--generate-scene", action="store_true", dest="genSceneOnly",
                      help="generate POVRAY scene and quit")

    parser.add_option("-G", "--ignore-geometry", action="store_true", dest="ignoreGeometry",
                      help="ignore Window geometry resources")
    parser.add_option("--gen-doc", dest="genDoc", action="store_true", 
                      help="generate documentation (internal use only)")

    parser.add_option("--hilight", dest="highlightValueMaxLen", type="int", action="store", default=0,
                      help="maximum length of a value string to display during graphical debugging")

    parser.add_option("-H", "--hide-ports", dest="hideports", action="store_true",
                      help="Do not show messages in ports (useful for domain models containing activities only)")

    parser.add_option("-i", "--information", dest="info", action="store_true",
                      help="print possibly useful information") #OK
    parser.add_option("-I", "--no-implicit-connections", dest="noImplicit", action="store_true",
                      help="do not render implicit connections")
                      
    parser.add_option("-l", "--library", type="string", dest="library", action="store",
                      default="m3lib", help="library to store object files and generated code")
    parser.add_option("-m", "--no-summary-messages", dest="nosummarymessages", action="store_true",
                      help="suppress summary messages (restricts output on regression tests)")
    parser.add_option("--main-program", dest="mainProgram", action="store_true",
                      help="generate a C main program also (if compiling a module with --ccode enabled)")
    parser.add_option("--no-XML-server",  action="store_true", dest="noXMLServer",
                      help="do not activate XML RPC Server")
    parser.add_option("--no-library-check", action="store_true", dest="noLibraryCheck",
                      help="do not perform library update check (internal)")
    parser.add_option("-p", "--no-python", action="store_false", dest="generate", default=True,
                      help="do not generate python code")
    parser.add_option("-P", "--profile", action="store_true", dest="profile", 
                      help="generate profile information")
    parser.add_option("--print", action="store_true", dest="printQuit", 
                      help="print the capsule and quit")
       
    parser.add_option("-r", "--regenerate-m3", action="store_true", dest="regenerate",
                      help="regenerate modula3 file from syntax tree")
    parser.add_option("-R", "--ignore-resources", action="store_true", dest="ignoreResources",
                      help="ignore all resources (use random positions)")

    parser.add_option("-s", "--syntax-only", action="store_true", dest="syntax_only",
                      help="quit before naming pass")
    parser.add_option("-S", "--script-output", default=0, dest="script_output", type="string",
                      help="where to put script output (default SessionScript.py")
#    parser.add_option("--screenshot", action="store_true", dest="screenshot",
#                      help="generate a screenshot of the capsule(s) and quit")
    parser.add_option("--slack", action="store_true", dest="slack",
                      help="only generate warnings for some errors (allows execution of incomplete models)")
    parser.add_option("--shadows", action="store_true", dest="shadows",
                      help="draw shadows in capsule editor")
    parser.add_option("--track-constant-expressions", dest="constExp", action="store_true",
                      help="track constant expression calculation")
    parser.add_option("-v", "--verbose", type="string", dest="verbosity", action="store", default="0",
                      help="Track syntax checking over rules 0=none;1=matched symbols;2=all rules")
    parser.add_option("-w", "--no-warnings", dest="nowarnings", action="store_true",
                      help="suppress warnings")
    parser.add_option("--what-if", dest="whatif", action="store_true",
                      help="only list the files which would be compiled (useful with --force-compile-closure and --closure")
    parser.add_option("-x", "--xml-dump", action="store_true", dest="xmldump",
                      help="dump generated xml to console")
    parser.add_option("-X", "--raise-unhandled-exceptions", action="store_true", dest="raiseUnhandled",
                      help="raise unhandled exceptions rather than transforming them to M3 world")

    options, args = parser.parse_args()

    if options.syntax_only:
        options.generate = False



