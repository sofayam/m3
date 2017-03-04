from Message import error, warning, info, hasErrors
import string
import os
import re
import Options
import m3
import types
from LUT import LUT, LUTEntry
import M3TypeLib
import M3Types
import SetUtils
import Scaling
import CompilationUnit
import DeclTable
class ConstantValueError(Exception):
    "raised on failure of attempt to derive the constant value of an expression"

class BaseUser:
    "Provides default methods for all nodes in this aspect"
    def createLUT(self): self.hasLUT = False
    def insertLUT(self): pass
    def doCapsuleLUT(self): pass
    def dumpLUT(self): pass
    def getLUT(self):
        if self.hasLUT:
            return self.lut
        elif self.parent:
            return self.parent.getLUT()
        else:
            return None    
#    def getVal(self):             # keep this because one day you will need it when
#        raise ConstantValueError  # you try doing as much comp-time checking as possible

    def flushType(self): pass
    def getExprType(self): pass
    def checkAsst(self): pass
    def checkIntention(self): pass
    def checkCallSt(self): pass
    def checkIf(self): pass
    def checkTryXpt(self): pass
    def checkRaise(self): pass
    def checkCaseSt(self): pass
    def checkResetSt(self): pass    
    def checkExitSt(self): pass
    def checkTCase(self): pass
    def preloadObj(self): pass
    def patchObj(self): pass
    def checkMethodAsst(self): pass    
    def checkIdMatch(self): pass
    def checkSpecMatch(self): pass
    def checkReturn(self): pass
    def checkReturnMissing(self): pass
    def insertExceptionLUT(self): pass
    def checkCapsule(self): pass
    def checkConnection(self): pass
    def checkTransition(self): pass
    def checkActivity(self): pass
    def checkRoot(self, root): # TBD throw this out :  it probably doesn't work anyway
        # finds recursive calls
        if root:
            rootstring = string.join([r.image() for r in root],"; ")
        else:
            rootstring = "None"                                           
        #print "root ", rootstring
        if not root: root = []
        if self in root:
            res = root, True
        else:
            root.append(self)
            res = root, False
        return res
    def getEnclosingProc(self):
        if self.parent:
            return self.parent.getEnclosingProc()
        else:
            return None
    def getEnclosingExpr(self):
        if self.parent:
            return self.parent.getEnclosingExpr()
        else:
            return None
    def getEnclosingActTrans(self):
        if self.parent:
            return self.parent.getEnclosingActTrans()
        else:
            return None
    def getCachedType(self):
        if hasattr(self, "cachedType"):
            return self.cachedType
        else:
            return None
    def isNamedType(self):
        return hasattr(self, "namedType")
    def getStamp(self):
        return "%s:%s" % (self.getTopNode().getObjectName(), self.refid)
    def inLoop(self):
        return self.parent.inLoop()
    def isCapsuleEntity(self):
        return self.parent.isCapsuleEntity()
    def getCapsuleBlock(self):
        return self.parent.getCapsuleBlock()
    def isSep(self):
        return False
    def kidsNoSep(self): # filters out all seperators from a list
        return [kid for kid in self.kids if not kid.isSep()]
    def fixLeadChars(self,prevIdx,txt):
        for kid in self.kids:
            nextIdx = kid.fixLeadChars(prevIdx,txt)
            prevIdx = nextIdx
        return prevIdx
    def isTerminal(self):
        return False
    def gatherProcedureDecls(self, dict):
        for kid in self.kids:
            if kid:
                kid.gatherProcedureDecls(dict)
    def collectAfters(self,res):
        for kid in self.kids:
            if kid:
                kid.collectAfters(res)
    def collectCapsuleChildren(self,res):
        for kid in self.kids:
            if kid:
                kid.collectCapsuleChildren(res)
class Terminal:
    def fixLeadChars(self,prevIdx,txt):
        def crunchCRs(s):
            crunched = s.replace('\r\n','%0A')
            crunched = crunched.replace('\n','%0A')            
            return crunched
        self.leadChars = crunchCRs(txt[prevIdx:int(self.startCol)])
        #print "[",prevIdx,'|%s|' % self.leadChars,self.startCol,"]:",self,self.lineno,self.tokLength()
        newIdx = int(self.startCol) + len(self.tokVal())
        return newIdx
    def tokVal(self): return self.token
    def returnCount(self):
        #print "<",self.leadChars
        if self.leadChars == None:
            return 0
        else:
            return len(re.findall('%0A',self.leadChars))
    def isTerminal(self):
        return True
class TopNode:
    def getTopNode(self):
        return self 
    def checkExports(self):
        pass
    def inInterface(self):
        return False
    def inLoop(self):
        return False
    def checkIdMatch(self):
        if not self.endId.isNULL():
            if self.modname.idname != self.endId.idname:
                error("Mismatch for end identifier %s of compilation unit" % self.endId.idname, self.endId)            
    def isGeneric(self):
        return False
    def isInstantiation(self):
        return False
    def setSource(self, source):
        self.source = source
    def isCapsuleEntity(self):
        return False
    def getCapsuleBlock(self):
        return False
    def getWriteDependencies(self, dummy):
        return dummy
    def checkProcsImplemented(self): pass
class LUTOwner:
    def createLUT(self):
        self.lut = LUT(self)
        self.hasLUT = True        
    def dumpLUT(self):
        self.lut.dump()
        
class TypeOwner:
    def getType(self):
        if not hasattr(self,"typeCreated"):
            self.typeCreated = True
            self.createType()
        return self.type
    def flushType(self):
        self.getType().flush()

class CapsuleInterfaceUser(LUTOwner,TopNode,TypeOwner): 
    def createType(self):
        ports = self.portList.getPorts()
        specType = M3Types.M3CapsuleSpecType(self,ports)
        self.type = specType
    def getBaseName(self):
        return Options.options.library + os.sep + self.modname.idname + "CapInt"
    def getObjectName(self):
        return self.modname.idname + "." + CompilationUnit.unitTypeNames["CapsuleInterface"]
    def getHumanName(self):
        return "Capsule Interface %s" % self.modname.idname
    def getDependencies(self):
        return self.imports.getDependencies()
    def getUnit(self):
        return CompilationUnit.CompilationUnit(unitName=self.modname.idname, unitType="CapsuleInterface")

class CapsuleUser(LUTOwner,TopNode,TypeOwner):
    def createType(self):
        self.specNode = m3.compile(fileName=self.getInterfaceName())
        ports = self.specNode.portList.getPorts()
        specType = M3Types.M3CapsuleSpecType(self.specNode,ports)
        self.type = M3Types.M3CapsuleBodyType(specType)
    def getPortOfMessage(self,messageName):
        myType = self.getType()
        return myType.getPortOfMessage(messageName)
    def checkExports(self):
        specXML = m3.compile(fileName=self.getInterfaceName())
        specXML.renumber()
        #print specXML.toXML()
        ports = specXML.portList.getPorts()
        for port in ports:
            self.getLUT().enter(port.name, LUTEntry(node=port.node,declarer="TYPE"),port.node)
            for message in port.protocol.messages:
                name = message.name                
                if self.getType().spec.isUnique(name):
                    #print "unique name", name
                    mtype = message
                    self.getLUT().enter(mtype.name,LUTEntry(node=message.node,declarer="TYPE"),message)
                else:
                    pass
                    #print "ambiguous name", name
    def getUsedCapsuleNames(self):
        return self.usedCapsules.getUsedCapsuleNames()

    def isCapsuleEntity(self):
        return True
    def getCapsuleBlock(self):
        return self
        
    def getInterfaceName(self):
        if not self.implId.isNULL():
            name = self.implId.idname
        else:
            name = self.modname.idname
        return name + "." + CompilationUnit.unitTypeNames["CapsuleInterface"]
    def getBaseName(self):
        return Options.options.library + os.sep + self.modname.idname + "CapMod"
    def getObjectName(self):
        return self.modname.idname + "." + CompilationUnit.unitTypeNames["Capsule"]
    def getHumanName(self):
        return "Capsule Module %s" % self.modname.idname
    def getDependencies(self):
        return self.imports.getDependencies() + self.getUsedCapsuleNames()
    def getUnit(self):
        return CompilationUnit.CompilationUnit(unitName=self.modname.idname, unitType="Capsule")
        
class InterfaceUser(LUTOwner,TopNode):
    def getBaseName(self):
        return Options.options.library + os.sep + self.modname.idname + "Int"
    def getObjectName(self):
        return self.modname.idname + "." + CompilationUnit.unitTypeNames["Interface"]
    def getHumanName(self):
        return "Interface %s" % self.modname.idname
    def inInterface(self):
        return True
    def getDependencies(self):
        return self.imports.getDependencies()
    def getUnit(self):
        return CompilationUnit.CompilationUnit(unitName=self.modname.idname, unitType="Interface")
    
class GenericInterfaceUser(LUTOwner,TopNode): 
    def getObjectName(self):
        return self.modname.idname + "." + CompilationUnit.unitTypeNames["GenericInterface"]
    def getHumanName(self):
        return "Generic Interface %s" % self.modname.idname
    def inInterface(self):
        return True
    def isGeneric(self):
        return True
    def getDependencies(self):
        return self.importList.getDependencies()
    def getUnit(self):
        return CompilationUnit.CompilationUnit(unitName=self.modname.idname, unitType="GenericInterface")
    
class GenericModuleUser(TopNode): 
    def getObjectName(self):
        return self.modname.idname + "." + CompilationUnit.unitTypeNames["Generic"]
    def getHumanName(self):
        return "Generic Module %s" % self.modname.idname
    def isGeneric(self):
        return True
    def getDependencies(self):
        return [str(self.modname.idname)] + self.importList.getDependencies()
    def getUnit(self):
        return CompilationUnit.CompilationUnit(unitName=self.modname.idname, unitType="Generic")

class GenFormalsUser: pass
class GenActualsUser: pass

class InstantiationUser:
    def makeFromImportList(self, formals, actuals):
        # immitate parser node construction actions
        import RuleNodes
        from RuleNodes import NullNode
        if formals.idlist.length() != actuals.idlist.length():
            error("differing numbers of formal and actual generic parameters",self)
            raise "GenericInstantiationAborted"
        aiList = RuleNodes.AsImportListNode()
        for formal,actual in zip(formals.idlist.kidsNoSep(), actuals.idlist.kidsNoSep()):
            # create the nodes for "IMPORT <actual> AS <formal>" for each one
            aiItem=RuleNodes.RenamedImportItemNode(origId=actual, kwa=NullNode(), newId=formal)
            aiList.add(aiItem)
        aiNode=RuleNodes.AsImportNode(kwi=NullNode(),importList=aiList)
        return aiNode
    def isInstantiation(self):
        return True
    
class InterfaceInstantiationUser(InstantiationUser, TopNode): 
    def getBaseName(self):
        return Options.options.library + os.sep + self.modname.idname + "Int"
    def getObjectName(self):
        return self.modname.idname + "." + CompilationUnit.unitTypeNames["InterfaceInstantiation"]
    def getHumanName(self):
        return "Generic Interface Instantiation %s" % self.modname.idname
    def inInterface(self):
        return True
    def substituteTree(self):
        import RuleNodes
        from RuleNodes import NullNode
        genIntTree = m3.compile(fileName=self.genname.idname + "." + CompilationUnit.unitTypeNames["GenericInterface"])
        fromImports = genIntTree.importList
        fromImports.add(self.makeFromImportList(genIntTree.genericFormals,self.genActuals))
        newTopNode = RuleNodes.InterfaceNode(kwi=NullNode(),
                                             modname=self.modname,
                                             imports=fromImports,
                                             decls=genIntTree.declList,
                                             kwe=NullNode(),
                                             endId=self.modname)
        newTopNode.setSource(genIntTree.source)
        # TBD Line numbering on generic instantiations is not working : FIX ME
        # STARTDBG
        #newTopNode.renumber()
        #for kid in newTopNode.kids:
        #    print kid, kid.refid, kid.regen()
        # ENDDBG
        return newTopNode
    def getDependencies(self):
        return [self.genname.idname] + [act.idname for act in self.genActuals.idlist.kidsNoSep()]
    def getUnit(self):
        return CompilationUnit.CompilationUnit(unitName=self.modname.idname, unitType="InterfaceInstantiation")

class ModuleUser(LUTOwner,TopNode):
    def getBaseName(self):
        return Options.options.library + os.sep + self.modname.idname + "Mod"
    def getObjectName(self):
        return self.modname.idname + "." + CompilationUnit.unitTypeNames["Module"]
    def getInterfaceName(self):
        return self.modname.idname + "." + CompilationUnit.unitTypeNames["Interface"]
    def hasDefaultInterfaceFile(self):
        res =  os.path.exists(Options.options.library + os.sep + self.getInterfaceName())
        return res
    def getExports(self):
        if self.exportIds.isNULL():
            if self.hasDefaultInterfaceFile():
                exports = [self.modname.idname]
            else:
                exports = []
        else:
            exports = [id.idname for id in self.exportIds.kidsNoSep()]
        return exports
    def getHumanName(self):
        return "Module %s" % self.modname.idname
    def checkExports(self):
        self.specProcDecls = {}
        exports = self.getExports()
        #print "Exports %s" % string.join(exports," ")
        for export in exports:
            expNode = m3.compile(fileName=export + "." + CompilationUnit.unitTypeNames["Interface"])
            if not expNode: return
            expNode.renumber()
            expNode.gatherProcedureDecls(self.specProcDecls)
            topLUT = expNode.decls.lut
            for name in topLUT.table:
                self.block.lut.enter(name, topLUT.table[name])
    def getDependencies(self):
        return self.imports.getDependencies() + self.getExports()
    def getUnit(self):
        return CompilationUnit.CompilationUnit(unitName=self.modname.idname, unitType="Module")
    def checkProcsImplemented(self):
        bodyProcDecls = {}
        self.gatherProcedureDecls(bodyProcDecls)
        for specProcDeclName in self.specProcDecls:
            if specProcDeclName not in bodyProcDecls:
                if Options.options.slack:
                    msg = warning
                else:
                    msg = error
                msg("No implementation supplied for procedure %s" % specProcDeclName, self.specProcDecls[specProcDeclName])

class ModuleInstantiationUser(InstantiationUser, TopNode):
    def getBaseName(self):
        return Options.options.library + os.sep + self.modname.idname + "Int"    
    def getObjectName(self):
        return self.modname.idname + "." + CompilationUnit.unitTypeNames["ModuleInstantiation"]
    def getHumanName(self):
        return "Generic Module Instantiation %s" % self.modname.idname
    def substituteTree(self):
        import RuleNodes
        from RuleNodes import NullNode
        genModTree = m3.compile(fileName=self.genname.idname + "." + CompilationUnit.unitTypeNames["Generic"])
        fromImports = genModTree.importList
        fromImports.add(self.makeFromImportList(genModTree.genericFormals,self.genActuals))
        newTopNode = RuleNodes.ModuleNode(kwm=NullNode(),
                                          modname=self.modname,
                                          kwex=NullNode(),
                                          exportIds=self.exportIds,
                                          imports=fromImports,
                                          block=genModTree.block,
                                          endId=self.modname)
        newTopNode.setSource(genModTree.source)        
        return newTopNode
    def getDependencies(self):
        return [self.genname.idname] + [
            act.idname for act in self.genActuals.idlist.kidsNoSep()] + [
            exp.idname for exp in self.exportIds.kidsNoSep()]
    def getUnit(self):
        return CompilationUnit.CompilationUnit(unitName=self.modname.idname, unitType="ModuleInstantiation")

class AsImportUser:
    def dep(self):
        return self.importList.deps()
class AsImportListUser:
    def deps(self):
        return [kid.dep() for kid in self.kidsNoSep()]
    
class IdListUser: pass

class ImportListUser:
    def getDependencies(self):
        deps = []
        for kid in self.kids:
            deps += kid.dep()
        return deps

class FromImportUser:
    def insertLUT(self):
        impXML = m3.compile(fileName=self.impname.idname + "." + CompilationUnit.unitTypeNames["Interface"])
        if not impXML: return
        topLUT = impXML.decls.lut
        for impitem in self.implist.kidsNoSep():
            impid = impitem.idname
            if impid not in topLUT.table.keys():
                error("%s does not export %s" % (self.impname.idname,impid),self)
            else:
                res = self.getLUT().enter(impitem.idname,topLUT.table[impitem.idname])
    def dep(self):
        return [self.impname.idname]
    
class ImportItemUser:
    def insertLUT(self):
        impXML = m3.compile(fileName=self.id.idname + "." + CompilationUnit.unitTypeNames["Interface"],obj=self)
        if not impXML: return
        topLUT = impXML.decls.lut
        modType = M3Types.M3ModuleType(topLUT)
        res = self.getLUT().enter(self.id.idname,LUTEntry(tipe=modType,declarer="MODULE"))
    def dep(self):
        return self.id.idname
class RenamedImportItemUser:
    def insertLUT(self):
        impXML = m3.compile(fileName=self.origId.idname + "." + CompilationUnit.unitTypeNames["Interface"])
        if not impXML: return 
        topLUT = impXML.decls.lut
        modType = M3Types.M3ModuleType(topLUT)
        res = self.getLUT().enter(self.newId.idname,LUTEntry(tipe=modType,declarer="MODULE"))
    def dep(self):
        return self.origId.idname
    
    
class DeclListUser:
    def tabulate(self):
        res = DeclTable.DeclTable()
        for decl in self.kids:
            decl.tabulate(res)
        return res
class InterfaceDeclListUser(LUTOwner): pass
class BlockUser(LUTOwner):
    def getCapsuleBlock(self):
        return False
class CapsuleBlockUser(LUTOwner): 
    def getCapsuleBlock(self):
        return self
class ConstDeclsUser:
    def tabulate(self,res):
        for const in self.constList.kidsNoSep():
            const.tabulate(res)
        
class ConstDeclsListUser: pass

class TypeDeclsUser:
    def tabulate(self,res):
        for tipe in self.typeList.kidsNoSep():
            tipe.tabulate(res)
class TypeDeclsListUser: pass

class ExceptionDeclsUser:
    def tabulate(self,res):
        for exception in self.exceptionList.kidsNoSep():
            exception.tabulate(res)

class ExceptionDeclsListUser: pass
class VariableDeclsUser:
    def tabulate(self,res):
        for decl in self.variables.kidsNoSep():
            decl.tabulate(res)
class VariableDeclsListUser: pass

class ProcedureDeclUser(LUTOwner):
    def tabulate(self,res):
        res.add("procedure",self.procHead.name.idname,self)
    def checkReturnMissing(self):
        if (not self.procHead.signature.tipe.isNULL()) and (
            not self.procBlock.isNULL()) and (
            not hasattr(self, "hasReturn")):
            error("missing return statement for function",self)
    def getType(self, root=None):
        root,recursive = self.checkRoot(root)
        return self.procHead.getType()
    def insertLUT(self):
        lut = self.getLUT().getEnclosingLUT()
        name = self.procHead.name.idname

        if self.inInterface():
            if not self.procBlock.isNULL():
                error("illegal procedure body declaration for %s in interface" % name, self) 
            lut.enter(name, LUTEntry(node=self, declarer="TYPE"),self)
        else:
            if self.procBlock.isNULL():
                error("illegal body-less procedure declaration for %s in module" % name, self)
            self.enteredOver = LUTEntry(node=self, declarer="VAR",isIvar=self.parent.isCapsuleEntity())
            lut.enterOver(name, self.enteredOver,self)
        # TBD - You may have a previous declaration, if so check that it fits : but do this later

    def checkSpecMatch(self):
        if hasattr(self,"enteredOver"):
            if hasattr(self.enteredOver,"spec"):
                self.getType().checkMatch(self.enteredOver.spec.getTipe(), self)
            
    def checkIdMatch(self):
        if not self.endId.isNULL():
            if self.procHead.name.idname != self.endId.idname:
                error("Mismatch for end identifier %s of procedure" % self.endId.idname, self.endId)
    def getEnclosingProc(self):
        return self
    def isCapsuleEntity(self):
        return False
        # This allows us to have variables
        #within (auxiliary) procedures within (message/method) procedures within capsules
    def gatherProcedureDecls(self, decls):
        name = self.procHead.name.idname
        if self.getTopNode() in [self.parent.parent.parent, self.parent.parent]:
            decls[name] = self
class ProcedureHeadUser(TypeOwner):
    def createType(self):
        self.type = M3Types.M3ProcedureType(node=self.parent)
        if self.signature.tipe.isNULL():
            returnval = M3Types.M3ProcedureNullReturn
        else:
            returnval = self.signature.tipe.getType()
        if self.signature.raises.isNULL():
            raises = []
        else:
            raises = self.signature.raises.getRaiseList()
        formals = self.signature.formals.createTable()
        self.type.formals = formals
        self.type.raises = raises
        self.type.returnval = returnval
        self.type.name = self.name.idname
        
class SignatureUser: pass
class MethodSignatureUser(LUTOwner): pass
class FormalsUser:
    def getNameOrder(self):
        nameorder = []
        for f in self.kidsNoSep():
            for id in f.idList.kidsNoSep():
                nameorder.append(id.idname)
        return nameorder
    
    def createTable(self):
        #print "create table"
        sortedtable = []
        luttable = self.getLUT().table
        # default = False
        for name in self.getNameOrder():
            sortedtable.append(luttable[name]) # TBD don't clone this yet, defaults are not set up
#            print "formal image", luttable[name].image()
#            if luttable[name].default:
#                default = True
#            elif default:
#                error("non-default formal follows default formal",self)
        self.sortedtable = sortedtable
        return sortedtable
        
    def getTable(self):
        return self.sortedtable
                
class FormalUser:
    def insertLUT(self):
        lut = self.getLUT()
        if self.mode.isNULL():
            mode = "VALUE"
        else:
            mode = self.mode.token
        if self.constExpr.isNULL():
            default = None
        else:
            default = self.constExpr.getConstVal()
        for id in self.idList.kidsNoSep():
            lut.enter(id.idname, LUTEntry(declarer="VAR", mode=mode, node=self.tipe, default=default),self)
                                                  
class RevealsUser:
    def tabulate(self,res):
        for kid in self.revealsList.kidsNoSep():
            kid.tabulate(res)

class RevealsListUser: pass
class RevealUser:
    def tabulate(self,res):
        res.add("reveal",self.qualid.image(),self)
    def insertLUT(self):
        self.tipe.namedType = True # Some of these nodes are handled with phased typing
        self.tipe.phase = "CATEGORY"
        lut = self.getLUT()
        opaqueEntry = self.qualid.getEntry()
        if not opaqueEntry.declarer == "OPAQUE":
            error("Attempt to reveal non-opaque item %s" % opaqueEntry.name, self)
#        print "patching revealed type#############################"
        opaqueEntry.patchReveal(newNode=self, partial=self.sign.token=="<:")
        # patch up that old entry and let type discovery do the rest
        self.typeCode = opaqueEntry.typeCode
        #print "opaqueEntry", opaqueEntry.image()
    def getType(self, root=None):
        return self.tipe.getType()
    
class ConstDeclUser:
    def tabulate(self,res):
        res.add("const",self.id.idname, self)
    def getType(self, root=None):
        root,recursive = self.checkRoot(root)
        res = self.getCachedType()
        if res: return res
        ttype = None
        if not self.tipe.isNULL(): ttype = self.tipe.qualId.getType()
        etype = self.constExpr.getType()
        constVal = self.constExpr.getConstVal()
        if ttype:
            if not ttype.fits(etype):
                rtype=M3Types.M3ErrorType(error("Type mismatch in initialisation", self))
            else:
                ttype = etype
        self.cachedType = res
        return etype
    def getVal(self):
        return self.constExpr.getConstVal()
    def insertLUT(self):
        lut = self.getLUT()
        res = self.getLUT().enter(self.id.idname, LUTEntry(node=self, declarer="VAR",isIvar=self.isCapsuleEntity()))
        
class TypeDeclUser:
    def tabulate(self, res):
        res.add("type",self.id.idname,self)

    def getType(self, root=None):
        res = self.tipe.getType()
        res.CCodeName = "%s__%s" % (self.getModuleName(), self.id.idname)
        return res
    
    def insertLUT(self):
        self.tipe.namedType = True # Currently needed to handle anonymous capsules
        self.tipe.phase = "CATEGORY"

        declarer = {"=": "TYPE", "<:": "OPAQUE"}[self.sign.token]
        
        entry = LUTEntry(node=self, declarer=declarer,isIvar=self.isCapsuleEntity())
        res = self.getLUT().enter(self.id.idname, entry, self)
        M3TypeLib.enter(entry)
        self.tipe.typeCode = entry.typeCode
        # this is vital later for generating references to the pickled types
        
        
    def getVal(self):
        return self.getType()


class ExceptionDeclUser:
    def tabulate(self,res):
        res.add("exception",self.id.idname,self)
    def insertLUT(self):
        if self.tipe.isNULL():
            excParam = None
        else:
            excParam = self.tipe.getType()
        self.getLUT().enter(self.id.idname,
                            LUTEntry(tipe=M3Types.M3ExceptionType(self.id.idname, excParam),
                                     declarer="EXCEPTION"))
class VariableDeclUser:
    def tabulate(self,res):
        res.add("variablegroup", "group%s" % self.refid, self)
        for id in self.idlist.kidsNoSep():
            res.add("variablesingle",id.idname,self)
        
    def getType(self, root=None):
        root,recursive = self.checkRoot(root)        
        # if both type and expr exist then check them against each other
        # otherwise just use the type of the one we found
        #
        # also deal with the differences between types and expressions which syntax analysis
        # has not caught
        ttype = None
        etype = None
        if not self.tipe.isNULL():
            if self.tipe.__class__.__name__ == "TypeNameNode":
                tentry = self.tipe.qualId.getEntry()
                if tentry.declarer not in  ["TYPE","OPAQUE"] :
                    error("%s is not a type" % self.tipe.qualId.image(), self)
                ttype = tentry.getTipe()
            else:
                ttype = self.tipe.getType()
        if ttype and ttype.isOpen:
            error("Declaration with open array", self) 
        if not self.expr.isNULL():
            # make sure this is not a type but a real expression
            if self.expr.expr.__class__.__name__ == "TypeNameNode":
                tentry = self.expr.expr.qualId.getEntry()
                if tentry.declarer == "TYPE":
                    error("%s is a type and not a value" % self.expr.expr.qualId.image(), self)
            etype = self.expr.getExprType()
        if ttype and etype:
            if not ttype.fits(etype):
                error("Type mismatch in initialisation", self)
            rtype = ttype # still return a type so we don't get an error storm
        else:
            rtype = ttype or etype
        self.vartype = rtype # sneakily save this for a rainy day (when we generate code)
        return rtype

    def insertLUT(self):
        for id in self.idlist.kidsNoSep():
            res = self.getLUT().enter(id.idname, LUTEntry(node=self,declarer="VAR", isIvar=self.isCapsuleEntity()),obj=self)
    def collectCapsuleChildren(self,res):
        type = self.getType()
        if type.isCapsuleSpec:
            for id in self.idlist.kidsNoSep():
                res.append((id.idname, type))

class TypeDeclListUser:pass
class ExceptionDeclListUser:pass
class VariableDeclListUser:pass
class RaisesUser:
    def isAny(self):
        return self.raiseList.isAny()
    def getRaiseList(self):
        return self.raiseList.getRaiseList()
class RaisesAnyUser:
    def isAny(self):
        return True
class RaisesListUser:
    def isAny(self):
        return False
    def getRaiseList(self):
        res = []
        for raiseElem in self.kidsNoSep():
            entry = raiseElem.getEntry()
            if entry.declarer != "EXCEPTION":
                error("%s is not an exception" % raiseElem.image(), self)
            if entry.getTipe() in res:
                error("%s occurs twice in raise list" % raiseElem.image(), self)
            res.append(entry.getTipe())
        return res

class StatementsUser: pass
class AssignStUser:
    def checkAsst(self):
        # handle scalings as special case
        lhs = self.lhs.exprType
        rhs = self.rhs.exprType
        if lhs.isInteger and rhs.isInteger and lhs.scaling and rhs.scaling:
            if lhs.scaling != rhs.scaling:
                warning("suspicious assignment involving scaled object",self)
            
        if not lhs.fits(rhs):
            error("type conflict in assignment : lhs is type %s, rhs is type %s" %
                  (lhs.image(), rhs.image()),
                  self)



class CallStUser:
    def isCall(self):
        return self.expr.exprType == M3Types.M3ProcedureNullReturn

    def checkCallSt(self):
        if not (self.isCall() or self.expr.exprType.isError): # they have been punished already for their mistake
            error("Only call to null return procedure allowed here \n" + 
                  "(Hint: did you type '=' instead of ':=' in an assignment?)", self)


class SendStUser:
    def checkCallSt(self):
        if not ((self.expr.exprType == M3Types.M3MessageNullReturn) or
                self.expr.exprType.isError): # they have been punished already for their mistake
            error("Only call to OUTGOING message allowed here",self)
        # TBD are we in a capsule at all ?
        self.after.checkAfter()
        
class SynCallStUser:
    def checkCallSt(self):
        if not ((self.expr.exprType == M3Types.M3SynchNullReturn) or
                self.expr.exprType.isError): # they have been punished already for their mistake
            error("Only call to OUTGOING message allowed here",self)
        # TBD are we in a capsule at all ?

class ReplyStUser:
    def checkCallSt(self):
        if not ((self.expr.exprType == M3Types.M3MessageNullReturn) or
                self.expr.exprType.isError): # they have been punished already for their mistake
            error("Only call to OUTGOING message allowed here",self)
        # TBD are we in a capsule at all ?
        #self.after.checkAfter()
    
class AssertStUser:
    def checkCallSt(self):
        if not self.expr.exprType.isBoolean:
            error("assert statement must contain boolean expression", self)
        
class PythonStUser: pass

class ResetStUser:
    def checkResetSt(self):
        # TBD are we in a capsule ?
        if not self.level.isNULL():
            levelType = self.level.getExprType()
            if not levelType.isInteger:
                error("RESET expression must evaluate to integer", self)
            
        # is the level an integer (or 0?)
class CaseStUser:
    def checkCaseSt(self):
        # check that type of expression corresponds to types of guards
        # make sure nothing overlaps
        # make sure poss values are exhausted if no else
        exprType = self.expr.getExprType()
        if not exprType.isOrdinal:
            error("type of case expression is not ordinal",self)
            return
        self.caseElts.checkExpr(exprType)
        # snippet testing all takes place at integer level
        fullRange = SetUtils.SnippetList(exprType.getFirst().ord().val,
                                     exprType.getLast().ord().val)
        self.caseElts.exhaust(fullRange)
        if not fullRange.isEmpty() and self.elseStatements.isNULL():
            leftOvers = fullRange.image()
            error("case statement does not exhaust range of tested expression (leftover: %s)" % leftOvers,self)
        if fullRange.isEmpty() and (not self.elseStatements.isNULL()):
            error("else statement is superfluous, range is covered completely", self)

class CaseEltListUser:
    def checkExpr(self,exprType):
        for kid in self.kidsNoSep():
            kid.checkExpr(exprType)
    def exhaust(self, fullRange):
        for kid in self.kidsNoSep():        
            kid.exhaust(fullRange)
class VCaseEltListUser(CaseEltListUser): pass

class CaseEltUser:
    def checkExpr(self,exprType):
        for label in self.labelList:
            label.checkExpr(exprType)
    def exhaust(self, fullRange):
        for kid in self.kids:        
            kid.exhaust(fullRange)
class ExitStUser:
    def checkExitSt(self):
        if not self.inLoop():
            error("exit called outside of loop",self)

class EvalStUser: pass

class ForStUser(LUTOwner):
    def inLoop(self): return True
    def checkForSt(self):
        err = None
        looptype = self.startExpr.getExprType()
        if not looptype.isOrdinal:
            err = error("cannot loop with non-Ordinal type %s" % looptype.name, self)
        if not looptype.fits(self.toExpr.getExprType()):
            err = error("mismatched types for start and end values for loop", self)
        if not self.byExpr.isNULL():
            inctype = self.byExpr.getExprType()
            if not inctype.fits(M3Types.M3IntegerBase):
                err = error("bad loop increment type %s" % inctype.name, self)
        if err:
            self.looptype = M3Types.M3ErrorType(err)
        else:
            self.looptype = looptype
            
class IfStUser:
    def checkIf(self):
        if not self.ifExpr.getExprType().fits(M3Types.M3Boolean):
            error("condition for if statement must be BOOLEAN",self)
        self.elsifList.check()

class ElsifListUser:
    def check(self):
        for elsif in self.kids:
            elsif.checkElsif()

class ElsifUser:
    def checkElsif(self):
        if not self.elseExpr.getExprType().fits(M3Types.M3Boolean):
            error("condition for if statement must be BOOLEAN",self)

class LockStUser: pass

class LoopStUser:
    def inLoop(self):
        return True

class RaiseStUser:
    def checkRaise(self):
        entry = self.raiseId.getEntry()
        if entry.declarer != "EXCEPTION":
            error("attempt to raise non-exception",self)
        formalType = entry.getTipe().tipe
        actualType = None
        if not self.expr.isNULL():
            actualType = self.expr.getExprType()
        if not (formalType or actualType): return # all clear no param and none supplied
        elif formalType and not actualType:
            error("No parameter supplied in raise", self)
        elif actualType and not formalType:
            error("Parameter supplied in raise for parameterless exception", self)
        elif not actualType.fits(formalType):
            error("Raised exception parameter does not fit type in declaration",self)
            
class RepeatStUser:
    def inLoop(self):
        return True

class ReturnUser:
    def checkReturn(self):
        # are we in a procedure ?
        proc = self.getEnclosingProc()

        if not proc:
            error("RETURN only allowed inside a procedure")
        else:
            proc.hasReturn = True
            returnval = proc.procHead.getType().returnval
            if self.expr.isNULL():
                if returnval != M3Types.M3ProcedureNullReturn:
                    error("RETURN statement must have a value", self);    
            else:
                # does the value we are returning match the type declared for the procedure ?
                if not returnval.fits(self.expr.exprType):
                    error("Type mismatch in RETURN statement",self)



class TryXptStUser:
    def checkTryXpt(self):
        # look for the handlers and check that they really are exceptions
        self.handlerList.check()
class TryFinStUser:
    pass # Nothing needs checking here (strange but true ?!)

class WhileStUser:
    def inLoop(self):
        return True

class WithStUser(LUTOwner): pass

class BindingListUser: pass


class HandlerListUser:
    def check(self):
        # gather all the names across the handlers to test for uniqueness,
        # (also checks exception parameters while it is down there)
        excNames = []
        for handler in self.kidsNoSep():
            excNames = handler.checkHandler(excNames)
class IdUser(Terminal):
    def tokVal(self): return self.idname
class BindingIdUser(Terminal):
    def tokVal(self): return self.idname
class ForIdUser(Terminal):
    def getType(self, root=None):
        self.parent.checkForSt()
        return self.parent.looptype
    def insertLUT(self):
        self.getLUT().enter(self.idname, LUTEntry(node=self, declarer="VAR"))
    def tokVal(self): return self.idname
class TCaseStUser:
    # TBD TypeCase is not really finished
    def checkTCase(self):
        # check that the tested expression and all the choices are refs or objects
        exprType =  self.expr.getExprType()
        if not(exprType.isRef or exprType.isObject):
            error("expression of a Typecase must be either a reference or an object", self);
        self.tCaseList.checkTCase()

class TCaseListUser:pass

class TCaseUser(LUTOwner):
    def caseTypeForId(self):
        if self.qualidList.length() != 1:
            error("Type case variable not allowed with multiple types in one case");
        res = self.qualidList.kids[0].getType()
        return res

class TCaseIdUser(Terminal):
    def insertLUT(self):
        # TBD the case id here may be an implicit object declaration, which means we need to stay in line with phased declaration
        # and not be in too much of a hurry to get the type
        promise = self.parent.qualidList.kids[0].qualId.getEntry().node
        self.getLUT().enter(self.idname, LUTEntry(node=promise, declarer="VAR"))
    def getType(self, root=None):
        self.parent.caseTypeForId()
    def tokVal(self): return self.idname
class IntUser(Terminal):
    def getVal(self):
        return eval(self.intname)
    def tokVal(self): return self.intname
class LabelsListUser:
    def checkExpr(self,exprType):
        for kid in self.kidsNoSep():
            kid.checkExpr(exprType)
    def exhaust(self,fullRange):
        for kid in self.kidsNoSep():
            kid.exhaust(fullRange)
    def getCases(self):
        cases = []
        for kid in self.kidsNoSep():
            cases.append(kid.caseLimits())
        return cases
               
class LabelsUser:
    def checkExpr(self,exprType):
        for constExpr in self.kidsNoSep():
            if not constExpr.getType().fits(exprType):
                error("Bad type for case value %s" % constExpr, self)
    def exhaust(self,fullRange):
        # Remember the DOTDOT in the middle
        if self.length() == 1:
            res = self.exhaustSingle(fullRange,self.kids[0])
        elif self.length() == 3:
            res = self.exhaustRange(fullRange,self.kids[0],self.kids[2])
        else:
            raise "compiler anomaly : strange range" 
        if not res:
            error("overlapping range in case", self)
    def exhaustSingle(self,fullRange,item):
        return fullRange.deleteItem(item.getConstVal().ord().val)
    def exhaustRange(self,fullRange,first,last):
        return fullRange.deleteRange(first.getConstVal().ord().val,last.getConstVal().ord().val)        
    def caseLimits(self):
        if self.length() == 1:
            return self.kids[0].getConstVal().ord().val
        elif self.length() == 3:
            return (self.kids[0].getConstVal().ord().val,self.kids[2].getConstVal().ord().val)

        

class CaseUser:
    def checkExpr(self,exprType):
        self.labelList.checkExpr(exprType)
    def exhaust(self,fullRange):
        self.labelList.exhaust(fullRange)

class VCaseUser(CaseUser):
    def getCaseFields(self):
        return self.labelList.getCases(),self.fields.getTable()

class HandlerUser(LUTOwner):
    def insertExceptionLUT(self):
        if not self.id.isNULL():
            handlerEntry = self.qualidList.getSingleHQI()
            paramType = handlerEntry.getTipe().tipe
            self.getLUT().enter(self.id.idname, LUTEntry(tipe=paramType, declarer="VAR"))
    def checkHandler(self, hqiList):
        single = self.qualidList.getSingleHQI()
        # check for the right combination of parameterised handler and parameterised exception declaration
        if single:
            if (not self.id.isNULL()) and (not single.getTipe().tipe):
                error("Exception parameter for a parameterless exception",self)
        else:
            if not self.id.isNULL():
                error("Exception parameter with more than one exception alternative",self)
        # finally check for dupes
        return self.qualidList.check(hqiList)
       
class HandlerQualidListUser:
    def check(self, hqiList):
        for hqi in self.kidsNoSep():
            entry = hqi.getEntry()
            qi = hqi.image()
            if entry.declarer != "EXCEPTION":
                error("Non-exception %s in handler" % qi, self)
            if qi in hqiList:
                error("Exception %s occurs more than once in handlers" % qi, self)
            else:
                hqiList.append(qi)
        return hqiList
    def getSingleHQI(self):
        return (len(self.kids) == 1) and (self.kids[0].getEntry())
class TypeListUser:
    def getIndices(self):
        return [kid.getType() for kid in self.kidsNoSep()]
class BindingUser:
    def insertLUT(self):
        self.getLUT().enter(self.id.idname, LUTEntry(node=self.expr.expr, declarer="VAR", mode="VAR"))
        # mode added here to help C code gen

class ActualExprUser:
    def getEntry(self):
        if self.id.isNULL():
            name = None
        else:
            name = self.id.idname
        try:
            val = self.expr.getVal()
        except:
            # TBD we try to get the value of anything here - the underlying reason is that some predefined
            # procedures need constexprs but we have not specified this syntactically
            val = None
#        print "getting actual", self.expr.getExprType()
        return {"name":name, "tipe":self.expr.getExprType(), "val": val}

class ActualUser:
    def getEntry(self):
        raise "cannot handle types as actual params yet"
        return self.tipe
    
class ArrayUser(TypeOwner):
    def createType(self):
        self.type = M3Types.M3ArrayType()
        indices = self.typeList.getIndices()
        elementType = self.tipe.getType()
        self.type.setStructure(elementType, indices)


class PackedUser:pass

class BracketedTypeUser(TypeOwner):
    def createType(self):
        self.type = self.tipe.getType()

class EnumUser(TypeOwner):
    def createType(self):
        self.type = M3Types.M3EnumType([item.idname for item in self.idlist.kidsNoSep()])

class ObjectUser(TypeOwner):
    def createType(self):
        self.type = M3Types.M3ObjectType(swper = None,
                                         fields = None,
                                         methods = None,
                                         overrides = None,
                                         stamp = self.getStamp())
        self.type.setSwper((not self.tipe.isNULL()) and self.tipe.getType())
        self.type.setFields(self.fields.getTable())
        self.type.setMethods((not self.methods.isNULL()) and self.methods.getMethods(), self)
        self.type.setOverrides((not self.overrides.isNULL()) and self.overrides.getOverrides(),self)
    def getFillerStamps(self):
        res = []
        allnames = []
        if not self.methods.isNULL():
            allnames = self.methods.getFillerStamps()
        if not self.overrides.isNULL():
            allnames += self.overrides.getFillerStamps()
        for name in allnames:
            if name and (name not in res):
                res.append(name)
        return res

class ObjectListUser:pass

class ProcedureUser(TypeOwner):  # TBD refactor this with procedurehead eventually
    def createType(self):
        self.type = M3Types.M3ProcedureType(node=self)
        if self.signature.tipe.isNULL():
            returnval = M3Types.M3ProcedureNullReturn
        else:
            returnval = self.signature.tipe.getType()
        if self.signature.raises.isNULL():
            raises = []
        else:
            raises = self.signature.raises.getRaiseList()
        formals = self.signature.formals.createTable()
        self.type.formals = formals
        self.type.raises = raises
        self.type.returnval = returnval



class RecordUser(TypeOwner):
    def createType(self):
        self.type = M3Types.M3RecordType()        
        self.type.setFields(self.fields.getTable())

class VariantRecordUser(TypeOwner):
    def createType(self):
        self.type=M3Types.M3VariantRecordType()

        
        # check tag is ordinal
        tagField = self.tagField.getEntries()
        if len(tagField) > 1:
            error("only one tag field allowed",self)
        tagField = tagField[0]
        tagType = tagField.tipe
        if not tagType.isOrdinal:
            error("type of tag for variant record must be discrete", self) 

        # set tag field
        
        self.type.setTag(tagField)


        # check that case fields do not overlap
        fullRange = SetUtils.SnippetList(tagType.getFirst().ord().val,
                                     tagType.getLast().ord().val)
        self.caseElts.exhaust(fullRange)
        if not fullRange.isEmpty() and self.efields.isNULL():
            leftOvers = fullRange.image()
            error("variants do not exhaust range of tag type (leftover: %s)" % leftOvers,self)
        if fullRange.isEmpty() and (not self.efields.isNULL()):
            error("else arm of variant is superfluous, range is covered completely", self)
        

        # set field groups from variant case arms
        for elt in self.caseElts.kidsNoSep():
            case,fields = elt.getCaseFields()
            self.type.setCaseFields(case,fields,self)
            
        # set opt else fields
        if not self.efields.isNULL():
            self.type.setElseFields(self.efields.getTable(),self)
        if not self.sfields.isNULL():
            self.type.setStaticFields(self.sfields.getTable(),self)
        # set opt static fields

class RefUser(TypeOwner):
    def createType(self):
        self.type = M3Types.M3RefType(None)
        self.type.setReferent(self.tipe.getType())
        
class SetUser(TypeOwner):
    def createType(self):
        self.type = M3Types.M3SetType(None)
        if not self.isNamedType():
            res = M3Types.M3ErrorType(error("anonymous sets not supported yet", self))
        else:
            setRange = self.setconst.getType()
            if not setRange.isOrdinal:
                res = M3Types.M3ErrorType(error("set range must be an ordinal type", self))
            else:
                self.type.rangeType = setRange


class SubrangeUser(TypeOwner):
    def createType(self):
        type1 = self.const1.getType()
        type2 = self.const2.getType()
        if type1.isError or type2.isError:
            self.type = M3Types.M3ErrorType(error("invalid subrange boundary", self))
            return
        if not type1.isOrdinal:
            self.type = M3Types.M3ErrorType(error("subrange must use ordinal type", self))
            return
        if not type1.fits(type2):
            self.type = M3Types.M3ErrorType(error("types of subrange must be identical",self))
            return 
        self.type = type1.createSubType(first=self.const1.getConstVal().val, last=self.const2.getConstVal().val)


class BrandUser:pass
class FieldListUser:
    def getTable(self, root=None):
        root,recursive = self.checkRoot(root)                
        table = []
        for field in self.kidsNoSep():
            entries = field.getEntries()
            for newentry in entries:
                if newentry.name in [oldentry.name for oldentry in table]:
                    error("duplicate record keys using %s" % newentry.idname, self)
                table.append(newentry)
        return table
class FieldUser:
    def getEntries(self):
        tipe = self.tipe.getType()
        if self.constExpr.isNULL():
            default = None
        else:
            default = self.constExpr.getConstVal()
        return [M3Types.Field(id.idname, tipe, default, self.constExpr) for id in self.idlist.kidsNoSep()]
            
class MethodListUser:
    def getMethods(self):
        return [kid.getMethod() for kid in self.kidsNoSep()]
    def getFillerStamps(self):
        return [kid.getFillerStamp() for kid in self.kidsNoSep()]
class MethodUser(TypeOwner):
    def createType(self):
        self.type = M3Types.M3ProcedureType(node=self)
        if self.signature.tipe.isNULL():
            returnval = M3Types.M3ProcedureNullReturn
        else:
            returnval = self.signature.tipe.getType()
        if self.signature.raises.isNULL():
            raises = []
        else:
            raises = self.signature.raises.getRaiseList()
        formals = self.signature.formals.createTable()
        self.type.formals = formals
        self.type.raises = raises
        self.type.returnval = returnval
    def getMethod(self): 
        meth = LUTEntry(node=self,
                        declarer="TYPE",
                        name=self.name.idname,
                        default=self.getFillerStamp()
                        )
        return meth
        
    def checkMethodAsst(self):
        #print "lineno", self.getTopNode().source, self.lineno
        if not self.expr.isNULL():
            slot = self.getType()
            filler = self.expr.getType()
            slot.checkMatch(other=filler,obj=self,ignoreFirstFormal=True)
            # check that the first argument of filler has the same type as the object
            # for which it is being used
            fillerObjectTarget = filler.formals[0].getTipe()
            owningObject = self.parent.parent.getType()
            if fillerObjectTarget not in owningObject.swperList():
                error("First parameter of slot filler is not identical to or supertype of target object", self)

    def getFillerStamp(self):
        if not self.expr.isNULL():
            res = self.expr.getType().node.getStamp()
            #print "Stamp", res
            return res
        else:
            return False
    
class OverrideListUser:
    def getOverrides(self):
        return [kid.getOverride() for kid in self.kidsNoSep()]
    def getFillerStamps(self):
        return [kid.getFillerStamp() for kid in self.kidsNoSep()]
class OverrideUser:
    def getOverride(self):
        return LUTEntry(name = self.id.idname, tipe = self.expr.getType(), default=self.getFillerStamp())
    def getFillerStamp(self):
        if not self.expr.isNULL():
            res = self.expr.getType().node.getStamp()
            #print "Stamp", res
            return res
        else:
            return False
#    def getOverrideName(self):
#        return (self.id.idname, self.getFillerStamp())
class ConstExprUser:
    def getConstVal(self):
        if hasErrors():
            return M3Types.M3IntegerBase.createObject(0);
        try:
            constVal = self.expr.getVal()
        except ConstantValueError :
            error("Constant expression cannot be evaluated",self)
            constVal = None
        #print "constVal", constVal
        return constVal
    def getType(self, root=None):
        res = self.getCachedType()
        if res: return res        
        res = self.expr.getExprType(root)
        self.cachedType = res
        return res
class BracketedExprUser:
    def flatten(self):
        self.expr = self.expr.flatten()
        return self
    def getType(self):
        return self.expr.getType()
    def getVal(self):
        return self.expr.getVal()
class BinaryExprUser:
    def flatten(self):
        if not self.exprList.length():
            fl = self.expr and self.expr.flatten()
            return fl
        else:
            return self
    def getType(self, root=None):
        res = self.getCachedType()
        if res: return res        
        leftType = self.expr.getType()
#        print self.exprList
        res = self.exprList.getType(leftType,root)
        self.cachedType = res
        return res
    def getVal(self):
        leftVal = self.expr.getVal()
        res = self.exprList.getVal(leftVal)
        return res
class UnaryExprUser:
    def flatten(self):
        if not self.opList.length():
            fl = self.expr and self.expr.flatten()
            return fl
        else:
            return self
    def getType(self, root=None):
        res = self.getCachedType()
        if res: return res        
        # Assumption - unary operations always return the type of their operand
        res = self.expr.getType()
        self.cachedType = res
        return res
    
    def getVal(self):
        expr = self.expr.getVal()
        return self.opList.getVal(expr)
            
class OpExpUser:
    def isLogical(self,op):
        return op in ["=","#",">","<",">=","<="]
    def getType(self,leftType,root=None):
        myOp = self.operator.token
        # Handle the SET IN operator which is the one exception to the rule that binary operators
        # always have the same type on both sides
        rightType = self.expr.getType()
        #print "myOp", myOp
        if myOp == "IN":
            if rightType.isSet:
                if leftType.fits(rightType.rangeType):
                    return M3Types.M3Boolean
                else:
                    return M3Types.M3ErrorType(error("Types not valid for SET membership test", self))
            elif rightType.isList:
                if leftType.fits(rightType.elementType):
                    return M3Types.M3Boolean
                else:
                    return M3Types.M3ErrorType(error("Types not valid for LIST membership test", self))
            else:
                return M3Types.M3ErrorType(error("IN only allowed with SETS and LISTs", self))

        if not rightType.fits(leftType):
            return M3Types.M3ErrorType(error("unmatched types for operator %s with left %s and right %s" % (
                myOp, leftType, rightType), self))

        # handle scaling warnings as a special case

        if leftType.isInteger and rightType.isInteger and myOp in ["+","-"]:
            if leftType.scaling != rightType.scaling:
                warning("suspicious operation on scaled objects", self)
                return M3Types.M3IntegerBase
            else:
                return rightType
            
        # kill scaling on all other returned integer values

        err = None
        
        if myOp in ["MOD", "DIV"]:
            if rightType.fits(M3Types.M3IntegerBase):
                res = rightType
            else:
                err = error("%s on nonInteger type %s" % (myOp, rightType.name), self)
        elif myOp in ["+","-","*"]: # TBD sort numerics here
            if rightType.isNumeric or rightType.isSet:
                res = rightType
            else:
                err = error("%s on nonNumeric or nonset type %s" % (myOp, rightType.name), self)
        elif myOp in ["/"]:
            if rightType.fits(M3Types.M3RealBase) or rightType.isSet:
                res = rightType
            else:
                err = error("%s allowed on Reals and sets only (not on %s)" % (myOp, rightType.name), self)
        elif myOp in ["AND","OR"]:
            if rightType.fits(M3Types.M3Boolean):
                res = rightType
            else:
                err = error("%s on nonBoolean type %s" (myOp, rightType.name), self)
        elif self.isLogical(myOp):
            # first of all we say all objects which are of the same type can be compared
            # TBD this works nicely for sets but what about compound types ?????
            res = M3Types.M3Boolean
        elif myOp == "&":
            if rightType.fits(M3Types.M3Text):
                res = rightType
            else:
                #print myOp
                #print rightType.name
                err = error("%s on nonText type %s" % (myOp, rightType.name), self)
        else:
            err = error("unhandled operator %s" % myOp, self)
        if err:
            return M3Types.M3ErrorType(err)
        else:
            if res.isInteger and res.scaling:
                return M3Types.M3IntegerBase
            else:
                return res
            
    def getVal(self, accum):
        rightVal = self.expr.getVal()
        myOp = self.operator.token
        oddOps = {"=": "==", "#": "!=", "AND": "and", "OR": "or", "&": "+"}
        if myOp in oddOps.keys():
            pyOp = oddOps[myOp]
        else:
            pyOp = myOp
        #print "in getVal", myOp, accum, rightVal
        if accum.tipe.isText:
            exp = "'%s' %s '%s'" % (accum.val, pyOp, rightVal.val)
        else:
            if accum.tipe.isBoolean:
                left = accum.ord().val
            else:
                left = accum.val
            if rightVal.tipe.isBoolean:
                right = rightVal.ord().val
            else:
                right = rightVal.val
            exp = "%s %s %s" % (left, pyOp, right)
        if Options.options.constExp:
            print "EXP>>>", exp #OK
        res = eval(exp)
        if self.isLogical(myOp):
            return M3Types.M3Boolean.createObject(res)
        else:
            return rightVal.clone(res)

class DerefBase:
    def getEnclosingExpr(self):
        return self
    def addDeref(self,source):
        # This is smuggled in here, although it is motivated by C Code generation,
        # because it is called during basic type calculation on expressions.
        # We must move REF dereferences, (either explicit with "^",
        # or implicit with "." and "[" on composite referents)
        # from the "back" or middle of the expression to the front,
        # where they can be generated as (* in C code.
        if not hasattr(self,"derefDict"):
            self.derefDict = {} # use a dict to keep call idempotent
        self.derefDict[source] = True
    def countDerefs(self):
        if not hasattr(self,"derefDict"):
            res = 0
        else:
            res = len(self.derefDict)
        return res



class SelectorExprUser(DerefBase):
    def getVal(self):
        val = self.expr.getVal()
        for sel in self.selectorList.kids:
            val = val.derefVal(sel)
        return val
            
    def flatten(self):
        if not self.selectorList.length():
#            print "about to flatten" , self.expr
#            print "flattening sel %s getting %s" % (self.refid, self.expr.refid)
            fl = self.expr and self.expr.flatten()

            return fl
        else:
            return self
    def getType(self, root=None):
        self.selectorList.notifyCarets()
        base = self.expr.getType()
        # test for illegal use of <arraytype> [ <subscript> ] 
        baseDecl = self.expr.qualId.getEntry().declarer
        self.selectorList.kids[0].checkDeclarer(baseDecl)
        ref = base
        for sel in self.selectorList.kids:
            ref = sel.deref(ref)
        return ref.getTipe()

class SelectorListUser:
    # This hack needed to deal with explicit/implicit carets in dereference with arrays and records
    # yet another consequence of using the concrete syntax to direct code generation
    def notifyCarets(self):
        kids = self.kidsNoSep()
        kids[0].hasPrecedingCaret = False
        for ctr, kid in enumerate(kids):
            if ctr < (len(kids) - 1):
                kids[ctr+1].hasPrecedingCaret = (kid.__class__.__name__ == "CaretNode")

class ExprUser(DerefBase):
    def getExprType(self, root=None):
        res = self.getCachedType()
        if res: return res
        myType = self.expr.getType()
        self.exprType = myType
        self.cachedType = myType
        return myType
    def getVal(self):
        #print "generation", self.genPy()
        return self.expr.getVal()
class ExprListUser:
    def flatten(self):
        if self.length() == 1:
            return self.kids[0].flatten()
        else:
            return self
    def getType(self,unanymousType,root=None):
        # TBD cheapo check here all members must have same type
        #unanymousType = self.kids[0].getType()
        for k in self.kids:
            if not k.getType(unanymousType,root).fits(unanymousType):
                error("type discrepancy in exprlist", self)
        return unanymousType
    def getVal(self, accum):
        for k in self.kids:
            accum = k.getVal(accum)
        return accum
class OpUser(Terminal):
    def getVal(self, expr):
        myOp = self.token
        opdict = {"NOT": "not"}
        if myOp in opdict:
            myOp = opdict[myOp]
        
        if type(expr) == types.InstanceType:
            if expr.tipe.isBoolean:
                exprval = expr.ord().val
            else:
                exprval = expr.val
        else:
            raise "Naked value"
        res = eval("%s %s" % (myOp, exprval))
        return expr.clone(res)
class OpListUser:
    def getVal(self, expr):
        rkids = self.kids[:]
        rkids.reverse()
        res = expr
        for op in rkids:
            res = op.getVal(res)
        return res
class CaretUser:
    def deref(self,ref):
        self.getEnclosingExpr().addDeref(self.refid) 
        if ref.__class__.__name__ == "LUTEntry":
            ref = ref.getTipe()
        if ref.isRef:
#            print "ref" + str(ref)
            return LUTEntry(tipe=ref.referent)
        else:
            res = error("Use of '^' selector on non-reference", self)
            return LUTEntry(tipe=M3Types.M3ErrorType(res))
    def checkDeclarer(self, declarer):
        if declarer and declarer != "VAR":
            error("Use of '^' selector on type", self)

            
class DotUser:
    def deref (self,ref):
        if ref.getTipe().isRecord or ref.getTipe().isObject:
#            print "rec" + str(ref)
            return  ref.deref(self.id.idname,self)
        else:
            res = error("Use of '.' selector on non-record", self)
            return LUTEntry(tipe=M3Types.M3ErrorType(res))
    def checkDeclarer(self, declarer):
        if declarer and declarer != "VAR":
            error("Use of '.' selector on type", self)


class ArrayRefSelectorUser:
    def deref(self,ref):
        #raise "hell"
        def dereffable(ref):
            if ref.__class__.__name__ == "LUTEntry":
                ref = ref.getTipe()
            return ref.isArray or ref.isRef or ref.isList or ref.isDict

        indices = self.exprList.getType()
        for index in indices:
            if dereffable(ref):
                ref = ref.deref(index, self)
            else:
                res = error("Use of subscript on non-array", self)
                return LUTEntry(tipe=M3Types.M3ErrorType(res))
        return ref
    def checkDeclarer(self, declarer):
        if declarer and declarer != "VAR":
            #print self.regen()
            error("Use of subscript on type", self)

class ProcCallSelectorUser:
    def deref(self,ref):
        if ref.__class__.__name__ == "LUTEntry": ref = ref.getTipe()
        if ref and ref.isProcedure:
            return LUTEntry(tipe=ref.deref(self.actualList.getTable(), self))
        else:
            res = error("Procedure call on non-procedure", self)
            return LUTEntry(tipe=M3Types.M3ErrorType(res))
    def checkDeclarer(self, declarer): pass
    
class ActualListUser:
    def getTable(self):
        table = []
        for actual in self.kidsNoSep():
            table.append(actual.getEntry())
        return table
class IndexListUser:
    def getType(self, root=None):
        return [kid.getType() for kid in self.kidsNoSep()]
class ConstructorUser:
    def flatten(self):
        if self.consEltList.isNULL(): #) or (not self.consEltList.length()):
            #print "flattening con %d" % self.refid
            return self.tipe and self.tipe.flatten()
        else:
            return self
    def getType(self, root=None):
        # TBD cache this value
        # check that the elements are ok
        tipe = self.tipe.getType()
        if tipe.isRecord:
            self.consEltList.checkRecordConstructor(tipe)
        elif tipe.isArray:
            self.consEltList.checkArrayConstructor(tipe)
        elif tipe.isSet:
            self.consEltList.checkSetConstructor(tipe)
        elif tipe.isList:
            self.consEltList.checkListConstructor(tipe)
        elif tipe.isDict:
            self.consEltList.checkDictConstructor(tipe)
        else:
            res = error("Constructor not available for type %s" % tipe.image(), self)
            tipe = M3Types.M3ErrorType(res)
        return tipe
    def getVal(self):
        return None # TBD constructors should return values !!!!!!!!!!!!!!!!!!!
        
class ConsEltListUser:
    def checkRecordConstructor(self,tipe):
        actuals = [elt.getRecordElt() for elt in self.kidsNoSep()]
        tipe.checkConstructor(actuals,self)

    def checkListConstructor(self,tipe):
        actuals = [elt.getArrayElt() for elt in self.kidsNoSep()]
        if "DOTDOT" in actuals:
            error(".. not allowed in LIST constructors", self)
            return 
        tipe.checkConstructor(actuals,self)

    def checkDictConstructor(self,tipe):
        actuals = [elt.getDictElt() for elt in self.kidsNoSep()]
        tipe.checkConstructor(actuals,self)
        
    def checkArrayConstructor(self,tipe):
        containedType = tipe.elementType
        actuals = [elt.getArrayElt() for elt in self.kidsNoSep()]
        if "DOTDOT" in actuals:
            for index, actual in enumerate(actuals):
                if (actual == "DOTDOT") and (index+1 != len(actuals)):
                    error(".. only allowed at the end of an array constructor", self)
                    return
            if tipe.isOpen:
                error(".. not allowed in constructors for open arrays", self)
                return        
        tipe.checkConstructor(actuals,self)
        
    def checkSetConstructor(self, tipe):
        actuals = [elt.getSetElt() for elt in self.kidsNoSep()]        
        tipe.checkConstructor(actuals,self)

class ConsEltAssUser: # TBD refactor this verbiage someday
    def getRecordElt(self):
        try:
            val = self.expr.getVal()
        except:
            val = None
        return {"name": self.id.idname, "tipe": self.expr.getExprType(), "val": val}
    def getArrayElt(self):
        err = error("keyword assignment not valid in array constructor", self)
        return Types.M3ErrorType(err)
    def getSetElt(self):
        err = error("keyword assignment not valid in set constructor", self)
        return Types.M3ErrorType(err)
    def getDictElt(self):
        err = error(".. not a valid constructor element for DICT")
        return Types.M3ErrorType(err)

class ConsEltRangeUser:
    def getRecordElt(self):
        err = error("Range not a valid constructor element for record", self)
        return {"name": None, "tipe": Types.M3ErrorType(err), "val":None}
    def getArrayElt(self):
        err = error("range not valid in array constructor")
        return Types.M3ErrorType(err)
    def getSetElt(self):
        return (self.startExpr.getExprType(), self.endExpr.getExprType())
    def getDictElt(self):
        err = error("range is not a valid constructor element for DICT")
        return Types.M3ErrorType(err)

class ConsEltExprUser:
    def getRecordElt(self):
        try:
            val = self.expr.getVal()
        except:
            val = None
        return {"name":None, "tipe": self.expr.getExprType(), "val": val}    
    def getArrayElt(self):
        try:
            val = self.expr.getVal()
        except:
            val = None
        return {"tipe": self.expr.getExprType(), "val": val}    
    def getSetElt(self):
        return self.expr.getExprType()
    def getDictElt(self):
        err = error(".. not a valid constructor element for DICT")
        return Types.M3ErrorType(err)

class ConsEltDotdotUser: 
    def getRecordElt(self):
        err = error(".. not a valid constructor element for RECORD")
        return {"name": None, "tipe": M3Types.M3ErrorType(err), "val":None}
    def getArrayElt(self):
        return "DOTDOT"
    def getSetElt(self):
        err = error(".. not a valid constructor element for SET")
        return Types.M3ErrorType(err)
    def getDictElt(self):
        err = error(".. not a valid constructor element for DICT")
        return Types.M3ErrorType(err)
        
class ConsEltDictUser:
    def getRecordElt(self): 
        err = error("Invalid constructor element for RECORD")
        return Types.M3ErrorType(err)
    def getArrayElt(self): 
        err = error("Invalid constructor element for ARRAY")
        return Types.M3ErrorType(err)
    def getSetElt(self): 
        err = error("Invalid constructor element for SET")
        return Types.M3ErrorType(err)
    def getDictElt(self): # TBD what about values here ?
        return {"name": self.t, "tipe": self.expr.getExprType()};
        
class QualIdUser:

    def getBaseName(self):
        return self.kids[0].idname

    def getBaseEntry(self):
        entry = self.getLUT()
        entry = entry.deref(self.getBaseName(),self)
        return entry
        
    def getEntry(self):
        entry = self.getLUT()
        for ctr,chunk in enumerate(self.kidsNoSep()):
            #print "qualid", chunk.idname, self.lineno
            entry = entry.deref(chunk.idname,self)
        return entry

    def getEmbeddedImplicitDerefs(self):
        res = []
        entry = self.getLUT()
        for ctr,chunk in enumerate(self.kidsNoSep()):
            entry = entry.deref(chunk.idname,self)
            if entry.getTipe().isRef:
                res.append(ctr)
        return res
        
    def getType(self,root=None):
        #print "qualid getType", self.image()
        root,recursive = self.checkRoot(root)
        res = self.getEntry().getTipe(root)
        return res
    def image(self):
        return string.join(self.idList(),".")
    def idList(self):
        return [id.idname for id in self.kidsNoSep()]
    def getVal(self):

        val = None
        tipe = self.getLUT()

        # getting value means dereferencing a possible leading module or enum id
        # and then walking through the value tree from there on

        idsOnly = self.kidsNoSep()

        if len(idsOnly) == 1:
            return tipe.getVal(self.kids[0].idname)
        elif len(idsOnly) == 2:
            tipe = tipe.deref(idsOnly[0].idname, self).getTipe()
            return tipe.getVal(idsOnly[1].idname, self)
        else:
            ctr = 0
            while ctr+1 < len(idsOnly):
                tipe = tipe.deref(idsOnly[ctr].idname, self).getTipe()
                ctr += 1
            return tipe.getVal(idsOnly[ctr].idname, self)

class TypeNameUser:
    def getType(self, root=None):
        root,recursive = self.checkRoot(root)
        res = self.qualId.getType()
        return res
    def getEntry(self):
        return self.qualId.getEntry()
    def getVal(self):
        return self.qualId.getVal()
class RootUser:
    def getType(self, root=None):
        return M3Types.M3Root
class UntracedRootUser:pass
class NumberUser:
    def getType(self, root=None):
        self.getScale()
        if self.scaleType:
            return self.scaleType
        elif self.numberRest.isNULL():
            return M3Types.M3IntegerBase
        else:
            return M3Types.M3RealBase
    def getScale(self):
        if self.scaling and (not self.scaling.isNULL()):
            scale = Scaling.getScaling(self.scaling.idname)
            if scale:
                self.scaleMult = scale.mult
                self.scaleType = scale.type or M3Types.M3IntegerBase
                return
        self.scaleMult = 1
        self.scaleType = None
    def getVal(self):
        self.getScale()
        if self.numberRest.isNULL():
            return M3Types.M3IntegerBase.createObject(self.intVal.getVal() * self.scaleMult)
        else:
            return M3Types.M3RealBase.createObject(eval(self.intVal.intname + "." + self.numberRest.intname))
class CharLiteralUser(Terminal):
    def getType(self, root=None):
        return M3Types.M3Char
    def getVal(self):
        return M3Types.M3Char.createObject(self.token[1:-1])
class TextLiteralUser(Terminal):
    def getType(self, root=None):
        return M3Types.M3Text
    def getVal(self):
        #print "getting value of %s" % self.token
        return M3Types.M3Text.createObject(self.token[1:-1])
class KeyWordUser(Terminal):
    def operator(self):
        return self.token

class NullUser:
    def isNULL(self):
        return True
    def kidsNoSep(self):
        return []

class ActivityDeclUser(LUTOwner):
    def getEnclosingActTrans(self):
        return self
    def tabulate(self,res):
        res.add("activity",self.activityHead.name.idname,self)
    def insertLUT(self):
        name = self.activityHead.name.idname
        lut = self.getLUT().getEnclosingLUT()        
        # look to see if we exist at all
        exists = lut.lookupEntry(name,errorOnMissing=False)
        self.internal = False
        if not exists:
            self.internal = True # suppress some checking later
            # enter us into the LUT as an internalactivity
            lut.enter(name,LUTEntry(node=self,declarer="TYPE",internal=True))
        #print "Activity %s is %s" % (name, {False: "external", True: "internal"}[self.internal])
    def getType(self):
        return self.activityHead.getType()
    def isCapsuleEntity(self):
        return False
    def checkActivity(self):
        if not self.endId.isNULL():
            if self.activityHead.name.idname != self.endId.idname:
                error("Mismatch for end identifier %s of activity" % self.endId.idname, self.endId)
        self.after.checkAfter()
        if self.internal: return 
        self.activityHead.checkMessageMatch()
        # register this transition with the message entry down on the type        
        me = self.activityHead.getMessageEntry()
        if me:
            me.setActivity(self)

class MessageImplementer:
    def checkFormals(self,formals): 
#        self.checkMsgInfo(formals)
        for formal in formals:
            if formal.mode != "VALUE":
                error("Message Handler parameters may only be of mode VALUE",self)
    def checkMessageMatch(self):
        messageEntry = self.getMessageEntry()
        if messageEntry:
            messageType = messageEntry.type
            messageType.checkMatch(self.getType(), self)
    def getMessageEntry(self):
        capsule = self.getCapsuleBlock().parent.getType()
        name = self.name.idname
        if name not in capsule.spec.uniqueMessages:
            #print "No message entry in capsule spec for %s" % name
            if name not in capsule.internalDict:
                #print "internalDict entry",name
                capsule.internalDict[name] = M3Types.MessageDictEntry(self.getType())
            messageEntry = capsule.internalDict[name]
        else:
            if (name not in capsule.spec.uniqueMessagePorts) or (capsule.spec.uniqueMessagePorts[name] not in capsule.spec.inDict):
                error("No interface definition for message %s" % name, self)
                messageEntry = None
            else:
                messageEntry = capsule.spec.inDict[capsule.spec.uniqueMessagePorts[name]]
        return messageEntry
        
        
class ActivityHeadUser(TypeOwner,MessageImplementer):
    def createType(self):
        self.type = M3Types.M3ProcedureType(node=self.parent)
        formals = self.signature.formals.createTable()
        self.checkFormals(formals)
        self.type.formals = formals
        self.type.raises = []
        self.type.name = self.name.idname
        self.type.returnval = M3Types.M3MessageNullReturn
        self.type.isMessageHandler = True
        if not self.getCapsuleBlock():
            error("Activity can only be defined in capsule",self)
class PortUser(TypeOwner):
    def createType(self):
        self.type = M3Types.M3PortType(self,self.id.idname, self.protocol.getType())    

class MessageGroupUser:
    def getDir(self):
        return self.kwdir.token
    def getSynch(self):
        return not self.kwsyn.isNULL()
    def getGroup(self):
        return self.msgList.getMsgs()
class MessageGroupListUser:
    def getGroups(self):
        groups = []
        for msgGroup in self.kidsNoSep():
            groups += msgGroup.getGroup()
        return groups
    
class MessageUser(TypeOwner,LUTOwner):
    # TBD unify with msghandler above
    def createType(self):
        self.type = M3Types.M3ProcedureType(node=self)
        formals = self.signature.formals.createTable()
        self.type.formals = formals
        self.type.raises = []
        if self.parent.getSynch():
            self.type.synch = True
            self.type.returnval = M3Types.M3SynchNullReturn
        else:
            self.type.synch = False
            self.type.returnval = M3Types.M3MessageNullReturn
            
        self.type.dir = self.parent.getDir()

        self.type.name = self.name.idname
        #print "created a message spec for %s" % self.name.idname
class MessageListUser:
    def getDir(self):
        return self.parent.getDir()
    def getSynch(self):
        return self.parent.getSynch()
    def getMsgs(self):
        return [msg.getType() for msg in self.kidsNoSep()]

class PortListUser:
    def getPorts(self):
        return [port.getType() for port in self.kidsNoSep()]

class TriggerUser(TypeOwner):
    def tabulate(self,res):
        res.add("trigger",self.triggerId.idname,self)
    
    def insertLUT(self):
        self.getLUT().enter(self.triggerId.idname,LUTEntry(node=self,declarer="VAR"))
    def createType(self):
        self.type = M3Types.M3TriggerType()

        if not self.triggerExpr.getExprType().isBoolean:
            error("Trigger expression must be of Boolean type", self)

class TimerUser(TypeOwner):
    def createType(self):
        hasDelay = not self.delayExpr.isNULL()
        #print self.periodicity, self.variability
        #(self.changeable, self.periodic) = self.modifiers.check(hasDelay)
        self.periodic = False
        if (not self.periodicity.isNULL()) and (self.periodicity.token == "PERIODIC"):
            self.periodic = True
        self.changeable = True
        if (not self.variability.isNULL()) and  (self.variability.token == "FIXED"):
            self.changeable = False
        if hasDelay:
            if not self.delayExpr.getExprType().isInteger:
                error("Timer delay must be an integer value", self)
        self.type = M3Types.M3TimerType()

class ConnectionsUser: pass
class ConnectionListUser: pass
class PortConnectionUser:
    def compareProtocols(self,sameDirDesired):
        def complainMissing(endImage,name):
            error("Incompatible portToPort connection: %s is missing message %s" % (endImage,name),self)            
        end1Dict = {}
        for message in self.end1.getType().protocol.messages:
            mtype = message.getType()
            end1Dict[mtype.name] = mtype
        for message in self.end2.getType().protocol.messages:
            mtype = message.getType()
            if mtype.name not in end1Dict:
                complainMissing(self.end1.image(),mtype.name)
            else:
                mtype.checkMatch(end1Dict[mtype.name],self)
                sameDir = (mtype.dir == end1Dict[mtype.name].dir)
                if sameDir != sameDirDesired:
                    error("Incompatible directions on message %s" % mtype.name,self)
                end1Dict[mtype.name] = None
        for name in end1Dict:
            if end1Dict[name]:
                complainMissing(self.end2.image(),mtype.name)                

    def compareProtocolsLax(self,sameDirDesired):
        found = False
        end1Dict = {}
        for message in self.end1.getType().protocol.messages:
            mtype = message
            end1Dict[mtype.name] = mtype
        for message in self.end2.getType().protocol.messages:
            mtype = message
            if mtype.name in end1Dict:
                found = True
                mtype.checkMatch(end1Dict[mtype.name],self)
                sameDir = (mtype.dir == end1Dict[mtype.name].dir)
#                if sameDir != sameDirDesired:
#                    error("Incompatible directions on message %s" % mtype.name,self)
        if not found:
            warning("Connection is pointless, ports share no messages")
        
        
    def checkConnection(self):
        for end in self.end1, self.end2:
            type = end.getType()
            if not type.isPort:
                error("%s is not a port" % end.image(), end)
                return 
        # is this child <=> parent or child <=> child
        end1l = len(self.end1.idList())
        end2l = len(self.end2.idList())
        if end1l == 1 and end2l == 1:
            error("%s and %s are both parent ports" % (self.end1.image(), self.end2.image()), self)
            return
        self.end1l = end1l
        self.end2l = end2l
        if end1l == 1 or end2l == 1:
            self.connectionType = "updown"
            #print "parent <=> child"
            #check equality
            self.compareProtocolsLax(sameDirDesired=True)
        else:
            self.connectionType = "across"
            #print "child <=> child"
            #check reciprocity
            self.compareProtocolsLax(sameDirDesired=False)


                 
class ConnectionUser:
    def checkConnection(self):
        # TBD check for double connections etc. here
        # message is either messageName, port.messageName, capsule.messageName or capsule.port.messageName
        # source is either a trigger, a timer or message
        # destination is always a message
        #import pdb; pdb.set_trace()
        source = self.end1.getType()
        dest = self.end2.getType()

        if not dest.isProcedure:
            error("Bad destination for connector",self)
                
        if source.isTrigger or source.isTimer:
            # dest must be an asynch entity
            if dest.returnval != M3Types.M3MessageNullReturn:
                error("Bad destination for connector",self)
            else:
                if len(dest.formals):
                    error("Trigger or Timer destination must be parameterless", self)
                        
        elif source.isProcedure:
            # is this a synch or An asynch connection ?
            if not source.returnval.fits(dest.returnval):
                #import pdb; pdb.set_trace()
                error("Connected items do not match",self)
            else:
                source.checkMatch(dest,self)
        else:
            error("Bad source for connector",self)


        self.source = source
        self.dest = dest
        

class TransitionListUser: pass
class TransitionDeclUser(LUTOwner):
    def getEnclosingActTrans(self):
        return self

    def insertLUT(self):
        name = self.transHead.name.idname
        lut = self.getLUT().getEnclosingLUT()        
        # look to see if we exist at all
        exists = lut.lookupEntry(name,errorOnMissing=False)
        self.internal = False
        if exists and exists.internal:
            self.internal = True
        if not exists:
            self.internal = True # suppress some checking later
            # enter us into the LUT as an internal transition
            lut.enter(name,LUTEntry(node=self,declarer="TYPE",internal=True))
        #print "Transition %s is %s" % (name, {False: "external", True: "internal"}[self.internal])    
    def getType(self):
        return self.transHead.getType()
    def getStateName(self):
        return self.parent.parent.stateId.idname
    def checkTransition(self): 
        # name should match end
        if not self.endId.isNULL():
            if self.transHead.name.idname != self.endId.idname:
                error("Mismatch for end identifier %s of transition" % self.endId.idname, self)
        # must contain at least one NEXT
        # TBD really?
        self.after.checkAfter()
        #if self.internal: return # TBD this is missing out on all kinds of checking
        stateName = self.parent.parent.stateId # TBD what is a good idiom to get around fragile statements like this?
        # register this transition with the message entry down on the type
        me = self.transHead.getMessageEntry()
        if me:
            # signature must fit msg in spec
            self.transHead.checkMessageMatch()
            me.setTransition(self.getStateName(),self)
        
class TransitionHeadUser(TypeOwner,MessageImplementer):
    def createType(self):
        self.type = M3Types.M3ProcedureType(node=self.parent)
        formals = self.signature.formals.createTable()
        self.checkFormals(formals)
        self.type.formals = formals
        self.type.raises = []
        self.type.name = self.name.idname
        self.type.returnval = M3Types.M3MessageNullReturn
        self.type.isMessageHandler = True
        if not self.getCapsuleBlock():
            error("Activity can only be defined in capsule")

class StateDeclUser:
    def tabulate(self,res):
        res.add("state",self.stateId.idname,self)
    def checkStateDecl(self):
        if not self.getCapsuleBlock(): error("State only allowed in a capsule block", self)
        # state name should be unique
        # only allowed at top level of capsule
        
class NextStUser:
    def checkNextSt(self): pass
        # Only allowed in START and Transitions
        # acts as a return : should only be at end of code branch
class StartDeclUser:
    def tabulate(self,res):
        res.add("start","start",self)

    def checkStartDecl(self): pass
       # TBD must contain Next
       # TBD Start state must exist

class UseCapsuleUser: 
    def insertLUT(self):
        for usedCapsule in self.idList.kidsNoSep():
            impXML = m3.compile(fileName=usedCapsule.idname + ".ci3o")
            self.getLUT().enter(usedCapsule.idname,LUTEntry(node=impXML,declarer="TYPE"))
    def addUsedNames(self,names):
        for usedCapsule in self.idList.kidsNoSep():
            names.append(usedCapsule.idname)
            
class UseCapsuleListUser:
    def getUsedCapsuleNames(self):
        names = []
        for useClause in self.kids:
            useClause.addUsedNames(names)
        return names

class DataDependencyUser:
    def tabulate(self,res):
        pass
    def checkIntention(self):
        dataType = self.dataName.getType()
        # currently allow anything that passes the getType test

class SendsDeclUser:
    def tabulate(self,res):
        pass
    def checkIntention(self):
        sendType = self.messName.getType()
        if not (sendType.isProcedure or sendType.isError):
            error("SENDS not used on activity",self)

class TokUser(Terminal): pass

class SepUser(Terminal):
    def isSep(self):
        return True

class ListUser(TypeOwner):
    def createType(self):
        elementType = self.tipe.getType()
        self.type = M3Types.M3ListType(elementType)

class DictUser(TypeOwner):
    def createType(self):
        elementType = self.tipe.getType()
        if self.idx.isNULL():
            indexType = M3Types.M3Text
        else:
            indexType = self.idx.getType()
        self.type = M3Types.M3DictType(indexType,elementType)


class ForEachStUser(LUTOwner):
    def inLoop(self): return True
    def checkForSt(self):
        err = None
        listType = self.listExpr.getExprType()
        if listType.isList or listType.isArray:
            self.looptype = listType.elementType
        else:
            err = error("FOREACH over non-list", self)
            self.looptype = M3Types.M3ErrorType(err)

class ProtocolUser(TypeOwner):
    def createType(self):
        #import pdb; pdb.set_trace()
        self.type = M3Types.M3ProtocolType(self.mgl.getGroups())
        dict = {}
        for msg in self.type.messages:
            if msg.name in dict:
                error("Message %s used twice in this protocol" % msg.name, self)
            dict[msg.name] = True
        

class ConjugatedProtocolUser(TypeOwner):
    def createType(self):
        # TBD check that this actually is a protocol
        type = self.pro.getType()
        if type.isProtocol:
            self.type = type.conjugate()
        else:
            error("Only protocol types may be conjugated",self)
            self.type = type
            
class AggregatedProtocolUser(TypeOwner):
    def createType(self):
        type1 = self.t1.getType()
        type2 = self.t2.getType()
        err = None
        if not type1.isProtocol:
            err = error("left hand type in aggregation is not a protocol", self)
        if not type2.isProtocol:
            err = error("right hand type in aggregation is not a protocol", self)
        if err:
            self.type = type1 # just to keep things rolling
        else:
            self.type = type2.aggregate(type1,self)


class ScaledTypeUser(TypeOwner):
    def createType(self):
        self.scaling = None
        coreType = self.tn.getType()
        if not coreType.isInteger:
            error("only integer types can be scaled", self)
            self.type = coreType
        else:
            self.scaling = self.calcScaling()
            #print "created scaled type", self.scaling
            self.type = coreType.makeScaledType(self.scaling)            
            Scaling.setScalingType(self.scaling, self.type)
    def calcScaling(self):
        return self.scaleList.calcScaling(self.unit.idname)

class ScaleEltUser:
    def getElt(self):
        n = self.n.getVal()
        if not n.tipe.isInteger:
            error("Only integers allowed in scaling clauses", self)
        n = n.val
        return (self.i.idname,n)

class ScaleListUser:
    def calcScaling(self,unit):
        #import pdb; pdb.set_trace()
        scaleRes = [(unit, 1)]
        Scaling.addScaling(unit, 1, self)
        if self.length():
            mult = 1
            for kid in self.kids:
                n,i = kid.getElt()
                if n in scaleRes:
                    error("%s used twice in this scaling clause" % n, self)
                else:
                    mult *= i
                    Scaling.addScaling(n,mult,self)
                    scaleRes.append((n,mult))
        scaleRes.reverse()
        return scaleRes
    
class AfterClauseUser:
    def checkAfter(self):
        if not self.afterExpr.isNULL():
            et = self.afterExpr.getExprType()
            if not et.isInteger:
                error("Bad type used in AFTER clause expected INTEGER and got %s" % et, self);
        

    def collectAfters(self,res):
        if not self.afterExpr.isNULL():
            res.append(self.afterExpr)
