from Message import error
import M3Types

class LUTEntry:
    # TBD this is becoming a fat little chappy, because every idiosyncracy of every kind of object is stored here now
    def __init__(self, node=None, tipe=None, val=None, declarer=None, mode=None, default=None, name=None, isIvar=False, internal=False):
        self.typeCode = -1 # if this stays this way then we know that we have a non-library type
        #if isIvar: print "ivar %s registered" % node
        self.isIvar = isIvar
        if tipe.__class__.__name__ == "LUTEntry": raise "hell"
        if tipe and tipe.isType: pass
        if node and node.isNode: pass # bug trap for bad parameter types
        self.finalTipe = tipe # The type - an M3Types object, usually derived from inside
        #if val:
        #    print "warning value %s constructed into entry" % val #OK
        self.finalVal = val # The value : if and only if this object is a constant
        self.node = node
        if declarer and declarer not in ["MODULE","VAR", "TYPE", "EXCEPTION",  "OPAQUE", "ENUM"]:
            raise "bogus declarer %s" % declarer 
            # MODULE : modules
            # VAR : formals, consts, vars, bindings, forids, tcaseids
            # TYPE : procedures, types
            # EXCEPTION : proves the rule
            # OPAQUE : we can overwrite these later
        self.declarer = declarer
        if mode and mode not in ["VALUE", "VAR", "READONLY"]:
            raise "bogus mode %s" % mode
        self.mode = mode
        # VALUE
        # VAR
        # READONLY TBD not yet checked in bodies of procedures
        self.default = default
        self.name = name
        self.internal = internal
        self.findingType = False
    def deref(self,name,obj):
        #print "dereffing any", self.image(), self.getTipe()
        # TBD currently an adhoc solution for the case where a method is accessed over an ObjectType 
        tipe = self.getTipe()
        if tipe.isObject:
            return tipe.deref(name,obj,self.declarer)
        else:
            return tipe.deref(name,obj)
    def image(self):
        return "LUTEntry No:%s T:%s V:%s D:%s M:%s D:%s Na:%s tc:%s Iv:%s Int:%s" % (
            self.node and self.node.image(),
            self.finalTipe, self.finalVal, self.declarer, self.mode,
            self.default, self.name, self.typeCode, self.isIvar, self.internal)
    def clone(self):
        return LUTEntry(
            node=self.node, tipe=self.finalTipe, val=self.finalVal, declarer=self.declarer,
            mode=self.mode, default=self.default, name=self.name, isIvar=self.isIvar, internal=self.internal)
    def getTipe(self,root=None):
        #print "root", root
        if not self.finalTipe:
            if self.findingType:
                self.finalTipe = M3Types.M3ErrorType(error("Recursive type definition (ask FJG for coaching)", self.node))
            else:
                self.findingType = True # detects recursive type definitions
                self.finalTipe = self.node.getType()
                self.findingType = False
        return self.finalTipe        
    def getVal(self):
        if not self.finalVal:
            #print "getting val for entry", self.image()
            self.finalVal = self.node.getVal()
        return self.finalVal
    def patchReveal(self, newNode, partial):
        if not partial: # TBD multiple partial revelations in the same scope will not work yet
            self.declarer = "TYPE" 
        self.finalTipe = None
        self.node = newNode
class LUT:
    def __init__(self,home):
        self.home = home
        self.table = {}
        self.enclosingLUT = None
    def dump(self):
        print "%s::%s" % (self.home.__class__.__name__,self.home.lineno) #OK
        for name in self.table:
            print "%s : %s" % (name, self.table[name].image()) #OK
    def enterOver(self,name,entry,obj):
        import Lexis
        if name in Lexis.reservedWords:
            error("%s is a reserved word" % name, obj,code="001")
        if name in self.table:
            if self.table[name].declarer != "TYPE":
                error("Procedure %s declared more than once" % name, obj, code="002")
            entry.spec = self.table[name]
            # TBD squirrel the spec away so you can check the match once everything is ready (but not yet)
        self.table[name]=entry
    def enter(self,name,entry,obj=None):
        import Lexis
        #print "Enter %s with entry %s" % (name, entry.image())
        if name in Lexis.reservedWords:
            error("%s is a reserved word" % name,obj, code="001")
        if name in Lexis.pythonReservedWords:
            error("%s is a python reserved word" % name, obj)
        if name in self.table:
            #self.dump()
            error("%s already declared" % name,obj, code="004")
        if entry.__class__.__name__ != "LUTEntry": raise "Only LUTEntries allowed"
        entry.name = name
        self.table[name]=entry

    def lookupEntry(self,name,obj=None,errorOnMissing=True):
        import Lexis
        import M3Reserved
        #print "looking up %s" % name
        res = None
        if name in Lexis.reservedWords:
            res = M3Reserved.getEntry(name, obj)
        elif name in self.table:
            res = self.table[name]
        else:
            enclut = self.getEnclosingLUT()
            if enclut:
                res = enclut.lookupEntry(name,obj,errorOnMissing)
        if not res and errorOnMissing:
            err = error("Unknown Identifier %s" % name,obj, code="005")
            res = LUTEntry(tipe=M3Types.M3ErrorType(err))
        return res
    def lookupLocalEntry(self, name): # Don't look any further than the current LUT
        if name in self.table:
            return self.table[name]
        else:
            return None
    def lookup(self,name,obj=None):
        res = self.lookupEntry(name,obj)
        return res.getTipe()
    def deref(self,name,obj):
        res = self.lookupEntry(name,obj)
        return res
    def getVal(self,name):
        res = self.lookupEntry(name)
        if not res:
            raise "compiler error in value lookup for %s" % name
            res = M3Types.M3ErrorType(res)
        return res.getVal()

    def getEnclosingLUT(self):
        if not self.enclosingLUT:
#            print self.home
            if self.home.parent:
                self.enclosingLUT = self.home.parent.getLUT()
            else:
                return None
        return self.enclosingLUT
        
        
