#
#  Generate AST Nodes with features for
#   Traversal
#   XML Marshalling
#   User specialisation 
#      Typing/Naming
#      Python Generation
#      M3 Regeneration
#      Graphical Editing
import sys
import string
klasses = {}
klassList = []
ruleClasses = """
# -----------------------------------------------------
# This is automatically generated code : do not edit!!!
# See NodeGenerator.py for details
# -----------------------------------------------------
from Nodes import Node
from UserNodes import *
from PyGenNodes import *
from M3GenNodes import *
from EditNodes import *
from CGenNodes import *
"""
def gen(NodeClass, atts, kids):
    global ruleClasses,klasses
    if NodeClass in klasses.keys():
        raise "Duplicate Class Definition %s " % NodeClass
    klasses[NodeClass] = True
    klassList.append(NodeClass)
    if not len(atts) + len(kids):
        ruleClasses += "\nclass %sNode(%sUser,BaseUser,%sPyGen,BasePyGen,%sM3Gen,BaseM3Gen,%sEdit,BaseEdit,%sCGen,BaseCGen,Node): pass\n" % (NodeClass,NodeClass,NodeClass,NodeClass,NodeClass,NodeClass)
        return 
    allents = atts+kids
    allparams = string.join([param + "=None" for param in allents],",")
    kidslist = string.join(kids,",")
    attslist = string.join(['"' + att + '"' for att in atts],",")
    makevars = string.join(["self.%s=%s" %
                            (param,param) for param in allents],"\n        ")
    makeslots = string.join(["self.makeSlot(self.%s,'%s')" %
                            (param,param) for param in allents],"\n        ")

    if kids:
        restorelhs = "[" + string.join(["self.%s" % kid for kid in kids],",") + "]"
        restorerhs = "self.kids"
        restore = "%s=%s" % (restorelhs, restorerhs)
    else:
        restore = "pass"
    ruleClasses += """
class %sNode(%sUser,BaseUser,%sPyGen,BasePyGen,%sM3Gen,BaseM3Gen,%sEdit,BaseEdit,%sCGen,BaseCGen,Node):
    def __init__(self, %s):
        Node.__init__(self)
        %s
        self.add(%s)
        self.attributes=[%s]
    def setSlots(self):
        %s
    def restore(self):
        %s
""" % (NodeClass,NodeClass,NodeClass,NodeClass,NodeClass,NodeClass,
allparams,makevars,kidslist,attslist,makeslots,restore)

gen("CapsuleInterface", ["source"], ["kwc","kwi","modname","ts","imports","portList","kwe","endId","td"])

gen("Capsule", ["source"], ["kwc","modname","kwi","implId","ts","imports","usedCapsules","block","endId","td"])                                     

gen("Interface", ["source"], ["kwi","modname","ts","imports","decls","kwe","endId","td"])
gen("GenericInterface", ["source"], ["kwg","kwi","modname","genericFormals","ts","importList","declList","kwe","endId","td"])
gen("GenericModule", ["source"], ["kwg","kwm","modname","genericFormals","ts","importList","block","endId","td"])
gen("InterfaceInstantiation", ["source"], ["kwi","modname","kweq","genname","genActuals","kwe","endId","td"])
gen("Module", ["source"], ["kwm","modname", "kwex","exportIds","ts","imports","block","endId","td"])
gen("ModuleInstantiation", ["source"], ["kwm","modname","kwex","exportIds","kweq","genname","genActuals","kwe","endId","td"])
gen("FromImport", [],["kwf","impname","kwi","implist","ts"])
gen("UseCapsule", [], ["kwu","idList","ts"])
gen("UseCapsuleList", [], [])
gen("AsImport", [],["kwi","importList","ts"])
gen("AsImportList", [],[])
gen("IdList", [],[])
gen("ImportList", [],[])
gen("ImportItem", [],["id"])
gen("RenamedImportItem", [],["origId","kwa","newId"])
gen("InterfaceDeclList", [],[])
gen("DeclList", [],[])
gen("Block", [],["decList","kwb","statements","kwe"])
gen("CapsuleBlock", [],["decList","connections","kwb","statements","kwe"])
gen("ConstDecls", [],["kwc","constList"])
gen("ConstDeclsList", [],[])
gen("TypeDecls", [],["kwt","typeList"])
gen("TypeDeclsList", [],[])
gen("ExceptionDecls", [],["kwe","exceptionList"])
gen("ExceptionDeclsList", [],[])
gen("VariableDecls", [],["kwv","variables"])
gen("VariableDeclsList", [],[])
gen("ProcedureHead", [],["kwp","name","signature"])
gen("ProcedureDecl", [],["procHead","kweq","procBlock","endId","ts"])
gen("Signature", [],["lbr","formals","rbr","col","tipe","kwr","raises"])
gen("MethodSignature", [],["lbr","formals","rbr","col","tipe","kwr","raises"])
gen("Formals", [],[])
gen("Formal", [],["mode","idList","col","tipe","ass","constExpr"])                   # att
gen("Reveals", [],["kwr","revealsList"])
gen("RevealsList", [],[])
gen("Reveal", [],["qualid","sign","tipe","ts"])
gen("GenFormals", [], ["lbr","idlist","rbr"])
gen("GenActuals", [], ["lbr","idlist","rbr"])
gen("ConstDecl", [],["id","col","tipe","kweq","constExpr"])
gen("TypeDecl", [],["id","sign","tipe"])
gen("ExceptionDecl", [],["id","lbr","tipe","rbr"])
gen("VariableDecl", [],["idlist","col","tipe","ass","expr"])
gen("Raises", [],["lcr","raiseList","rcr"])
gen("RaisesList", [],[])
gen("RaisesAny", [],["kwa"])
gen("Statements", [],[])
gen("AssignSt", [],["lhs","ass","rhs"])
gen("CallSt", [],["expr"])
gen("SendSt", [], ["kws","expr","after"])
gen("SynCallSt", [], ["kwc","expr"])
gen("ReplySt", [], ["kwr","expr","ac"])
gen("AssertSt", [], ["kwa","expr"])
gen("CaseSt", [],["kwc","expr","kwo","caseElts","kwel","elseStatements","kwe"])
gen("CaseEltList", [],[])
gen("VCaseEltList", [],[])
gen("CaseElt", [],[])
gen("ExitSt", [],["kwe"])
gen("EvalSt", [],["kwe","expr"])
gen("ForSt", [],["kwf","forId","ass","startExpr","kwt","toExpr","kwb","byExpr","kwd","statements","kwe"])
gen("IfSt", [],["kwi","ifExpr","kwt","ifConsequence","elsifList","kwel","elseStatement","kwe"])
gen("ElsifList", [],[])
gen("Elsif", [],["kwe","elseExpr","kwt","elseStatement"])
gen("LockSt", [],["kwl","expr","kwd","statements","kwe"])
gen("LoopSt", [],["kwl","statements","kwe"])
gen("RaiseSt", [],["kwr","raiseId","lbr","expr","rbr"])
gen("RepeatSt", [],["kwr","statements","kws","untilExpr"])
gen("Return", [],["kwr","expr"])
gen("TCaseSt", [],["kwt","expr","kwo","tCaseList","kwel","elseStatement","kwe"])
gen("TCaseList", [],[])
gen("TryXptSt", [],["kwt","statements","kwex","handlerList","kwel","elseStatement"])
gen("TryFinSt", [],["kwt","tryStatement","kwf","finallyStatement","kwe"])
gen("WhileSt", [],["kww","whileExpr","kwd","statements","kwe"])
gen("WithSt", [],["kww","bindingList","kwd","statements","kwe"])
gen("BindingList", [],[])
gen("HandlerList", [],[])
gen("LabelsList", [],[])
gen("Labels", [],[])
gen("Case", [],["labelList","kwa","statements"])
gen("VCase", [],["labelList","kwa","fields"])
gen("Handler", [],["qualidList","lbr","id","rbr","kwa","statement"])
gen("HandlerQualidList", [],[])
gen("TypeList", [],[])
gen("TCase", [],["qualidList","lbr","id","rbr","statement"])
gen("Binding", [],["id","kweq","expr"])
gen("ActualExpr", [],["id","ass","expr"])
gen("Actual", [],["tipe"])
gen("Array", [],["kwa","typeList","kwo","tipe"])
gen("Packed", [],["kwb","constExpr","kwf","tipe"])
gen("BracketedType", [], ["lbr","tipe","rbr"])
gen("Enum", [],["lcr","idlist","rcr"])
gen("Object", [],["tipe","brand","kwob","fields","kwm","methods","kwov","overrides","kwe","objectList"])
gen("ObjectList", [],[])
gen("Procedure", [],["kwp","signature"])
gen("Record", [],["kwr","fields","kwe"])                         
gen("VariantRecord", [],["kwr","kwc","tagField","kwo","caseElts","kwel","efields","kwce","ts","sfields","kwe"])
gen("Ref", [],["kwu","brand","kwr","tipe"])
gen("Set", [],["kws","kwo","setconst"])
gen("Subrange", [],["lsq","const1","tdd","const2","rsq"])
gen("Brand", [],["kwb","brandname"])
gen("FieldList", [],[])
gen("Field", [],["idlist","col","tipe","ass","constExpr"])
gen("MethodList", [],[])
gen("Method", [],["name","signature","ass","expr"])
gen("OverrideList", [],[])
gen("Override", [],["id","ass","expr"])
gen("ConstExpr", [],["expr"])
gen("BracketedExpr", [],["lbr","expr","rbr"])
gen("BinaryExpr", [],["expr","exprList"])
gen("UnaryExpr", [],["opList","expr"])
gen("OpExp", [],["operator","expr"])
gen("SelectorExpr", [],["expr","selectorList"])
gen("SelectorList", [],[])
gen("ExprList", [],[])
gen("Expr", [],["expr"])

gen("OpList", [],[])
gen("Caret", [],["op"])
gen("Dot", [],["td","id"])
gen("ArrayRefSelector", [],["lsq","exprList","rsq"])
gen("ProcCallSelector", [],["lbr","actualList","rbr"])
gen("ActualList", [],[])
gen("IndexList", [],[])
gen("Constructor", [],["tipe","lcr","consEltList","rcr"])
gen("ConsEltList", [],[])
gen("ConsEltAss", [],["id","ass","expr"])
gen("ConsEltRange", [],["startExpr","tdd","endExpr"])
gen("ConsEltExpr", [],["expr"])
gen("ConsEltDotdot", [],["tdd"])
gen("QualId", [],[])

gen("TypeName", [],["qualId"])
gen("Root", [],["kwr"])
gen("UntracedRoot", [],["kwu","kwr"])
gen("Number", [],["intVal","td","numberRest","scaling"])

# Terminals

gen("CharLiteral", ["token","startCol","leadChars"],[])
gen("TextLiteral", ["token","startCol","leadChars"],[])
gen("Id", ["idname","startCol","leadChars"],[])
gen("ForId", ["idname","startCol","leadChars"],[])
gen("TCaseId", ["idname","startCol","leadChars"],[])
gen("Int", ["intname","startCol","leadChars"],[])

# Autogenerated terminals

gen("KeyWord", ["token","startCol","leadChars"],[])
gen("Tok", ["token","startCol","leadChars"],[])
gen("Sep", ["token","startCol","leadChars"],[])
gen("Op", ["token","startCol","leadChars"],[])

gen("Null", [],[])

# RTMX Rules (not M3)

gen("Port", [], ["kwp","id","col","protocol"])
gen("MessageGroup", [], ["kwsyn","kwdir","msgList"])
gen("MessageGroupList", [], [])
gen("Message", [], ["kwm","name","signature"])
gen("MessageList", [], [])
gen("PortList", [], [])
gen("ActivityDecl", [], ["activityHead","kweq","handlerBlock","endId","after","ts"])
gen("ActivityHead", [], ["kwh","name","signature"])
gen("StateDecl", [], ["kws","stateId","transitionList","ts"])

gen("Trigger", [], ["kwt","triggerId","kwo","triggerExpr","ts"])
gen("Timer", [], ["periodicity", "variability", "kwt","kwd","delayExpr"])

gen("Connection", [], ["end1","kwc","end2"])
gen("PortConnection", [], ["end1","kwc","end2"])
gen("ConnectionList", [], [])
gen("Connections", [], ["kwc","connectionList","ts"])

gen("TransitionList", [], [])
gen("TransitionHead", [], ["kwo","name","signature"])
gen("TransitionDecl", [], ["transHead","kweq","block","endId","after"])
gen("NextSt", [], ["kwn","stateId"])
gen("StartDecl", [], ["kws","kweq","kwb","statements","kwe","ts"])
gen("PythonSt", [], ["kwp","pythonText"])
gen("ResetSt", [], ["kwr","level"])
gen("DataDependency", [], ["kwd","dataName","ts"])
gen("SendsDecl", [], ["kws","messName","ts"])

gen("List", [], ["kwl","kwo","tipe"])
gen("Dict", [], ["kwd","idx","kwo","tipe"])
gen("ForEachSt", [], ["kwf","forId","tin","listExpr","kwd","statements","kwe"])
gen("ConsEltDict", [], ["t","ass","expr"])
gen("Protocol", [], ["kwp","mgl","kwe"])
gen("ConjugatedProtocol", [], ["tokt", "pro"])
gen("AggregatedProtocol", [], ["t1","op","t2"])

gen("ScaledType", [], ["kws", "tn", "lsq", "unit", "scaleList", "rsq"])
gen("ScaleList", [], [])
gen("ScaleElt", [], ["tc1", "n", "tc2", "i"])
gen("AfterClause", [], ["kwa","afterExpr"])
# Create a set of dummy classes when starting a new aspect
M3GenClasses = ""
if len(sys.argv) > 1:
    for klass in klassList:
        M3GenClasses += "class %sCGen: pass\n" % (klass)

print M3GenClasses + ruleClasses #OK
