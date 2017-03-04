import tpg
import m3parser
import Options
import Errors
import compro
import sys
import os
import os.path
from Message import error, info, warning

turbo = False

def breakOffsets(txt):
    res = []
    for ind,char in enumerate(txt):
        if char == "\n":
            res.append(ind)
    return res

def load(fileName=None,src=None,patchFileName=None):
    if not (fileName or src):
        raise "Catastrophic problem with load - neither a fileName nor a sourcefile"
    p = m3parser.Parser()
    p.verbose = int(Options.options.verbosity)
    if fileName:
        if not os.path.exists(fileName):
            error("File %s does not exist" % fileName)
            return
        f = open(fileName)
        txt = f.read()
    else:
        txt = src
    txt = compro.commentkiller(txt)
    txt = compro.umlautkiller(txt)
    if Options.options.errorTest:
        Errors.findDirective(txt)
    try:
     topNode = p(txt)
    except tpg.SyntacticError, e:
        error(e.msg,  None, fileName or patchFileName, e.line, catastrophic=True, code="CAT002")
        raise
    if fileName:
        topNode.setSource(os.path.abspath(fileName))
    if patchFileName:
        topNode.setSource(os.path.abspath(patchFileName))
    regulariseTree(topNode)
    topNode.fixLeadChars(0,txt)
    topNode.renumber()
    
    if not os.path.exists(Options.options.library):
        os.mkdir(Options.options.library)

    f = open(Options.options.library + os.sep + topNode.getObjectName(),"w")
    f.write(topNode.toXML())
    f.close()
    if fileName and topNode:
        fileBase = os.path.splitext(os.path.basename(fileName))[0]
        unitName = topNode.modname.idname
        if fileBase != unitName:
            warning("File name %s and unit name %s do not match" % (fileBase,unitName))
    return topNode

def regulariseTree(node):
#    print "regularize"
    if turbo: return 
    node.visit(lambda x: x.collapse())
    node.visit(lambda x: x.restore())
    node.setRefs()
    node.setParents()
    node.visit(lambda x: x.setSlots())
    node.renumber()

def compileFragment(ruleName,fragString):
    #print "compileFragment",fragString
    p = m3parser.Parser()
    fragNode = p.parse(ruleName,fragString)
    fragNode.fixLeadChars(0,fragString)
    return fragNode

def setTurbo(setting=True):
    global turbo
    turbo = setting
