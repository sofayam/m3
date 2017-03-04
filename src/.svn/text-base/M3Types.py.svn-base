import M3Objects
from Message import error
import string
import types
import M3ProcLib
typecodectr = 1
class M3Type:
    def __init__(self):
        global typecodectr
        self.isType = True
        self.isNumeric = False        # These may look clumsy but they keep reflection out of UserNodes
        self.isOrdinal = False
        self.isText = False
        self.isArray = False
        self.isSubArray = False        
        self.isProcedure = False
        self.isSet = False
        self.isRecord = False
        self.isModule = False
        self.isReal = False
        self.isInteger = False
        self.isEnum = False
        self.isBoolean = False        
        self.isChar = False
        self.isRef = False
        self.isNull = False
        self.predef = False
        self.isOpen = False
        self.isObject = False
        self.isSet = False
        self.isSubrange = False
        self.isError = False
        self.isCapsuleBody = False
        self.isCapsuleSpec = False
        self.isTimer = False
        self.isTrigger = False
        self.isList = False
        self.isDict = False
        self.isProtocol = False
        self.isPort = False
        self.tcode = typecodectr
        typecodectr += 1
    def isScalar(self):
        return self.isInteger or self.isReal or self.isEnum
    def fits(self, other, obj=None):
        # TBD you can expand this to deal with sub- and opaque types later
        return self.__class__.__name__ == other.__class__.__name__
    def pyTypeName(self,val):
        return "M3Types.%s.createObject(%s)" % (self.name, val)
    def typecode(self):
        return M3Cardinal.createObject(self.tcode)
    def image(self):
        return self.__class__.__name__
    def coerce(self,cval,allowChoices=False):
        # check for choice object
        if type(cval) != types.InstanceType:
            return self.specCoerce(cval, allowChoices)
        elif not allowChoices:
            raise "Choices only allowed in expected results specifications : %s" % cval.image() 
        else:
            # now tell the choice object to do the coercion, but tell it how
            return cval.doCoerce(self.specCoerce)
    def flush(self): pass

class M3TextType(M3Type):
    def createObject(self,val=None):
        return M3Objects.M3Text(self,val)
    def clone(self):
        return M3Objects.M3Text(self)
    def fits(self,other,obj=None):
        return other.isText
    def specCoerce(self, val, allowChoices):
        return self.createObject(str(val))
M3Text = M3TextType()
M3Text.predef = True
M3Text.name = "M3Text"
M3Text.isText = True


# This is a strange type - users never see this
class M3ModuleType(M3Type):
    def __init__(self,lut):
        M3Type.__init__(self)
        self.isModule = True
        self.lut = lut
    def deref(self,field,obj):
        return self.lut.deref(field,obj)
    def derefString(self,right):
        return ".%s" % right
    def getVal(self, field, obj):
        return self.lut.getVal(field)

class M3NumericType(M3Type):
    def __init__(self):
        M3Type.__init__(self)
        self.isNumeric = True


class M3RealType(M3NumericType):
    def __init__(self):
        M3NumericType.__init__(self)
        self.isReal = True
    def createObject(self,val=None):
        return M3Objects.M3Real(self,val)
    def clone(self):
        return M3Objects.M3Real(self,None)
    def specCoerce(self,val,allowChoices):
        if type(val) not in [types.IntType, types.FloatType]:
            raise "test input coercion error : %s cannot be coerced to real" % val
        return self.createObject(val)
    def image(self):
        return "REAL"

M3RealBase = M3RealType()
M3RealBase.predef = True
M3RealBase.name = "M3RealBase"

class M3IntegerType(M3NumericType):
    def __init__(self, limits=None, scaling=None):
        M3NumericType.__init__(self)
        self.first, self.last = limits
        self.scaling = scaling
        if type(self.first) == types.InstanceType:
            self.first = self.first.val
            raise "stripping first"
            
        if type(self.last) == types.InstanceType:
            self.last = self.last.val
            raise "stripping last"
        #print "types:::",type(self.first),type(self.last)  
        self.isOrdinal = True
        self.isInteger = True
        self.cBaseOffset = self.first
    def createObject(self,val=None):
        if val == None:
            return M3Objects.M3Integer(self)
        else:
            return M3Objects.M3Integer(self, val)
    def clone(self):
        return M3Objects.M3Integer(self,None)
    def createSubType(self, first, last):
        #print "subtype: first, last", first, last
        return M3IntegerType((first,last))
    def baseType(self):
        return "M3IntegerType"
    def rangeExpr(self):
        if not (self.first or self.last):
            raise "RangeTooBigForArraySubscript"
        last = self.last
        first = self.first
        return range(first,last+1)
    def getFirst(self):
        return self.createObject(self.first)
    def getLast(self):
        return self.createObject(self.last)
    def width(self):
        last = self.last
        first = self.first
        return (last - first) + 1
    def relative(self, val):
        first = self.first
        if type(val) == types.InstanceType: val = val.val                
        return val - first
    def makeval(self, val):
        return val
    def specCoerce(self,cval,allowChoices):
        # This is where we do conversion from scaled images back to values
        # we must deal with cases like "1 volt + 10 mvolt" which will occur in input files
        if type(cval) == types.ListType:
            if self.scaling:
                res = 0
                scaled = False
                for val, factor in cval:
                    for name,mult in self.scaling:
                        if name == factor:
                            res += val * mult
                            scaled = True
                if not scaled:
                    raise "scaling %s not valid for type %s" % (factor, self)
                return self.createObject(res)
            else:
                raise "type %s has no scaling, but you are trying to create a value with %s" % (self, cval)
        if type(cval) == types.IntType:
            return self.createObject(cval)
        else:
            raise "test input coercion error : %s is not an integer" % str(cval)
    def image(self):
        return "INTEGER"
    def makeScaledType(self, scaling):
        return M3IntegerType((self.first,self.last),scaling)
    
M3IntegerBase = M3IntegerType((-(2**127), (2**127)-1))
M3IntegerBase.name = "M3IntegerBase"
M3IntegerBase.predef = True

M3Cardinal = M3IntegerBase.createSubType(0,M3IntegerBase.last)
M3Cardinal.name = "M3Cardinal"
M3Cardinal.predef = True

class M3EnumType(M3Type):
    def __init__(self, values, limits=None, base=None):
        M3Type.__init__(self)
        self.declarer = "VAR" # sneaky cheat because these values are sometimes looked up
        self.values = values
        self.isOrdinal = True
        self.isEnum = True
        self.first, self.last = limits or (values[0],values[-1])
        self.orddict = {}
        for idx,val in enumerate(values):
            self.orddict[val] = idx
        self.firstord = self.orddict[self.first]
        self.lastord = self.orddict[self.last]
        self.cBaseOffset = self.firstord
        self.base = base or self
    def rangeExpr(self): #TBD wont work for subtypes FIX ME !! 
        return self.values
    def width(self):
        return (self.lastord - self.firstord) + 1
    def fits(self,other, obj=None):
        return other.isEnum and (self.base == other.base)  # TBD not M3 type equivalence FIX ME
    def createSubType(self, first, last):
        import types
        if type(first) not in [types.StringType, types.UnicodeType, types.IntType] :
            first = first.val
        if type(last) not in [types.StringType, types.UnicodeType, types.IntType] :            
            last = last.val
        if (first not in self.values) or (last not in self.values):
            err=error("subtype not valid with first %s and last %s for values %s" % (first,last,self.values))
            return M3ErrorType(err)
        return M3EnumType(self.values, (first,last), self.base)
    def createObject(self,val=None):
        return M3Objects.M3Enum(self,val)
    def deref(self, value, obj):
        import LUT
        if value not in self.values:
            res=error("%s not a value for this enum type" % value, obj)
            res=M3ErrorType(res)
        else:
            res=self
        return LUT.LUTEntry(tipe=res,declarer="ENUM") 
    def pyTypeName(self,name,enumvals):
        return "M3Types.M3EnumType('%s',[%s])" % (name,enumvals)
    def derefString(self, right):
        return ".withVal('%s')" % right
    def withVal(self, val):
        return self.createObject(val)
    def clone(self):
        return self.createObject()
    def getVal(self,eltname,obj):
        if eltname not in self.values:
            res=error("Element name %s not in possible values of enumerated type" % eltname, obj)
        return self.withVal(eltname)
    def getFirst(self):
        return self.createObject(self.first)
    def getLast(self):
        return self.createObject(self.last)
    def relative(self,val):
        return self.orddict[val] - self.orddict[self.first]
    def makeval(self, val):
        val = val.val
        if val >= 0 and val <= len(self.values):
            return self.createObject(self.values[val])
        else:
            import M3Predefined
            raise M3Predefined.M3ConstraintError.createObject()
    def specCoerce(self, val,allowChoices):
        if type(val) not in [types.StringType, types.UnicodeType]:
            raise "test input coercion error : %s is not a string (needed by boolean)" % val
        if val not in self.values:
            raise "test input coercion error : %s is not a possible value for this enum" % val
        return self.createObject(val)
    def image(self):
        return "ENUM"
class M3CharType(M3Type):
    def __init__(self,limits=None):
        M3Type.__init__(self)
        self.isOrdinal = True
        self.isChar = True
        if limits:
            self.first, self.last = limits
        else:
            self.first = chr(0)
            self.last = chr(255)
    def createObject(self,val=None):
        return M3Objects.M3Char(self,val)
    def createSubType(self, first, last):
        return M3CharType((first,last))
    def width(self):
        return (ord(self.last) - ord(self.first)) + 1
    def relative(self,val):
        return ord(val) - ord(self.first)
    def clone(self):
        return M3Objects.M3Char(self,None)
    def makeval(self, int):
        if not int.tipe.isInteger:
            raise "Compiler Bug : makeval called with non-integer"
        res = M3Objects.M3Char(self,None)
        res.val = chr(int.val)
        return res
    def getFirst(self):
        return M3Objects.M3Char(self,self.first)
    def getLast(self):
        return M3Objects.M3Char(self,self.last)
    def specCoerce(self, val, allowChoices):
        return self.createObject(self,val)
    def image(self):
        return "CHAR"

M3Char = M3CharType()
M3Char.predef = True
M3Char.name = "M3Char"
class M3BooleanType(M3EnumType):
    # Functionality is all in the object
    # Extra Boolean type defined here to emphasise non-pythonic strictness
    def __init__(self):
        M3EnumType.__init__(self,["FALSE","TRUE"])
        self.isBoolean = True
    def createObject(self,val=None):
        return M3Objects.M3Boolean(val)
    def pyTypeName(self,val):
        return "M3Types.M3Boolean.createObject(%s)" % val
    def image(self):
        return "BOOLEAN"
M3Boolean = M3BooleanType() 
M3Boolean.predef = True



class Field:
    def __init__(self, name, tipe, default, defaultNode = None):
        self.name = name
        self.tipe = tipe
        self.default = default
        self.defaultNode = defaultNode
    def clone(self):
        return Field(self.name,self.tipe,self.default, self.defaultNode)
    def image(self):
        return "%s: %s" % (self.name,self.tipe.image())
    def getTipe(self):
        # makes this conform to the LUTEntry interface
        return self.tipe

class M3RecordType(M3Type):
    def __init__(self, fields=None):
        M3Type.__init__(self)
        self.fielddict = {}
        self.fieldnames = []
        self.isRecord = True
        if fields:
            self.setFields(fields)
    def setFields(self, recfields):
        self.fields = recfields
        for recfield in recfields:
            self.fielddict[recfield.name] = recfield
            self.fieldnames.append(recfield.name)
    def createObject(self,val=None):
        return M3Objects.M3Record(self,val)
    def deref(self, field, obj):
        import LUT
        if field not in self.fielddict:
            res=error("%s not a field of %s" % (field,self.image()),obj)
            res=M3ErrorType(res)
        else:
            res=self.fielddict[field].tipe
        return LUT.LUTEntry(tipe=res,declarer="VAR") # TBD dressing this up as an entry is strange but helps the general case
    def derefString(self, right):
        return ".getField('%s')" % right
    def clone(self):
        return self.createObject()
    def checkConstructor(self, actuals, obj):
        procRecCheck(self.fields,actuals,obj,strict=False)
    def construct(self, *posargs, **kwargs):
        res = M3Objects.M3Record(self,None)
        for lhs,rhs in zip(self.fieldnames,posargs):
            res.val[lhs].assign(rhs)
        for name,val in kwargs.items():
            res.val[name].assign(val)
        return res  
    def fits(self, other, obj=None):
        if other == M3RefAny: return True
        return (self == other) # TBD structural equivalence
    def image(self):
        return "RECORD {%s}" % string.join([field.image() for field in self.fields],", ")
    def specCoerce(self, rawValues, allowChoices):
        if type(rawValues) != types.DictType:
            raise "test input coercion error : %s cannot be a record" % str(rawValues)
        res = M3Objects.M3Record(self,None)
        for k,v in rawValues.items():
            if k not in self.fieldnames:
                raise "test input coercion error : field %s not present in record" % k
            res.val[k] = self.fielddict[k].tipe.coerce(v,allowChoices)
        return res
    def offsetForFieldName(self,fieldName):
        for ctr,field in enumerate(self.fields):
            if field.name == fieldName:
                return ctr
        raise "compiler bug"
class M3VariantRecordType(M3RecordType):
    def __init__(self):
        M3Type.__init__(self)
        self.isRecord = True
        self.casectr = 0
        self.fielddict = {}
        self.caselist = []
        self.elselist = []
        self.staticlist = []
        self.checked = False
    def fieldWithName(self,fields,name):
        for field in fields:
            if field['name'] == name:
                return field
        return None
    def setTag(self,tagfield):
        self.tagname = tagfield.name
        self.fielddict[tagfield.name] = tagfield
    def checkConstructor(self,actuals,obj):
        if not actuals[0]['name']:
            tag = actuals[0]
        else:
            tag = self.fieldWithName(actuals,self.tagname)
        if (not tag) and self.fielddict[self.tagname].default:
            tag = {'val': self.fielddict[self.tagname].default}
        if not tag: 
            error("tag field not present in constructor for variant record", obj)
        elif not tag['val']:
            error("tag field value is not statically determinable in constructor for variant record", obj)
        else:
            fieldnames = self.getValidFieldNames(tag['val'].ord().val)
            fieldsInOrder = []
            for fieldname in fieldnames:
                fieldsInOrder.append(self.fielddict[fieldname])
        if not self.checked:
            procRecCheck(fieldsInOrder,actuals,obj,strict=False)
            self.checked = True

    def construct(self, *posargs, **kwargs):
        res = M3Objects.M3VariantRecord(self,None)
        if posargs:
            tag = posargs[0]
        elif self.tagname in kwargs:
            tag = kwargs[self.tagname]
        else:
            tag = self.fielddict[self.tagname].default
            
        fieldnames = self.getValidFieldNames(tag.ord().val)
        for lhs,rhs in zip(fieldnames,posargs):
            res.val[lhs].assign(rhs)
        for name,val in kwargs.items():
            res.val[name].assign(val)
        return res  

    def addFields(self,fields,obj):
        for field in fields:
            if field.name in self.fielddict:
                error("field %s present twice in variant record" % field.name, obj)
            else:
                self.fielddict[field.name] = field
    def setCaseFields(self,cases,fields,obj):
        self.addFields(fields,obj)
        self.caselist.append((cases,[field.name for field in fields]))
    def setElseFields(self,fields,obj):
        self.addFields(fields,obj)        
        self.elselist = [field.name for field in fields]
    def setStaticFields(self,fields,obj):
        self.addFields(fields,obj)
        self.staticlist = [field.name for field in fields]
    def createObject(self,val=None):
        return M3Objects.M3VariantRecord(self,val)
    def getValidFieldNames(self,tagval):
        #import pdb; pdb.set_trace()
        validFields = None
        for cases,fields in self.caselist:
            for elt in cases:
                if type(elt) == types.TupleType:
                    min,max = elt
                    if (tagval <= max) and (tagval >= min):
                        validFields = fields
                        break
                elif tagval == elt:
                    validFields = fields
                    break
        if validFields == None: # Warning, empty cases return [], so differentiate
            validFields = self.elselist
        validFields = [self.tagname] + validFields + self.staticlist
        return validFields
    def specCoerce(self, rawValues, allowChoices):
        if type(rawValues) != types.DictType:
            raise "test input coercion error : %s cannot be a record" % str(rawValues)
        if self.tagname not in rawValues:
            raise "bad variant value : tag field %s missing" % self.tagname
        tag = self.fielddict[self.tagname].tipe.coerce(rawValues[self.tagname])
        fieldnames = self.getValidFieldNames(tag.ord().val)        
        res = M3Objects.M3Record(self,None)
        for k,v in rawValues.items():
            if k not in fieldnames:
                raise "test input coercion error : field %s not present in record" % k
            res.val[k] = self.fielddict[k].tipe.coerce(v,allowChoices)
        return res


    def image(self):
        return "VARIANT RECORD" # {%s}" % string.join([field.image() for field in self.fields],", ")
                    
                    
class M3ArrayType(M3Type):
    def __init__(self,elementType=None,indices=None):      
        M3Type.__init__(self)       
        self.isArray = True
        if elementType:
            self.setStructure(elementType,indices)
    def setStructure(self,elementType,indices):
        if len(indices) == 0:
            self.isOpen = True
            self.indexType = None
            self.elementType = elementType
        else:
            self.indexType = indices[0]
            if len(indices) == 1:
                self.elementType = elementType
            else:
                self.elementType = M3ArrayType(elementType,indices[1:])
        
    def fits(self, other, obj=None):
        # TBD : currently one fits fits all uses for arrays, but is there a difference between param checking and assignment ?
        # TBD Structural equivalence probably means that you have to abandon the index type of the original
        if not other.isArray:
            return False
        if not self.elementType.fits(other.elementType):
            return False
        if self.isOpen:
#            print "an open arrays alway fits"
            return True
        if (not self.isOpen) and (not other.isOpen):
            return self.length() == other.length()
#            return (self.getFirst().val == other.getFirst().val) and (self.getLast().val == other.getLast().val)
        return True
    def getFirst(self):
        return self.indexType.getFirst()
    def getLast(self):
        return self.indexType.getLast()
    def getNumber(self):
        return M3IntegerBase.createObject(self.length())
    def createObject(self,val=None):
        return M3Objects.M3Array(self,val)
    def deref(self, subscript, obj=None):
        import LUT
        if type(subscript) != types.InstanceType:
            error("Bad array access", obj)  
        elif (not subscript.isError) and (not self.isOpen) and (not subscript.fits(self.indexType)):
            error("Type clash in array subscript, expected: %s given: %s " % (self.indexType, subscript), obj)
        return LUT.LUTEntry(tipe=self.elementType,declarer="VAR")
    def checkConstructor(self, actuals, obj):
        for act in actuals:
            if act != "DOTDOT":
                if not self.elementType.fits(act["tipe"]):
                    error("Type clash in array constructor element", obj)
    def construct(self, *elts):
        #print "construct"
        #import pdb; pdb.set_trace()
        if self.isOpen:
            # we must copy this open array type so we can fix the boundaries in the copy without wrecking them in
            # the original open type which may be used later for further declarations
            closedArray = M3ArrayType(self.elementType, [])
            newArray = M3Objects.M3Array(closedArray,None)
        else:
            closedArray = self
        newArray = M3Objects.M3Array(closedArray,None)
        if elts[-1] == "DOTDOT":
            duperest = True
            elts = elts[:-1]
            lastelt = elts[-1]
        else:
            duperest = False
        if closedArray.isOpen:
            closedArray.indexType = M3IntegerBase.createSubType(0,len(elts) -1)
            newArray.val = [None] * closedArray.length()
        if len(elts) > closedArray.length():
            raise "TooManyElementsInArrayConstructor"
        for eltoffset, arrindex in enumerate(closedArray.indexRange()):
            if eltoffset > (len(elts)-1):
                if duperest:
                    newArray.getElement(eltoffset).assign(lastelt)
                else:
                    raise "NotEnoughElements"
            elif elts[eltoffset].isChoice:
                newArray.pokeElt(eltoffset, elts[eltoffset]) # Choices are more brutal
            else:
                #print "assigning in constructor"
                elt = newArray.getElement(eltoffset)
                #print "elt, elt.val", elt, elt.val
                elt.assign(elts[eltoffset])
        return newArray
    def indexRange(self):
        return self.indexType.rangeExpr()
    def length(self):
        if self.indexType:
            return self.indexType.width() # TBD This is a inefficient for large arrays
        else:
            return None
    def clone(self):
        return self.createObject()
    def close(self, lengths):
        # A run time operation used by NEW to close a (potentially multidimensional) array
        if not self.isOpen: raise "compiler bug : close on an already closed array"
        if len(lengths) > 1:
            if not self.elementType.isArray:
                raise "compiler bug : too many dimensions in NEW to close array"
            newEltType = self.elementType.close(lengths[1:])
        else:
            newEltType = self.elementType
        closedArray = M3ArrayType(newEltType, [M3IntegerBase.createSubType(0,lengths[0]-1)])
#        closedArray.indexType = M3IntegerBase.createSubType(0,lengths[0])
        return closedArray
    #    Code generation
    def specCoerce(self, rawValues,allowChoices):
        if type(rawValues) != types.ListType:
            raise "test input coercion error : %s cannot be an array" % str(rawValues) 
        halfCooked = [self.elementType.coerce(rawValue,allowChoices) for rawValue in rawValues]
        return self.construct(*halfCooked)
    def image(self):
        return "ARRAY"
class M3SubArrayType(M3Type):
    def __init__(self, arrayBaseType):
        M3Type.__init__(self)
        self.isOpen = True # TBD maybe one day we can use constant evaluation here
        self.isArray = True
        self.isSubArray = True
        self.arrayBaseType = arrayBaseType
        self.elementType = arrayBaseType.elementType
    def createObject(self, arrayBase, start, length):
        return M3Objects.M3SubArray(self, arrayBase, start, length)
    def fits(self, other):
        return self.elementType.fits(other.elementType)
    def deref(self, subscript, obj=None):
        return self.arrayBaseType.deref(subscript,obj)
    def image(self):
        return "SUBARRAY"

def procRecCheck(formals,actuals,obj,strict):
    res = True
#    print "formals: "
#    for f in formals:
#        print f.image()
#    print "actuals ",actuals
    if formals == []:
        if actuals == []:
            return res
        else:
            error("zero length formal list may not take actuals", obj)
    # This is where we do matching of (procedure|record constructor) formal and actual parameters
    # formals is the dict from the LUT (so we need to dereference it)
    # actuals is a list of types
    afterAnon = False
    names = [formal.name for formal in formals]
    for actual in actuals:
        if actual["name"]:
            afterAnon = True
        if afterAnon and not actual["name"]:
            error("illegal use of anonymous after named parameters", obj)
            res=False
    # Product is a copy of the formals list into which we write the results of our parameter check
    product = []
    for formal in formals: product.append(formal.clone())
    erledigt = {} # This is the list of parameters which have been written
    # Now assign the anonymous actuals
    if len(actuals) > len(product):
        error("Too many actual parameters", obj)
    for actual,prod in zip(actuals,product):
        if actual["name"]: break
        if not prod.getTipe().fits(actual["tipe"],obj):
            #raise "hell"
            error("parameter type mismatch between %s and %s" %(prod.getTipe(),actual["tipe"]), obj, code="003")
            #import pdb; pdb.set_trace()
            res = False
        else:
            erledigt[prod.name] = True
            prod.val = actual["val"]
    # Now do the keyword ones
    for actual in actuals:
        for prod in product:
            if actual["name"]:
                if (actual["name"] == prod.name):
                    if not prod.getTipe().fits(actual["tipe"]):
                        error("parameter type mismatch between %s and %s" %(prod.getTipe(),actual["tipe"]), obj)
                        #import pdb; pdb.set_trace()
                        res = False
                    elif prod.name in erledigt.keys():
                        error("clash between positional and named element %s" % prod.name, obj)
                        res = False
                    else:
                        prod.val = actual["val"]
                    erledigt[prod.name] = True
                elif actual["name"] not in names:
                    error("name %s is not a formal" % actual["name"], obj)
                    #import pdb; pdb.set_trace()
                    res = False
    # Finally check that no-one has been left out
    # First add the ones which were preinitialised, so use the pristine formals list for that
    for formal in formals:
        if formal.default:
            erledigt[formal.name] = True
    for prod in product:
        if (prod.name not in erledigt) and strict: # records are not strict on this
            error("parameter %s omitted in actual list" % prod.name, obj)
            res = False
    return res

class M3PredefProcedureType(M3Type):
    def __init__(self,name,compileAction,valueAction=None):
        M3Type.__init__(self)
        self.name = name
        self.isProcedure = True
        self.predef = True
        self.compileAction = compileAction
        self.valueAction = valueAction

    def deref(self, actuals, obj):
        # No fancy parameter checking for the predefineds
        return self.compileAction(actuals, obj)
    def derefVal(self, sel=None):
        if not self.valueAction:
            raise "No value for ", self
        return self.valueAction(sel)
class M3ProcedureHolder:
    def __init__(self,fun):
        self.fun = fun
    def __call__(self, *args, **kwargs):
        return self.fun(*args, **kwargs)
class M3ProcedureHolderType:
    def createObject(self, fun):
        return M3ProcedureHolder(fun)
    

class M3ProcedureType(M3Type):
#    def __setattr__(self,name,value):
#        if name == "returnval":
#            name = value.__class__.__name__
#            print "set returnval", name
#            if name == "M3Type": raise "hell"
#        self.__dict__[name] = value
    def getTipe(self,dummy):
        return self
    def __init__(self,formals=None,returnval=None,raises=None,node=None):
        M3Type.__init__(self)
        self.formals = formals
        self.returnval = returnval
        self.raises = raises
        self.isProcedure = True
        self.node = node
        self.isMessageHandler = False
    def conjugate(self):
        c = M3ProcedureType(self.formals,self.returnval,self.raises,self.node)
        c.dir = {"INCOMING": "OUTGOING", "OUTGOING": "INCOMING"}[self.dir]
        c.isMessageHandler = self.isMessageHandler
        c.name = self.name
        c.synch = self.synch
        return c
    def prependTargetObject(self, target): # TBD kludgy procedure massaging to satisfy direct calls on methods from types
        import LUT
        newformals = [LUT.LUTEntry(tipe=target, name="_")] + self.formals
        return M3ProcedureType(newformals, self.returnval, self.raises, None)
    def deref(self, actuals, obj):
        if self.isMessageHandler:
            formals = self.formals[1:]
        else:
            formals = self.formals
        res = procRecCheck(formals,actuals,obj,strict=True)
        if res:
            return self.returnval
        else:
            return M3ErrorType("parameter error")
    def image(self):
        return "Procedure %s " % self.name
    def checkMatch(self, other, obj, ignoreFirstFormal=False):
        # Checks two signatures against each other
        # We check that the names, types and modes are equal, we do NOT check default values !!!! TBD
        otherformals = other.formals
        #print other.isMessageHandler, self.isMessageHandler
        #print other.formals, self.formals
        if ignoreFirstFormal:
            # trim the object parameter from the front
            if not len(otherformals):
                error("Method candidate must have at least one parameter", obj)
                return False
            otherformals = otherformals[1:]
        if (len(self.formals) != len(otherformals)):
            #print self, self.formals, other, otherformals
            error ("Parameter count mismatch between %s and %s" % (self.name, other.name), obj)
            #import pdb; pdb.set_trace()
            return False
        for p1,p2 in zip(self.formals, otherformals):
            #print "p1, p2", p1.image(), p2.image(), p1.getTipe(), p2.getTipe()
            if not p1.getTipe().fits(p2.getTipe()):
                error ("Parameter type mismatch btw spec (%s) and body (%s)" % (p1.getTipe(), p2.getTipe()), obj, code="003")
                #import pdb; pdb.set_trace()
                return False                
            if p1.name != p2.name:
                import pdb; pdb.set_trace()
                error ("Name mismatch between parameters '%s' and '%s'" % (p1.name, p2.name), obj)
                return False
            if p1.mode != p2.mode:
                error ("Mode mismatch between '%s'(%s) and '%s'(%s)" % (p1.name, p1.mode, p2.name, p2.mode), obj)
                return False
        # and now check that the raises fit
        if len(self.raises) != len(other.raises):
            error ("Raise count mismatch btw spec and body", obj)
            return False
        for r1, r2 in zip(self.raises, other.raises):
            if r1 != r2:
                error ("Raise list mismatch btw spec and body", obj)
                return False
        if not (other.returnval.fits(self.returnval) or self.returnval.fits(other.returnval)):
            print self.returnval.image(), other.returnval.image()
            
            #print dir(self), dir(other)
            error ("Return value mismatch btw spec and body", obj)
            return False
        return True
    def flush(self):
        # Forces an eventual check of what may not be done with the lazy type evaluation scheme
        for formal in self.formals:
            tmp = formal.getTipe()
    def offsetForParamName(self,id):
        for ctr,formal in enumerate(self.formals):
            if formal.name == id.idname:
                return ctr
        raise "compiler bug"
class M3InternalActivityType(M3Type):
    def __init__(self):
        M3Type.__init__(self)
        
class M3RefType(M3Type):
    def __init__(self,referent):
        M3Type.__init__(self)
        self.referent = referent
        self.isRef = True
        # Deal with recursive declarations see above in M3RecordType for current restrictions
    def setReferent(self, referent):
        if self.referent:
            raise "compiler bug : referent already exists"
        self.referent = referent

    def createObject(self):
        return M3Objects.M3Ref(self)
    def fits(self, other,obj=None):
        import M3Predefined 
        if not other: error("other is null", obj)
        #print "fitting refs: ", self, other
        res = other.isRef and (other.isNull or
                                self.isNull or
                                self.referent.fits(other.referent))
        if not res:
            print "ref fit failed",self,other,M3Null #OK
        return res
    def fitsTCase(self, candidates):
        for candidate in candidates:
            if candidate.isRef and self.referent.fits(candidate.referent):
                return True
        return False
    def clone(self):
        return self.createObject()
    def deref(self, fieldOrIndex, obj=None):
        # This is called on implicit doubledereference (explicit single dereference is done in CaretUser)
        import LUT
        obj.getEnclosingExpr().addDeref(obj.refid) 
        if not self.referent:        # TBD this shouldn't happen - some wierdness with refany
            return LUT.LUTEntry(tipe=M3ErrorType(error("Reference has no referent", obj)))
        elif self.referent.isRecord:
            #print "deref rec ", fieldOrIndex
            res = self.referent.deref(fieldOrIndex, obj)
            #print "res of deref rec", res
            #print self.referent.image()
            return res
        elif self.referent.isArray:
            return self.referent.deref(fieldOrIndex, obj)
        else:
            err = error("referent is not an array or a record", obj)
            return LUT.LUTEntry(tipe=M3ErrorType(err))
        
    # ---- CODE Generation stuff     
    def derefString(self,right):
        return ".getRef().getField('%s')" % right
    def image(self):
        return "REF %s" % self.referent.image()

class DummyReferent(M3Type): pass


M3RefAny = M3RefType(DummyReferent())
def fitsanything(self, x=None): return True
M3RefAny.fits = fitsanything
#print "any, referent", M3RefAny, M3RefAny.referent


class M3ErrorType(M3Type):      # These are created on the fly to control semantic error propagation
    def __init__(self,name):
        M3Type.__init__(self)
        self.name=name
        self.isError = True
    def deref(self, field=None, obj=None):
        import LUT
        return LUT.LUTEntry(tipe=self)
    def image(self):
        return "ERROR"
 
class M3ExceptionType(M3Type):  # This is the mapping for Exceptions raised by and declared in Modula3
    def __init__(self,name,tipe=None):
        M3Type.__init__(self)
        self.tipe = tipe
        self.name = name
    def createObject(self, val=None):
        return M3Objects.M3Exception(self,val)
    def image(self):
        return "EXCEPTION"
class M3ExitException:
    "used internally to implement exit from loops"

class M3ProcedureNullReturnType(M3Type):
    def fits(self,other):
        return (self == other) or (other == M3SynchNullReturn)
M3ProcedureNullReturn = M3ProcedureNullReturnType()

class M3MessageNullReturnType(M3Type): pass
M3MessageNullReturn = M3MessageNullReturnType()

class M3SynchNullReturnType(M3Type):
    def fits(self,other):
        return (self == other) or (other == M3ProcedureNullReturn)

M3SynchNullReturn = M3SynchNullReturnType()

class M3ObjectType(M3Type):
    def __init__(self, swper, fields, methods, overrides, stamp):
        M3Type.__init__(self)
        self.setup(swper, fields, methods, overrides)
        self.stamp = stamp
    def getField(self, methodName):  # This is only used for calls direct to the type at run time
        res = self.fielddict[methodName].default
        if not res:
            raise M3Predefined.M3ConstraintError.createObject()
        if not type(res) == types.StringType:
            raise "compiler bug : bad method stamp"
        return M3ProcLib.lookup(res)
    def getFieldNewCheck(self, name):
        if name in self.fieldnames:
            return self.fielddict[name]
        if self.swper:
            return self.swper.getFieldNewCheck(name)
        return False
    def setup(self, swper, fields, methods, overrides):
        self.isObject = True        
        self.swper = swper
        self.fields = fields
        self.fielddict = {}
        self.fieldnames = []
        if not fields: fields = []
        for field in fields:
            if field.name in self.fieldnames:
                error("Duplicate field name %s" % field.name, obj)
            else:
                self.fielddict[field.name] = field
                self.fieldnames.append(field.name)
        # methods are added to the fields
        if not methods: methods = []
        for method in methods:
            if method.name in self.fieldnames:
                error("Duplicate field name %s" % field.name, obj)
            else:
                self.fielddict[method.name] = method
                self.fieldnames.append(method.name)
        self.methods = methods
        self.overrides = overrides
    def setSwper(self,swper):
        self.swper = swper
        return self
    def findMethod(self,name):
        if name not in self.fieldnames:
            if not self.swper:
                return False
            else:
                res = self.swper.findMethod(name)
        else:
            res = self.fielddict[name]
        return res
    def setFields(self,fields):
        if not fields: return self
        for field in fields:
            if field.name in self.fieldnames:
                error("Duplicate field name %s" % field.name, obj)
            else:
                self.fielddict[field.name] = field
                self.fieldnames.append(field.name)
        return self
    def setMethods(self,methods,obj):
        #error("calling setmethods",obj)
        if not methods: return self
        for method in methods:
            #print "method", method
            #print "fieldnames", self.fieldnames
            if method.name in self.fieldnames:
                error("Duplicate method name %s" % method.name,obj)
            else:
                self.fielddict[method.name] = method
                self.fieldnames.append(method.name)
        self.methods = methods
        return self
    def checkOverride(self, name, proc, obj):
        # TBD check that the field exists in the superclass, is a function and matches
        meth = self.findMethod(name)
        if not meth:
            error("No method available for override of %s" % name, obj)
        else:
            meth = meth.getTipe()
            if proc.formals[0].getTipe() not in self.swperList():
                error("First parameter of overriding procedure for %s is not identical to or supertype of target object" % name, obj)
            meth.checkMatch(proc, obj, ignoreFirstFormal=True)
    def setOverrides(self,overrides,obj=None):
        #print "setting overrides", overrides
        self.overrides = overrides
        if not overrides: return 
        if not obj: return
        # these are compiletime checks only (is this sharing healthy?)
        names = []
        for override in overrides:
            #print override.image()
            if override.name in names:
                error("Override %s defined twice" % override.name,obj)
            names.append(override.name)
            self.checkOverride(override.name, override.getTipe(), obj)
        return self
    def image(self):
        return "Object with fields [%s]" % string.join(self.fieldnames,",")

    def fits(self, other, obj=None):
        #print "object fit test btw %s and %s " % (self, other)
        if self == other: return True
        if other == M3RefAny:
            return True # Flickwerk !!!
        if not other.isObject: return False
        # check that one is at least in the type hierarchy of the other : this will need a NARROW at runtime 
        if self in other.swperList():
            return True
        if other in self.swperList():
            return True
        if other.isNull or self.isNull:
            return True
        if (other == M3Root) or (self == M3Root): # TBD this is papering over a nasty hole in partial revelation FIXME
            return True
        return False
    def fitsTCase(self, candidates):
        for candidate in candidates:
            if candidate.isObject and (candidate in self.swperList()):
                return True
        return False
    def swperList(self):
        if not self.swper:
            return [self]
        else:
            return [self] + self.swper.swperList()
    def createObject(self,val=M3Objects.NullInstance()):
        newobj = M3Objects.M3Object(self)
        newobj.val = val 
        return newobj
    def clone(self):
        res = self.createObject()
        res.new()
        return res
    def deref(self, name, obj, declarer):
        import LUT
        if declarer == "VAR":
            if name in self.fieldnames:
                res = self.fielddict[name].getTipe()
            elif self.swper:
                return self.swper.deref(name, obj, declarer)
            else:
                res = M3ErrorType(error("field %s does not exist in object" % name, obj))
        elif declarer == "TYPE":
            if name in self.fieldnames:
                res = self.fielddict[name].getTipe()
                if not res.isProcedure:
                    res = M3ErrorType(error("field %s does not contain a method in object type" % name, obj))
                else: res = res.prependTargetObject(self)
            else:
                res = M3ErrorType(error("field %s does not exist in object type" % name, obj))
        else:
            raise "Compiler bug : invalid declarer in object type dereference : %s" % declarer
        return LUT.LUTEntry(tipe=res)
    def derefString(self, right):
        return ".getField('%s')" % right
        
M3Root = M3ObjectType(None, [], [], [], "ROOTSTAMP")

class M3SetType(M3Type):
    def __init__(self, rangeType):
        M3Type.__init__(self)
        self.rangeType = rangeType
        self.isSet = True
    def createObject(self, val=None):
        return M3Objects.M3Set(self,val)
    def clone(self):
        return M3Objects.M3Set(self)
    def checkConstructor(self,actuals,node):
        res = True
        for actual in actuals:
            #print "actual",actual
            if type(actual) == types.TupleType:
                start, end = actual
                if not (self.rangeType.fits(start) and self.rangeType.fits(end)):
                    res = False
            else:
                if not self.rangeType.fits(actual):
                    res = False
        if not res:
            error("Type error in set constructor", node)
                        
    def construct(self, *elts):
        newSet = M3Objects.M3Set(self)
        for elt in elts:
            if type(elt) == types.TupleType:
                newSet.addRange(elt)
            else:
                newSet.addMember(elt)
        return newSet
        # elements are either single or range tuples
    def specCoerce(self, rawValues,allowChoices):
        if type(rawValues) != types.ListType:
            raise "test input coercion error : %s cannot be a set" % str(rawValues) 
        halfCooked = [self.rangeType.coerce(rawValue) for rawValue in rawValues]
        return self.construct(*halfCooked)
    def image(self):
        return "SET OF %s" % self.rangeType.image()
class M3NullType(M3Type):
    def __init__(self):
        M3Type.__init__(self)
        self.isNull = True
        self.isRef = True
        self.isObject = True
    def swperList(self):
        return []
    def createObject(self):
        return M3Objects.M3Nil
    def fits(self, other):
        return other.isRef or other.isObject
    def fitsTCase(self, candidates):
        return True
    def image(self):
        return "NULL"
M3Null = M3NullType()
M3Objects.M3Nil.tipe = M3Null # this is a special hack for NIL/NULL
M3Null.referent = M3Null

class M3PortType(M3Type):
    def __init__(self, node, name, protocol):
        M3Type.__init__(self)
        self.isPort = True
        self.node = node
        self.name = name
        self.protocol = protocol
    def deref(self,field,obj):
        import LUT
        for m in self.protocol.messages:
            if m.name == field:
                return LUT.LUTEntry(tipe=m,declarer="VAR")
        err = error("Port %s has no message %s" % (self.name, field), obj)
        return LUT.LUTEntry(tipe=M3ErrorType(err),declarer="VAR") # so that the later phases dont burp
    def derefString(self, right):
        return ".%s" % right
    def getMessagesFor(self,otherPort, connectionType):
        #print connectionType
        mydict = {}
        for message in self.protocol.messages:
            mydict[str(message.name)] = message
        otherdict = {}
        for message in otherPort.protocol.messages:
            otherdict[str(message.name)] = message
        res = []
        dirMap = {"across": ("OUTGOING", "INCOMING"), "down": ("OUTGOING", "OUTGOING"), "up": ("INCOMING", "INCOMING")}
        mydir, hisdir = dirMap[connectionType]
        for name in [key for key in mydict.keys() if key in otherdict.keys()]:            
            if (mydict[name].dir == mydir) and (otherdict[name].dir == hisdir):
                res.append(name)
        #print res
        return res
    def getSynchFor(self,otherPort):
        # TBD this is a bad temporary implementation, you should refactor and use the logic from getMessagesFor
        synch = True
        for message in self.protocol.messages:
            if not message.synch: synch = False
        for message in otherPort.protocol.messages:
            if not message.synch: synch = False
        return synch
            
class MessageDictEntry:
    # for checking usage of messages in capsule body
    def __init__(self,type):
        self.type = type
        self.user = None
        self.stateNames = []
        self.generated = False
    def setActivity(self,node):
        if self.user:
            error("Activity must have exclusive use of message %s" % self.type.name, node)
        else:
            self.user="ACTIVITY"
    def setTransition(self,stateName,node):
        if self.user and self.user != "TRANSITION":
            error("State transition name %s already used for %s" % (self.type.name, self.user), node)
        else:
            self.user="TRANSITION"
        if stateName in self.stateNames:
            error("Transition already exists for message %s in state %s" % (self.type.name, stateName), node)
        else:
            self.stateNames.append(stateName)
class M3CapsuleBodyType(M3Type):
    # We assume that all messages receivable by a capsule are separate
    def __init__(self,spec):
        M3Type.__init__(self)        
        self.isCapsuleBody = True
        self.spec = spec
        self.internalDict = {}
    def createObject(self):
        return M3Objects.M3CapsuleBody(self)
    def deref(self,name,obj):
        self.spec.deref(name,obj)
    def derefString(self,right):
        return ".%s" % right
    def getPortOfMessage(self,messageName):
        return self.spec.getPortOfMessage(messageName)
    def image(self):
        return "CAPSULE BODY"
class M3CapsuleSpecType(M3Type):
    def __init__(self,node,ports):
        M3Type.__init__(self)
        self.node = node
        self.isCapsuleSpec = True
        self.ports = ports
        self.uniqueMessages=[]
        self.uniqueMessagePorts={}
        self.portDict = {}
        messageDict = {}
        for port in ports:
            self.portDict[port.name] = port
            if not port.protocol.isProtocol:
                error("Port %s does not have protocol type" % port.name, port.node)
                port.protocol.messages = [] # patch this up to simplify later checking 
                return
            for message in port.protocol.messages:
                name = message.name
                if name not in messageDict: messageDict[name] = 0
                messageDict[name] += 1
        for messageName in messageDict:
            if messageDict[messageName] == 1:
                self.uniqueMessages.append(messageName)
                self.uniqueMessagePorts[str(messageName)] = "%s.%s" % (str(self.getPortOfMessage(messageName).name), str(messageName))

        self.inDict = {}
        self.outDict = {}
        self.messDict = {}
        for port in self.ports:
            for message in port.protocol.messages:
                t = message
                entry = MessageDictEntry(t)
                self.messDict[t.name] = entry
                if t.dir == "INCOMING":
                    self.inDict["%s.%s" % (port.name,t.name)] = entry
                elif t.dir == "OUTGOING":
                    self.outDict["%s.%s" % (port.name,t.name)] = entry
                else:
                    raise "compiler bug :strange direction"
                
    def getPortOfMessage(self,messageName):
        #print "getPortOfMessage", messageName
        if messageName not in self.uniqueMessages:
            print messageName, " not unique"
            return None
        for port in self.ports:
            for message in port.protocol.messages:
                if message.name == messageName:
                    #print "getPortOfMessage", messageName, port
                    return port
        #print "getPortOfMessage", None                
        return None
    def isUnique(self,name):
        return name in self.uniqueMessages
    def image(self):
        return "CAPSULE SPEC"
    def deref(self,name,obj):
        # This copes with statements of the both types: SEND port.message and SEND message (with implicit port)
        import LUT        
        found = False
        if name in self.messDict and self.isUnique(name): 
            res = self.messDict[name].type
        elif name in self.portDict:
            res = self.portDict[name]
        else:
            res = M3ErrorType(error("No incoming message %s in capsule" % name, obj))
        return LUT.LUTEntry(tipe=res)
        
class PredefCapsule:
    "Common functionality for Triggers and Timers"
    def __init__(self):
        self.target = False
    def connect(self,srcMsg,destMsg,destObj):
        # srcMsg is a dummy to make generation logic easier
        if self.target:
            raise "Timer/Trigger already connected"
        self.target = (destMsg,destObj)
    def send(self):
        destMsg,destObject = self.target
        destObj.send(self, destMsg)
        
class M3TriggerType(M3Type,PredefCapsule):
    def __init__(self):
        M3Type.__init__(self)
        PredefCapsule.__init__(self)
        self.isTrigger = True

class M3TimerType(M3Type,PredefCapsule):
    def __init__(self):
        M3Type.__init__(self)
        PredefCapsule.__init__(self)        
        self.isTimer = True
    def image(self):
        return "TIMER"


class M3ListType(M3Type):
    def __init__(self, elementType):
        M3Type.__init__(self)
        self.isList = True
        self.elementType = elementType
    def construct(self, *vals):
        vals = list(vals) # this comes in as a tuple
        return self.createObject(vals)
    def createObject(self,val=None):
        return M3Objects.M3List(self,val)        
    def deref(self, index, obj):
        import LUT
        if not index.isInteger:
            error("List index must be of integer type", obj)
        return LUT.LUTEntry(tipe=self.elementType)
    def image(self):
        return "LIST OF %s" % self.elementType.image()
    def checkConstructor(self, actuals, obj):
        for actual in actuals:
            if not actual["tipe"].fits(self.elementType):
                error("%s cannot accept %s in constructor" % (self.image(), actual["tipe"].image()), obj)
                return 
    def specCoerce(self, rawValues,allowChoices):
        if type(rawValues) != types.ListType:
            raise "test input coercion error : %s cannot be a LIST" % str(rawValues) 
        halfCooked = [self.elementType.coerce(rawValue,allowChoices) for rawValue in rawValues]
        return self.construct(*halfCooked)
    def clone(self):
        return self.createObject()

M3TextListType = M3ListType(M3Text) 

class M3DictType(M3Type):
    def __init__(self, indexType, elementType):
        M3Type.__init__(self)
        self.isDict = True
        self.elementType = elementType
        self.indexType = indexType
    def construct(self, vals):
        #print "construct", vals
        return self.createObject(vals)        
    def createObject(self,val=None):
        return M3Objects.M3Dict(self,val)        
    def deref(self, index, obj):
        import LUT
        if not index.fits(self.indexType):
            error("DICT index expected %s and given %s" % (self.indexType, index), obj)
        return LUT.LUTEntry(tipe=self.elementType)
    def image(self):
        return "DICT OF %s" % self.elementType.image()
    def checkConstructor(self, actuals, obj):
        for actual in actuals:
            if not actual["tipe"].fits(self.elementType):
                error("%s cannot accept %s in constructor" % (self.image(), actual["tipe"].image()), obj)
                return 
    def specCoerce(self, rawValues, allowChoices):
        if type(rawValues) != types.DictType:
            raise "test input coercion error : %s cannot be a DICT" % str(rawValues)
        res = {}        
        for k,v in rawValues.items():
            res[k] = self.elementType.coerce(v, allowChoices)
        return self.construct(res)
    def clone(self):
        return self.createObject()


class M3ProtocolType(M3Type):
    def __init__(self,messages):
        M3Type.__init__(self)
        self.isProtocol = True
        self.messages = messages
    def fits(self,other,obj=None):
        if other.isPort:
            return self.fits(other.protocol,obj)
        else:
            return M3Type.fits(self,other)
    def deref(self,field,obj):
        import LUT
        for m in self.messages:
            if m.name == field:
                return LUT.LUTEntry(tipe=m,declarer="VAR")
        err = error("Protocol has no message %s" % (self.name, field), obj)
        return LUT.LUTEntry(tipe=M3ErrorType(err),declarer="VAR") # so that the later phases dont burp
        
    def conjugate(self):
        return M3ProtocolType([message.conjugate() for message in self.messages])
    def getMessageWithName(self,name,messages):
        for message in messages:
            if message.name == name:
                return message
        raise "no message with name %s" % name
    def aggregate(self, other, node):
        mynames = [message.name for message in self.messages]
        othernames = [message.name for message in other.messages]
        myUnique = []
        for name in mynames:
            if name in othernames:
                if not self.getMessageWithName(name,self.messages).fits(self.getMessageWithName(name,other.messages)):
                    error("conflicting message %s on both sides of a protocol aggregation" % name, node)
                    return self
            else:
                myUnique.append(self.getMessageWithName(name,self.messages))
        return M3ProtocolType(myUnique + other.messages)
    def derefString(self,right):
        return ".%s" % right
