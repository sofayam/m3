from Message import error, getLocation
from FakeFile import FakeFile
import Options
import CompilationUnit
import os
import m3
import string
def sp(ind):
    return ' ' * (ind)

class BasePyGen: 
    "Provides default methods for all nodes in this aspect(for code generation there are none yet)"

class NonGen:
    def generatePython(self,saveOutput):
        pass
    def genPy(self):
        pass
    def genInterface(self,forMod):
        pass

class InterfacePyGen:
    def generatePython(self, saveOutput, forMod=None):
        if saveOutput:
            s = open(self.getBaseName() + ".py","w")
        else:
            s = FakeFile()
        s.write("import M3Objects\n")
        s.write("import M3Types\n")
        s.write("import M3Predefined\n")
        s.write("import M3TypeLib\n")
        s.write("import M3ProcLib\n")
        if forMod:
            typeLib = forMod
        else:
            typeLib = self
        s.write("M3TL=M3TypeLib.internaliseTypes(r'%s')\n" % typeLib.getBaseName())
        for imp in self.imports.kids:
            imp.genPy(s)
        self.decls.genInterface(s,forMod)
        s.close()
class GenericInterfacePyGen(NonGen): pass
class GenericModulePyGen(NonGen): pass
class InterfaceInstantiationPyGen(NonGen): pass
class ModuleInstantiationPyGen: pass
class ModulePyGen:

    def generatePython(self, saveOutput):
        for export in self.getExports():
            expXML = m3.compile(fileName=export + "." + CompilationUnit.unitTypeNames["Interface"],saveOutput=saveOutput)
            expXML.generatePython(saveOutput=saveOutput, forMod=self)

            #print "generating from  export %s" % export
        if saveOutput:
            f = open(self.getBaseName() + ".py","w")
        else:
            f = FakeFile()
        f.write("import M3Objects\n")
        f.write("import M3Types\n")
        f.write("import M3Predefined\n")                
        for export in self.getExports():
            f.write("from %sInt import *\n" % export)
        for imp in self.imports.kids:
            imp.genPy(f)
        f.write("import M3TypeLib\n")
        f.write("import M3ProcLib\n")        
        f.write("M3TL=M3TypeLib.internaliseTypes(r'%s')\n" % self.getBaseName())
        f.write("from Statistics import M3incStat\n")
        self.block.genMain(f,self.modname.idname)
        f.close()

class AsImportPyGen:
    def genPy(self,s):
        for imp in self.importList.kidsNoSep():
            imp.genPy(s)

class AsImportListPyGen: pass

class IdListPyGen:
    def genPy(self):
        return string.join([kid.idname for kid in self.kidsNoSep()],",")

class ImportListPyGen: pass

class FromImportPyGen:
    def genPy(self,s):
        s.write("from %sInt import %s\n" %(self.impname.idname, self.implist.genPy()))

class ImportItemPyGen:
    def genPy(self,s):
        s.write("import %sInt as %s\n" % (self.id.idname,self.id.idname))

class RenamedImportItemPyGen:
    def genPy(self,s):
        s.write("import %sInt as %s\n" % (self.origId.idname, self.newId.idname))

class InterfaceDeclListPyGen:
    def genInterface(self, s, forMod):
        for decl in self.kids:
            decl.genInterface(s,forMod)
        for decl in self.kids:
            decl.genVar(s,0)
class DeclListPyGen:
    def genPy(self,s,ind):
        for decl in self.kids:
            decl.genPy(s,ind)
        for decl in self.kids:
            decl.genVar(s,ind)
    def genCapsule(self,s,ind):
        # This special handling for capsules ensures that type and variable 
        # code is collected for a constructor, and also that the BEGIN..END code
        # is called from the constructor with a "self"
        for decl in self.kids:
            decl.genCapClassDecl(s,ind+1)
        f = FakeFile()
        for decl in self.kids:
            decl.genCapInitDecl(f,ind+2)
        for decl in self.kids:            
            decl.genVar(f,ind+2)
        constructorCode = f.cont
        s.write("%sdef __init__(self,level,runtimeName):\n" % sp(ind+1)) # TBD evil hardwired indentation
        s.write("%sself.runtimeName = runtimeName\n" % sp(ind+2))        
        s.write("%sself.__level = level\n" % sp(ind+2))
        s.write("%sRTSTypes.M3CapsuleRuntimeType.__init__(self,level)\n" % sp(ind+2))
        if constructorCode:
            s.write(constructorCode)
        s.write("%sself.__init_capsule_connect()\n" % sp(ind+2))        
        s.write("%sself.__init_capsule_begin_end()\n" % sp(ind+2))
        s.write("%sself.__init_param_converters()\n" % sp(ind+2))

class BlockPyGen:
    def genMain(self,s,modname):
        self.decList.genPy(s,ind=0)
        if len(self.statements.kidsNoSep()) > 0:
            s.write("def %sMain():\n" % modname)
            self.statements.genPy(s,1)
            s.write("%sMain()\n" % modname)                

    def genPy(self,s,ind):
        self.decList.genPy(s,ind)
        self.statements.genPy(s,ind)

class CapsuleBlockPyGen:

    def genMain(self,s,modname):
        s.write("class %s(RTSTypes.M3CapsuleRuntimeType):\n" % modname)
        res = self.decList.tabulate()
        self.decList.genCapsule(s,0)
        
        if self.connections.isNULL():
            s.write("%sdef __init_capsule_connect(self): pass\n" % sp(1))
        else:
            s.write("%sdef __init_capsule_connect(self):\n" % sp(1))            
            self.connections.genPy(s,2)

        if len(self.statements.kids) == 0:
            s.write("%sdef __init_capsule_begin_end(self): pass # capsule BEGIN .. END\n" % sp(1))
        else:
            s.write("%sdef __init_capsule_begin_end(self): # capsule BEGIN .. END\n" % sp(1))
            for statement in self.statements.kidsNoSep():
                statement.genPy(s,2)
        s.write("%sdef __init_param_converters(self):\n" % sp(1))
        # go through each input message in the type and create a dict of name: type
        # { 'messname1': (('p1', M3Integer), .... }
        param_converters = ""
        #import pdb; pdb.set_trace()
        for mname,mval in self.parent.getType().spec.inDict.items() + self.parent.getType().spec.outDict.items():
            # which protocol did this come from and where was it defined ???
            protoModule = mval.type.node.getTopNode().modname.idname
            param_converters += "'%s' : %s," % (mname, mval.type.node.genFormalTable(protoModule))
        s.write("%sself.M3param_converters = {%s}\n" % (sp(2), param_converters))
        
        s.write("%sself.M3port_converters = %s\n" % (sp(2), str(self.parent.getType().spec.uniqueMessagePorts)))
        
    def genPy(self,s,ind):
        self.decList.genCapsule(s,ind)
        # the following all lands in the __init__ of the class defined above
        if not self.connections.isNULL():
            self.connections.genPy(s,ind+2)
        for statement in self.statements.kids:
            statement.genPy(s,ind+2)

class ConstDeclsPyGen:
    def genInterface(self,s,forMod):
        self.genPy(s,0)
    def genPy(self, s, ind):
        for const in self.constList.kidsNoSep():
            const.genPy(s,ind)
    def genVar(self,s,ind): pass
    def genCapClassDecl(self,s,ind):
        for const in self.constList.kidsNoSep():
            const.genCapClassDecl(s,ind)
    def genCapInitDecl(self,s,ind):
        for const in self.constList.kidsNoSep():
            const.genCapInitDecl(s,ind)



class ConstDeclsListPyGen: pass

class TypeDeclsPyGen:
    def genPy(self,s,ind):
        for tipe in self.typeList.kidsNoSep():
            tipe.genPy(s,ind)

    def genInterface(self,s,forMod):
        for tipe in self.typeList.kidsNoSep():
            tipe.genPy(s,0)
    def genCapClassDecl(self,s,ind):
        for tipe in self.typeList.kidsNoSep():
            tipe.genCapClassDecl(s,ind)
    def genCapInitDecl(self,s,ind):
        for tipe in self.typeList.kidsNoSep():
            tipe.genCapInitDecl(s,ind)

    def genVar(self,s,ind): pass
    
class TypeDeclsListPyGen: pass

class ExceptionDeclsPyGen:
    def genInterface(self, s, forMod):
        self.genPy(s,0)
    def genPy(self, s, ind):
        self.exceptionList.genPy(s, ind)
#    def genFixObj(self,s,ind): pass
    def genVar(self,s,ind): pass
    
class ExceptionDeclsListPyGen:
    def genPy(self, s, ind):
        for excDecl in self.kidsNoSep():
            excDecl.genPy(s, ind)    

class VariableDeclsPyGen:
    def genPy(self,s,ind): pass
    def genCapClassDecl(self,s,ind): pass
    def genInterface(self,s,forMod): pass
    def genVar(self,s,ind):
        for decl in self.variables.kidsNoSep():
            decl.genPy(s,ind)
    def genCapsule(self,s,ind): pass
    def genCapInitDecl(self,s,ind): pass

class VariableDeclsListPyGen: pass

class ProcedureHeadPyGen: pass

class ProcedureDeclPyGen:
    def genInterface(self,s,forMod):
        pname = self.procHead.name.idname
        formlist = self.procHead.signature.formals.genPy()
        #print "self.procHead.signature.formals", self.procHead.signature.formals
        tmp = self.procHead.getType()
        varlist = string.join(self.procHead.signature.formals.getNameOrder(),",")
        if not forMod:
            modname = self.getTopNode().modname.idname
        else:
            modname = forMod.modname.idname    
        s.write("""
def %s(%s):
    import %sMod
    return %sMod.%s(%s)
""" %(pname,formlist,modname,modname,pname,varlist))
        s.write("M3ProcLib.enter('%s',%s)\n" % (self.getStamp(), pname))

    def genPy(self,s,ind):
        if self.procBlock.isNULL(): return
        pname = self.procHead.name.idname
        formlist = self.procHead.signature.formals.genPy()
        if self.parent.isCapsuleEntity():
            prefix = "self, "
        else:
            prefix = ""
        s.write("%sdef %s(%s%s):\n" % (sp(ind), pname, prefix, formlist))
        s.write("%sM3incStat('CALL','%s')\n" % (sp(ind+1), pname))
        s.write("%stry:\n" % sp(ind+1))
        self.valueDupe(s,ind+2)
        self.narrowObjs(s,ind+2);
        self.procBlock.genPy(s,ind+2)
        if not self.procHead.signature.tipe.isNULL():
            s.write("%sraise M3Objects.M3FunctionNoReturnError\n" % sp(ind+2))

        # Handle returns
        s.write("%sexcept M3Objects.M3ReturnException, e:\n" % sp(ind+1))
        s.write("%sreturn e.retval\n" % sp(ind+2))
        
        # Handle user defined exception propagation
        raises = self.procHead.signature.raises
        s.write("%sexcept M3Types.M3ExceptionType, e:\n" % sp(ind+1))

        # Any raises everything for the caller
        if (not raises.isNULL()) and raises.isAny():
            s.write("%sraise\n" % sp(ind+2))
            return

        # Otherwise only raise those in the raiseList
        if raises.isNULL():
            raiseList = ""
        else:
            raiseList = self.procHead.signature.raises.genPy()
        s.write("%sif e in [%s]:\n" % (sp(ind+2), raiseList))
        s.write("%sraise\n" % sp(ind+3))
        s.write("%selse:\n" % sp(ind+2))
        if Options.options.raiseUnhandled:
            s.write("%sraise # compiled with -X\n" % sp(ind+3))
        else:
            s.write("%sraise M3Objects.M3UnhandledException(e)\n" % sp(ind+3))
        s.write("%sM3ProcLib.enter('%s',%s)\n" % (sp(ind), self.getStamp(), pname))

    def genCapClassDecl(self,s,ind):
        self.genPy(s,ind)
    def genCapInitDecl(self,s,ind): pass

#    def genCapsule(self,s,ind):
#        pname = self.procHead.name.idname
#        formlist = self.procHead.signature.formals.genPy()
#        s.write("%sdef %s(self, %s):\n" % (sp(ind), pname, formlist))
#        self.procBlock.genPy(s,ind+1)        

    def gatherVar(self, ind): return ''

    def narrowObjs(self,s,ind):
        for entry in self.procHead.signature.formals.getTable():
            tipe = entry.getTipe()
            if tipe.isObject:
                s.write("%s%s=%s.getNarrowed(%s)\n" % (
                    sp(ind), entry.name, entry.name, entry.node.genPy()))


    def valueDupe(self,s,ind):
        for entry in self.procHead.signature.formals.getTable():
            if entry.mode == "VALUE" and (not entry.getTipe().isProcedure):
                s.write("%s%s=%s.dupe()\n" % (sp(ind), entry.name, entry.name))

#    def genFixObj(self,s,ind): pass
    def genVar(self,s,ind): pass    

class SignaturePyGen: pass

class MethodSignaturePyGen: pass

class FormalsPyGen:
    def genPy(self):
        return string.join([kid.genPy() for kid in self.kidsNoSep()],",")

class FormalPyGen:
    def genPy(self):
        # TBD you need to deal with modes here somewhere
        res = []
        for id in self.idList.kidsNoSep():
            if self.constExpr.isNULL():
                res.append(id.idname)
            else:
                res.append("%s=%s" % (id.idname, self.constExpr.genPy()))
        return string.join(res,",")
    def addFormalEntry(self, protoModule):
        entry = ""
        # TBD Fixme nasty hack to cope with the case where these type names
        # are local to the module which defined the protocol
        #

        defNode = self.tipe.getEntry().node
        if defNode and defNode.getTopNode().modname.idname == protoModule:
            pref = protoModule + "."
        else:
            pref = ""
        for id in self.idList.kidsNoSep():
            # OK this is not a real dict any more, because we need to deal with positionals too
            entry += "('%s', %s%s)," % (id.idname, pref, self.tipe.genPy())
        return entry
class RevealsPyGen:
    def genInterface(self,s,formod):
        self.revealsList.genPy(s,0)
    def genPy(self,s,ind):
        self.revealsList.genPy(s,ind)
#    def genFixObj(self,s,ind):
#        self.revealsList.genFixObj(s,ind)
    def genVar(self,s,ind): pass


class RevealsListPyGen:
    def genPy(self,s,ind):
        for kid in self.kids:
            kid.genPy(s,ind)
        
#    def genFixObj(self,s,ind):
#        for kid in self.kids:
#            kid.genFixObj(s,ind)
    

class RevealPyGen:

#    def genFixObj(self,s,ind):
#        if hasattr(self.tipe,"genFixObj"):
#            s.write("%s%s.%s" % (sp(ind), self.qualid.image(), self.tipe.genFixObj()))

        
    def genPy(self,s,ind):
        # for each reveal generate a file : Reveal<ModuleName>_<TypeName>
        # containing a function revealType()
        # which loads this modules pickle and returns the type with the code of this item
        #
        # TBD no checking yet that there have not been multiple reveals

        if self.sign == "<:": return
        # partial revelations are only interesting at compile time (to see what more is allowed)
        # and at link time (to check that everything is OK
        
        f = open(Options.options.library + os.sep + "Reveal%s_%s.py" % (
            self.getTopNode().modname.idname, self.qualid.image()),"w")
        f.write("""
import M3TypeLib
def revealType():
    M3TL=M3TypeLib.internaliseTypes(r'%s')
    return M3TL[%s].finalTipe
""" % (self.getTopNode().getBaseName(), self.typeCode))
        f.close()



class GenFormalsPyGen: pass

class GenActualsPyGen: pass

class ConstDeclPyGen:
    def genPy(self,s,ind):
        initval = "%s" % self.constExpr.genPy()
#       Deal with anon types here later (is there any such thing as an anonymous type for a constant - what would it mean?)
        if self.isCapsuleEntity():
            prefix = "self."
        else:
            prefix = ""
        if self.tipe.isNULL():
            constval = initval
        else:
            typename = self.tipe.qualId.image()
            if self.tipe.getType().predef:
                constval = self.getType().pyTypeName("%s.val" % initval)
            else:
                constval = "%s.createObject(%s.val)" % (typename, initval)
        s.write("%s%s%s=%s\n" % (sp(ind), prefix, self.id.idname, constval))
    def genCapClassDecl(self,s,ind): pass
    def genCapInitDecl(self,s,ind):
        self.genPy(s,ind)

class TypeDeclPyGen:
    def genInterface(self,s,forMod):
        self.genPy(s,0)
    def genPy(self,s,ind):
        # capsules are defined as classes and are thus a special case
#        if self.tipe.getType().isCapsuleBody:
#            self.tipe.genPy(s,ind,self.id.idname)
        if self.sign.token == "=":
            if self.isCapsuleEntity():
                prefix = "self."
            else:
                prefix = ""
            res = self.tipe.genPy()
            if res:
                s.write("%s%s%s=%s\n" % (sp(ind), prefix, self.id.idname, res))
        elif self.sign.token == "<:":
            s.write("%simport Reveal%s_%s\n" % (sp(ind), self.getTopNode().modname.idname, self.id.idname))
            s.write("%s%s = Reveal%s_%s.revealType()\n" % (sp(ind), self.id.idname, self.getTopNode().modname.idname, self.id.idname))
        else:
            raise "compiler bug"
    def genCapClassDecl(self,s,ind): pass
    def genCapInitDecl(self,s,ind): self.genPy(s,ind)

class ExceptionDeclPyGen:
    def genPy(self,s,ind):
        if self.isNamedType():
            return "M3TL[%s].finalTipe" % self.typeCode
        else:
            s.write("%s%s=M3Types.M3ExceptionType('%s')\n" % (sp(ind), self.id.idname, self.id.idname))

class VariableDeclPyGen:
    def genInterface(self,s,forMod):
        self.genPy(s,0)
    def genPy(self,s,ind):
        initval = ""
        if not self.expr.isNULL():
            initval = self.expr.genPy()
            if not self.expr.getExprType().isProcedure:
                initval += ".val"
#       Deal with anon types here later
        if self.tipe.isNULL():
            valstr = self.expr.genPy()
        else:
            if self.tipe.__class__.__name__ == "TypeNameNode":
                typename = self.tipe.qualId.image()
                if self.tipe.qualId.getEntry().isIvar:
                    typename = "self." + typename
                #print typename
                if self.getType().predef:
                    valstr = self.vartype.pyTypeName(initval)
                elif self.getType().isCapsuleBody:
                    pass # we do this at the end now because we need the id value
                else:
                    valstr="%s.createObject(%s)" % (typename, initval)
            else:
                # type is anonymous
                valstr = "%s.createObject(%s)" % (self.tipe.genPy(), initval)
        if self.isCapsuleEntity():
            prefix = "self."
        else:
            prefix = ""
        for id in self.idlist.kidsNoSep():
            if self.getType().isCapsuleSpec:
                valstr="CapsuleMap.createCapsule(self.__level+1,'%s',self.runtimeName+'.'+'%s')" % (typename,id.idname)
            s.write("%s%s%s=%s\n" % (sp(ind), prefix, id.idname, valstr))
    def gatherVar(self,s,ind):
        self.genPy(s,ind)


class RaisesPyGen:
    def genPy(self):
        return self.raiseList.genPy()

class RaisesListPyGen:
    def genPy(self):
        return string.join([raiseElem.image() for raiseElem in self.kidsNoSep()],",")

class RaisesAnyPyGen: pass

class StatementsPyGen:
    def genPy(self,s,ind):
        if len(self.kidsNoSep()) == 0:
            s.write("%spass\n" % sp(ind))
        else:
            for statement in self.kidsNoSep():
                statement.genPy(s,ind)

class AssignStPyGen:
    def genPy(self,s,ind):
        s.write("%s%s.assign(%s)\n" % (sp(ind), self.lhs.genPy(), self.rhs.genPy()))

class CallStPyGen:
    def genPy(self,s,ind):
        s.write("%s%s\n" % (sp(ind),self.expr.genPy()))

class ReplyStPyGen:
    def genPy(self,s,ind):
        s.write("%sM3incStat('REPLY','%s')\n" % (sp(ind), self.expr.regen()))
        s.write("%s%s\n" % (sp(ind),self.expr.genPy()))
        

class SendStPyGen:
    def genPy(self,s,ind):
        target,msgName = self.expr.expr.genSendTarget()
        s.write("%sM3incStat('SEND','%s')\n" % (sp(ind), msgName))
        if self.after.afterExpr.isNULL():
           afterString = "0"
        else:
            afterString = "%s.val" % self.after.afterExpr.genPy()
        s.write("%s%s.sendAfter(self, self.__level, '%s', %s, %s)\n" % (sp(ind),target,msgName,afterString,self.expr.genSend()))

class SynCallStPyGen:
    def genPy(self,s,ind):
        target,msgName = self.expr.expr.genSendTarget()
        s.write("%s%s.call('%s', %s)\n" % (sp(ind),target,msgName,self.expr.genSend()))

class AssertStPyGen:
    def genPy(self,s,ind):
        details = "%s:%s" % getLocation(self)
        exprText = self.expr.regen().replace("\n"," ")
        s.write("%sM3Predefined.M3Assert(%s,'%s','%s')\n" % (sp(ind), self.expr.genPy(),details,exprText))
        
class PythonStPyGen:
    def genPy(self,s,ind):
        s.write("%s%s #inserted via PYTHON statement\n" % (sp(ind), self.pythonText.token[1:-1]))
class ResetStPyGen:
    def genPy(self,s,ind):
        if self.level.isNULL():
            level = "0"
        else:
            level = "%s.val" % self.level.genPy()
        s.write("%sself.M3Reset(%s)\n" % (sp(ind), level))
class CaseStPyGen:
    def genPy(self,s,ind):
        casevar = "M3CaseVar%s" % self.refid
        s.write("%s%s=%s\n" % (sp(ind), casevar, self.expr.genPy()))
        s.write("%sif False: pass\n" % sp(ind))
        self.caseElts.genPy(s,ind,casevar)
        if not self.elseStatements.isNULL():
            s.write("%selse:\n" % sp(ind))
            self.elseStatements.genPy(s,ind+1)
                    

class CaseEltListPyGen:
    def genPy(self,s,ind,casevar):
        for kid in self.kidsNoSep():
            kid.genPy(s,ind,casevar)
class VCaseEltListPyGen(CaseEltListPyGen): pass

class CaseEltPyGen:
    def genPy(self,s,ind,casevar):
        s.write("%s%s\n" % (sp(ind), casevar))

class ExitStPyGen:
    def genPy(self,s,ind):
        s.write("%sraise M3Types.M3ExitException\n" % sp(ind))

class EvalStPyGen:
    def genPy(self,s,ind):
        s.write("%s%s\n" % (sp(ind),self.expr.genPy()))

class ForStPyGen:
    def genPy(self,s,ind):
        # TBD fix this to deal with enums and steps without raising constraint errors
        if self.byExpr.isNULL():
            incString = "M3Types.M3IntegerBase.createObject(1)"
        else:
            incString = self.byExpr.genPy()
        s.write("%sdef loop%s(%s):\n" % (sp(ind), self.refid, self.forId.idname))
        s.write("%stry:\n" % sp(ind+1))        
        s.write("%swhile True:\n" % sp(ind+2))
        self.statements.genPy(s,ind+3)
        s.write("%sif %s.ord().plus(%s).greater(%s.ord()).toBool(): break\n" % (sp(ind+3), self.forId.idname, incString, self.toExpr.genPy()))
        s.write("%s%s.add(%s)\n" % (
            sp(ind+3), self.forId.idname, incString))
        s.write("%sexcept M3Types.M3ExitException: pass\n" % sp(ind+1))
        initval = "%s.val" % self.startExpr.genPy()
        s.write("%sloop%s(%s)\n" % (
            sp(ind), self.refid, self.startExpr.genPy()))

class IfStPyGen:
    def genPy(self,s,ind):
        s.write("%sif %s.toBool():\n" % (sp(ind), self.ifExpr.genPy()))
        self.ifConsequence.genPy(s,ind+1)
        for elsif in self.elsifList.kids:
            elsif.genPy(s,ind)
        if not self.elseStatement.isNULL():
            s.write("%selse:\n" % sp(ind))
            self.elseStatement.genPy(s,ind+1)
            
            
class ElsifListPyGen: pass

class ElsifPyGen:
    def genPy(self,s,ind):
        s.write("%selif %s.toBool():\n" % (sp(ind), self.elseExpr.genPy()))
        self.elseStatement.genPy(s,ind+1)

class LockStPyGen:
    def genPy(self,s,ind):
        self.statements.genPy(s,ind);

class LoopStPyGen:
    def genPy(self,s,ind):
        s.write("%stry:\n" % sp(ind))
        s.write("%swhile True:\n" % sp(ind+1))
        self.statements.genPy(s,ind+2)
        s.write("%sexcept M3Types.M3ExitException: pass\n" % sp(ind))        

class RaiseStPyGen:
    def genPy(self,s,ind):
        if not self.expr.isNULL():
            raiseExpr = self.expr.genPy()
        else:
            raiseExpr = ""
        s.write("%sraise %s.createObject(%s)\n" % (sp(ind), self.raiseId.genPy(), raiseExpr))

class RepeatStPyGen:
    def genPy(self,s,ind):
        s.write("%stry:\n" % sp(ind))
        s.write("%swhile True:\n" % sp(ind+1))
        self.statements.genPy(s,ind+2)
        s.write("%sif %s.toBool():\n" % (sp(ind+2), self.untilExpr.genPy()))
        s.write("%sraise M3Types.M3ExitException\n" % sp(ind+3))
        s.write("%sexcept M3Types.M3ExitException: pass\n" % sp(ind))
                
class ReturnPyGen:
    def genPy(self,s,ind):
        if not self.expr.isNULL():
            retstr = self.expr.genPy()
        else:
            retstr = ""
        s.write("%sraise M3Objects.M3ReturnException, %s\n" % (sp(ind), retstr))


class TCaseStPyGen:
    def genPy(self,s,ind):
        caseVar = "M3TCaseVar%s" % self.refid
        s.write("%s%s=%s\n" % (sp(ind), caseVar, self.expr.genPy()))
        s.write("%sif False: pass\n" % sp(ind))
        self.tCaseList.genPy(s,ind,caseVar)
        if not self.elseStatement.isNULL():
            s.write("%selse:\n" % sp(ind))
            self.elseStatement.genPy(s,ind+1)

class TCaseListPyGen:
    def genPy(self,s,ind,caseVar):
        for case in self.kidsNoSep():
            case.genPy(s,ind,caseVar)

class TryXptStPyGen:
    def genPy(self,s,ind):
        s.write("%stry:\n" % sp(ind))
        self.statements.genPy(s,ind+1)
        s.write("%sexcept M3Objects.M3Exception, M3Target:\n" % sp(ind))
        self.handlerList.genPy(s,ind+1)
        s.write("%selse:\n" % sp(ind+1))
        if self.elseStatement.isNULL():
            s.write("%sraise M3Objects.M3UnhandledException(M3Target)\n" % sp(ind+2))
        else:
            self.elseStatement.genPy(s, ind+2)

class TryFinStPyGen:
    def genPy(self,s,ind):
        s.write("%stry:\n" % sp(ind))
        self.tryStatement.genPy(s,ind+1)
        s.write("%sfinally:\n" % sp(ind))
        self.finallyStatement.genPy(s,ind+1)
class WhileStPyGen: 
    def genPy(self,s,ind):
        s.write("%stry:\n" % sp(ind))
        s.write("%swhile True:\n" % sp(ind+1))
        s.write("%sif not %s.toBool():\n" % (sp(ind+2), self.whileExpr.genPy()))
        s.write("%sraise M3Types.M3ExitException\n" % sp(ind+3))
        self.statements.genPy(s,ind+2)
        s.write("%sexcept M3Types.M3ExitException: pass\n" % sp(ind))



class WithStPyGen:
    def genPy(self,s,ind):
##         if len(self.bindingList.kidsNoSep()) == 1:
##             withProcName = "M3WithProc%s" % self.refid
##             s.write("%sdef %s(%s):\n" % (sp(ind),withProcName,self.bindingList.getFormals()))
##             self.statements.genPy(s,ind+1)
##             s.write("%s%s(%s)\n" % (sp(ind), withProcName, self.bindingList.genPy()))
##         else:
        def climbBindings(bindings,ind):
            binding = bindings[0]
            withProcName = "M3WithProc%s" % binding.refid
            s.write("%sdef %s(%s):\n" % (sp(ind), withProcName, binding.getId()))
            if len(bindings) > 1:
                climbBindings(bindings[1:],ind+1)
            else:
                self.statements.genPy(s,ind+1)
            s.write("%s%s(%s)\n" % (sp(ind), withProcName, binding.genPy()))
        climbBindings(self.bindingList.kidsNoSep(),ind)
        
class BindingListPyGen:
        def genPy(self):
            return string.join([binding.genPy() for binding in self.kidsNoSep()],",")
        def getFormals(self):
            return string.join([binding.getId() for binding in self.kidsNoSep()],",")
class HandlerListPyGen:
    def genPy(self, s, ind):
        # generative sugar added here
        # so that the handlers can all use 'elif' and we can catch the rest with an 'else'        
        s.write("%sif False: pass\n" % sp(ind))
        for handler in self.kidsNoSep():
            handler.genPy(s, ind)

class IdPyGen: pass

class ForIdPyGen: pass

class BindingIdPyGen: pass

class TCaseIdPyGen: pass

class IntPyGen: pass

class LabelsListPyGen:
    def genPy(self,casevar):
        return string.join([label.genPy(casevar) for label in self.kidsNoSep()]," or ")

class LabelsPyGen:
    def genPy(self,casevar):
        if self.length() == 1:
            return "%s.equals(%s).toBool()" % (casevar, self.kids[0].genPy()) 
        elif self.length() == 3:
            
            return "(%s.greatereq(%s).toBool() and %s.lesseq(%s).toBool())" % (
                casevar, self.kids[0].genPy(), casevar, self.kids[2].genPy())  
        else: raise "compiler anomaly : utter madness"             
            

class CasePyGen:
    def genPy(self,s,ind,casevar):
        
        s.write("%selif %s:\n" % (sp(ind), self.labelList.genPy(casevar)))
        self.statements.genPy(s,ind+1)

class VCasePyGen(CasePyGen): pass
class HandlerPyGen:
    def genPy(self, s, ind):
        s.write("%selif M3Target.tipe in [%s]:\n" % (sp(ind), self.qualidList.genPy())) # TBD what about that id ?
        handlerProcName = "M3Handler%s" % self.refid
        if self.id.isNULL():
            handlerId = "M3Dummy"
        else:
            handlerId = self.id.idname
        s.write("%sdef %s(%s):\n" % (sp(ind+1),handlerProcName,handlerId))
        self.statement.genPy(s,ind+2)
        s.write("%s%s(M3Target.val)\n" % (sp(ind+1), handlerProcName))

class HandlerQualidListPyGen:
    def genPy(self):
        return string.join([id.genPy() for id in self.kidsNoSep()],",")

class TypeListPyGen:
    def genPy(self):
        res = string.join([kid.genPy() for kid in self.kidsNoSep()],",")
        return "[%s]" % res

class TCasePyGen:
    def genPy(self,s,ind,caseVar):
        s.write("%selif %s.tipe.fitsTCase(%s):\n" % (sp(ind), caseVar, self.qualidList.genPy()))
        tCaseProcId = "M3TCaseProc%s" % self.refid
        if self.id.isNULL():
            tCaseId = "M3Wasted"
        else:
            tCaseId = self.id.idname
        s.write("%sdef %s(%s):\n" % (sp(ind+1), tCaseProcId, tCaseId))
        self.statement.genPy(s,ind+2)
        if self.qualidList.length() != 1: raise "compiler bug"
        targetType = self.qualidList.kids[0]
        if targetType.getType().isObject:
            s.write("%s%s(%s.getNarrowed(%s))\n" % (sp(ind+1),tCaseProcId,caseVar,targetType.genPy()))
        else:
            s.write("%s%s(%s)\n" % (sp(ind+1), tCaseProcId, caseVar))


class BindingPyGen:
    def genPy(self):
        return "%s=%s" % (self.id.idname, self.expr.genPy())
    def getId(self):
        return self.id.idname
class ActualExprPyGen:
    def genPy(self):
        if self.id.isNULL():
            return "%s" % self.expr.genPy()
        else:
            return "%s=%s" % (self.id.idname, self.expr.genPy()) 

class ActualPyGen: pass
class ArrayPyGen:
    def genPy(self):
        if self.isNamedType():
            return "M3TL[%s].finalTipe" % self.typeCode
        else:
            eltType = self.tipe.genPy()
            indices = self.typeList.genPy()
            return "M3Types.M3ArrayType(elementType=%s,indices=%s)" % (eltType, indices)

class PackedPyGen: pass

class BracketedTypePyGen:
    def genPy(self):
        return self.tipe.genPy()

class EnumPyGen:
    def genPy(self):
        if self.isNamedType():
            return "M3TL[%s].finalTipe" % self.typeCode
        else:
            name = self.parent.id.idname 
            return self.getType().pyTypeName(
                name,
                string.join(["'%s'" % item.idname for item in self.idlist.kidsNoSep()],","))



class ObjectPyGen:
    def genPy(self):
        if not self.isNamedType(): raise "Code gen restriction : anon objects not supported"
        return "M3TL[%s].finalTipe" % self.typeCode

class ObjectListPyGen: pass

class ProcedurePyGen:
    def genPy(self):
        return "M3Types.M3ProcedureHolderType()"   # procedure type of some type

class RecordPyGen:
    def genPy(self):
        if self.isNamedType():
            return "M3TL[%s].finalTipe" % self.typeCode
        else:
            return "M3Types.M3RecordType([%s])" % self.fields.genPy()

class VariantRecordPyGen(RecordPyGen): pass

class RefPyGen:
    def genPy(self):
        if self.isNamedType():
            return "M3TL[%s].finalTipe" % self.typeCode
        else:
            referent = self.tipe.genPy()
        return "M3Types.M3RefType(%s)" % referent

    
class SetPyGen:
    def genPy(self):
        if self.isNamedType():
            return "M3TL[%s].finalTipe" % self.typeCode
        else:
            error("anonymous sets not supported yet");

class SubrangePyGen:
    def genPy(self):
        if self.isNamedType():
            return "M3TL[%s].finalTipe" % self.typeCode
        
        tipe = self.getType()
        if tipe.isNumeric:
            return "M3Types.%s((%s,%s))" % (tipe.baseType(), tipe.first, tipe.last)
        elif tipe.isEnum:
            # get the expression to create an object of the base class
            base1 = self.const1.genPy()
            base2 = self.const2.genPy()
            return "%s.tipe.createSubType(%s.val,%s.val)" % (base1, base1, base2)
        elif tipe.isChar:
            base1 = self.const1.genPy()
            base2 = self.const2.genPy()
            return "M3Types.M3Char.createSubType(%s.val,%s.val)" % (base1, base2)            
        else:
            error("subranges only allowed for numeric, char and enum types (How the hell did this get through??)", self)

class BrandPyGen: pass

# TBD (we don't need this when we stop generating code for Objects altogether : currently none generated
# because we don't do anonymous objects)

class FieldListPyGen:
    def genPy(self):
        return string.join([kid.genPy() for kid in self.kidsNoSep()],",")

class FieldPyGen:
    def genPy(self):
#        raise "hell"        
        tipe = self.tipe.genPy()
        if self.constExpr.isNULL():
            default = "None"
        else:
            default = self.constExpr.genPy()
        res = string.join(["M3Types.Field('%s', %s, %s)" % (id.idname, tipe, default) for id in self.idlist.kidsNoSep()],",")
        return res

class MethodListPyGen:
    def genPy(self):
        res = string.join([kid.genPy() for kid in self.kids],",")
        return res

class MethodPyGen: 
    def genPy(self):
        return "M3Types.Field('%s', None, %s)" % (self.name.idname, self.expr.genPy())

class OverrideListPyGen:
    def genPy(self):
        res = string.join([kid.genPy() for kid in self.kids],",")        
        return res

class OverridePyGen: 
    def genPy(self):
        return "M3Types.Field('%s', None, %s)" % (self.id.idname, self.expr.genPy())

class ConstExprPyGen:
    def genPy(self):
        return self.expr.genPy()

class BracketedExprPyGen:
    def genPy(self):
        return self.expr.genPy()
        # Brackets not needed here because we use object-call notation for all exprs

class BinaryExprPyGen:
    def genPy(self):
        return self.expr.genPy() + self.exprList.genPy()

class UnaryExprPyGen:
    def genPy(self):
        return self.opList.genPy(self.expr.genPy())

class OpExpPyGen:
    def genPy(self):
        return ".%s(%s)" % (self.operator.genPy(), self.expr.genPy())


class ObjMsgConstructor:
    def constructObjMsg(self,endPoint):
        capInt = self.getTopNode().getType().spec
        endLen = len(endPoint)
        if endLen == 1:
            Obj = "self"
            portName = capInt.getPortOfMessage(endPoint[0]).name
            Msg = "%s.%s" % (portName,endPoint[0])

        elif endLen == 2:
            # is this port.message or child.message ?
            if endPoint[0] in capInt.portDict:
                #print "port.message", endPoint 
                Obj = "self"
                Msg = "%s.%s" % (endPoint[0],endPoint[1])
            else:
                #print "child.message", endPoint
                # child.message (so we have to find the port)
                Obj = "self.%s" % endPoint[0]
                childSpec = self.getLUT().lookup(endPoint[0])
                portName = childSpec.getPortOfMessage(endPoint[1]).name
                Msg = "%s.%s" % (portName,endPoint[1])
        elif endLen == 3:
            # child.port.message
            Obj = "self.%s" % endPoint[0]
            Msg = "%s.%s" % (endPoint[1], endPoint[2])
        else:
            raise "compiler bug : more than than three ids in connection endpoint qualid"
        return Obj,Msg

    def isEntity(self,name):
        entry = self.getLUT().lookupEntry(name)
        entryName = entry.node.__class__.__name__
        return entryName in ['TransitionDeclNode', 'ActivityDeclNode', 'ProcedureDeclNode']



class SelectorExprPyGen(ObjMsgConstructor):
    def genPy(self):
        res = self.expr.genPy()
        for sel in self.selectorList.kids:
            res += sel.genPy()
        return res

    def genSendTarget(self):
        idsOnly = self.expr.qualId.idList()
        # see ObjMsgConstructor for child.port.msg disambiguation logic
        if len(idsOnly) == 1 and self.isEntity(idsOnly[0]):
            obj = "self"
            msg = idsOnly[0]
        else:
            obj,msg = self.constructObjMsg(idsOnly)
        return obj,msg
##         if len(idsOnly) == 1:
##             return "self",  idsOnly[0]
##         elif len(idsOnly) == 2:
##             return ("self.%s" %  idsOnly[0]), idsOnly[1]
##         else:
##             raise "compiler bug, bad qualid for send: %s" % self.expr.qualId.image()
        
    def genSend(self):
        if self.selectorList.length() > 1:
            error("SEND can only be a single selector", self)
        return self.selectorList.kids[0].genSend()

class SelectorListPyGen: pass

class ExprListPyGen:
    def genPy(self):
        return string.join([kid.genPy() for kid in self.kids],"")
    
class ExprPyGen: 
    def genPy(self):
        return self.expr.genPy()
    def genSend(self):
        return self.expr.genSend()
class OpPyGen:
    def genPy(self):
        myOp = self.token
        opdict = {"+": "plus","-": "minus","*": "times","/": "divide", "=": "equals",
                  "#": "notequals", ">": "greater", "<": "less",
                  ">=": "greatereq", "<=": "lesseq", "AND": "opand", "OR": "opor",
                  "MOD": "mod", "DIV": "divide", "&": "concat", "IN": "isIn"}
        if myOp in opdict:
            return opdict[myOp]
        else:        
            return error("unhandled operator %s" % myOp, self)
    def genPyUnary(self):
        myOp = self.token
        opdict = {"+": "unplus","-": "unminus", "NOT": "opnot"}
        if myOp in opdict:
            return opdict[myOp]
        else:
            return error("unhandled operator %s" % myOp, self)
        
class OpListPyGen:
    def genPy(self, expr):
        rkids = self.kids[:]
        rkids.reverse()
        res = expr
        for op in rkids:
            res += ".%s()" % op.genPyUnary()
        return res
            

class CaretPyGen:
    def genPy(self):
        return ".getRef()"

class DotPyGen:
    def genPy(self):
        return ".getField('%s')" % self.id.idname
class ArrayRefSelectorPyGen:
    def genPy(self):
        return self.exprList.genPy()
#        for kids in self.exprList.kids:
#        return ".getElement(%s)" % self.exprList.genPy()

class ProcCallSelectorPyGen:
    def genPy(self):
        return "(" + self.actualList.genPy() + ")"
    def genSend(self):
        return self.actualList.genPy()

class ActualListPyGen:
    def genPy(self):
        #print self.kids
        #for actual in self.kids:
        #    print ">" + str(actual.expr.genPy)
        actualStrings = [actual.genPy() for actual in self.kidsNoSep()]
        return string.join(actualStrings,",")

class IndexListPyGen:
    def genPy(self):
        return string.join([".getElement(%s)" % kid.genPy() for kid in self.kidsNoSep()],"")

class ConstructorPyGen:
    def genPy(self):
        tipe = self.tipe.genPy()
        elts = string.join([elt.genPy() for elt in self.consEltList.kidsNoSep()],",")
        if self.tipe.getType().isDict:
            return "%s.construct({%s})" % (tipe, elts)
        else:
            return "%s.construct(%s)" % (tipe, elts)

class ConsEltDictPyGen:
    def genPy(self):
        return "%s:%s" %  (self.t.token, self.expr.genPy())
class ConsEltListPyGen: pass

class ConsEltAssPyGen:
    def genPy(self):
        return "%s=%s" % (self.id.idname, self.expr.genPy())

class ConsEltRangePyGen:
    def genPy(self):
        return "(%s,%s)" % (self.startExpr.genPy(), self.endExpr.genPy())

class ConsEltExprPyGen:
    def genPy(self):
        return "%s" % self.expr.genPy()

class ConsEltDotdotPyGen:
    def genPy(self):
        return '"DOTDOT"'

PredefTable = {
    "ABS":  "M3Predefined.M3ABS",
    "APPEND": "M3Predefined.M3APPEND",
    "CARDINAL": "M3Types.M3Cardinal",
    "DEC": "M3Predefined.M3DEC",
    "DEL": "M3Predefined.M3DEL",
    "DISPOSE": "M3Predefined.M3DISPOSE",
    "FALSE": "M3Types.M3Boolean.withVal('FALSE')",
    "FIRST": "M3Predefined.M3FIRST",
    "FLOAT": "M3Predefined.M3FLOAT",    
    "INC": "M3Predefined.M3INC",
    "INDEX": "M3Predefined.M3INDEX",
    "IMAGE": "M3Predefined.M3IMAGE",
    "KEYS": "M3Predefined.M3KEYS",    
    "LAST": "M3Predefined.M3LAST",
    "NARROW": "M3Predefined.M3NARROW",
    "NUMBER": "M3Predefined.M3NUMBER",    
    "MAX": "M3Predefined.M3MAX",
    "MIN": "M3Predefined.M3MIN",    
    "NEW": "M3Predefined.M3RefNEW",
    "NIL": "M3Objects.M3Nil",
    "NULL": "M3Types.M3Null",
    "MUTEX": "M3Types.M3Null",        
    "ORD": "M3Predefined.M3ORD",
    "POP": "M3Predefined.M3POP",
    "REFANY": "M3Types.M3RefAny",
    "ROOT": "M3Types.M3Root",
    "SUBARRAY": "M3Predefined.M3SUBARRAY",
    "TRUE": "M3Types.M3Boolean.withVal('TRUE')",
    "TYPECODE": "M3Predefined.M3TYPECODE",
    "ISTYPE": "M3Predefined.M3ISTYPE",
    "VAL": "M3Predefined.M3VAL",
    "ROUND": "M3Predefined.M3ROUND",
    "TRUNC": "M3Predefined.M3TRUNC",
    "FLOOR": "M3Predefined.M3FLOOR",
    "CEILING": "M3Predefined.M3CEILING",    
    
    "ConstraintError": "M3Predefined.M3ConstraintError",
    "DivideByZeroError": "M3Predefined.M3DivideByZeroError",
    "UninitialisedError": "M3Predefined.M3UninitialisedError",
    "NullPointerError": "M3Predefined.M3NullPointerError",
    "AssertError": "M3Predefined.M3AssertError",
}


class QualIdPyGen:
    def genPy(self):

        # deal with special case port object passed as callback parameter (yes, this IS a dirty hack)
        if self.getType().isPort:
            return "RTSTypes.M3RunTimeCallBackType(self,'%s')" % self.image()

        self.embeddedImplicitDerefs = []
        idsOnly = self.kidsNoSep()
        # prepend a "self" if this is an instance variable (e.g. belongs to a capsule)        
        if self.getBaseEntry().isIvar:
            prefix = "self."
        else:
            prefix = ""
        
        if len(idsOnly) == 1:
            image = self.image()
            if image in PredefTable.keys():
                return PredefTable[image]
            else:
                return prefix + image

        lut = self.getLUT()



        # deal with special case use of BOOLEAN.TRUE and BOOLEAN.FALSE
        if len(idsOnly) == 2:
            left = idsOnly[0].idname
            right = idsOnly[1].idname
            lefttype = lut.lookup(left)
            if left == "BOOLEAN":
                left = "M3Types.M3Boolean"
            return prefix + left + lefttype.derefString(right)
        else:
            # Noodle your way through a whole series of dereferencing
            # first prime the pump
            res = idsOnly[0].idname
            ctr = 1
            tipe = lut.lookupEntry(res)
            # and then set it rolling
            while ctr < len(idsOnly):
                #print ctr, tipe, res
                tipe = tipe.getTipe()
                res += tipe.derefString(idsOnly[ctr].idname)
                tipe = tipe.deref(idsOnly[ctr].idname, self)
                #print ctr, tipe, res
                ctr += 1    
            return prefix + res
        
class RevealQualIdPyGen: pass

class TypeNamePyGen:
    def genPy(self):
        name = self.qualId.genPy()
        predefs = {"INTEGER": "M3Types.M3IntegerBase",
                   "REAL":    "M3Types.M3RealBase",
                   "LONGREAL": "M3Types.M3RealBase",
                   "TEXT":    "M3Types.M3Text",
                   "BOOLEAN": "M3Types.M3Boolean",
                   "CHAR":    "M3Types.M3Char",
                   "CARDINAL": "M3Types.M3Cardinal", }
                   
        if name in predefs:
            return predefs[name]
        else:
            return name
        
class RootPyGen: pass

class UntracedRootPyGen: pass

class NumberPyGen:
    def genPy(self):
        res = self.intVal.intname
        if self.numberRest.isNULL():
            if self.scaleMult > 1:
                res += " * %s" % self.scaleMult
            return "M3Types.M3IntegerBase.createObject(%s)" % res
        else:
            res += "." + self.numberRest.intname
            return "M3Types.M3RealBase.createObject(%s)" % res

class CharLiteralPyGen:
    def genPy(self):
        return "M3Types.M3Char.createObject(%s)" % self.token
 
class TextLiteralPyGen:
    def genPy(self):
        return "M3Types.M3Text.createObject(%s)" % self.token

class KeyWordPyGen:
    def genPy(self):
        return OpPyGen.genPy(self)

class NullPyGen: pass

class ActivityDeclPyGen:
    def genPy(self,s,ind):
        self.activityHead.genPy(s,ind)
        self.handlerBlock.genPy(s,ind+1)
        self.after.genPy(s,ind+1,self)
    def genVar(self,s,ind): pass
    def genCapClassDecl(self,s,ind): self.genPy(s,ind)
    def genCapInitDecl(self,s,ind): pass
        
class ActivityHeadPyGen:
    def genPy(self,s,ind):    
        pname = self.name.idname
        formlist = self.signature.formals.genPy()
        s.write("%sdef %s(self, %s):\n" % (sp(ind), pname, formlist))
        s.write("%sM3incStat('RECEIVE','%s')\n" % (sp(ind+1), pname))
# -- None of these should ever be generated
class PortPyGen: pass
class MessageGroupPyGen: pass
class MessageGroupListPyGen: pass
class MessagePyGen:
    def genFormalTable(self,protoModule):
        table = ""
        for formal in self.signature.formals.kidsNoSep():
            table += formal.addFormalEntry(protoModule)
        return "(" + table + ")"
class MessageListPyGen: pass
class PortListPyGen: pass

class TimerModifierListPyGen: pass
class TriggerPyGen:
    def genCapClassDecl(self,s,ind):
        self.triggerProcName = "M3TriggerProc%s" % self.refid
        s.write("%sdef %s(self):\n" % (sp(ind), self.triggerProcName))
        s.write("%sreturn %s\n" % (sp(ind+1), self.triggerExpr.genPy()))
    def genCapInitDecl(self,s,ind): 
        s.write("%sself.%s = RTSTypes.M3TriggerType(self.%s)\n" % (
            sp(ind), self.triggerId.idname, self.triggerProcName))
    def genPy(self,s,ind): pass
    def genVar(self,s,ind): pass
class TimerPyGen:
    def genPy(self):
        if self.delayExpr.isNULL():
            delay = "None"
        else:
            delay = self.delayExpr.genPy()
        return "RTSTypes.M3TimerRuntimeType(delay=%s,periodic=%s,changeable=%s)" % (
            delay, self.periodic, self.changeable)
    
class ConnectionsPyGen:
    def genPy(self,s,ind):
        self.connectionList.genPy(s,ind)
class ConnectionListPyGen:
    def genPy(self,s,ind):
        for connection in self.kidsNoSep():
            connection.genPy(s,ind)

class PortConnectionPyGen(ObjMsgConstructor):
    def genPy(self,s,ind):
        # This could be boiled down even more but would then probably loose any clarity it might now have
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
                    startObj = "self.%s" % child2
                    startMsg = "%s.%s" % (port2,messageName)
                    endObj = "self.%s" % child1
                    endMsg = "%s.%s" % (port1,messageName)                    
                else:
                    # across,OUT IN
                    startObj = "self.%s" % child1
                    startMsg = "%s.%s" % (port1,messageName)                    
                    endObj = "self.%s" % child2
                    endMsg = "%s.%s" % (port2,messageName)
            else:                
                if mtype.dir == "INCOMING":
                    
                    if self.end1l == 1:
                        # updown,IN IN,par->child
                        startObj = "self"
                        startMsg = "%s.%s" % (port1,messageName)
                        endObj = "self.%s" % child2
                        endMsg = "%s.%s" % (port2,messageName)
                    else:
                        # updown,IN IN,child->par
                        startObj = "self"
                        startMsg = "%s.%s" % (port2,messageName)
                        endObj = "self.%s" % child1
                        endMsg = "%s.%s" % (port1,messageName)
                        
                else:
                    if self.end1l == 1:
                        # updown,OUT OUT,par->child                        
                        startObj = "self.%s" % child2
                        startMsg = "%s.%s" % (port2,messageName)
                        endObj = "self" 
                        endMsg = "%s.%s" % (port1,messageName)
                        
                    else:
                        # updown,OUT OUT,child->par                        
                        startObj = "self.%s" % child1
                        startMsg = "%s.%s" % (port1,messageName)
                        endObj = "self" 
                        endMsg = "%s.%s" % (port2,messageName)
            s.write("%s%s.connect(self,'%s','%s',%s,self.__level)\n" % (sp(ind),startObj,startMsg,endMsg,endObj))                    
class ConnectionPyGen(ObjMsgConstructor):
    def genPy(self,s,ind):
        # form can be either
        # 1 messageName/entityName
        #   1.1 end1 entities can be Timer or Trigger
        #   1.2 end2 entities can be Transition or Activity or Procedure
        # 2 portName.messageName
        # 3 childName.messageName
        # 4 childName.portName.messageName
        
        if self.source.isProcedure:
            startObj,startMsg = self.constructObjMsg(self.end1.idList())
        else: # Trigger or Timer
            startMsg = "" # the message is just an anonymous occurrence
            startObj = "self." + self.end1.kids[0].idname

        #print "dest is", self.dest
        goalIds = self.end2.idList()
        if len(goalIds) == 1 and self.isEntity(goalIds[0]):
            endObj = "self"
            endMsg = goalIds[0]
        else:
            endObj,endMsg = self.constructObjMsg(goalIds)

        s.write("%s%s.connect(self,'%s','%s',%s,self.__level)\n" % (sp(ind),startObj,startMsg,endMsg,endObj))

class StateDeclPyGen:
    def genPy(self,s,ind):
        self.transitionList.genPy(s,ind)
    def genVar(self,s,ind):
        pass
    def genCapClassDecl(self,s,ind): self.genPy(s,ind)
    def genCapInitDecl(self,s,ind): pass    

class TransitionListPyGen:
    def genPy(self,s,ind):
        for transition in self.kidsNoSep():
            transition.genPy(s,ind)
class TransitionHeadPyGen:
    def genCatchallHandler(self,s,ind,pname,formlist):
        messageEntry = self.getMessageEntry()
        if not messageEntry.generated:
            # generate the catch-all
            s.write("%sdef %s(self,%s):\n" % (sp(ind), pname, formlist))
            s.write("%sif self.M3State in %s:\n" % (sp(ind+1), messageEntry.stateNames))
            s.write("%sm=getattr(self,'M3%s__'+self.M3State)\n" % (sp(ind+2), pname))
            s.write("%sself.M3TransitionCallHook('%s',self.M3State)\n" % (sp(ind+2),pname))
            s.write("%sm(%s)\n" % (sp(ind+2), formlist))
            s.write("%selse:\n" % sp(ind+1))
            s.write("%sself.M3NoTransitionForMessageInState('%s',self.M3State)\n" % (sp(ind+2),pname))
            s.write("%sself.M3TransitionFinishedHook(self.M3State)\n" % sp(ind+1))
            messageEntry.generated = True
    def genPy(self,s,ind):
        formlist = self.signature.formals.genPy()
        pname = self.name.idname        
        self.genCatchallHandler(s,ind,pname,formlist)
        # generate the specific one for this transition
        s.write("%sdef M3%s__%s(self,%s):\n" % (sp(ind), pname, self.parent.getStateName(), formlist))
        s.write("%sM3incStat('RECEIVE','%s')\n" % (sp(ind+1), pname))
class TransitionDeclPyGen:
    def genPy(self,s,ind):
        self.transHead.genPy(s,ind)
        self.block.genPy(s,ind+1)
        self.after.genPy(s,ind+1,self)
    def genVar(self,s,ind):
        pass
    
class NextStPyGen:
    def genPy(self,s,ind):
        s.write("%sself.M3State='%s'\n" % (sp(ind), self.stateId.idname))
class StartDeclPyGen:
    def genPy(self,s,ind):
        s.write("%sdef M3startCapsule(self):\n" % sp(ind))
        self.statements.genPy(s,ind+1)
        s.write("%sself.M3TransitionFinishedHook(self.M3State)\n" % sp(ind+1))
    def genVar(self,s,ind):
        pass
    def genCapClassDecl(self,s,ind): self.genPy(s,ind)
    def genCapInitDecl(self,s,ind): pass    
    

class CapsuleInterfacePyGen(NonGen): pass
class CapsulePyGen:
    # TBD refactor this back together with module
    def generatePython(self,saveOutput):
        if saveOutput:
            f = open(self.getBaseName() + ".py","w")
        else:
            f = FakeFile()
        f.write("import M3Objects\n")
        f.write("import M3Types\n")
        f.write("import RTSTypes\n")
        f.write("import M3Predefined\n")                
        for imp in self.specNode.imports.kids:
            imp.genPy(f)
        for imp in self.imports.kids:
            imp.genPy(f)
        f.write("import M3TypeLib\n")
        f.write("import M3ProcLib\n")
        f.write("import CapsuleMap\n")
        f.write("from Statistics import M3incStat\n")
        f.write("M3TL=M3TypeLib.internaliseTypes(r'%s')\n" % self.getBaseName())
        # TBD generate the imports from the capsule spec in case they are needed for types
        # which are handed through
        self.usedCapsules.genPy(f,0)
        self.block.genMain(f,self.modname.idname)
        f.write("def runcap():\n")
        f.write("%simport Simulator\n" % sp(1))
        f.write("%sSimulator.run(createCapsule(1,'top'))\n" % sp(1))
        f.write("def createCapsule(level,hName):\n")
        f.write("%sreturn %s(level,hName)\n" % (sp(1), self.modname.idname))
        f.write("if __name__ == '__main__': runcap()\n")        
        f.close()
        
class UseCapsulePyGen: pass
#    def genPy(self,s,ind):
#        pass
#        for usedCapsule in self.idList.kidsNoSep():
#            name = usedCapsule.idname
#            s.write("%sfrom %sCapMod import %s\n" % (sp(ind),name,name))
class UseCapsuleListPyGen:
    def genPy(self,s,ind):
        pass
#        for useCapsule in self.kids:
#            useCapsule.genPy(s,ind)

class DataDependencyPyGen:
    def genPy(self,s,ind): pass
    def genVar(self,s,ind): pass
    def genCapClassDecl(self,s,ind): pass
    def genCapInitDecl(self,s,ind): pass

class SendsDeclPyGen:
    def genPy(self,s,ind): pass
    def genVar(self,s,ind): pass
    def genCapClassDecl(self,s,ind): pass
    def genCapInitDecl(self,s,ind): pass
    
class TokPyGen:
    def genPy(self,s):
        raise "compiler bug"
        
class SepPyGen: pass

class ListPyGen:
    def genPy(self):
        if self.isNamedType():
            return "M3TL[%s].finalTipe" % self.typeCode
        else:
            eltType = self.tipe.genPy()
            return "M3Types.M3ListType(elementType=%s)" % eltType

class DictPyGen:
    def genPy(self):
        if self.isNamedType():
            return "M3TL[%s].finalTipe" % self.typeCode
        else:
            eltType = self.tipe.genPy()
            if self.idx.isNULL():
                idxType="M3Types.M3Text"
            else:
                idxType = self.idx.genPy()
            return "M3Types.M3DictType(indexType=%s,elementType=%s)" % (idxType,eltType)

class ForEachStPyGen:
    def genPy(self,s,ind):
        s.write("%stry:\n" % sp(ind))
        s.write("%sfor %s in %s.iterables():\n" % (sp(ind+1),self.forId.idname,self.listExpr.genPy()))
        self.statements.genPy(s,ind+2)
        s.write("%sexcept M3Types.M3ExitException: pass\n" % sp(ind))
                
        
                
class ProtocolPyGen:
    def genPy(self):
        return "None"

class ConjugatedProtocolPyGen:
    def genPy(self):
        return "None"

class ScaledTypePyGen:
    def genPy(self):
        return "%s.makeScaledType(%s)" % (self.tn.genPy(), self.scaling)
    
class ScaleEltPyGen: pass
class ScaleListPyGen: pass
class AggregatedProtocolPyGen:
    def genPy(self):
        return "None"
class AfterClausePyGen:
    def genPy(self, s, ind,top):
        afters = []
        top.collectAfters(afters)
        #print afters
        if len(afters) == 0:
            return
        elif len(afters) == 1:
            howLong = "%s.val" % afters[0].genPy()
        else:
            maxArgs = string.join(["%s.val" % afterExpr.genPy() for afterExpr in afters],",")
            howLong = "max(%s)" % maxArgs
        s.write("%sself.M3LockProcessor(%s)\n" % (sp(ind), howLong))
