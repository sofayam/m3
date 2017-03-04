import os
import sys
import M3Types
import cPickle
TypeTable = {}
TableCtr = 1 # the counter is the type code


def enter(lutEntry):
    global TableCtr
    TypeTable[TableCtr] = lutEntry
    lutEntry.typeCode = TableCtr
    TableCtr += 1

def m3home():
    res = os.environ['M3_HOME']
    if res[0] in ["'", '"']:
        res = res[1:-1]
    return res

def getLibName(baseName):
    return baseName + "TypeLib"
    
def getExistingLibName(baseName):
    #print "libName",baseName
    libName = baseName + "TypeLib"
    if not os.path.exists(libName):
        libName = m3home() + os.sep + "lib" + os.sep + libName
        if not os.path.exists(libName):
            raise "Type Library for %s Not Found" % baseName
    return libName

def externaliseTypes(baseName):
    # first tickle all the LUT entries to make sure the types have been generated from their nodes
    for key,entry in TypeTable.items():
        if entry:
            tmp = entry.getTipe()
            if tmp.isProtocol:           # TBD FIXME : hack to zap protocol types because they won't pickle
                TypeTable[key] = None
            entry.node = None #TBD FIXME : another hole brutally plugged (Timer tests where somehow dragging in Tkinter functions which wouldn't pickle)
    f = open(getLibName(baseName),"w")
    cPickle.dump(TypeTable,f)
    f.close()

loadedTypes = {}

def internaliseTypes(baseName):
    if baseName in loadedTypes:
        return loadedTypes[baseName]
    f = open(getExistingLibName(baseName),"r")    
    tl = cPickle.load(f)
    loadedTypes[baseName] = tl
    return tl
    
def flush():
    global loadedTypes
    loadedTypes = {}
