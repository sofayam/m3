import M3Types
import M3Predefined
import LUT

EntryDict = {
    "ABS":     LUT.LUTEntry(tipe=M3Predefined.M3PredefABS,declarer="TYPE",val=M3Predefined.M3PredefABS),
    "APPEND":  LUT.LUTEntry(tipe=M3Predefined.M3PredefAPPEND,declarer="TYPE"),
    "BOOLEAN": LUT.LUTEntry(tipe=M3Types.M3Boolean,declarer="TYPE", val=M3Types.M3Boolean),
    "CARDINAL":LUT.LUTEntry(tipe=M3Types.M3Cardinal,declarer="TYPE",val=M3Types.M3Cardinal),
    "CEILING": LUT.LUTEntry(tipe=M3Predefined.M3PredefCEILING,declarer="TYPE", val=M3Predefined.M3PredefCEILING),
    "CHAR":    LUT.LUTEntry(tipe=M3Types.M3Char,declarer="TYPE", val=M3Types.M3Char),
    "DISPOSE": LUT.LUTEntry(tipe=M3Predefined.M3PredefDISPOSE,declarer="TYPE"),
    "DEC":     LUT.LUTEntry(tipe=M3Predefined.M3PredefDEC,declarer="TYPE"),
    "DEL":     LUT.LUTEntry(tipe=M3Predefined.M3PredefDEL,declarer="TYPE"),
    "FALSE":   LUT.LUTEntry(tipe=M3Types.M3Boolean,declarer="VAR",val=M3Types.M3Boolean.createObject("FALSE")),
    "FIRST":   LUT.LUTEntry(tipe=M3Predefined.M3PredefFIRST,declarer="TYPE", val=M3Predefined.M3PredefFIRST),
    "FLOAT":   LUT.LUTEntry(tipe=M3Predefined.M3PredefFLOAT,declarer="TYPE", val=M3Predefined.M3PredefFLOAT),
    "FLOOR":   LUT.LUTEntry(tipe=M3Predefined.M3PredefFLOOR,declarer="TYPE", val=M3Predefined.M3PredefFLOOR),
    "INC":     LUT.LUTEntry(tipe=M3Predefined.M3PredefINC,declarer="TYPE"),
    "IMAGE":   LUT.LUTEntry(tipe=M3Predefined.M3PredefIMAGE,declarer="TYPE"),
    "INDEX":   LUT.LUTEntry(tipe=M3Predefined.M3PredefINDEX,declarer="TYPE"),
    "INTEGER": LUT.LUTEntry(tipe=M3Types.M3IntegerBase,declarer="TYPE", val=M3Types.M3IntegerBase),
    "ISTYPE":  LUT.LUTEntry(tipe=M3Predefined.M3PredefISTYPE,declarer="TYPE"),    
    "KEYS":    LUT.LUTEntry(tipe=M3Predefined.M3PredefKEYS,declarer="TYPE"),
    "LAST":    LUT.LUTEntry(tipe=M3Predefined.M3PredefLAST,declarer="TYPE", val=M3Predefined.M3PredefLAST),
    "MAX":     LUT.LUTEntry(tipe=M3Predefined.M3PredefMAX,declarer="TYPE",val=M3Predefined.M3PredefMAX),     
    "MIN":     LUT.LUTEntry(tipe=M3Predefined.M3PredefMIN,declarer="TYPE",val=M3Predefined.M3PredefMIN), 
    "NARROW":  LUT.LUTEntry(tipe=M3Predefined.M3PredefNARROW,declarer="TYPE"),
    "NEW":     LUT.LUTEntry(tipe=M3Predefined.M3PredefNEW,declarer="TYPE"),
    "NIL":     LUT.LUTEntry(tipe=M3Types.M3Null,declarer="VAR"),    
    "NULL":    LUT.LUTEntry(tipe=M3Types.M3Null,declarer="TYPE"),
    "NUMBER":  LUT.LUTEntry(tipe=M3Predefined.M3PredefNUMBER,declarer="TYPE",val=M3Predefined.M3PredefNUMBER),
    "ORD":     LUT.LUTEntry(tipe=M3Predefined.M3PredefORD,declarer="TYPE", val=M3Predefined.M3PredefORD),
    "POP":     LUT.LUTEntry(tipe=M3Predefined.M3PredefPOP,declarer="TYPE"),
    "REAL":    LUT.LUTEntry(tipe=M3Types.M3RealBase,declarer="TYPE", val=M3Types.M3RealBase),
    "REFANY":  LUT.LUTEntry(tipe=M3Types.M3RefAny,declarer="TYPE"),
    "ROOT":    LUT.LUTEntry(tipe=M3Types.M3Root,declarer="TYPE"),
    "ROUND":   LUT.LUTEntry(tipe=M3Predefined.M3PredefROUND,declarer="TYPE",val=M3Predefined.M3PredefROUND),
    "SUBARRAY":LUT.LUTEntry(tipe=M3Predefined.M3PredefSUBARRAY,declarer="TYPE"),    
    "TEXT":    LUT.LUTEntry(tipe=M3Types.M3Text,declarer="TYPE", val=M3Types.M3Text),
    "TRUE":    LUT.LUTEntry(tipe=M3Types.M3Boolean,declarer="VAR", val=M3Types.M3Boolean.createObject("FALSE")),
    "TRUNC":   LUT.LUTEntry(tipe=M3Predefined.M3PredefTRUNC,declarer="TYPE",val=M3Predefined.M3PredefTRUNC),
    "TYPECODE":LUT.LUTEntry(tipe=M3Predefined.M3PredefTYPECODE,declarer="TYPE"),
    "VAL":     LUT.LUTEntry(tipe=M3Predefined.M3PredefVAL,declarer="TYPE",val=M3Predefined.M3PredefVAL),
    
# Predefined Exceptions not defined in standard Modula-3
    "ConstraintError":    LUT.LUTEntry(tipe=M3Types.M3ExceptionType("ConstraintError"),declarer="EXCEPTION"),
    "DivideByZeroError":  LUT.LUTEntry(tipe=M3Types.M3ExceptionType("DivideByZeroError"),declarer="EXCEPTION"),
    "UninitialisedError": LUT.LUTEntry(tipe=M3Types.M3ExceptionType("UninitialisedError"),declarer="EXCEPTION"),
    "NullPointerError":   LUT.LUTEntry(tipe=M3Types.M3ExceptionType("NullPointerError"),declarer="EXCEPTION"),
    "AssertError":   LUT.LUTEntry(tipe=M3Types.M3ExceptionType("AssertError"),declarer="EXCEPTION"),
    
}
    
#for word in Words:
#    if word not in EntryDict.keys():
#        print "%s not supported" % word

seen = []

def getEntry(reservedWord, obj):
    global seen
    import Message
    #print seen
    if reservedWord not in EntryDict.keys():
        if reservedWord in ["LONGREAL", "EXTENDED"]:
            if obj not in seen:
                Message.warning("%s not supported, using REAL instead" % reservedWord, obj)
                seen.append(obj)
            return EntryDict["REAL"]
        elif reservedWord == "MUTEX":
            if obj not in seen:
                Message.warning("MUTEX not supported, using NULL", obj)
                seen.append(obj)
            return EntryDict["NULL"]    
        else:
            if obj not in seen:
                Message.error("%s not supported" % reservedWord, obj)
                seen.append(obj)
            return EntryDict["NULL"]                 

    return EntryDict[reservedWord]
