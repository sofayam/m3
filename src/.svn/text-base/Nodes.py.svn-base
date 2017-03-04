import string
import types
import xml.sax.saxutils

parserInstance = None


globalAtts = ["refid", "slot"] # every node uses these attributes
class Node:
    def isNULL(self):
        return False
    def __init__(self):
        self.isNode = True
        self.slot = "anon"
        self.attributes = []
        self.kids = []
        self.refid = "Vergessen und verschlampt!!!!!!"
    def makeSlot(self,slotvar,slotname):
#        print slotvar, slotname
        if type(slotvar) == types.InstanceType:
            slotvar.slot=slotname
    def setSlots(self): pass
    def dump(self): pass
#    def lookup(self):
#        return None
    def reset(self): self.kids=[]
    def restore(self): pass
    def add(self,*kids):
        for kid in kids:
            self.kids.append(kid)
    def length(self):return len(self.kids)
    def visit(self,func):
        # do something like test against dir() here
        func(self)
        for kid in self.kids:
            if kid:
                kid.visit(func)
    def collapse(self):
#        print "collapsing %d" % self.refid
        self.kids = [(kid and kid.flatten()) for kid in self.kids]
    def flatten(self):
#        print "default flatten %d" % self.refid
        return self
    def asXML(self,indent=0):
        name = self.__class__.__name__
        # Trim "Node": XML is fat enough already
        if name[-4:] != "Node":
            raise "Bad Node Class Name %s" % name
        name = name[:-4]
        spaces = " " * indent
        if self.kids:
            terminator = ""
        else:
            terminator = "/"
        pre = spaces + ("<%s %s%s>\n" % (name, self.atts(), terminator))
        children = ""
        if self.kids:
            for kid in self.kids:
                if kid:
                    children += kid.asXML(indent+1)
                else:
                    children += ((" " * indent) + "<None/>\n")
            post = spaces + "</%s>\n" % name 
        else:
            post = ""
        return pre + children + post 
    def atts(self):
        def convert(obj):
            if type(obj) == types.InstanceType:
                return obj.refid
            elif type(obj) != types.StringType:
                obj = str(obj)
            return xml.sax.saxutils.quoteattr(obj)
        res = ""
        localAtts = self.attributes
        res = string.join([
            "%s=%s" % (att, convert(getattr(self,att)))
            for att in localAtts + globalAtts
            ], " ")
        return res
    def toXML(self):
        top = '<?xml version="1.0"?>\n'
        rump = self.asXML()
        return top + rump
    def restoreSlots(self):
        anon = False
        named = False
        for kid in self.kids:
            if kid.slot == "anon":
                anon = True
            else:
                setattr(self,kid.slot,kid)
                named = True
        if anon and named:
            print "pathological mixture of named and unnamed slots : fix this at once" #OK
    def setParents(self,top=True):
        if top:
            self.parent = None
        for kid in self.kids:
            if kid:
                kid.parent = self
                kid.setParents(False)

##     def fixStartCol(self,breakOffsets):
##         def fixSub():
##             for off in breakOffsets:
##                 if self.startCol > off:
##                     return self.startCol - (off + 1)
##             return self.startCol
##         self.startCol = fixSub()
##         for kid in self.kids:
##             if kid:
##                 kid.fixStartCol(breakOffsets)

    def setRefs(self, ctr=0):
        ctr += 1
        self.refid = ctr
        for kid in self.kids:
            if kid:
                ctr = kid.setRefs(ctr)
        return ctr
    
    # Type checking "whatever" methods for visit
    def getTopNode(self):
        return self.parent.getTopNode()
    def inInterface(self):
        return self.parent.inInterface()

    # Diagnostic
    def image(self):
        return "<%s : src: %s : id: %s>" % (
            self.__class__.__name__,
            self.getTopNode().getHumanName(),
            self.refid)
