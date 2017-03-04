# use the dependency database to compute a compilation order for the closure of units starting from a given unit

import string
import pdb
import os
import stat
import os.path
import glob
import Options


import depDB

db = None
roster = {}

def grabDB():
    global db
    db = depDB.read()


def root(unit):
    return string.split(unit,".")[0]

def ext(unit):
    ss = string.split(unit,".")
    if len(ss) == 1:
        return None
    elif len(ss) == 2:
        return ss[1]
    else:
        raise "bad unit string"

def naked(unit):
    return len(string.split(unit,".")) == 1

def isSpec(unit):
    res = ext(unit) in ["ci3o", "i3o", "gi3o"]
    return res

def isBody(unit):
    return ext(unit) in ["cm3o", "m3o", "gm3o"]

def isGenBody(unit):
    return ext(unit) == "gm3o"

def makeSpec(unit):
    base = root(unit)
    capSpec = base + ".ci3o"
    if capSpec in db: return capSpec
    genSpec = base + ".gi3o"
    if genSpec in db: return genSpec
    modInt = base + ".i3o"
    if modInt in db: return modInt
    return None

def makeBody(unit):
    base = root(unit)
    capBody = base + ".cm3o"
    if capBody in db: return capBody
    modBody = base + ".m3o"
    if modBody in db: return modBody
    genBody = base + ".gm3o"
    if genBody in db: return genBody    
    return None


def makeUnit(unit):
    return makeBody(unit)
        
def getRequiredInterfaces(unit):
    if naked(unit):
        unit = makeBody(unit)
    reqints = [makeSpec(intf) for intf in db[unit] if makeSpec(intf)]
    if isBody(unit):
        s = makeSpec(unit)
        if s:
            reqints.append(s)
    return reqints

def getClosure(unit):
    closure = []
    if makeSpec(unit):
        closure.append(makeSpec(unit))
    if makeBody(unit):
        closure.append(makeBody(unit))            
            
    closure += getRequiredInterfaces(unit)
    newbs = True
    while newbs:
        newbs = []
        for unit in closure:
            intfs = getRequiredInterfaces(unit)
            for intf in intfs:
                if intf not in closure:
                    newbs.append(intf)
            b = makeBody(unit)
            if b and (b not in closure):
                newbs.append(b)
        closure = closure + newbs
    return closure

def compOrder(closure):
    for unit in closure:
        roster[unit] = getRequiredInterfaces(unit)
    order = []
    newbs = True
    while newbs:
        newbs = []
        # find the ones with no dependencies any more
        for cand in roster:
            if not len(roster[cand]):
                newbs.append(cand)
        for newb in newbs:
            del(roster[newb])
        # delete the dependencies from all the rest
        for unit in roster:
            for newb in newbs:
                if newb in roster[unit]:
                    roster[unit] = [ent for ent in roster[unit] if ent != newb]
        order = order + newbs
    if roster:
        print "unresolved dependencies"
    return order
            
def dependsOn(rawunit):
    unit = specifyUnit(rawunit)
    if isBody(unit):
        return []
    res = []
    for cand in db:
        if unit in [makeSpec(elt) for elt in db[cand]]:
            res.append(cand)
            res += dependsOn(cand)
    res.append(unit)
    if isSpec(unit):
        if makeBody(unit):
            res.append(makeBody(unit))
    return delDupes(res)

def allUnitFiles():
    # return all units in the library
    pref = Options.options.library + os.sep
    preflen = len(pref)
    paths = glob.glob("m3lib" + os.sep + "*.*o")
    return paths
#    return [unit[preflen:] for unit in paths]

def sourceFor(unitPath):
    map = {"ci3o" : "i3", "i3o": "i3", "cm3o": "m3", "m3o": "m3", "gm3o": "m3", "gi3o": "i3"}
    unit = unitFor(unitPath)
    root, suff = string.split(unit,".")
    sourceSuff = map[suff]
    return "%s.%s" % (root, sourceSuff)

def objFor(sourceFile):
    e = ext(sourceFile)
    if not e:
        raise "naked source file"
    if e == "i3":
        return makeSpec(sourceFile)
    elif e == "m3":
        return makeBody(sourceFile)
    
def unitFor(unitPath):
    return os.path.split(unitPath)[-1]

def outDated(): # things whose source is newer than their object
    res = []
    for unitFile in allUnitFiles():
        source = sourceFor(unitFile)
        if os.path.exists(source):
            sourcetime = os.stat(source)[stat.ST_MTIME]
            objtime = os.stat(unitFile)[stat.ST_MTIME]
            if sourcetime > objtime:
                res.append(unitFor(unitFile))
    # and now an afterburner to deal with generic body changes
    afters = []
    for unit in res:
        if isGenBody(unit) and makeSpec(unit) not in res:
            afters.append(makeSpec(unit))
    return res + afters

def specifyUnit(rawunit):
    # make it a spec if there is any doubt (and one exists)
    if naked(rawunit):
        if  makeSpec(rawunit):
            unit = makeSpec(rawunit)
        elif makeBody(rawunit):
            unit = makeBody(rawunit)
        else:
            raise "unit not available here"
    else:
        unit = rawunit
    return unit

def delDupes(dupes):
    res = []
    for dupe in dupes:
        if dupe not in res:
            res.append(dupe)
    return res

def getObsolete():  # things that need recompilation 
    obsolete = []
    for oldunit in outDated():
        obsolete += dependsOn(oldunit) + [oldunit]
    obsolete = delDupes(obsolete) # not strictly needed
    return obsolete

def isLib(unit):
    libfilename = string.join([os.environ['M3_HOME'],'lib','m3lib',unit], os.sep)
    return os.path.exists(libfilename)

def needRecompile(rawunit):
    unit = specifyUnit(rawunit)
    obsolete = getObsolete()
    allposs = compOrder(getClosure(unit))
    units = [unit for unit in allposs if not isLib(unit)]
    if not Options.options.forceCompile:
        units = [unit for unit in units if unit in obsolete]
    return [sourceFor(unit) for unit in units]

def getCompileCandidates(sourceFiles):
    res = []
    grabDB()
    for sourceFile in sourceFiles:
        res += getCompileCandidatesHelper(sourceFile)
    return delDupes(res)

def getCompileCandidatesHelper(sourceFile):
    obj = objFor(sourceFile)
    if not obj:
        return [sourceFile]
    else:
        return needRecompile(obj)

def getCClosure(unit):
    # Used for C Code generation, this dictates the execution order
    # of the elaboration code in the __main function
    grabDB()
    allUnits = compOrder(getClosure(unit))
    res = []
    for unit in allUnits:
        if isBody(unit):
            res.append(root(unit))
    return res

if __name__ == "__main__":
    Options.setOptions()
    grabDB()
#    print db
    #pdb.set_trace()
    #print getRequiredInterfaces("CapRTC1")
    import sys
    if len (sys.argv) == 2 :
        unit = sys.argv[1]
    else:
        unit = "StackUser.m3o"
    closure = getClosure(unit)
    print "closure (all those I need)", closure
    print "compOrder (in order)", compOrder(closure)
    print "depends (my dependents)", dependsOn(unit)
    print "outdated (src younger than obj)" , outDated()
    print "obsolete (dep on outdated)", getObsolete()
    print "needRecompile (obsolete /\ comporder)", needRecompile(unit)
    print "compileCandidates", getCompileCandidates(["StackUser.m3"])
