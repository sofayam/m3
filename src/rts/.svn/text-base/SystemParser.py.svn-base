import tpg
import compileSystemGrammar
compileSystemGrammar.metaCompile()
from SystemGrammar import Cmd
import Global
import Processors
import Time
import string
import os.path
def makeFile(name,ext):
    base,givenExt = os.path.splitext(name)
    if givenExt:
        return name
    else:
        return "%s.%s" % (name,ext)


def parseMapping(mapfile):
    mapfile = makeFile(mapfile,"map")
    try:
        maptxt = open(mapfile).read()
    except:
        print "Error opening mapfile %s " % mapfile
        return None,None
    parser = Cmd()
    try:
        mapdef = parser.parse("mapping",maptxt)
    except tpg.Error, e:
        print "%s:%s: %s " % (mapfile,e.line,e.msg)
        return None,None
    sysdef = parseArch(mapdef['sysid'])
    if not sysdef:
        return None,None
    else:
        return mapdef,sysdef

def parseArch(archfile):
    sysfile = archfile + ".sys"
    try:        
        systxt = open(sysfile).read()
    except:
        print "Error opening system architecture file %s " % sysfile
        return None        
    try:
        parser = Cmd()
        sysdef = parser.parse("architecture",systxt)
        return sysdef
    except tpg.Error, e:
        print "%s:%s: %s " % (sysfile,e.line,e.msg)
        return None

def calcSpeeds(sysdef):
    procDict = {}
    for proc,factor in sysdef['processors']:
        procDict[proc] = factor
    Processors.setSpeeds(procDict)
    return procDict


def calcCosts(sysdef):
    linkCosts = {}
    for source,dest,both,costNum,costId in sysdef['links']:
        if costId not in Time.FactorNames:
            print "Error in sys file : cost must use one of %s" % Time.FactorNames.keys()
            return False
        cost = int(Time.FactorNames[costId] * costNum)
        def setUnique(label,cost):
            if label in linkCosts:
                print "Error in sys file : link %s specified more than once" % label
                return False
            else:
                linkCosts[label] = cost
                return True
        if not setUnique("%s->%s" % (source,dest),cost): return False
        if both:
            if not setUnique("%s->%s" % (dest,source),cost): return False
    Processors.setLinkCosts(linkCosts)

def processMapfile():
    if not Global.systemMapping: return True
    mapdef,sysdef = parseMapping(Global.systemMapping)
    if not mapdef:
        return False
    #print mapdef,sysdef
    procDict = calcSpeeds(sysdef)
    capProcMap = {}
    for capid,proc in mapdef['allocations']:
        if proc not in procDict:
            print "Error in map file : processor %s not defined" % proc
            return False
        else:
            capidstr = string.join(capid,".")
            if capidstr in capProcMap:
                print "Error in map file : capsule %s mapped twice" % capidst
                return False
            capProcMap[capidstr] = proc
    Processors.setCapsuleProcessorMap(capProcMap)
    calcCosts(sysdef)
    return True

def processArchfile():
    if not Global.systemArchitecture: return True
    if Global.systemMapping:
        print "Error : you cannot supply a map file and a system file"
        return False
    sysdef = parseArch(Global.systemArchitecture)
    procDict = calcSpeeds(sysdef)
    calcCosts(sysdef)
    return procDict
    

def setCapsuleProcessorMapFromOption(option,systemArchitecture):
    mapPairs = string.split(option,",")
    speeds = {}
    arch = False
    if systemArchitecture:
        procDict = processArchfile()
        arch = True

    capsuleProcessorMap = {}
    for pair in mapPairs:
        capProc = string.split(pair,"=")
        if len(capProc) != 2:
            raise "error in capsule processor mapping option %s" % option
        else:
            cap, pro = capProc
            if arch:
                if pro not in procDict:
                    raise "error : processor %s not defined" % pro
            capsuleProcessorMap[cap]=pro
            if not arch:
                speeds[pro] = 1.0
    if not arch:
        Processors.setSpeeds(speeds)
    Processors.setCapsuleProcessorMap(capsuleProcessorMap)


if __name__ == "__main__":
    import RTSOptions
    RTSOptions.setOptions()
    import Options
    Options.setOptions()

    process("foo.map")
    
