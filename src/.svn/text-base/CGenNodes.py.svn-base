# TODO
#  Initialisation of static data with non-constant values in elab code (does this lead to inefficiency?)
#
#

from Message import error, warning
from FakeFile import FakeFile
import Options
import os
import string
import m3
import CompilationUnit
import M3Reserved
import CompOrder
def sp(ind):
    return ' ' * (ind)

nocando = "Cannot generate C code"
enum_prefix = "ENUMLIT__"

class BaseCGen:
    def getCFileBaseName(self):
#        return "ccode" + os.sep + self.getModuleName()
         return self.getModuleName()
    def getModuleName(self):
        return self.getTopNode().modname.idname
    def generateC(self,saveOutput):
        error("%s for '%s' construct" % (nocando, self.__class__.__name__), self)
    def modularize(self,name):
        return "%s__%s" % (self.getModuleName(), name)
    def genCPost(self): return ""

class NoC:    
    def genC(self,s,ind):        
        error("%s for this statement" % nocando, self)
class CapsuleInterfaceCGen:
    def generateC(self,saveOutput):
        pass # codegeneration for capsules is driven by the body

    def generateCapsuleHeader(self,s):
        s.write("/* locals and signatures */\n")
        basename = self.getCFileBaseName()

        for imp in self.imports.kids:
            imp.genC(s)
            
        s.write("typedef struct _%s__descr {\n" % basename)
        s.write("/* Messagepoints */\n")
        self.generateMessagePoints(s)
        # derive the port type and generate field for each message
        s.write("/* Local Data */\n")
        s.write("%s__locals locals;\n" % basename)
        s.write("} %s__%s;\n" % (basename,basename))
        return s
    def generateMessagePoints(self,s):
        ports = self.getType().ports
        for port in ports:
            pname = str(port.name)
            for message in port.protocol.messages:
                mname = str(message.name)
                s.write("vps__messagePoint %s__%s;\n" % (pname,mname))
        
class CapsuleCGen:
    def generateC(self,saveOutput):
        # get the spec
        filename = self.getCFileBaseName()

        if saveOutput:
            header = open(filename + ".h","w")
        else:
            header = FakeFile()

        header.write("#ifndef %s_h\n" % filename)
        header.write("#define %s_h\n" % filename)
        header.write('#include "vps.h"\n')

        for usedCapsule in self.usedCapsules.kids:
            usedCapsule.genC(header)

        self.block.decList.generateCapsuleHeaderPhase1(header)
        
        self.specNode.generateCapsuleHeader(header)

        self.block.decList.generateCapsuleHeaderPhase2(header)

        for imp in self.imports.kids:
            imp.genC(header)

        header.write("/* types not supported */\n")

        header.write("#endif\n")

        header.close()
        
        # create a .c file with bodies of all acts, trans and procs, transformed as described above
        if saveOutput:
            body = open(filename + ".c","w")
        else:
            body = FakeFile()
        body.write('#include "%s.h"\n' % filename)
        
        body.write("/* functions for activities */\n")
        self.block.generateCapsuleBody(body)
        body.close()
    
class InterfaceCGen:
    def generateC(self,saveOutput):
        if saveOutput:
            s = open(self.getCFileBaseName() + ".h","w")
        else:
            s = FakeFile()
        s.write("#ifndef %s_h\n" % self.modname.idname)
        s.write("#define %s_h\n" % self.modname.idname)

        for imp in self.imports.kids:
            imp.genC(s)
        self.decls.genCSpec(s)
        s.write("void %s__elaboration();\n" % self.modname.idname)
        s.write("#endif\n")
    def generateCBody(self,s):
        self.decls.genCBody(s)
class ModuleCGen:
    def generateC(self,saveOutput):
        if saveOutput:
            s = open(self.getCFileBaseName() + ".c","w")
        else:
            s = FakeFile()
        s.write('#include "M3Predef.h"\n')
        exps = self.getExports()
        if exps != []:
            s.write('#include "%s.h"\n' % self.modname.idname)
        for imp in self.imports.kids:
            imp.genC(s)
        if not self.exportIds.isNULL():
            error("%s for explicit exports" % nocando, self)
        else:
            # Variables in interfaces need to be shifted down into the body (extern left in the header)
            if len(exps) == 1:
                expXML = m3.compile(fileName=exps[0] + "." + CompilationUnit.unitTypeNames["Interface"],saveOutput=saveOutput)
                expXML.generateCBody(s)
                
        self.block.genC(s,0,module=True)
        if Options.options.mainProgram and saveOutput:
            mp = open(self.getCFileBaseName() + "__main.c","w")
            myname = self.modname.idname
            mods = CompOrder.getCClosure(myname)
            mp.write("int main() { \n")
            for mod in mods:
                if mod != myname:
                    mp.write("   %s__elaboration();\n" % mod)                            
            mp.write("   %s__elaboration();\n};\n" % myname)                    
            mp.close()
class GenericInterfaceCGen: pass
class GenericModuleCGen: pass

class InterfaceInstantiationCGen: pass
class ModuleInstantiationCGen: pass

class FromImportCGen:
    def genC(self,s):
        s.write('#include "%s.h"\n' % self.impname.idname)
class UseCapsuleCGen:
    def genC(self,s):
        for id in self.idList.kidsNoSep():
            s.write('#include "%s.h"\n' % id.idname)
class UseCapsuleListCGen: pass
class AsImportCGen:
    def genC(self,s):
        for imp in self.importList.kidsNoSep():
            imp.genC(s)
class AsImportListCGen: pass
class IdListCGen: pass
class ImportListCGen: pass
class ImportItemCGen:
    def genC(self,s):
        s.write('#include "%s.h"\n' % self.id.idname)
class RenamedImportItemCGen:
    def genC(self,s):
        s.write('#include "%s.h"\n' % self.origId.idname)
class InterfaceDeclListCGen:
    def genCSpec(self,s):
        for decl in self.kids:
            decl.genCSpec(s)
    def genCBody(self,s):
        for decl in self.kids:
            decl.genCBody(s)
    def genC(self,s):
        for decl in self.kids:
            decl.genC(s)

class DeclListCGen:
    def genC(self,s):
        for decl in self.kids:
            decl.genC(s)

    def generateCapsuleHeaderPhase1(self,s):
        # create an .h file with a definition of the capsule struct as follows:
        #   locals (including child capsules)
        #   messagePoints
        #   extern defs for 
        #     activities, transitions, procedures all defined with self 
        #     acts and trans with parameters condensed into struct, procs with plain params
        filename = self.getCFileBaseName()

        self.decltable = self.tabulate()
            
        s.write("typedef struct _%s__locals {\n" % filename)
        for val in self.decltable.category("variablegroup").values():
            val.generateCapsuleHeaderLocals(s)
        s.write("} %s__locals;\n" % filename)

    def generateCapsuleHeaderPhase2(self,s):        
        for val in self.decltable.category("activity").values():
            val.generateCapsuleHeaderSignatures(s)            
        return s

    def generateCapsuleBody(self,s):
        for decl in self.kids:
            decl.generateCapsuleBody(s)
    
class BlockCGen:
    def genC(self,s,ind,module=False):
        self.decList.genC(s)
        if module: 
            s.write("void %s__elaboration(){\n" % self.getModuleName())
        self.statements.genC(s,ind)
        if module:
            s.write("};\n")
class CapsuleBlockCGen: 
     def generateCapsuleBody(self,body):
         self.decList.generateCapsuleBody(body)
class ConstDeclsCGen:
    def genCSpec(self,s):
        for const in self.constList.kidsNoSep():
            const.genCSpec(s)        
    def genC(self,s):
        for const in self.constList.kidsNoSep():
            const.genC(s)
    def genCBody(self,s):
        for const in self.constList.kidsNoSep():
            const.genC(s)        
class ConstDeclsListCGen: pass
class TypeDeclsCGen:
    def genCBody(self,s):
        pass
    def genCSpec(self,s):
        self.genC(s)
    def genC(self,s):
        for tipe in self.typeList.kidsNoSep():
            tipe.genC(s)
class TypeDeclsListCGen: pass
class ExceptionDeclsCGen: pass
class ExceptionDeclsListCGen: pass
class VariableDeclsCGen:
    def genCBody(self,s):
        for variable in self.variables.kidsNoSep():
            variable.genCBody(s)
    def genCSpec(self,s):
        for variable in self.variables.kidsNoSep():
            variable.genCSpec(s)
    def genC(self,s):
        for variable in self.variables.kidsNoSep():
            variable.genC(s)
    def generateCapsuleBody(self,s):
        pass
class VariableDeclsListCGen: pass
class ProcedureHeadCGen:
    def genC(self,s):
        if self.signature.tipe.isNULL():
            retval = "void"
        else:
            retval = self.signature.tipe.genC()
        pname = self.name.idname
        formlist = self.signature.formals.genC()
        s.write("%s %s__%s ( %s )" % (retval,self.getModuleName(),pname,formlist)) 
class ProcedureDeclCGen:
    def genCBody(self,s): pass
    def genCSpec(self,s):
        self.genC(s)
    def genC(self,s):
#        if self.inInterface():
#            s.write("extern ")
        self.procHead.genC(s)
        if self.inInterface():
            s.write(";\n")
        else:
            s.write("{\n")
            self.procBlock.genC(s,0)
            s.write("}\n")
        
class SignatureCGen: pass
        
class MethodSignatureCGen: pass
class FormalsCGen:
    def genC(self):
        return string.join([formal.genC() for formal in self.kidsNoSep()],",")
    def generateCapsuleHeaderSignature(self):
        return string.join([formal.genC() for formal in self.kidsNoSep()],";\n")
class FormalCGen:
    def genC(self):
        res = ""
        for id in self.idList.kidsNoSep():
            if (not self.mode.isNULL()) and self.mode.token == "VAR":
                ptrsign = "*"
            else:
                ptrsign = ""
            res += ("%s %s%s__%s," % (self.tipe.genC(),ptrsign,self.getModuleName(),id.idname))
        return res[:-1] # snip that last comma off
class RevealsCGen: pass
class RevealsListCGen: pass
class RevealCGen: pass
class GenFormalsCGen: pass
class GenActualsCGen: pass
class ConstDeclCGen:
    def genCSpec(self,s):
        s.write("extern ")
        self.genC(s,noInit=True)
    def genC(self,s,noInit=False):
        name = "%s__%s" % (self.getModuleName(),self.id.idname)
        if noInit:
            initval = ""
        else:
            initval = " = " + self.constExpr.getConstVal().genC()
        if self.tipe.isNULL():
            tipestr = getCCodeName(self.constExpr.getType(),self)
        else:
            tipestr = self.tipe.genC()
        s.write("const %s %s %s;\n" % (tipestr, name ,initval))
class TypeDeclCGen:
    def genC(self,s):
        self.tipe.genCDecl(s,self.id.idname)
class ExceptionDeclCGen: pass

def getCCodeName(tipe,self):
    if hasattr(tipe,"CCodeName"):
        tipestr = tipe.CCodeName
    elif tipe.isBoolean:
        tipestr = "M3Predef__BOOLEAN"
    elif tipe.isInteger or tipe.isEnum:
        tipestr = "M3Predef__INTEGER"
    elif tipe.isReal:
        tipestr = "M3Predef__REAL"
    else:
        error("%s deriving C name for type '%s'" % (nocando, self.regen()), self)
        tipestr = "ERROR"
    return tipestr

class VariableDeclCGen:
    def genCSpec(self,s):
        # called during compilation of the interface
        s.write("extern ")
        self.genC(s,noInit=True)
    def genCBody(self,s):
        # called on the interface during compilation of the module body
        self.genC(s)
    def genC(self,s,noInit=False):
        if self.tipe.isNULL():
            impliedtipe = self.expr.getExprType()
            tipe = getCCodeName(impliedtipe,self)
        else:
            tipe = self.tipe.genCType()
        if self.expr.isNULL() or noInit: 
            init = ""
        else:
            init = " = %s" % self.expr.genC()
        ids = string.join(["%s__%s%s" % (self.getModuleName(),id.idname,self.tipe.genCPost()) for id in self.idlist.kidsNoSep()],",")
        s.write("%s %s%s;\n" % (tipe,ids,init))
    def generateCapsuleHeaderLocals(self,s):
        # generate variable declarations as fields for a struct
        self.genC(s,noInit=True)
class RaisesCGen: pass
class RaisesListCGen: pass
class RaisesAnyCGen: pass
class StatementsCGen:
    def genC(self,s,ind):
        for statement in self.kidsNoSep():
            statement.genC(s,ind)
class AssignStCGen:
    def genC(self,s,ind):

        etype = self.lhs.exprType
        if etype.isArray or etype.isRecord:
            # if this is a value on the right then create a temporary to hold the value and do a memcopy
            # else just do the memcopy
            if etype.isRecord:
                pref = "&"
            else:
                pref = ""
            rhsKind = self.rhs.expr.__class__.__name__
            if rhsKind in ("TypeNameNode", "SelectorExprNode"):
                s.write("%smemcpy(%s%s,%s%s,sizeof(%s));\n" % (sp(ind),
                                                               pref,self.lhs.genC(),
                                                               pref,self.rhs.genC(),self.lhs.genC()))
            elif rhsKind == "ConstructorNode": 
                tempName = "TMP%s" % self.refid
                s.write("%s{\n" % sp(ind))
                arrayTypeName = self.rhs.expr.tipe.genC()
                s.write("%s%s %s=%s;\n" % (sp(ind+1),arrayTypeName,tempName,self.rhs.genC()))
                s.write("%smemcpy(%s%s,%s%s,sizeof(%s));\n" % (sp(ind+1),
                                                               pref,self.lhs.genC(),
                                                               pref,tempName,arrayTypeName))
                s.write("%s};\n" % sp(ind))
            else:
                raise ("unhandled assign" +  rhsKind)
        else:            
            s.write("%s%s = %s;\n" % (sp(ind),self.lhs.genC(), self.rhs.genC()))
class CallStCGen:
    def genC(self,s,ind):
        s.write("%s%s;\n" % (sp(ind),self.expr.genC()))
class SendStCGen:
    def genC(self,s,ind):
        s.write("%s{\n" % sp(ind))
        # find the message point
        s.write("%svps__messagePoint mp;\n" % sp(ind+1))
        # wrap the parameters in a block
        s.write("%svoid *params;\n" % sp(ind+1))
        s.write("%svps__send(mp,params);\n" % sp(ind+1))
        s.write("%s}\n" % sp(ind))
class SynCallStCGen: pass
class ReplyStCGen: pass
class AssertStCGen: pass
class CaseStCGen:
    def genC(self,s,ind):
        s.write("%sswitch(%s) {\n" % (sp(ind),self.expr.genC()))
        self.caseElts.genC(s,ind+1)
        if not self.elseStatements.isNULL():
            s.write("%sdefault:\n" % sp(ind+1))
            self.elseStatements.genC(s,ind+2)
            s.write("%sbreak;\n" % sp(ind+2))
        s.write("%s};\n" % sp(ind))
        
class CaseEltListCGen:
    def genC(self,s,ind):
        for kid in self.kidsNoSep():
            kid.genC(s,ind)
class VCaseEltListCGen: pass
class CaseEltCGen: pass
class ExitStCGen:
    def genC(self,s,ind):
        s.write("%sbreak;\n" % sp(ind))
class EvalStCGen:
    def genC(self,s,ind):
        s.write("%s%s;\n" % (sp(ind), self.expr.genC()))
class ForStCGen:
    def genC(self,s,ind):
        
        if self.byExpr.isNULL():
            steptxt = "++"
        else:
            steptxt = "+= %s" % self.byExpr.genC()
        id = "%s__%s" % (self.getModuleName(),self.forId.idname)
        s.write("%s{\n" % sp(ind))
        s.write("%sint %s;\n" % (sp(ind+1),id))
        s.write("%sfor(%s = %s; %s <= %s; %s%s){\n" %
                (sp(ind+1),id,self.startExpr.genC(),id,self.toExpr.genC(),id,steptxt))
        self.statements.genC(s,ind+2)
        s.write("%s};\n" % sp(ind+1))
        s.write("%s};\n" % sp(ind))        
class IfStCGen:
    def genC(self,s,ind):
        s.write("%sif(%s) {\n" % (sp(ind),self.ifExpr.genC()))
        self.ifConsequence.genC(s,ind+1)
        s.write("%s}" % sp(ind))
        for elsif in self.elsifList.kids:
            elsif.genC(s,ind)
        if not self.elseStatement.isNULL():
            s.write(" else {\n")
            self.elseStatement.genC(s,ind+1)
            s.write("%s};" % sp(ind))
        s.write("\n")
class ElsifListCGen: pass
class ElsifCGen:
    def genC(self,s,ind):
        s.write(" else if (%s) {\n" % (self.elseExpr.genC()))
        self.elseStatement.genC(s,ind+1)
        s.write("%s}" % sp(ind))
class LockStCGen(NoC): pass
class LoopStCGen:
    def genC(self,s,ind):
        s.write("%swhile (1) {\n" % sp(ind))
        self.statements.genC(s,ind+1)
        s.write("%s};\n" % sp(ind))
class RaiseStCGen(NoC): pass
class RepeatStCGen:
    def genC(self,s,ind):
        s.write("%sdo {\n" % sp(ind))
        self.statements.genC(s,ind+1)
        s.write("%s} while (!(%s));\n" % (sp(ind),self.untilExpr.genC()))
class ReturnCGen:
    def genC(self,s,ind):
        if self.expr.isNULL():
            retstr = ""
        else:
            retstr = self.expr.genC()        
        s.write("%sreturn %s;\n" % (sp(ind), retstr))
class TCaseStCGen(NoC): pass
class TCaseListCGen(NoC): pass
class TryXptStCGen(NoC): pass
class TryFinStCGen(NoC): pass
class WhileStCGen:
    def genC(self,s,ind):    
        s.write("%swhile (%s) {\n" % (sp(ind), self.whileExpr.genC()))
        self.statements.genC(s,ind+1)
        s.write("%s};\n" % sp(ind))
    
class WithStCGen:
    def genC(self,s,ind):
        def climbBindings(bindings,ind):
            binding = bindings[0]
            s.write("%s{\n" % sp(ind))
            s.write("%s%s;\n" % (sp(ind+1), binding.genC()))
            if len(bindings) > 1:
                climbBindings(bindings[1:],ind+1)
            else:
                self.statements.genC(s,ind+1)
            s.write("%s};\n" % sp(ind))
        climbBindings(self.bindingList.kidsNoSep(),ind)
class BindingListCGen: pass
class HandlerListCGen: pass
class LabelsListCGen:
    def genC(self,s,ind):
        for label in self.kidsNoSep():
            label.genC(s,ind)
class LabelsCGen:
    def genC(self,s,ind):
        if self.length() == 1:
            s.write("%scase %s:\n" % (sp(ind),self.kids[0].genC()))
        else:
            startVal = self.kids[0].getConstVal().ord().val
            stopVal = self.kids[2].getConstVal().ord().val
            for caseVal in range(startVal,stopVal+1):
                s.write("%scase %s:\n" % (sp(ind),caseVal))

class CaseCGen:
    def genC(self,s,ind):
        self.labelList.genC(s,ind)
        self.statements.genC(s,ind+1)
        s.write("%sbreak;\n" % sp(ind+1))
class VCaseCGen: pass
class HandlerCGen: pass
class HandlerQualidListCGen: pass
class TypeListCGen:
    def getCRanges(self):
        return string.join(["[%d]" % kid.getType().width() for kid in self.kidsNoSep()])
        
class TCaseCGen: pass
class BindingCGen:
    def genC(self):
        return "%s * %s = &(%s)" % (getCCodeName(self.expr.getExprType(),self),
                               self.modularize(self.id.idname), self.expr.genC())
class ActualExprCGen:
    def genC(self):
        if not self.id.isNULL():
            error("%s for named actual parameters" % nocando,self)
        return self.expr.genC()
        
class ActualCGen: pass
class ArrayCGen:
    def genCPost(self):
        return self.typeList.getCRanges()
    def genC(self): # called on anonymous arrays
        return "%s" % self.tipe.genC()
    def genCDecl(self,s,name):
        modname = self.getModuleName()
        typename = "%s__%s" % (modname, name)
        elttype = self.tipe.genC()
        ranges = self.typeList.getCRanges()
        s.write("typedef %s %s %s;\n" % (elttype, typename, ranges))
    def genCType(self):
        return self.tipe.genC()
class PackedCGen: pass
class BracketedTypeCGen: pass
class EnumCGen:
    def genCDecl(self,s,name):
        modname = self.getModuleName()
        typename = "%s__%s" % (modname, name)
        for ctr, item in enumerate(self.idlist.kidsNoSep()):
            s.write("#define %s%s__%s %s\n" % (enum_prefix,typename, item.idname, ctr))
        s.write("typedef int %s;\n" % typename) # TBD maybe make this short or just a char if it fits

class ObjectCGen: pass
class ObjectListCGen: pass
class ProcedureCGen: pass
class RecordCGen:
    
    def genCDecl(self,s,name):
        structcore = self.genCType()
        typename = self.modularize(name)
        s.write("typedef %s %s;\n" % (structcore, typename))


    def genCType(self):
        modname = self.getModuleName()
        tmpname = "%s__%d" % (modname, self.refid)
        res = "struct %s {\n" % tmpname
        res += self.fields.genC()
        res += "} "
        return res

class VariantRecordCGen: pass
class RefCGen:
    def genC(self):
        return "%s*" % self.tipe.genC() 
    def genCDecl(self,s,name):
        modname = self.getModuleName()
        typename = "%s__%s" % (modname, name)
        referent = "%s__REFERENT" % (typename)
        self.tipe.genCDecl(s, "%s__REFERENT" % name)
        s.write("typedef %s* %s;\n" % (referent, typename))

    def genCType(self):
        return self.genC()
class SetCGen: pass
class SubrangeCGen:
    def genCDecl(self,s,name):
        modname = self.getModuleName()
        typename = "%s__%s" % (modname, name)
        s.write("typedef int %s;\n" % typename) # TBD all subranges are ints

    def genC(self):
        return "int" # TBD this will do for now
    def genCType(self):
        return self.genC()
class BrandCGen: pass
class FieldListCGen:
    def genC(self):
        res = ""
        for field in self.kidsNoSep():
            res += field.genC()
        return res
class FieldCGen:
    def genC(self):
        res = ""
        for id in self.idlist.kidsNoSep():
            res += "%s %s %s;\n" % (self.tipe.genC(),id.idname,self.tipe.genCPost())
        return res
class MethodListCGen: pass
class MethodCGen: pass
class OverrideListCGen: pass
class OverrideCGen: pass
class ConstExprCGen:
    def genC(self):
        return self.expr.genC()
class BracketedExprCGen:
    def genC(self):
        return "(%s)" % self.expr.genC()
class BinaryExprCGen:
    def genC(self):
        if self.expr.getType().isArray:
            # arrays need special treatment
            arrayops = {"=": "!memcmp", "#": "memcmp"}
            return "%s(%s,%s,sizeof(%s))" % (arrayops[self.exprList.operator.token], self.expr.genC(), self.exprList.genC(noop=True), self.expr.genC())
        else:
            return self.expr.genC() + self.exprList.genC()
class UnaryExprCGen:
    def genC(self):
        return self.opList.genC(self.expr.genC())
class OpExpCGen:
    def genC(self,noop=False):
        if noop:
            op = ""
        else:
            op = self.operator.genC()
        return "%s %s" % (op, self.expr.genC())

class DerefBase:
    def derefStarter(self):
        return "(*" * self.countDerefs()
    
class SelectorExprCGen(DerefBase):
    def genC(self):
        # catch the predefined functions here so you can do parameter transformation
        predef = self.expr.getPredefined()
        if predef:
            res = "M3Predef__%s" % predef
            if predef == "NEW":                
                return self.genCNEW(res)
        else:
            res = self.expr.genC()
        # find the root array type
        indicesPtr = [self.expr.getType()] # box this so we can mutate it
        for sel in self.selectorList.kids:
            res += sel.genC(indicesPtr)
        return self.derefStarter() + res
    def genCNEW(self,res):
        # only handle the first item in the selector list (LIMITATION)
        param = self.selectorList.kids[0].actualList.kids[0].expr.expr
        nodename = param.__class__.__name__
        if nodename == "RefNode":
            return "%s(%s)" % (res, param.tipe.genC())
        elif nodename == "TypeNameNode":
            return "%s(%s__REFERENT)" % (res, param.genC())            
        else:
            error("%s NEW parameter too complex (%s)" % (nocando, nodename), self)

        # simple case - just a type name
        # nastier case - an anonymous type
        # nastiest case - some parameters as well 
        
class SelectorListCGen: pass
class ExprListCGen:
    def genC(self):
        return string.join([kid.genC() for kid in self.kids],"")

class ExprCGen(DerefBase):
    def genC(self):
        return self.derefStarter() + self.expr.genC()
class OpListCGen:
    def genC(self,expr):
        res = ""
        for op in self.kids:
            res += "%s" % op.genC()
        return res + expr
        
        
class CaretCGen:
    def genC(self,dummy):
        return ")" # This was opened up at the beginning of the expression
class DotCGen:
    def genC(self,indicesPtr):
        closeDeref = ""
        if indicesPtr[0].isRef:
            if not self.hasPrecedingCaret:
                closeDeref = ")" # opened at beginning of expression
        return closeDeref + "." + self.id.idname 
class ArrayRefSelectorCGen:
    def genC(self,indicesPtr):
        # here we also close possible derefs which we opened up at the beginning of the expr
        res = ""
        closeDeref = ""
        for indexItem in self.exprList.kidsNoSep():
            if indicesPtr[0].isRef:
                if not self.hasPrecedingCaret: # catch the implicit derefs
                    closeDeref = ")"
                indicesPtr[0] = indicesPtr[0].referent
            offset = indicesPtr[0].indexType.cBaseOffset
            if offset != 0:
                offtxt = " - %d" % offset
            else:
                offtxt = ""
            res += "%s[%s%s]" % (closeDeref,indexItem.genC(), offtxt)
            indicesPtr[0] = indicesPtr[0].elementType
        return res
        #return string.join(["[%s]" % indexItem.genC(indicesPtr) for indexItem in self.exprList.kidsNoSep()])     

class ProcCallSelectorCGen:
    def genC(self,rootType):
        calledProc =  self.parent.parent.expr.getType()
        if calledProc.predef:
            return "(" + self.actualList.genC() + ")"
        # start with a row of empty boxes
        params = [None] * len(calledProc.formals)
        # populate the boxes with defaults from the actuals
        for ctr, param in enumerate(calledProc.formals):
            if param.default:
                params[ctr] = param.default.genC()
        positional = True
        for ctr, actual in enumerate(self.actualList.kidsNoSep()):
            if positional:
                if actual.id.isNULL():
                    params[ctr] = actual.expr.genC()
                else:
                    positional = False
            if not positional:
                params[calledProc.offsetForParamName(actual.id)] = actual.expr.genC()
        # and finally wrap an address call round the VAR params
        for ctr, param in enumerate(calledProc.formals):
            if param.mode == "VAR":
                params[ctr] = "&%s" % params[ctr]
        return "(" + string.join(params,",") + ")"

class ActualListCGen:
    def genC(self):
        actualStrings = [actual.genC() for actual in self.kidsNoSep()]
        return string.join(actualStrings,",")
class IndexListCGen: pass
class ConstructorCGen:
    def genC(self):
        tipe = self.tipe.getType()
        if tipe.isArray:
            return "{ %s }" % self.consEltList.genCArray(tipe.length())
        elif tipe.isRecord:
            return "{ %s }" % self.consEltList.genCRecord(tipe) 
        else:
            error("%s constructor not supported for this type (yet)" % nocando,self)
class ConsEltListCGen:
    def genCArray(self,length):
        res = ""
        kids = self.kidsNoSep()
        if kids[-1].__class__.__name__ == "ConsEltDotdotNode":
            kids = kids[0:-1]
            padout = True
        else:
            padout = False
        for kid in kids:
            res += "%s," % kid.genC()
        if padout:
            remaining = length - len(kids)
            res += ("%s," % kids[-1].genC()) * remaining
        return res
    def genCRecord(self,tipe):
        # start with a row of empty boxes
        fields = [None] * len(tipe.fields)
        # populate boxes with defaults
        for ctr, field in enumerate(tipe.fields):
            if field.default:
                fields[ctr] = field.defaultNode.genC()
        positional = True # start processing constructor in positional mode
        for ctr, kid in enumerate(self.kidsNoSep()):
            if positional:
                if kid.__class__.__name__ == "ConsEltExprNode":
                    fields[ctr] = kid.genC()
                else:
                    positional = False
            if not positional:
                # place the named field into the right box
                fields[tipe.offsetForFieldName(kid.id.idname)] = kid.expr.genC()
        for ctr, field in enumerate(fields):
            # catch incomplete case (box will still be empty)
            if field == None:
                error("C Code - incomplete constructor, missing value for field %s" % tipe.fields[ctr].name)
                return ""
        # finally generate the completed aggregate        
        return string.join(fields,",")

class ConsEltAssCGen:
    def genC(self):
        return self.expr.genC()
class ConsEltRangeCGen: pass
class ConsEltExprCGen:
    def genC(self):
        return self.expr.genC()
class ConsEltDotdotCGen: pass

CPredefs = {"INTEGER": "int",
            "REAL":    "float",
            "LONGREAL": "float",
            "TEXT":    "char*",
            "BOOLEAN": "int",
            "CHAR":    "char",
            "CARDINAL": "int",
            "FALSE":    "0",
            "TRUE":     "1"}



class QualIdCGen:
    def genC(self):
        #import pdb; pdb.set_trace()
        # general formats
        # 0. id - predefined or ultrasimple
        # 1. [module.]enum.value  - special case
        # 2. [module.]obj[.deref]* - everything else

        name = self.image()
        if name in CPredefs:
            return CPredefs[name]

        prefix = ""
        if self.getEnclosingActTrans():
            if self.getBaseEntry().mode in ["VAR", "VALUE"]:
                prefix = "params->"
        if self.getBaseEntry().isIvar:
            prefix = "self->locals."

        
        idsOnly = [kid.idname for kid in self.kidsNoSep()]
        if len(idsOnly) == 1:                  
            entry = self.getEntry()
            #print name,entry.mode
            res = "%s%s__%s" % (prefix,entry.node.getModuleName(),name)
            if entry.mode == "VAR":
                res = "(*%s)" % res
            return res

        else:
            lut = self.getLUT()
            entry = self.getEntry()
            
            if entry.declarer == "ENUM": # do special case for enum value
                if len(idsOnly) == 2:
                    typename = idsOnly[0]
                    entry = lut.deref(typename,self)
                    litname = idsOnly[1]
                elif len(idsOnly) == 3:
                    typename = idsOnly[1]
                    entry = lut.deref(idsOnly[0],self)
                    entry = entry.deref(typename,self)
                    litname = idsOnly[2]
                else:
                    raise "c code generation anomaly : an enum literal " + (
                        "value cannot have more than three elements : %s" % self.image())
                base = entry.getTipe().base
                CName = getCCodeName(base,self)
                return "%s%s__%s" % (enum_prefix, CName, litname)

            else:
                
                # first sort out the module prefix and the object name which is
                # either represented by the first only or by the first two
                entry = lut.deref(idsOnly[0],self)

                if entry.declarer == "MODULE":
                    rest = 2
                    name = idsOnly[1]
                    entry = entry.deref(name,self)
                    baseName = "%s__%s" % (entry.node.getModuleName(),name)
                else:
                    rest = 1
                    name = idsOnly[0]

                        
                    baseName = "%s%s__%s" % (prefix,entry.node.getModuleName(),name)

                    if entry.mode == "VAR":
                        baseName = "(*%s)" % baseName
                
                if len(idsOnly) > rest: # is there any more ?
                    # these can only be record fields - tack them on the end
                    trailers = idsOnly[rest:]
                    derefs = self.getEmbeddedImplicitDerefs()
                    # and intersperse closing deref brackets where you are doing an implicit pointer->struct dereference
                    for ctr, trailer in enumerate(trailers):
                        if ctr in derefs:
                            close = ")"
                        else:
                            close = ""
                        baseName += (close + "." + trailer)
                return baseName

class TypeNameCGen:
    def getPredefined(self):
        res = self.qualId.image()
        if res in M3Reserved.EntryDict:
            return res
        else:
            return None
    def genCType(self):
        return self.qualId.genC()
    def genC(self):
        return self.qualId.genC()
    def genCDecl(self,s,name):
        modname = self.getModuleName()
        typename = "%s__%s" % (modname,name)
        s.write("typedef %s %s;\n" % (self.qualId.genC(), typename))
class RootCGen: pass
class UntracedRootCGen: pass
class NumberCGen:
    def genC(self):
        res = self.intVal.intname
        if self.numberRest.isNULL():
            if self.scaleMult > 1:
                res += " * %s" % (self.scaleMult)
        else:
            res += "." + self.numberRest.intname
        return res
class CharLiteralCGen:
    def genC(self):
        return "%s" % self.token
    
class TextLiteralCGen:
    def genC(self):
        return self.token
class IdCGen: pass
class ForIdCGen: pass
class TCaseIdCGen: pass
class IntCGen: pass
class KeyWordCGen: pass
class TokCGen: pass
class SepCGen: pass
class OpCGen:
    def genC(self):
        myOp = self.token
        unchanged = ("+","-","*","/",">","<",">=","<=")
        
        opDict = {"=": "==",
                  "#": "!=",
                  "AND": "&&",
                  "OR": "||",
                  "NOT": "!",
                  "DIV": "/",}
        if myOp in unchanged:
            return myOp
        elif myOp in opDict:
            return opDict[myOp]
        else:
            return error("%s for operator %s" % (nocando,myOp), self)
class NullCGen: pass
class PortCGen: pass
class MessageGroupCGen: pass
class MessageGroupListCGen: pass
class MessageCGen: pass
class MessageListCGen: pass
class PortListCGen: pass
class ActivityDeclCGen:
    def generateCapsuleHeaderSignatures(self,s):
        self.activityHead.generateCapsuleHeaderSignature(s)
    def generateCapsuleBody(self,body):
        body.write("%s {\n" % self.activityHead.generateCapsuleSignature())
        self.handlerBlock.genC(body,1)
        body.write("};\n")
class ActivityHeadCGen:
    def generateCapsuleHeaderSignature(self,s):
        actname = "%s__%s" % (self.getModuleName(), self.name.idname)
        paramstructitems = self.signature.formals.generateCapsuleHeaderSignature() + ";\n"
        s.write("typedef struct _%s__params {\n" % actname)
        s.write(paramstructitems)
        s.write("} %s__params;\n" % actname)
        s.write("extern %s;\n" % self.generateCapsuleSignature())

    def generateCapsuleSignature(self):
        mname = self.getModuleName()
        actname = "%s__%s" % (mname, self.name.idname)
        return "void %s(%s__%s *self, %s__params *params)" %  (actname,mname,mname,actname)
    
class StateDeclCGen: pass
class TriggerCGen: pass
class TimerCGen: pass
class ConnectionCGen:
    def normalizeMessageId(self,idList):
        # This returns either
        #  None, activityName
        #  None, port.messageName
        #  ChildName, port.messageName
        print "****Normalising***"
        if len(idList) == 1 and self.isEntity(idList[0]):
            return (None, str(idList[0]))
        obj,msg = self.constructObjMsg(idList) # larcenous reuse from pygennodes
        objbits = string.split(obj,".")
        if len(objbits) > 1:
            return (str(objbits[1]),str(msg))
        else:
            return (None,str(msg))
        
    def setMessages(self,entity):
        # these can be either:
        #                     timer/trigger -> activity
        #                     timer/trigger -> outgoing message
        #                     timer/trigger -> child incoming message
        #                     incoming message -> activity
        #                     child outgoing message -> activity
        # (subset of portconnection)
        #                     incoming message -> child incoming message
        #                     child outgoing message -> outgoing message
        #                     child outgoing message -> child incoming message

        end2 = self.normalizeMessageId(self.end2.idList())        
        if self.source.isTrigger:
            entity.addTrigger(self.end1.idList()[0],end2)
            return
        if self.source.isTimer:
            entity.addTimer(self.end1.idList()[0],end2)
            return
        end1 = self.normalizeMessageId(self.end1.idList())                
        entity.addSingleConnection(end1,end2)
                              
class PortConnectionCGen:
    # This cooperates with elaboration code and is called on each entity. It is NOT called by the standard pro-capsule code
    # generation run. OK, so I stole the structure from PyGenNodes but how can you make this generic enough
    # to really share?
    def setMessages(self, entity):

        end2messageNames = [message.name for message in self.end2.getType().protocol.messages]
        for message in self.end1.getType().protocol.messages:

            messageName = message.name
            if messageName not in end2messageNames: continue # new gentle lax port connections
            mtype = message
            # who is the source ?
            if self.end1l == 2:
                child1 = self.end1.idList()[0]
                port1 = self.end1.idList()[1]
            else:
                port1 = self.end1.idList()[0]
            if self.end2l == 2:
                child2 = self.end2.idList()[0]
                port2 = self.end2.idList()[1]                
            else:
                port2 = self.end2.idList()[0]

            if self.connectionType == "across":
                
                if mtype.dir == "INCOMING":
                    # across,IN OUT
                    startMsg = "%s.%s" % (port2,messageName)
                    endMsg = "%s.%s" % (port1,messageName)
                    entity.connectChildren(child2,startMsg,child1,endMsg)
                else:
                    # across,OUT IN
                    startMsg = "%s.%s" % (port1,messageName)                    
                    endMsg = "%s.%s" % (port2,messageName)
                    entity.connectChildren(child1,startMsg,child2,endMsg)                    
            else:                
                if mtype.dir == "INCOMING":
                    
                    if self.end1l == 1:
                        # updown,IN IN,par->child
                        startMsg = "%s.%s" % (port1,messageName)
                        endMsg = "%s.%s" % (port2,messageName)
                        entity.connectToChild(startMsg,child2,endMsg)                    
                    else:
                        # updown,IN IN,child->par
                        startMsg = "%s.%s" % (port2,messageName)
                        endMsg = "%s.%s" % (port1,messageName)
                        entity.connectFromChild(child1,startMsg,endMsg)                                            
                else:
                    if self.end1l == 1:
                        # updown,OUT OUT,par->child                        
                        startMsg = "%s.%s" % (port2,messageName)
                        endMsg = "%s.%s" % (port1,messageName)
                        entity.connectToChild(startMsg,child2,endMsg)                                            
                    else:
                        # updown,OUT OUT,child->par                        
                        startMsg = "%s.%s" % (port1,messageName)
                        endMsg = "%s.%s" % (port2,messageName)
                        entity.connectFromChild(child1,startMsg,endMsg)                                            

    
class ConnectionListCGen: pass
class ConnectionsCGen: pass
class TransitionListCGen: pass
class TransitionHeadCGen: pass
class TransitionDeclCGen: pass
class NextStCGen: pass
class StartDeclCGen: pass
class PythonStCGen: pass
class ResetStCGen: pass
class DataDependencyCGen: pass
class SendsDeclCGen: pass
class ListCGen: pass
class DictCGen: pass
class ForEachStCGen: pass
class ConsEltDictCGen: pass
class ProtocolCGen: pass
class ConjugatedProtocolCGen: pass
class AggregatedProtocolCGen: pass
class ScaledTypeCGen: pass
class ScaleListCGen: pass
class ScaleEltCGen: pass
class AfterClauseCGen: pass
