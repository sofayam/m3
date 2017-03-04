import M3ProcLib
import Statistics
import DbgStub
import Scaling
import types
import string
import sets

#buglog = {}
#bugctr = 0
class M3Uninitialised:
    def image(self):
        return "***"
Uninitialised = M3Uninitialised()

def safeImage(obj):
    if type(obj) != types.InstanceType:
        return "?%s?" % str(obj)
    else:
        return obj.image()
def check(val):
    if val == Uninitialised:
        import M3Predefined
        raise M3Predefined.M3UninitialisedError.createObject()
    if val == None:
        raise "Compiler Bug : None value"
def applycompop(op1,op2,opfun):
    op1.incStatCtr("COMPARE")
    check(op1.val)
    check(op2.val)
    #print "compop", op1.val, op2.val
    res = M3Boolean(opfun(op1.val,op2.val))
    return res

def assignedHook(obj):
    while obj.owner:
        obj = obj.owner
    if hasattr(obj,"runtimeName"):
        
        objectName = string.split(obj.runtimeName,".")[-1]
        capsuleName = obj.owningCapsule.__class__.__name__
        newValue = safeImage(obj)
        #print "assignment : %s := %s (%s)" % (obj.runtimeName,newValue,capsuleName)
        DbgStub.showAssignment(capsuleName, objectName, newValue)

class M3Obj(Statistics.Gatherer):
    def __init__(self,tipe,val=Uninitialised):
        Statistics.Gatherer.__init__(self)
        if val == None:
            self.val = Uninitialised
        else:
            self.val=val
        self.tipe=tipe
#        self.isType = False
        self.isChoice = False
        self.owner = False
        self.hasPattern = False
    def assign(self, rhs):
        self.incStatCtr("ASSIGN")
        if rhs.val == Uninitialised:
            import M3Predefined
            raise M3Predefined.M3UninitialisedError.createObject()
        self.val = rhs.val
        assignedHook(self)
    def equals(self, obj):
        return applycompop(self,obj, lambda x, y: x == y)
    def notequals(self, obj):
        return applycompop(self, obj, lambda x, y: x != y)
    def less(self, obj):
        return applycompop(self, obj, lambda x, y: x < y)
    def greater(self, obj):
        return applycompop(self, obj, lambda x, y: x > y)
    def greatereq(self, obj):
        return applycompop(self, obj, lambda x, y: x >= y)
    def lesseq(self, obj):
        return applycompop(self, obj, lambda x, y: x <= y)
    def isIn(self, someSetorList):
        return someSetorList.containsElt(self)
    def isScalar(self):
        return self.tipe.isScalar()
class Numeric:
    def plus(self, obj):
        check(self.val)
        check(obj.val)
        return self.clone(self.val + obj.val)
    def add(self, obj):
        check(self.val)
        check(obj.val)
        self.val += obj.val
    def inc(self):
        check(self.val)
        self.rangeCheck(self.val + 1)
        self.val += 1
    def dec(self):
        check(self.val)
        self.rangeCheck(self.val - 1)
        self.val -= 1
    def minus(self, obj):
        check(self.val)
        check(obj.val)
        return self.clone(self.val - obj.val)
    def times(self, obj):
        check(self.val)
        check(obj.val)
        return self.clone(self.val * obj.val)
    def divide(self, obj):
        check(self.val)
        check(obj.val)
        if (obj.val == 0) or (obj.val == 0.0):
            import M3Predefined
            raise M3Predefined.M3DivideByZeroError.createObject()
        return self.clone(self.val / obj.val)
    def mod(self, obj):
        check(self.val)
        check(obj.val)
        return self.clone(self.val % obj.val)        
    def unplus(self):
        check(self.val)
        return self
    def unminus(self):
        check(self.val)
        return self.clone(-self.val)
    def rangeCheck(self, val):
        if (val < self.tipe.first) or (val > self.tipe.last):
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()
    def max(self, other):
        if self.val > other.val:
            return self.dupe()
        else:
            return other.dupe()
    def min(self, other):
        if self.val < other.val:
            return self.dupe()
        else:
            return other.dupe()

class M3Integer(M3Obj,Numeric):
    def __init__(self,tipe,val=Uninitialised):
        M3Obj.__init__(self,tipe)
        if val in  [None, Uninitialised]:
            self.val = Uninitialised
        else:
            self.val=val
            if type(self.val) == types.InstanceType: raise "run time bug : bad val"
        isType = False
        #print "val",self.val
    def clone(self,val=Uninitialised): # TBD this should shift up to the base type before assignment
        if val == None:
            raise "Compiler Bug : integer with None value"
        return M3Integer(self.tipe,val)
    def dupe(self):
        return M3Integer(self.tipe,self.val)
    def assign(self, rhs):
        self.incStatCtr("ASSIGN")
        if rhs.val == Uninitialised:
            import M3Predefined
            raise M3Predefined.M3UninitialisedError.createObject()
        if rhs.val == None:
            raise "Compiler Bug : integer with None value"
        if self.tipe.first:
            first = self.tipe.first
            if type(first) == types.InstanceType: first = first.val
            last = self.tipe.last
            if type(last) == types.InstanceType: last = last.val

            if (first <= rhs.val) and (rhs.val <= last):
                self.val = rhs.val
            else:
                import M3Predefined
                raise M3Predefined.M3ConstraintError.createObject()
                # TBD improve exception concept to contain more detailed error data
                #raise "Constraint Error : value %s outside of range [%s .. %s] for subtype" % (
                #   rhs.val, self.tipe.first, self.tipe.last)
        else:
            self.val = rhs.val
        assignedHook(self)
    def ord(self):
        return self
    def dump(self):
        return "Integer with val %s" % self.val
    def abs(self):
        return M3Integer(self.tipe,abs(self.val))
    def image(self):
        if self.val == Uninitialised:
            return "???"
        if self.tipe.scaling:
            return Scaling.image(self.tipe.scaling, self.val)
        else:
            return "%s" % self.val
    def genC(self):
        return "%s" % self.val

class M3Real(M3Obj,Numeric):
    def clone(self,val=Uninitialised):
        return M3Real(self.tipe,val)
    def dupe(self):
        return M3Real(self.tipe,self.val)
    def abs(self):
        return M3Real(self.tipe,abs(self.val))
    def image(self):
        if self.val == Uninitialised:
            return "???"
        return "%s" % self.val
    def genC(self):
        return "%s" % self.val
    
class M3Text(M3Obj):
    def assign(self,rhs):
        self.incStatCtr("ASSIGN")
        if rhs.val == Uninitialised:
            import M3Predefined
            raise M3Predefined.M3UninitialisedError.createObject
        self.val = rhs.val
        assignedHook(self)
    def dupe(self):
        return M3Text(self.tipe,self.val)
    def clone(self,val):
        return M3Text(self.tipe,val)
    def concat(self, other):
        return M3Text(self.tipe, self.val + other.val)
    def image(self):
        if self.val == Uninitialised:
            return "???"
        return self.val
boolInt = {True: 1, False: 0}
boolEnum = {True: "TRUE", False: "FALSE"}
enumBool = {"TRUE": True, "FALSE": False}
intEnum = {0: "FALSE", 1: "TRUE"}
            
class M3Record(M3Obj):
    def __init__(self, tipe, val):
        M3Obj.__init__(self,tipe,val)
        self.val = {}
        # first assign the defaults
        for k in tipe.fielddict:
            if tipe.fielddict[k].default:
                self.val[k] = tipe.fielddict[k].default.dupe()
            else:
                self.val[k] = tipe.fielddict[k].tipe.clone()
        # now set the value
        if val:
           for key in val:
               self.val[key] = val[key].dupe() 
        #import pdb; pdb.set_trace()
    def getField(self, fieldname):
        #print "getting field %s from %s" % (fieldname, self)
        field = self.val[fieldname]
        field.owner = self
        return self.val[fieldname]
    def dupe(self):
        fieldcopy = {}
        for k in self.val:
            fieldcopy[k] = self.val[k].dupe()
        rec = M3Record(self.tipe,None)
        rec.val = fieldcopy
        return rec
    def assign(self,rhs):
        self.incStatCtr("ASSIGN")
        self.val = rhs.dupe().val
        assignedHook(self)
    def clone(self):
        res = M3Record(self.tipe,None)
        return res
    def dump(self):
        return "M3Record with fields %s" % string.join(["%s -> %s" % (k,self.val[k].dump()) for k in self.val],",")
    def equals(self, other):
        if not self.tipe.fits(other.tipe):
            raise "compiler bug : equality test between incompatible records"
        res = True
        for field in self.val:
            if not self.val[field].equals(other.val[field]).toBool():
                res = False
                break
        return M3Boolean(res)
    def image(self):
        res = "{" + string.join(["%s: %s" % (k,safeImage(self.val[k])) for k in self.val],",") + "}"
        return res

class M3VariantRecord(M3Record):
    def getValidFieldNames(self):
        #import pdb; pdb.set_trace()
        tagval = self.val[self.tipe.tagname].ord().val
        return self.tipe.getValidFieldNames(tagval)
    def getField(self,fieldname):
        if fieldname == self.tipe.tagname:
            return self.val[fieldname]
        if fieldname in self.getValidFieldNames():
            return self.val[fieldname]
        else:
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()
    def image(self):
        res = "{" + string.join(["%s: %s" % (k,safeImage(self.val[k])) for k in self.getValidFieldNames()],",") + "}"
        return res

            
class M3Array(M3Obj):
    def __init__(self,tipe,val=None):
        M3Obj.__init__(self,tipe,val)
        if (not val) and (not tipe.isOpen):
            self.val = [None] * tipe.indexType.width()
        # self.proto = eltPrototype
    def clone(self, val=Uninitialised):
        # maybe needs deeper clone here
        return M3Array(self.tipe)
    def pokeElt(self, offset, elt): # used by choices to bypass the type/object system
        self.val[offset] = elt
    def getElement(self, offSet):
        self.incStatCtr("SUBSCRIPT")
        # You either supply an M3 Object or a true offSet (e.g. when constructing an open)
        if type(offSet) == types.InstanceType:
            offSet = self.tipe.indexType.relative(offSet.val)
#        print offSet
        if (offSet >= len(self.val)) or (offSet < 0):
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()
            # TBD use this info
            #raise "ArrayIndexConstraintError : index %s not in %s .. %s" % (offSet, self.tipe.indexType.first, self.tipe.indexType.last)
        if self.val[offSet] == None:
            #print "creating an array element"
            self.val[offSet] = self.tipe.elementType.clone()
        res = self.val[offSet]
#        print "res, res.val", res, res.val
        res.owner = self
        return res
    def dupe(self):
        cellcopy = []
        for cell in self.val:
            cellcopy.append(cell.dupe())
        arr = M3Array(self.tipe,None)
        arr.val = cellcopy
        return arr
    def assign(self,rhs):
        self.incStatCtr("ASSIGN")
        if rhs.tipe.isSubArray:
            rhs.push(self)
            return 
        if len(self.val) != len(rhs.val):
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()        
        for idx, (dest, src) in enumerate(zip(self.val, rhs.val)):
            if dest == None:
                dest = self.tipe.elementType.clone()
                self.val[idx] = dest                
            dest.assign(src)
        assignedHook(self)
    def getFirst(self):
        return self.tipe.getFirst()
    def getLast(self):
        return self.tipe.getLast()
    def getNumber(self):
        return self.tipe.getNumber()
    def dump(self):
        return "Array (TBD nice dump)"
    def equals(self, other):
        import M3Types
#        if self.tipe.isOpen or other.tipe.isOpen:
#            raise "Compiler Bug : comparison of open arrays"
        if self.tipe.fits(other.tipe):
            res = True
            for mine, his in zip(self.val, other.val):
                if not mine.equals(his).toBool():
                    res = False
                    break
        else:
            res = False
        return M3Boolean(res)
    def notequals(self, other):
        return M3Boolean(not(self.equals(other).toBool()))
    def image(self):
        return "[" + string.join([safeImage(elt) for elt in self.val],",") + "]"
    def iterables(self):
        return self.val
class M3SubArray(M3Obj):
    def __init__(self, tipe, arrayBase, start, length):
        M3Obj.__init__(self,tipe)
        self.arrayBase = arrayBase
        self.start = start
        self.length = length
        self.isType = False
    def getSlice(self):
        start = self.start.val
        finish = self.start.val + self.length.val
        # make sure there are no uninitialised sections here (otherwise the following assign would get lost in the slice)
        for idx in range(start, finish):
            if not self.arrayBase.val[idx]:
                self.arrayBase.val[idx] = self.arrayBase.tipe.element.clone()
        #print "getslice", start,finish

        res = self.arrayBase.val[start:finish]
        #print [elt.val for elt in res]
        return res
    def assign(self, other):
        self.incStatCtr("ASSIGN")
        # is the other an array ?
        if other.tipe.isSubArray:
            src = other.getSlice()
        else:
            src = other.val
        dest = self.getSlice()
        if len(dest) != len(src):
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()
        src = self.overlapCheck(src,dest)
        for destelt, srcelt in zip(dest,src):
            destelt.assign(srcelt)
        assignedHook(self)
    def push(self, destinationArray):
        # assign yourself to the contents of the other
        # only used when the other is a real array
        src = self.getSlice()
        dest = destinationArray.val
        if len(dest) != len(src):
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()
        src = self.overlapCheck(src,dest)
        for destelt, srcelt in zip(dest,src):
            destelt.assign(srcelt)        
    def overlapCheck(self, src, dest):
        if (src[0] != dest[0]) and ((src[0] in dest) or (dest[0] in src)):
            return [elt.dupe() for elt in src]
        return src
    def getElement(self, offset):
        self.incStatCtr("SUBSCRIPT")
        return self.getSlice()[offset.val] # Note that container creation was done for you in getslice


class M3Enum(M3Obj):
    def __init__(self,tipe,val=None):
        if not val:
            val=Uninitialised
        M3Obj.__init__(self,tipe,val)
        if val != Uninitialised:
            self.rangeCheck(val)
    def clone(self, val=Uninitialised):
        return M3Enum(self.tipe)
    def add(self, obj):
        if not type(obj) == types.IntType:
            obj = obj.val
        curidx = self.tipe.orddict[self.val]
        newidx = curidx + obj
        if newidx < 0 or newidx > len(self.tipe.values):
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()
        newval = self.tipe.values[newidx]
        self.rangeCheck(newval)
        self.val = newval
    def inc(self):
        self.add(1)
    def dec(self):
        self.add(-1)
    def ord(self):
        import M3Types
        idx = self.tipe.orddict[self.val]
        return M3Types.M3IntegerBase.createObject(idx)
    def dupe(self):
        return M3Enum(self.tipe,self.val)
    def rangeCheck(self, val):
        rhsord = self.tipe.orddict[val]
        #print self.tipe.firstord, rhsord, self.tipe.lastord
        if not ((self.tipe.firstord <= rhsord) and (rhsord <= self.tipe.lastord)):
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()
            #raise "Constraint Error : value outside of range for enum : %s is not between %s and %s" % (
            #    val, self.tipe.first, self.tipe.last)        
    def assign(self, rhs):
        self.incStatCtr("ASSIGN")
        if rhs.val == Uninitialised:
            import M3Predefined
            raise M3Predefined.M3UninitialisedError.createObject()

        if self.tipe.base != rhs.tipe.base:
            if self.tipe.values != rhs.tipe.values:
                raise "type mismatch - compiler bug!!!! self:%s rhs:%s" % (self.tipe.base,rhs.tipe.base)
        self.rangeCheck(rhs.val)
        self.val = rhs.val
        assignedHook(self)
    def less(self, other):
        res = self.ord().val < other.ord().val
        return M3Boolean(res)
    def greater(self, other):
        res = self.ord().val > other.ord().val
        return M3Boolean(res)
    def greatereq(self, other):
        res = self.ord().val >= other.ord().val
        return M3Boolean(res)
    def lesseq(self, other):
        res = self.ord().val <= other.ord().val
        return M3Boolean(res)
    def max(self,other):
        if self.ord().val > other.ord().val:
            return self.dupe()
        else:
            return other.dupe()
    def min(self,other):
        if self.ord().val < other.ord().val:
            return self.dupe()
        else:
            return other.dupe()
        
    def dump(self):
        return "Enum with val %s" % self.val
    def image(self):
        if self.val == Uninitialised:
            return "???"
        return self.val
    def genC(self):
        return "%s" % self.ord().val
class M3Boolean(M3Enum):
    def __init__(self,val):
        import M3Types
        Statistics.Gatherer.__init__(self)        
        self.tipe = M3Types.M3Boolean
        if val == None:
            self.val = Uninitialised
        elif type(val) == types.BooleanType:
            self.val = boolEnum[val]
        elif type(val) == types.StringType:
            if val in self.tipe.values:
                self.val = val
            else:
                raise "Compiler Bug :Bad Boolean String Value %s" % val
        elif type(val) == types.IntType:
            self.val = intEnum[val]
        else:
            raise "Compiler Bug : Bad Boolean Type %s" % val
        self.owner = False
        self.isChoice = False
    def toBool(self):
        if self.val == Uninitialised:
            import M3Predefined
            raise M3Predefined.M3UninitialisedError.createObject()
        return enumBool[self.val]
    def clone(self, val=Uninitialised):
        return M3Boolean(val)
    def opand(self, obj):
        check(self.val)
        check(obj.val)
        return M3Boolean(self.toBool() and obj.toBool())
    def opor(self, obj):
        check(self.val)
        check(obj.val)
        return M3Boolean(self.toBool() or obj.toBool())
    def opnot(self):
        check(self.val)
        return M3Boolean(not self.toBool())
    def dupe(self):
        return M3Boolean(self.val)

class M3Char(M3Obj):
    def __init__(self,tipe,val):
        M3Obj.__init__(self,tipe)
        if val == None:
            val = Uninitialised
        elif (type(val) == types.InstanceType) and val.tipe.isChar:
            val = val.val
        elif type(val) != types.StringType:
            raise "Compiler bug :Bad Character value %s" % val
            if len(val) != 1:
                raise "Character must be one character only : TBD fix this at compile time"

        self.val = val
        #print "-%s-%s-" % (self.tipe.first, self.tipe.last)
    def ord(self):
        import M3Types
        return M3Types.M3IntegerBase.createObject(ord(self.val))
    def dupe(self):
        return M3Char(self.tipe,self.val)    
    def add(self,inc):
        if type(inc) != types.IntType:
            inc = inc.val
        neword = ord(self.val) + inc
        self.rangeCheck(neword)
        self.val = chr(neword)
    def assign(self, other):
        self.incStatCtr("ASSIGN")
        self.rangeCheck(ord(other.val))
        self.val = other.val
        assignedHook(self)
    def inc(self):
        self.add(1)
    def dec(self):
        self.add(-1)
    def rangeCheck(self, int):
        #print "rangecheck int is", int, self.tipe.getFirst().ord()
        if (int < self.tipe.getFirst().ord().val) or (int > self.tipe.getLast().ord().val):
            import M3Predefined            
            raise M3Predefined.M3ConstraintError.createObject()
    def genC(self):
        return "'%s'" % self.val
        
class M3NilClass(M3Obj):
    def __init__(self):
        M3Obj.__init__(self,None)
        self.val = self
    def dupe(self):
        return self
    def getNarrowed(self, tipe):
        return self
        
M3Nil = M3NilClass()
        

class M3Ref(M3Obj):
    def __init__(self, tipe):
        M3Obj.__init__(self,tipe)
        self.val = M3Nil
    def dispose(self):
        self.val = M3Nil # TBD maybe poison dangling objects
    def new(self):
        self.val = self.tipe.referent.createObject()
    def check(self):
        if self.val == M3Nil:
            import M3Predefined
            raise M3Predefined.M3NullPointerError.createObject()
    def getRef(self):
        self.check()
        return self.val
    def getElement(self, offSet):
        self.incStatCtr("SUBSCRIPT")
        self.check()
        return self.val.getElement(offSet)
    def getField(self, fieldname):
        self.check()
        return self.val.getField(fieldname)
    def dupe(self):
        twin = M3Ref(self.tipe)
        twin.val = self.val
        return twin
    def dump(self):
        return "Ref to %s" % self.tipe
    def equals(self,other):
        return M3Boolean(self.val == other.val)
    def isType(self,tipe):
        res = self.tipe.fitsTCase([tipe]) 
        return M3Boolean(res)
    

class M3ReturnException(Exception):
    def __init__(self, retval):
        self.retval = retval

class M3FunctionNoReturnError(Exception): pass

class M3UnhandledException(Exception):
    def __init__(self, userException):
        self.exc = userException

class M3Object(M3Obj):
    def __init__(self, tipe):
        M3Obj.__init__(self,tipe)
        self.tipe = tipe
        # val is a window onto the instance chain which makes up the object
        self.val = M3Nil
        self.overrides = {}
    def dispose(self): # TBD maybe poison dangling objects
        self.val = M3Nil
        self.overrides = {}        
    def new(self):
        #print "in new"
        # build the instance chain from the tipe
        self.val = M3Instance(self.tipe,self)
        self.val.doOverrides()
        #print "self.val", self.val
    def getField(self, name):
        #print "calling getField", name
        if name in self.overrides:
            #print "getting override"
            res = self.overrides[name]
        else:
            res = self.val.getField(name)
        #print "getfield res", res
        return res
    def assign(self, other):
        self.incStatCtr("ASSIGN")
        if self.tipe == other.tipe:
            self.val = other.val
        else:
            #print "narrowing"
            #print "other, other.val", other, other.val
            narrowed = other.getNarrowed(self.tipe)
            self.val = narrowed.val
        self.overrides = other.overrides
        #print self.overrides
        assignedHook(self)
    def topVal(self):
        # go right to the top of the chain
        val = self.val
        while val.swper:
            val = val.swper
        return val
    def getNarrowed(self, tipe):
        val = self.topVal()
        # now hunt down for the equivalent type
        found = False
        while True:
            #print "narrowing down to %s" % val.tipe
            if (val.tipe == tipe) or (val.tipe.stamp == tipe.stamp):
                found = True
                break
            if not val.sub: break 
            val = val.sub
        if not found:
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()
        res = M3Object(tipe)
        res.val = val
        res.overrides = self.overrides
        return res
    def dupe(self):
        twin = M3Object(self.tipe)
        twin.val = self.val
        return twin
    def dump(self):
        val = self.topVal()
        while val:
            print val.tipe, val.val #OK
            val = val.sub
    def typecode(self):
        return self.tipe.typecode()
    def isType(self,tipe):
        res = self.tipe.fitsTCase([tipe]) 
        return M3Boolean(res)
class M3Instance(M3Obj):
    def __init__(self,tipe,obj):
        # create my instance using the tipe (supertype, fields, methods, overrides)
        # create all swperinstances using swpertipes
        self.obj = obj 
        self.tipe = tipe
        self.sub = None
        self.swper = None
        self.fields = {}
        for k in tipe.fielddict:
            if tipe.fielddict[k].default:
                defoe = tipe.fielddict[k].default
                #print "defoe", defoe
                if type(defoe) in [types.StringType, types.UnicodeType]: 
                    defoe = M3ProcLib.lookup(defoe)
                    self.fields[k] = M3MethodWrapper(defoe, obj)
                else:
                    #print "defoe", defoe
                    self.fields[k] = defoe.dupe()
            else:
                if tipe.fielddict[k].__class__.__name__ != "LUTEntry":
                    self.fields[k] = tipe.fielddict[k].getTipe().clone()
                else:
                    self.fields[k] = "function"
        if tipe.swper:
            self.swper = M3Instance(tipe.swper, self.obj)
            self.swper.sub = self

    def doOverrides(self):
        if self.swper:
            self.swper.doOverrides()
        if not self.tipe.overrides: return 
        for override in self.tipe.overrides:
            #print "override", override
            if not override.default: raise "compiler bug : null override default"
            meth= M3ProcLib.lookup(override.default)
            self.obj.overrides[override.name] = M3MethodWrapper(meth,self.obj)

    def getField(self, name):
        if name in self.fields:
            return self.fields[name]
        if self.swper:
            return self.swper.getField(name)
        else:
            raise "compiler bug : attempt to access non-existent object field %s" % name

class NullInstance:
    def __getattr__(self, name):
        import M3Predefined
        raise M3Predefined.M3NullPointerError.createObject()

class M3MethodWrapper:
    def __init__(self, meth, obj):
        self.meth = meth
        self.obj = obj
    def __call__(self, *args, **kwargs):
        # narrow the object to the tipe of the instance level where the method was found 
        return self.meth(self.obj, *args, **kwargs)
    
class M3Set(M3Obj):
    def __init__(self,tipe,val=None):
        M3Obj.__init__(self,tipe)
        if val==None:
            self.val = sets.Set()
        else:
            self.val = val
        self.firstOrd = self.tipe.rangeType.getFirst().ord().val
        self.lastOrd = self.tipe.rangeType.getLast().ord().val
    def dupe(self):
        return self.tipe.createObject(self.val.copy())
    def addElt(self, eltInt):
        if eltInt not in range(self.firstOrd, self.lastOrd+1):
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()
        self.val.add(eltInt)
    def addMember(self, elt):
        eltOrd = elt.ord().val
        self.addElt(eltOrd)
    def addRange(self, elt):
        first, last = elt
        firstOrd = first.ord().val
        lastOrd = last.ord().val
        for i in range(firstOrd,lastOrd+1):
            self.addElt(i)
    def containsElt(self, elt):
        ord = elt.ord().val
        return M3Boolean(ord in self.val)
    def plus(self, other):
        return self.tipe.createObject(self.val.union(other.val))
    def minus(self, other):
        return self.tipe.createObject(self.val.difference(other.val))
    def equals(self,other):
        return M3Boolean(self.val == other.val)
    def times(self, other):
        return self.tipe.createObject(self.val.intersection(other.val))
    def divide(self,other):
        return self.tipe.createObject(self.val.symmetric_difference(other.val))
    def notequals(self,other):
        return M3Boolean(self.val != other.val)
    def image(self):
        import M3Types
        # makeval is a runtime function so we need to convert the set member into an m3 integer before we can use it
        return "[" + string.join([self.tipe.rangeType.makeval(M3Types.M3IntegerBase.createObject(s)).image() for s in self.val],",") + "]" 
class M3Exception(M3Obj):
    def __init__(self, tipe=None, val=None, name=None):
        M3Obj.__init__(self,tipe,val)
        self.name = name
    def __str__(self):
        if self.val:
            return self.val
        else:
            return self.__class__.__name__
class M3CapsuleBody(M3Obj):
    def __init__(self, tipe=None):
        M3Obj.__init__(self,tipe,None)
        
        
class M3List(M3Obj):
    def __init__(self, tipe, val=None):
        M3Obj.__init__(self,tipe,val)
        if val==None:
            self.val = []
        if type(self.val) == type(()): raise "hell"
    def append(self,elt):
        self.val.append(elt)
    def getLast(self):
        import M3Types
        idx = len(self.val)
        return M3Types.M3IntegerBase.createObject(idx)
    def getFirst(self):
        import M3Types
        return M3Types.M3IntegerBase.createObject(1)
    def getElement(self, offSet):
        self.incStatCtr("SUBSCRIPT")
        offSet = offSet.val - 1 # These lists are 1-based: MWA says this is the way things are meant to be
        if offSet not in range(0,len(self.val)):
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()
        res = self.val[offSet]
        res.owner = self
        return res
    def image(self):
        return "[" + string.join([safeImage(elt) for elt in self.val],",") + "]"
    def iterables(self):
        return self.val
    def dupe(self):
        return self.tipe.createObject([item.dupe() for item in self.val])
    def delete(self,offSet):
        offSet = offSet.val - 1 # These lists are 1-based: MWA says this is the way things are meant to be
        if offSet not in range(0,len(self.val)):
            import M3Predefined            
            raise M3Predefined.M3ConstraintError.createObject()
        self.val = self.val[:offSet] + self.val[offSet+1:]
    def getNumber(self):
        import M3Types
        return M3Types.M3IntegerBase.createObject(len(self.val))
    def equals(self, other):
        res = len(self.val) == len(other.val)
        if res:
            for me,him in zip(self.val,other.val):
                res = me.equals(him).toBool()
                if not res: break
        return M3Boolean(res)

    def containsElt(self, elt):
        import M3Types
        res = self.index(elt, exc=False)
        return M3Boolean(not not res)
    def index(self, elt, exc=True):
        import M3Predefined
        import M3Types
        for idx in range(len(self.val)):
            if self.val[idx].equals(elt).toBool():
                return M3Types.M3IntegerBase.createObject(idx+1)
        if exc:
            raise M3Predefined.M3ConstraintError.createObject()
        else:
            return 0
        

class M3Dict(M3Obj):
    def __init__(self, tipe, val=None):
        M3Obj.__init__(self,tipe,val)
        if val==None:
            self.val = {}
    def makeKey(self, textKey):
        import CommandReader
        c = CommandReader.Cmd()
        parsedres = c.parse("value",textKey)
        # take the internal text key and turn it into a value of the index type
        typedres = self.tipe.indexType.coerce(parsedres)
        return typedres
    def getElement(self, key):
        self.incStatCtr("SUBSCRIPT")
        key = key.image()
        if key not in self.val:
            self.val[key] = self.tipe.elementType.createObject()
            
        res = self.val[key]
        res.owner = self
        return res
    def getKeys(self):
        import M3Types
        res = M3Types.M3ListType(self.tipe.indexType).createObject()
        for key in self.val:
            res.append(self.makeKey(key))
        return res
    def image(self):
        return "{" + string.join(["%s : %s" % (key, safeImage(self.val[key])) for key in self.val],",") + "}"
    def dupe(self):
        newdict = {}
        for key in self.val:
            newdict[key] = self.val[key].dupe()
        return self.tipe.createObject(newdict)
    def delete(self,key):
        key = key.image()
        if key not in self.val:
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()            
        del self.val[key]

    def equals(self, other):
        res = len(self.val.keys()) == len(other.val.keys())
        if res:
            for mykey in self.val.keys():
                res = mykey in other.val.keys()
                if not res: break
                res = self.val[mykey].equals(other.val[mykey]).toBool()
                if not res: break
        return M3Boolean(res)
    def index(self, element):
        import M3Types
        import M3Predefined
        for key in self.val.keys():
            if element.equals(self.val[key]).toBool():
                return self.makeKey(key)
        raise M3Predefined.M3ConstraintError.createObject()                        

# Wildcard patterns are also a kind of Object

class ChoiceHolder(M3Obj):
    def __init__(self):
        M3Obj.__init__(self,"No Type","No Value")
        self.isChoice = True
        
class Any(ChoiceHolder):
    def __init__(self):
        ChoiceHolder.__init__(self)
    def equals(self, other):
        return M3Boolean(True)
    def image(self):
        return "*"
class Range(ChoiceHolder):
    def __init__(self, small, large):
        ChoiceHolder.__init__(self)        
        self.small = small
        self.large = large
    def equals(self, other):
        return other.greatereq(self.small).opand(other.lesseq(self.large))
    def image(self):
        return "[[ %s .. %s ]]" % (self.small.image(), self.large.image())

class Alternatives(ChoiceHolder):
    def __init__(self, altList):
        ChoiceHolder.__init__(self)        
        self.altList = altList
    def equals(self, other):
        passed = False
        for alt in self.altList:
            if other.equals(alt).toBool():
                passed = True
                break
        return M3Boolean(passed)
    def image(self):
        return "[[ " + string.join([alt.image() for alt in self.altList],"; ") + " ]]" 

    
