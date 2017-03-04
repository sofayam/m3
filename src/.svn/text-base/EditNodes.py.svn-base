# Implements functionality needed for capsule editor
# includes
#   gathering avatars from capsule code,
#   adding new subtrees using source templates,
#   finding data dependencies
#
import string
import Avatars
class BaseEdit:
    def isEditable(self):
        return False
    def gatherDataStores(self):
        return []
    def gatherChildCapsules(self):
        return []
    def gatherActivities(self):
        return []
    def gatherTriggers(self):
        return []
    def gatherTimers(self):
        return []
    def gatherStates(self):
        return []
    def gatherTransitions(self):
        return []
    def gatherProcedures(self):
        return []
    def gatherSendStmtConnections(self):
        sendStmts = []
        for kid in self.kids:
            sendStmts += kid.gatherSendStmtConnections()
        return sendStmts
    def gatherSendsDecl(self):
        return []
    def gatherNexts(self):
        nexts = []
        for kid in self.kids:
            if kid:
                nexts += kid.gatherNexts()
        return nexts
    def gatherStart(self):
        for kid in self.kids:
            start = kid.gatherStart()
            if start: return start
    def getEnclosingState(self):
        return self.parent.getEnclosingState()
    def renumber(self,lineno=1):
        if self.isTerminal(): 
            lineno += self.returnCount()
            #print lineno
        self.lineno = lineno
        for kid in self.kids:
            if kid:
                lineno = kid.renumber(lineno)
        if self.length() and not self.kids[0].isNULL():
            self.lineno = self.kids[0].lineno # lineno is where our first leaf really starts
        return lineno
    def lineRangeSub(self,res):
        if self.isTerminal():
            res.append(self.lineno)
        for kid in self.kids:
            kid.lineRangeSub(res)
    def lineRange(self):
        res = []
        self.lineRangeSub(res)
        return res[0],res[len(res)-1]
    def getReadWriteDependencies(self,res):
        #print "getrwdeps", self
        for kid in self.kids:
            kid.getReadWriteDependencies(res)
    def getCapsuleEntityQualIds(self,res):
        for kid in self.kids:
            kid.getCapsuleEntityQualIds(res)
    def getCalls(self,res):
        for kid in self.kids:
            kid.getCalls(res)
class Gatherer:
    def gatherDataStores(self):
        dataStores = []
        for kid in self.kids:
            dataStores += kid.gatherDataStores()
        return dataStores
    def gatherChildCapsules(self):
        childCapsules = []
        for kid in self.kids:
            childCapsules += kid.gatherChildCapsules()
        return childCapsules
    def gatherActivities(self):
        activities = []
        for kid in self.kids:
            activities += kid.gatherActivities()
        return activities
    def gatherTriggers(self):
        triggers = []
        for kid in self.kids:
            triggers += kid.gatherTriggers()
        return triggers
    def gatherTimers(self):
        timers = []
        for kid in self.kids:
            timers += kid.gatherTimers()
        return timers
    def gatherStates(self):
        states = []
        for kid in self.kids:
            states += kid.gatherStates()
        return states
    def gatherTransitions(self):
        trans = []
        for kid in self.kids:
            trans += kid.gatherTransitions()
        return trans
    def gatherProcedures(self):
        procs = []
        for kid in self.kids:
            procs += kid.gatherProcedures()
        return procs
        
class CapsuleInterfaceEdit:
    def appendMessage(self, dialDict):
        import LoadSrc
        messageName = dialDict["name"]
        messageDir = dialDict["dir"]
        portName = dialDict["port"]
        timing = dialDict["tim"]
        if timing == "ASYNCHRONOUS":
            timing = ""
        else:
            timing += " "
        templateSpec = "\n %s%s MESSAGE %s() ;" % (timing, messageDir, messageName)
        messageSpec = LoadSrc.compileFragment('MessageGroup', templateSpec)        
        # A blank portname means just put it in the first one you find
        for port in self.portList.kidsNoSep():
            if (portName == '') or (port.id.idname == portName):
                if port.protocol.__class__.__name__ == "TypeNameNode":
                    print "cannot add message to externally defined protocol - use a text editor for advanced stuff like this"
                else:
                    if messageName in [msg.name for msg in port.protocol.getType().messages]:
                        print "message %s already exists" % messageName
                        return 
                    port.protocol.mgl.kids.append(messageSpec)
                return 
        raise "panic : this port does not exist"
        LoadSrc.regulariseTree(self)
    def messageNames(self):
        res = []
        for port in self.portList.kidsNoSep():
            for message in port.protocol.getType().messages:
                res.append(message.name)
        return res
    def gatherPorts(self):
        return [Avatars.Port(port.id.idname, port) for port in self.portList.kidsNoSep()]
    def appendPort(self,name):
        import LoadSrc
        portNode = LoadSrc.compileFragment('Port', "\nPORT %s : PROTOCOL\nEND" % name)
        sepNode = LoadSrc.compileFragment('tokSEMI',";")
        
        ports = self.portList.kids
        if len(ports) and (not ports[len(ports)-1].isSep()):
            ports.append(sepNode)
        ports.append(portNode)
        
        LoadSrc.regulariseTree(self)        
class CapsuleEdit:
    def appendActivity(self,name,specTopNode,dialDict):
        import LoadSrc
        visibility = dialDict['visibility']
        if visibility == "External":
            dialDict["dir"] = "INCOMING"
            dialDict["tim"] = "ASYNCHRONOUS"
            specTopNode.appendMessage(dialDict)
            LoadSrc.regulariseTree(specTopNode)            
        templateBody = "\n  ACTIVITY %s () = \n  BEGIN \n  END %s ;" % (name, name)
        activityNode = LoadSrc.compileFragment('Decl', templateBody)
        self.block.decList.kids.append(activityNode)
        LoadSrc.regulariseTree(self)

    def appendProcedure(self,name,specTopNode,dialDict):
        import LoadSrc
        visibility = dialDict['visibility']
        if visibility == "External":
            dialDict["dir"] = "INCOMING"
            dialDict["tim"] = "SYNCHRONOUS"            
            specTopNode.appendMessage(dialDict)
            LoadSrc.regulariseTree(specTopNode)            
        templateBody = "\n  PROCEDURE %s () = \n  BEGIN \n  END %s ;" % (name, name)
        procNode = LoadSrc.compileFragment('Decl', templateBody)
        self.block.decList.kids.append(procNode)
        LoadSrc.regulariseTree(self)


    def appendVarDecl(self,decl):
        self.block.decList.kids.append(decl)
    def appendDataStore(self, name, type):
        import LoadSrc
        dataNode = LoadSrc.compileFragment('Decl', '\n  VAR %s : %s ;' % (name, type))
        self.block.decList.kids.append(dataNode)
        LoadSrc.regulariseTree(self)
    def appendState(self,name):
        import LoadSrc
        stateNode = LoadSrc.compileFragment('Decl', "\n  STATE %s;" % (name))
        self.block.decList.kids.append(stateNode)    
        LoadSrc.regulariseTree(self)
    def appendTransition(self,specTopNode,fromState,dialDict):
        import LoadSrc
        transName = dialDict['name']
        transNode = LoadSrc.compileFragment(
            'TransitionDecl', "\n    ON %s() =\n      BEGIN\n      END %s" % (transName, transName))
        sepNode = LoadSrc.compileFragment('tokSEMI',";")
        fromState.node.appendTransition(transNode,sepNode)
        LoadSrc.regulariseTree(self)
        visibility = dialDict['visibility']
        if (not transName in specTopNode.messageNames()) and (visibility == 'External'):
            messageSpec = LoadSrc.compileFragment(
                'MessageGroup',"\n    INCOMING MESSAGE %s() ;" % transName)
            dialDict["dir"] = "INCOMING"
            specTopNode.appendMessage(dialDict)
            LoadSrc.regulariseTree(specTopNode)
        return transNode
    def appendStart(self,startState):
        import LoadSrc
        startDecl = LoadSrc.compileFragment(
            'Decl', "\n  START = BEGIN\n    NEXT %s\n  END;" % startState)
        self.block.decList.kids.append(startDecl)    
        LoadSrc.regulariseTree(self)
    def appendTrigger(self,name,dialDict):
        import LoadSrc
        triggerNode = LoadSrc.compileFragment('Decl',"\n  TRIGGER %s ON %s ;" % (name, dialDict['expr']))
        self.block.decList.kids.append(triggerNode)
        LoadSrc.regulariseTree(self)
    def appendTimer(self,name,dialDict):
        import LoadSrc
        if dialDict['delay']:
            delayValue = " DELAY %s %s" % (dialDict['delay'], dialDict['scale'])
        else:
            delayValue = ""
        fragment = "\n  VAR %s : %s %s TIMER %s ;" % (
            name, dialDict['periodicity'], dialDict['variability'], delayValue)
        timerNode = LoadSrc.compileFragment('Decl',fragment)        
        self.block.decList.kids.append(timerNode)
        LoadSrc.regulariseTree(self)
    def appendUseCapsule(self,useNode):
        self.usedCapsules.kids.append(useNode)
    def appendChild(self,childname,capsulename):
        import LoadSrc
        if capsulename not in self.getUsedCapsuleNames():
            useNode = LoadSrc.compileFragment('UseCapsule',"\n  USECAPSULE %s ;" % capsulename)
            self.appendUseCapsule(useNode)
        childNode = LoadSrc.compileFragment('Decl',"\n  VAR %s : %s ;" % (childname, capsulename))

        self.block.decList.kids.append(childNode)
#        self.node = childNode.variables.kids[0]
#        self.setup() # call this again now that the node has been set
       

    def appendConnectionSection(self, connectionSection):
        self.block.kids[1] = connectionSection # !!! TBD this is brittle !!!
        self.block.restore()
    def appendConnection(self,connection,sepNode):
        self.block.connections.connectionList.appendConnection(connection,sepNode)
    def isEditable(self):
        return True
    def gatherCapsule(self):
        return Avatars.Capsule(self.modname.idname,self)
    def gatherDataStores(self):
        return self.block.decList.gatherDataStores()
    def gatherChildCapsules(self):
        return self.block.decList.gatherChildCapsules()
    def gatherActivities(self):
        return self.block.decList.gatherActivities()
    def gatherTriggers(self):
        return self.block.decList.gatherTriggers()
    def gatherTimers(self):
        return self.block.decList.gatherTimers() 
    def gatherStates(self):
        return self.block.decList.gatherStates()         
    def gatherTransitions(self):
        return self.block.decList.gatherTransitions()
    def gatherProcedures(self):
        return self.block.decList.gatherProcedures()

    def gatherConnectMessageConnections(self):
        c = self.block.connections
        if  c.isNULL():
            return []
        else:
            return c.connectionList.gatherConnectMessageConnections()
    def gatherTransitionProxies(self,transitions):
        def getTransBaseName(avName):
            frags = string.split(avName,":")
            if len(frags) == 2:
                return frags[1]
            else:
                return ""
        class FakeNode:
            def getReadWriteDependencies(self,dummy): pass
        proxies = []
        for name in self.getType().internalDict:
            # check if it is a transition
            transBaseNames = [getTransBaseName(t.name) for t in transitions]
            if name in transBaseNames:
                proxies.append(Avatars.TransitionProxy(name,FakeNode()))
        return proxies

class ActivityDeclEdit:
    def gatherActivities(self):
        return [Avatars.Activity(self.activityHead.name.idname,self)]
    def appendDependencyInfo(self,depInfo,sepNode):
        self.handlerBlock.decList.appendDependencyInfo(depInfo,sepNode)
    def appendSendsDecl(self, sendsDecl):
        self.handlerBlock.decList.appendSendsDecl(sendsDecl)        
    def gatherSendMessageConnections(self):
        # get all the SENDS declarations 
        res = self.handlerBlock.decList.gatherSendsDeclConnections()
        # ... and all the SEND statements
        res += self.handlerBlock.statements.gatherSendStmtConnections()
        return res
class VariableDeclEdit:
    def gatherDataStores(self):
        type = self.getType()
        if not (type.isTrigger or type.isTimer or type.isCapsuleSpec):
            # Mark the entries as capsuleEntities as well
            for id in self.idlist.kidsNoSep():
                id.setCapsuleEntity()
            return [Avatars.DataStore(id.idname,self) for id in self.idlist.kidsNoSep()]
        else:
            return []
    def gatherChildCapsules(self):
        if self.getType().isCapsuleSpec:
            for id in self.idlist.kidsNoSep():
                id.setCapsuleEntity()
            return [Avatars.Child(id.idname,self) for id in self.idlist.kidsNoSep()]            
        else:
            return []
    def gatherTimers(self):
        if self.getType().isTimer:
            for id in self.idlist.kidsNoSep():
                id.setCapsuleEntity()
            return [Avatars.Timer(id.idname,self) for id in self.idlist.kidsNoSep()]
        else:
            return []


class TransitionDeclEdit:
    def appendNext(self,nextNode,sepNode1,sepNode2):
        stats = self.block.statements.kids
        if len(stats):
            if not stats[len(stats)-1].isSep():
                stats.append(sepNode1)
        stats.append(nextNode)
        stats.append(sepNode2)        
    def gatherTransition(self,owningState):
        name = owningState.name + ":" + self.transHead.name.idname
        avatar = Avatars.Transition(name, self)
        avatar.setOwningState(owningState)
        return [avatar]
    def appendDependencyInfo(self,depInfo,sepNode):
        self.block.decList.appendDependencyInfo(depInfo,sepNode)
    def appendSendsDecl(self, sendsDecl):
        self.block.decList.appendSendsDecl(sendsDecl)        
    def gatherSendMessageConnections(self):
        # get all the SENDS declarations and all the SEND statements
        res = self.block.decList.gatherSendsDeclConnections()
        res += self.block.statements.gatherSendStmtConnections()
        return res
class StateDeclEdit:
    def gatherStates(self):
        self.avatar = Avatars.State(self.stateId.idname,self)
        return [self.avatar]
    def appendTransition(self,transNode,sepNode):
        
        if len(self.transitionList.kids) > 0:
            self.transitionList.kids.append(sepNode)
        self.transitionList.kids.append(transNode)
    def gatherTransitions(self):
        trans = []
        for kid in self.transitionList.kidsNoSep():
            trans += kid.gatherTransition(self.avatar)
        return trans
class TriggerEdit:
    def gatherTriggers(self):
        return [Avatars.Trigger(self.triggerId.idname,self)]
    def getReadWriteDependencies(self,res):
        readers = []
        self.triggerExpr.getCapsuleEntityQualIds(readers)
        for reader in readers:
            res.append(("READS",reader))
class TransitionListEdit: pass

class NextStEdit:
    def gatherNexts(self):
        return [self.stateId.idname]
    
class DeclListEdit(Gatherer):
    def appendDependencyInfo(self,depInfo,sepNode):
        self.kids.append(depInfo)

    def appendSendsDecl(self,sendsDecl):
        self.kids.append(sendsDecl)   
    def gatherSendsDeclConnections(self):
        res = []
        for decl in self.kids:
            sd = decl.gatherSendsDecl()
            if sd:
                res.append(sd)                
        return res
    
class StartDeclEdit:
    def gatherStart(self):
        return Avatars.Start('*start*',self)

class ConnectionListEdit: 
    def gatherConnectMessageConnections(self):
        return [connection.gatherConnectMessageConnection() for connection in self.kidsNoSep()]
    def appendConnection(self,connection,sepNode):
        if len(self.kids):
            if not self.kids[len(self.kids)-1].isSep():
                self.kids.append(sepNode)
        self.kids.append(connection)
class PortConnectionEdit:
    def gatherConnectMessageConnection(self):
        return ("PC",self.end1.idList(),self.end2.idList()) # TBD        
class ConnectionEdit:
    def gatherConnectMessageConnection(self):
        # TBD Back in UserNodes we derived types for all this but they are no use to us here
        # TBD So just hand back the id elts from the qualids and let CapsuleDrawing sort it out for the time being
        return ("MC",self.end1.idList(),self.end2.idList())

class VariableDeclsEdit(Gatherer): pass
class VariableDeclsListEdit(Gatherer): pass


class DataDependencyEdit:
    def getReadWriteDependencies(self,res):
        if self.kwd.token == "READS":
            res.append(("READS",self.dataName.image()))
        if self.kwd.token == "WRITES":
            res.append(("WRITES",self.dataName.image()))

class AssignStEdit: 
    def getReadWriteDependencies(self,res):
        self.lhs.getWriteDependencies(res)
        readers = []
        self.rhs.getCapsuleEntityQualIds(readers)
        for reader in readers:
            res.append(("READS", reader))        

class ForStEdit: pass
    
class IfStEdit: pass
    
class QualIdEdit:
    def isCapsuleEntityReference(self):
        res = hasattr(self.getBaseEntry(),"CapsuleEntity")
        #print "is capsule entity " ,self.image(), res
        return res
    def getCapsuleEntityQualIds(self, res):
        if self.isCapsuleEntityReference():
            res.append(self.getBaseName())
    def getReadWriteDependencies(self,res):
        readers = []
        self.getCapsuleEntityQualIds(readers)
        for reader in readers:
            res.append(("READS", reader))
class ExprEdit: 
    def getWriteDependencies(self,res):
        self.expr.getWriteDependencies(res)
    def getReadDependencies(self,res):
        self.expr.getReadDependencies(res)

class TypeNameEdit:
    def getWriteDependencies(self,res):
        # this is where you currently catch procedure names
        if self.qualId.isCapsuleEntityReference():
            res.append(("WRITES",self.qualId.getBaseName()))
class NumberEdit: pass

class SelectorExprEdit: 
    def getReadWriteDependencies(self,res):
        writer = []
        self.expr.getCapsuleEntityQualIds(writer)
        if len(writer) == 0:
            pass 
        elif len(writer) == 1:
            res.append(("WRITES", writer[0]))
            #import pdb; pdb.set_trace()
            print "write deps for call to", writer[0]
        else:
            raise "data structure anomaly : expr of selector has more than one qualId"
        readers = []
        self.selectorList.getCapsuleEntityQualIds(readers)
        for reader in readers:
            res.append(("READS", reader))
    def getWriteDependencies(self,res):
        pass
        

class IdEdit:
    def setCapsuleEntity(self,parent=False):
        lut = self.getLUT()
        if parent:
            lut = lut.getEnclosingLUT()
        lut.lookupLocalEntry(self.idname).CapsuleEntity = True


class SendsDeclEdit:
    def gatherSendsDecl(self):
        res = self.messName.idList()
        return res
    def getReadWriteDependencies(self,res):
        pass
class SendStEdit:
    def gatherSendStmtConnections(self):
        return [self.expr.expr.expr.qualId.idList()]
        # TBD Send Statements use the procedure rule which uses expression rules
    def getReadWriteDependencies(self,res):
        readers = []
        self.expr.expr.selectorList.getCapsuleEntityQualIds(readers)
        for reader in readers:
            res.append(("READS",reader))

class ReplyStEdit: pass

class SynCallStEdit:
    def getCalls(self,res):
        res.append(self.expr.expr.expr.qualId.idList())
        # returning a list here will trigger port finding logic in CapsuleDrawing
    def getReadWriteDependencies(self,res):
        readers = []
        self.expr.expr.selectorList.getCapsuleEntityQualIds(readers)
        for reader in readers:
            res.append(("READS",reader))

class CallStEdit:
    def getCalls(self, res):
        self.expr.expr.expr.getCapsuleEntityQualIds(res)
    def getReadWriteDependencies(self,res):

        def addToRes(ids, formal, res):
            if formal.mode == "VAR":
                id = ids[0]
                res.append(("WRITES", id))
                # TBD the rest might be parameters, this is a grubby heuristic for the time being
                if len(ids) > 1:
                    for id in ids[1:]:
                        res.append(("READS", id))
            else:
                for id in ids:
                    res.append(("READS",id))

        actualQualids = self.expr.expr.selectorList.kids[0].actualList.getActualQualIdTable()

        # now find the sig of the procedure we are calling
        formals = self.expr.expr.expr.getType().formals

        # precook the formals into a tasty dictionary
        formalDict = {}
        for formal in formals:
            formalDict[formal.name] = formal

        ctr = 0
        for actual in actualQualids:
            # don't worry about order of positional/keyed, this has already be done for us
            key = actual['key']
            ids = actual['ids']
            if not len(ids): continue # don't bother if there were no ids involved
            if key:
                
                formal = formalDict[key]
                addToRes(ids, formal, res)
            else:
                formal = formals[ctr]
                addToRes(ids, formal, res)
            ctr += 1

class AssertStEdit: pass

class ProcedureDeclEdit: 
    def gatherProcedures(self):
        procName = self.procHead.name
        procName.setCapsuleEntity(parent=True) # do not use your own lookup table
        return [Avatars.Procedure(procName.idname,self)]    

class ActualListEdit:
    def getActualQualIdTable(self):
        table = []
        for actual in self.kidsNoSep():
            table.append(actual.getActualQualIdTableEntry())
        return table

class ActualExprEdit:
    def getActualQualIdTableEntry(self):
        if self.id.isNULL():
            name = None
        else:
            name = self.id.idname
        actIds = []
        self.expr.getCapsuleEntityQualIds(actIds)
        return {'key': name, 'ids': actIds}


class SelectorListEdit: pass

class ArrayRefSelectorEdit: pass

class ProcCallSelectorEdit: pass

#--------------------- Just along for the ride ---------------------

class InterfaceEdit: pass
class GenericInterfaceEdit: pass
class GenericModuleEdit: pass
class InterfaceInstantiationEdit: pass
class ModuleEdit: pass
class ModuleInstantiationEdit: pass
class FromImportEdit: pass
class UseCapsuleEdit: pass
class UseCapsuleListEdit: pass
class AsImportEdit: pass
class AsImportListEdit: pass
class IdListEdit: pass
class ImportListEdit: pass
class ImportItemEdit: pass
class RenamedImportItemEdit: pass
class InterfaceDeclListEdit: pass
class BlockEdit: pass
class CapsuleBlockEdit: pass
class ConstDeclsEdit: pass
class ConstDeclsListEdit: pass
class TypeDeclsEdit: pass
class TypeDeclsListEdit: pass
class ExceptionDeclsEdit: pass
class ExceptionDeclsListEdit: pass
class ProcedureHeadEdit: pass

class SignatureEdit: pass
class MethodSignatureEdit: pass
class FormalsEdit: pass
class FormalEdit: pass
class RevealsEdit: pass
class RevealsListEdit: pass
class RevealEdit: pass
class GenFormalsEdit: pass
class GenActualsEdit: pass
class ConstDeclEdit: pass
class TypeDeclEdit: pass
class ExceptionDeclEdit: pass
class RaisesEdit: pass
class RaisesListEdit: pass
class RaisesAnyEdit: pass


class CaseStEdit: pass
class CaseEltListEdit: pass
class VCaseEltListEdit: pass
class CaseEltEdit: pass
class ExitStEdit: pass
class EvalStEdit: pass

class LoopStEdit: pass

class ElsifListEdit: pass
class ElsifEdit: pass
class LockStEdit: pass

class RaiseStEdit: pass
class RepeatStEdit: pass
class ReturnEdit: pass
class TCaseStEdit: pass
class TCaseListEdit: pass
class TryXptStEdit: pass
class TryFinStEdit: pass
class WhileStEdit: pass
class WithStEdit: pass
class BindingListEdit: pass
class HandlerListEdit: pass
class LabelsListEdit: pass
class LabelsEdit: pass
class CaseEdit: pass
class VCaseEdit: pass
class HandlerEdit: pass
class HandlerQualidListEdit: pass
class TypeListEdit: pass
class TCaseEdit: pass
class BindingEdit: pass
class ActualEdit: pass
class ArrayEdit: pass
class PackedEdit: pass
class BracketedTypeEdit: pass
class EnumEdit: pass
class ObjectEdit: pass
class ObjectListEdit: pass
class ProcedureEdit: pass
class RecordEdit: pass
class VariantRecordEdit: pass
class RefEdit: pass
class SetEdit: pass
class SubrangeEdit: pass
class BrandEdit: pass
class FieldListEdit: pass
class FieldEdit: pass
class MethodListEdit: pass
class MethodEdit: pass
class OverrideListEdit: pass
class OverrideEdit: pass
class ConstExprEdit: pass
class BracketedExprEdit: pass
class BinaryExprEdit: pass
class UnaryExprEdit: pass
class OpExpEdit: pass


class ExprListEdit: pass
    
class OpListEdit: pass
class CaretEdit: pass
class DotEdit: pass
class ArrayRefSelectorEdit: pass
class ProcCallSelectorEdit: pass
        
class IndexListEdit: pass
class ConstructorEdit: pass
class ConsEltListEdit: pass
class ConsEltAssEdit: pass
class ConsEltRangeEdit: pass
class ConsEltExprEdit: pass
class ConsEltDotdotEdit: pass


class RootEdit: pass
class UntracedRootEdit: pass

class ForIdEdit: pass
class BindingIdEdit: pass
class TCaseIdEdit: pass
class IntEdit: pass
class CharLiteralEdit: pass
class TextLiteralEdit: pass
class KeyWordEdit: pass
class TokEdit: pass
class SepEdit: pass
class OpEdit: pass
class NullEdit: pass
class PortEdit: pass
class MessageGroupEdit: pass
class MessageGroupListEdit: pass
class MessageEdit: pass
class MessageListEdit: pass
class PortListEdit: pass
class ActivityHeadEdit: pass
class TimerModifierListEdit: pass
class TimerEdit: pass
class StatementsEdit: pass
class ConnectionsEdit: pass

class TransitionHeadEdit: pass

        
    

class PythonStEdit: pass
class ResetStEdit: pass
class ListEdit: pass
class DictEdit: pass
class ForEachStEdit: pass
class ConsEltDictEdit: pass
class ProtocolEdit: pass
class ConjugatedProtocolEdit: pass

class ScaledTypeEdit: pass
class ScaleEltEdit: pass
class ScaleListEdit: pass

class AggregatedProtocolEdit: pass
class AfterClauseEdit: pass
