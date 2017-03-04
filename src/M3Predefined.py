import types
import M3Types
import M3Objects
from Message import error

# --------------- NEW ------------------
# Run Time
def M3RefNEW(refType, *dims, **fields):
    import M3Objects

    if refType.isObject:
        ref = refType.createObject()
        ref.new()
        #print fields
        for name, value in fields.items():
            #print "Value", value
            if type(value) == types.FunctionType:
                ref.overrides[name] = M3Objects.M3MethodWrapper(value,ref)
            else:
                ref.getField(name).assign(value)
    elif len(dims):
        if not refType.referent.isArray:
            raise "compiler bug : New called on nonarray with unnamed params"
        # create a copy of the reference type so that we leave the original with an open arrar
        newRefType = M3Types.M3RefType(refType.referent)
        newRefType.referent = newRefType.referent.close([dim.val for dim in dims])
        ref = newRefType.createObject()
        ref.new()
    elif len(fields):
        if not refType.referent.isRecord:
            raise "compiler bug : New called on nonrecord with named params"
        ref = refType.createObject()
        ref.new()
        for k,v in fields.items():
            ref.val.getField(k).assign(v)
    else:
        ref = refType.createObject()
        ref.new()        
    return ref
# Compile Time
def doNEW(actuals,obj):
    tipe = actuals[0]['tipe']
    
    if not (tipe.isRef or tipe.isObject):
        error("NEW called on non-reference/object type %s" % tipe,  obj, code="006")
    elif tipe.isObject:
        
        for actual in actuals[1:]:
            actname = actual['name']
            if not actname:
                error("Arguments to NEW for object must be named",obj, code="007")
                break
            #print "name is", name
            acttipe = actual['tipe']
            field = tipe.getFieldNewCheck(actname)
#            print field.name, field.tipe, field.default
            if acttipe.isProcedure:
                tipe.checkOverride(actname, acttipe, obj)
            else:
                if not field.tipe.fits(acttipe):
                    error("Type conflict for field '%s' in NEW : actual: %s, formal: %s" % (
                        actname, acttipe, field.tipe), obj, code="010")
    elif tipe.referent.isOpen:
        if len(actuals) <= 1:
            error("Length not supplied for open array", obj,code="011")
        level = tipe.referent
        for dim in actuals[1:]:
            if dim['name']:
                error("Arguments to NEW for array may not be named", obj,code="012")
            if not dim['tipe'].isInteger:
                error("Arguments to NEW for array must be INTEGERs", obj, code="013")
            if level.isOpen:
                level = level.elementType
            else:                
                error("Dimension of array is not open", obj, code="014")
    elif tipe.referent.isObject:
        error("Ref to object currently unsupported (you probably do not mean this anyway!)", obj,code="008")
    elif tipe.referent.isRecord:
        for field in actuals[1:]:
            if not field['name']:
                error("Arguments to NEW for record must be named", obj, code="015")
            if field['name'] not in tipe.referent.fieldnames:
                error("Record does not have field %s" % field['name'], obj, code="016")
            else:
                if not field['tipe'].fits(tipe.referent.fielddict[field['name']].tipe):
                    error("Type mismatch for field %s in allocator" % field['name'], obj, code="009")
    return tipe

M3PredefNEW = M3Types.M3PredefProcedureType("NEW", doNEW)
# Run Time
def M3ORD(ord):
    return ord.ord()

# Compile Time
def doORD(actuals, obj):
    ord = actuals[0]['tipe']
    if not ord.isOrdinal:
        error("ORD called on object of non-ordinal type %s" % ord, obj, code="017")
    return M3Types.M3IntegerBase        

def valORD(callNode):
    tgt = callNode.actualList.kids[0].expr.getVal()
    return tgt.ord()

M3PredefORD = M3Types.M3PredefProcedureType("ORD", doORD, valORD)

# Run Time
def M3VAL(int, tipe):
    return tipe.makeval(int)
# Compile Time
def doVAL(actuals, obj):
    val = actuals[0]['tipe']
    if not val.isInteger:
        error("VAL called with first argument of non-integer type %s" % val, obj,code="019")
    tipe = actuals[1]['tipe']
    if not tipe.isOrdinal:
        error("VAL called with second argument of non-ordinal type %s" % tipe, obj,code="018")
    return tipe

def valVAL(callNode):
    int = callNode.actualList.kids[0].expr.getVal()
    tipe = callNode.actualList.kids[2].expr.getVal()
    return tipe.makeval(int);
    

M3PredefVAL = M3Types.M3PredefProcedureType("VAL", doVAL, valVAL)


# Compile Time for INC and DEC
def doINCDEC(actuals, obj):
    incdec = actuals[0]['tipe']
    if not incdec.isOrdinal:
        error("INC/DEC called with first argument of non-ordinal type %s" % incdec, obj, code="020")
    return M3Types.M3ProcedureNullReturn
# Run Time
def M3INC(inc):
    return inc.inc()



M3PredefINC = M3Types.M3PredefProcedureType("INC", doINCDEC)

# Run Time
def M3DEC(dec):
    return dec.dec()


M3PredefDEC = M3Types.M3PredefProcedureType("INC", doINCDEC)

def doLimit(actuals, obj, name):
    val = actuals[0]['val']
    tipe = actuals[0]['tipe']
    if tipe.isArray:
        return tipe.indexType or M3Types.M3IntegerBase
    elif tipe.isList:
        if hasattr(val,"isType"):
           error("LAST not allowed on LIST types", obj)
        return M3Types.M3IntegerBase
    elif tipe.isOrdinal:
        return tipe
    else:
        error("Cannot use %s on type %s" % (name, tipe), obj, code="021")
        return tipe
def doFIRST(actuals, obj,):
    return doLimit(actuals, obj, "FIRST")
def doLAST(actuals, obj):
    return doLimit(actuals, obj, "LAST")

def valLAST(callNode):
    tipe = callNode.actualList.kids[0].expr.getVal()
    return tipe.getLast()
def valFIRST(callNode):
    tipe = callNode.actualList.kids[0].expr.getVal()
    return tipe.getFirst()

M3PredefFIRST = M3Types.M3PredefProcedureType("FIRST", doFIRST, valFIRST)
M3PredefLAST = M3Types.M3PredefProcedureType("LAST", doLAST, valLAST)

def M3FIRST(refType):
    return refType.getFirst()
def M3LAST(refType):
    return refType.getLast()

def doNARROW(actuals,obj):
    ref = actuals[0]['tipe']
    tipe = actuals[1]['tipe']
    if not tipe.fits(ref):
        error("Narrow called on incompatible types (no common subtype)", obj,code="022")
    return tipe

def M3NARROW(obj,tipe):
    return obj.getNarrowed(tipe)

M3PredefNARROW = M3Types.M3PredefProcedureType("NARROW", doNARROW)

def doNUMBER(actuals,obj):
    val = actuals[0]['val']
    tipe = actuals[0]['tipe']

    if tipe.isOrdinal and hasattr(val,"isType"):
        pass
    elif tipe.isList and not hasattr(val,"isType"):
        pass
    elif tipe.isArray:
        pass
    else:
        error("NUMBER can only be called on Ordinal and ARRAY types or ARRAY and LIST values", obj, code="023")
    return M3Types.M3IntegerBase                

def M3NUMBER(obj):
    return obj.getNumber()

def valNUMBER(callNode):
    tgt = callNode.actualList.kids[0].expr.getVal()
    return tgt.getNumber()
    

M3PredefNUMBER = M3Types.M3PredefProcedureType("NUMBER", doNUMBER, valNUMBER)


def doFLOAT(actuals, obj):
    tipe = actuals[0]['tipe']
    if not tipe.fits(M3Types.M3IntegerBase):
        error("FLOAT can only be called on integers", obj, code="024")
    return M3Types.M3RealBase

def M3FLOAT(obj):
    return M3Types.M3RealBase.createObject(obj.val)
    
def valFLOAT(callNode):
    tgt = callNode.actualList.kids[0].expr.getVal()
    return M3FLOAT(tgt)
    
M3PredefFLOAT = M3Types.M3PredefProcedureType("FLOAT", doFLOAT, valFLOAT)

def doFLOATINTCONVERSION(functionName):
    def check (actuals, obj):
        tipe = actuals[0]['tipe']
        if not tipe.fits(M3Types.M3RealBase):
            error("%s can only be called on reals" % functionName, obj, code="025")
        return M3Types.M3IntegerBase
    return check

def valFLOATINTCONVERSION(functionName):
    def getVal(callNode):
        tgt = callNode.actualList.kids[0].expr.getVal()
        funcDict = {"ROUND": M3ROUND, "TRUNC": M3TRUNC, "FLOOR": M3FLOOR, "CEILING": M3CEILING}
        return funcDict[functionName](tgt)
    return getVal


def M3ROUND(obj):
    return M3Types.M3IntegerBase.createObject(round(obj.val))

def M3TRUNC(obj):
    return M3Types.M3IntegerBase.createObject(int(obj.val))

def M3FLOOR(obj):
    import math
    return M3Types.M3IntegerBase.createObject(int(math.floor(obj.val)))

def M3CEILING(obj):
    import math
    return M3Types.M3IntegerBase.createObject(int(math.ceil(obj.val)))

M3PredefROUND = M3Types.M3PredefProcedureType("ROUND", doFLOATINTCONVERSION("ROUND"), valFLOATINTCONVERSION("ROUND"))
M3PredefTRUNC = M3Types.M3PredefProcedureType("TRUNC", doFLOATINTCONVERSION("TRUNC"), valFLOATINTCONVERSION("TRUNC"))
M3PredefFLOOR = M3Types.M3PredefProcedureType("FLOOR", doFLOATINTCONVERSION("FLOOR"), valFLOATINTCONVERSION("FLOOR"))
M3PredefCEILING = M3Types.M3PredefProcedureType("CEILING", doFLOATINTCONVERSION("CEILING"), valFLOATINTCONVERSION("CEILING"))


def M3ABS(obj):
    return obj.abs()
    
def doABS(actuals, obj):
    tipe = actuals[0]['tipe']
    if not tipe.isNumeric:
        error("ABS can only be called on numeric types", obj, code="026")
    return tipe

def valABS(callNode):
    tgt = callNode.actualList.kids[0].expr.getVal()
    return tgt.abs()


M3PredefABS = M3Types.M3PredefProcedureType("ABS", doABS, valABS)

def M3MIN(obj1,obj2):
    return obj1.min(obj2)

def valMIN(callNode):
    tgt1 = callNode.actualList.kids[0].expr.getVal()
    tgt2 = callNode.actualList.kids[2].expr.getVal()
    return tgt1.min(tgt2) 
    
def M3MAX(obj1,obj2):
    return obj1.max(obj2)

def valMAX(callNode):
    tgt1 = callNode.actualList.kids[0].expr.getVal()
    tgt2 = callNode.actualList.kids[2].expr.getVal()
    return tgt1.max(tgt2) 

def doMAXMIN(functionName):
    def check(actuals,obj):
        tipe1 = actuals[0]['tipe']
        tipe2 = actuals[1]['tipe']
        if not tipe1.fits(tipe2):
            error("Arguments to %s must be identical type" % functionName, obj, code="027")
        if not (tipe1.isOrdinal or tipe1.isReal):
            error("Arguments to %s must be ordinal or real" % functionName, obj, code="028")
        return tipe1
    return check


M3PredefMAX = M3Types.M3PredefProcedureType("MAX", doMAXMIN("MAX"),valMAX)

M3PredefMIN = M3Types.M3PredefProcedureType("MIN", doMAXMIN("MIN"),valMIN)

def M3TYPECODE(obj):
    return obj.typecode()

def doTYPECODE(actuals, obj):
    tipe = actuals[0]['tipe']
    if not (tipe.isRef or tipe.isObject):
        error("TYPECODE can only be called with references or objects", obj, code="029")
    return M3Types.M3Cardinal

M3PredefTYPECODE = M3Types.M3PredefProcedureType("TYPECODE", doTYPECODE)

def M3ISTYPE(obj,tipe):
    return obj.isType(tipe)

def doISTYPE(actuals, obj):
    ref = actuals[0]['tipe']
    tipe = actuals[0]['tipe']
    if not ((ref.isRef or ref.isObject) and (tipe.isRef or tipe.isObject)):
        error("ISTYPE can only be called with references or objects", obj, code="030")
    return M3Types.M3Boolean

M3PredefISTYPE = M3Types.M3PredefProcedureType("ISTYPE", doISTYPE)

def M3DISPOSE(obj):
    obj.dispose()

def doDISPOSE(actuals, obj):
    ref = actuals[0]['tipe']
    if not (ref.isRef or ref.isObject):
        error("DISPOSE can only be called with references or objects", obj, code="031")
    return M3Types.M3ProcedureNullReturn

M3PredefDISPOSE = M3Types.M3PredefProcedureType("DISPOSE", doDISPOSE)

def doSUBARRAY(actuals, obj):
    failed = False
    arrayBase = actuals[0]['tipe']
    start = actuals[1]['tipe']
    length = actuals[2]['tipe']
    if not arrayBase.isArray:
        error("SUBARRAY first parameter must be an array",obj, code="032")
        failed = True
    if not start.isInteger:
        error("SUBARRAY second parameter must be an integer",obj, code="033")        
        failed = True
    if not length.isInteger:
        error("SUBARRAY third parameter must be an integer",obj, code="034")
        failed = True
    if failed:
        return M3Types.M3ErrorType("Subarray Error")
    else:
        return M3Types.M3SubArrayType(arrayBase)
        
def M3SUBARRAY(arrayBase, start, length):
    return M3Types.M3SubArrayType(arrayBase.tipe).createObject(arrayBase, start, length)

#
def doAPPEND(actuals, obj):
    listType = actuals[0]['tipe']
    if not listType.isList:
        error("APPEND called with non-list as first argument", obj)
    else:    
        eltType = actuals[1]['tipe']
        if eltType != listType.elementType:
            error("Attempted APPEND of type %s to LIST of type %s" % (eltType,listType), obj)
    return M3Types.M3ProcedureNullReturn    

M3PredefAPPEND = M3Types.M3PredefProcedureType("APPEND", doAPPEND)

def M3APPEND(list, elt):
    list.val.append(elt.dupe())
#
def doPOP(actuals, obj):
    listType = actuals[0]['tipe']
    if not listType.isList:
        error("POP called with non-list argument", obj)
    return listType.elementType
M3PredefPOP = M3Types.M3PredefProcedureType("POP", doPOP)
def M3POP(list):
    return list.val.pop()
#
def doIMAGE(actuals,obj):
    return M3Types.M3Text
M3PredefIMAGE = M3Types.M3PredefProcedureType("IMAGE", doIMAGE)
def M3IMAGE(item):
    return M3Types.M3Text.createObject(item.image())
#
def doKEYS(actuals, obj):
    dictType = actuals[0]['tipe']
    if not dictType.isDict:
        error("KEYS called with non-dict argument", obj)    
    return M3Types.M3ListType(dictType.indexType)
M3PredefKEYS = M3Types.M3PredefProcedureType("KEYS", doKEYS)
def M3KEYS(dict):
    return dict.getKeys()
#

def doDEL(actuals, obj):
    listType = actuals[0]['tipe']
    toDel = actuals[1]['tipe']
    if listType.isList:
        if not toDel.isInteger:
            error("2nd Argument of DEL for a LIST must be an INTEGER")
    elif listType.isDict:
        if not listType.indexType.fits(toDel):
            error("2nd Argument of DEL for a DICT should be %s and not %s" % (listType.indexType,toDel))
    else:
        error("DEL only allowed with LIST or DICT as 1st argument", obj)
    return M3Types.M3ProcedureNullReturn
M3PredefDEL = M3Types.M3PredefProcedureType("DEL", doDEL)
def M3DEL(dictOrList, keyOrIndex):
    dictOrList.delete(keyOrIndex)

def doINDEX(actuals, obj):
    def checkElement(container,containerName, elementType):
        if not container.elementType.fits(elementType):
            error("2nd Argument of INDEX for this %s must be %s" % (containerName,container.elementType), obj)
    containerType = actuals[0]['tipe']
    elementType = actuals[1]['tipe']
    
    if containerType.isList:
        checkElement(containerType, "LIST", elementType)
        return M3Types.M3IntegerBase        
    elif containerType.isDict:
        checkElement(containerType, "DICT", elementType)        
        return containerType.indexType
    else:
        error("INDEX only allowed with LIST or DICT as 1st argument", obj)
    return M3Types.M3ProcedureNullReturn
M3PredefINDEX = M3Types.M3PredefProcedureType("INDEX", doINDEX)
def M3INDEX(dictOrList, element):
    return dictOrList.index(element)



M3PredefSUBARRAY = M3Types.M3PredefProcedureType("SUBARRAY", doSUBARRAY)

M3ConstraintError = M3Types.M3ExceptionType("ConstraintError")
M3DivideByZeroError = M3Types.M3ExceptionType("DivideByZeroError")
M3UninitialisedError = M3Types.M3ExceptionType(name="UninitialisedError")
M3NullPointerError = M3Types.M3ExceptionType(name="NullPointerError")
M3AssertError = M3Types.M3ExceptionType(name="AssertError")

def M3Assert(cond,location,expression):
    if cond.toBool():
        return
    else:
        import Global
        text = "!!! ASSERT FAILED at %s on %s !!!" % (location,expression)
        if Global.assertRaises:
            raise M3AssertError.createObject(text)
        else:
            Global.results.putAssert(text)

