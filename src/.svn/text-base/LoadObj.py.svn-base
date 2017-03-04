import sys
from Nodes import *
from RuleNodes import *
from xml.sax import ContentHandler
import os.path
import os
import stat
import xml.sax
import relpath
from Message import error
class NodeHandler(ContentHandler):
    def __init__(self):
        self.nodeStack = []
        self.currNode = None
        ContentHandler.__init__(self)
    def startElement(self,name,attributes):
        import RuleNodes
        self.nodeStack.append(self.currNode)
        nodeName = name
#        print "start an element %s" % name
#        print dir()
#        print "nn",nodeName
        self.currNode = eval("RuleNodes." + nodeName + "Node()")
        self.currNode.reset() # get rid of the dummy kids
        for k,v in attributes.items():
            setattr(self.currNode,k,v)
    def endElement(self,name):
#        print "end an element %s" % name
        oldNode = self.currNode
        self.currNode = self.nodeStack.pop()
        if self.currNode:
            self.currNode.add(oldNode)
        else:
            self.topNode = oldNode
#            print "finished!"
        
def load(filename, obj=None):
    parser = xml.sax.make_parser()
    nh = NodeHandler()
    parser.setContentHandler(nh)
    if not os.path.exists(filename):
        # try looking in the predefined library
        base = os.path.basename(filename)
        libfilename = string.join([os.environ['M3_HOME'],'lib','m3lib',base], os.sep)
        if not os.path.exists(libfilename):
            error("%s does not exist" % filename, catastrophic=True, obj=obj, code="CAT001")
        else:
            #print "got library file %s" % libfilename
            filename = libfilename

    parser.parse(filename)
    tn = nh.topNode
#    tn.resolveRefs()
    tn.visit(lambda x: x.restoreSlots())
    if os.path.exists(tn.source):
        sourcetime = os.stat(tn.source)[stat.ST_MTIME]
        objtime = os.stat(filename)[stat.ST_MTIME]
        if sourcetime > objtime:
            import LoadSrc
            print "Recompiling %s from %s" % (filename,relpath.relcwd(tn.source)) #OK
            tn = LoadSrc.load(fileName=tn.source)
    return tn


        
if __name__ == "__main__":
    print load(sys.argv[1]).toXML() #OK
    
