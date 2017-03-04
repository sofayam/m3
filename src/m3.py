#
# Main driver for modula 3 compiler
#
import sys
import Options
import os.path
import UnitCache
import M3TypeLib
import depDB
import glob
#import profile
import Message
from Message import error, info, warning, messageOut
from FakeFile import FakeFile
import CompilationUnit
import CompOrder
import Exceptions        
import LibraryManager
def compile(fileName=None, src=None, mainProg=False, patchFileName=None, saveOutput=True,obj=None):
    options = Options.options
    fullFileName = None

    # Either swallow the program string directly or, depending on fileName, load from library or from src 
    if src:
        import LoadSrc
        topNode = LoadSrc.load(src=src, patchFileName=patchFileName)
    elif fileName[-1:] != "o": # TBD factor this out to somewhere where we know all about filetypes
        import LoadSrc
        topNode = LoadSrc.load(fileName=fileName)
    else:
        import LoadObj
        unitName = CompilationUnit.transformFileToUnit(fileName)
        res = UnitCache.loaded(unitName)
        if res:
            return res
        fullFileName = options.library + os.sep + fileName
        topNode = LoadObj.load(fullFileName,obj)
        if not topNode: return
        topNode.setParents()

    if not topNode: return 

    # update the dependency database

    deps = topNode.getDependencies()
    depDB.add(topNode.getObjectName(), deps)
    
    if (not options.syntax_only) and topNode.isInstantiation():
        topNode = topNode.substituteTree()
        topNode.setRefs()
        topNode.setParents()        
        topNode.visit(lambda x: x.setSlots())        
    if not (options.syntax_only or topNode.isGeneric()):
        naming(topNode,mainProg)
        typing(topNode,mainProg)
    if options.xmldump and mainProg:
        print topNode.toXML() #OK
    if Message.errors == 0:
        if options.generate and mainProg:
            codegen(topNode,saveOutput)
    else:
        Message.info("No Code Generated")
    if mainProg: Message.summary(topNode.getHumanName())
    UnitCache.add(topNode.getUnit(),topNode)
    if options.regenerate and mainProg:
        print topNode.regen() #OK
    if options.dumpLUT and mainProg:
        topNode.visit(lambda x: x.dumpLUT())

    return topNode

def naming(topNode,mainProg=False):
    options = Options.options
    topNode.visit(lambda x: x.checkIdMatch()) # check that start Ids match end Ids
    topNode.visit(lambda x: x.createLUT()) # create lookup tables at given points in tree
    topNode.checkExports()

    topNode.visit(lambda x: x.insertLUT()) # insert all imports and declarations into LUTs

    topNode.visit(lambda x: x.flushType())

    topNode.visit(lambda x: x.doCapsuleLUT()) # make capsule spec msgs visible in body

    topNode.visit(lambda x: x.checkMethodAsst()) 

    topNode.visit(lambda x: x.insertExceptionLUT()) # we have to leave this till last for compound objects which are exception parameters
    

def typing(topNode,mainProg=False):

    topNode.visit(lambda x: x.getExprType()) # derive the types of all expressions (this catches procedure calls too at the moment)

    topNode.visit(lambda x: x.checkCallSt()) # close syntactical loophole for call statements (could be any expression)
    topNode.visit(lambda x: x.checkAsst())   # check assignments

    topNode.visit(lambda x: x.checkIntention())
    
    # TBD Possibly group this lot into one set of statement checkers to save passes
    topNode.visit(lambda x: x.checkIf())             
    topNode.visit(lambda x: x.checkReturn())
    topNode.visit(lambda x: x.checkReturnMissing()) # Note that these two must be performed sequentially
    topNode.visit(lambda x: x.checkTryXpt())
    topNode.visit(lambda x: x.checkRaise())
    topNode.visit(lambda x: x.checkCaseSt())
    topNode.visit(lambda x: x.checkResetSt())
    topNode.visit(lambda x: x.checkExitSt())
    topNode.visit(lambda x: x.checkTCase())
    topNode.visit(lambda x: x.checkConnection())
    topNode.visit(lambda x: x.checkTransition())
    topNode.visit(lambda x: x.checkActivity())
    topNode.visit(lambda x: x.checkSpecMatch())
    
    topNode.checkProcsImplemented()
    
def codegen(topNode,saveOutput):
    if topNode.isGeneric(): return 
    topNode.generatePython(saveOutput)
    if Options.options.ccode:
        topNode.generateC(saveOutput)
    if saveOutput:
        M3TypeLib.externaliseTypes(topNode.getBaseName())

def doCompile():
    args = Options.args
    if len(args) == 1:
        fileList = glob.glob(args[0])
    else:
        fileList = args
    if fileList and (Options.options.closure or Options.options.forceCompile):
        #import pdb; pdb.set_trace()
        fileList = CompOrder.getCompileCandidates(fileList)
    if Options.options.whatif:
        for file in fileList:
            print "m3 %s" % file
            
    elif fileList:
        for file in fileList:
            import M3TypeLib
            M3TypeLib.flush()
            import UnitCache
            UnitCache.flush()
            # TBD : This is wasteful but it allows us to carry out destructive operations on types (I think)
            import Scaling
            Scaling.flush()
            compile(fileName=file,mainProg=True)
            if Message.errors:
                sys.exit("Errors during Compilation")
            Message.reset()
    else:
        compile(fileName=args[0],mainProg=True)
        if Message.errors:
            sys.exit("Errors during Compilation")

if __name__ == "__main__":
    Options.setOptions()
    LibraryManager.updateLib()
    if Options.options.profile:
        print "profiling..." #OK
        #profile.run("doCompile()","profile.dat")
    else:
        try:
            doCompile()
        except Exceptions.CompilerCatastrophic, res:
            messageOut("Compile aborted\n")

