import M3Objects
import M3Types
import RTSTypes
import M3Predefined
from BankTypesInt import Card
from BankTypesInt import Card
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/ATMSafeCapMod')
class ATMSafe(RTSTypes.M3CapsuleRuntimeType):
 def M3TriggerProc31(self):
  return self.failureCount.equals(M3Types.M3IntegerBase.createObject(3))
 def M3startCapsule(self):
  self.M3State='empty'
  self.M3TransitionFinishedHook(self.M3State)
 def insertCard(self,card):
  if self.M3State in ['empty']:
   m=getattr(self,'M3insertCard__'+self.M3State)
   self.M3TransitionCallHook('insertCard',self.M3State)
   m(card)
  else:
   self.M3NoTransitionForMessageInState('insertCard',self.M3State)
  self.M3TransitionFinishedHook(self.M3State)
 def M3insertCard__empty(self,card):
  M3incStat('RECEIVE','insertCard')
  self.cardInfo.assign(card)
  self.M3State='inserted'
 def inputSum(self,sum):
  if self.M3State in ['authorized']:
   m=getattr(self,'M3inputSum__'+self.M3State)
   self.M3TransitionCallHook('inputSum',self.M3State)
   m(sum)
  else:
   self.M3NoTransitionForMessageInState('inputSum',self.M3State)
  self.M3TransitionFinishedHook(self.M3State)
 def M3inputSum__authorized(self,sum):
  M3incStat('RECEIVE','inputSum')
  M3incStat('SEND','accounting.withdraw')
  self.sendAfter(self, self.__level, 'accounting.withdraw', 0, sum)
  M3incStat('SEND','cashSlot.emitCash')
  self.sendAfter(self, self.__level, 'cashSlot.emitCash', 0, )
  M3incStat('SEND','cardSlot.returnCard')
  self.sendAfter(self, self.__level, 'cardSlot.returnCard', 0, )
  self.M3State='empty'
 def inputPIN(self,pin):
  if self.M3State in ['inserted']:
   m=getattr(self,'M3inputPIN__'+self.M3State)
   self.M3TransitionCallHook('inputPIN',self.M3State)
   m(pin)
  else:
   self.M3NoTransitionForMessageInState('inputPIN',self.M3State)
  self.M3TransitionFinishedHook(self.M3State)
 def M3inputPIN__inserted(self,pin):
  M3incStat('RECEIVE','inputPIN')
  if pin.equals(self.cardInfo.getField('encodedPIN')).toBool():
   self.M3State='authorized'
  else:
   self.failureCount.assign(self.failureCount.plus(M3Types.M3IntegerBase.createObject(1)))
 def reject(self,):
  if self.M3State in ['inserted']:
   m=getattr(self,'M3reject__'+self.M3State)
   self.M3TransitionCallHook('reject',self.M3State)
   m()
  else:
   self.M3NoTransitionForMessageInState('reject',self.M3State)
  self.M3TransitionFinishedHook(self.M3State)
 def M3reject__inserted(self,):
  M3incStat('RECEIVE','reject')
  self.failureCount.assign(M3Types.M3IntegerBase.createObject(0))
  self.M3State='empty'
 def __init__(self,level,runtimeName):
  self.runtimeName = runtimeName
  self.__level = level
  RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
  self.shadyCustomer = RTSTypes.M3TriggerType(self.M3TriggerProc31)
  self.cardInfo=Card.createObject()
  self.failureCount=M3Types.M3IntegerBase.createObject(M3Types.M3IntegerBase.createObject(0).val)
  self.__init_capsule_connect()
  self.__init_capsule_begin_end()
  self.__init_param_converters()
 def __init_capsule_connect(self):
  self.shadyCustomer.connect(self,'','reject',self,self.__level)
 def __init_capsule_begin_end(self): pass # capsule BEGIN .. END
 def __init_param_converters(self):
  self.M3param_converters = {'cardSlot.insertCard' : (('card', Card),),'keyboard.inputPIN' : (('pin', M3Types.M3IntegerBase),),'keyboard.inputSum' : (('sum', M3Types.M3IntegerBase),),'cashSlot.emitCash' : (),'cardSlot.returnCard' : (),'accounting.withdraw' : (('sum', M3Types.M3IntegerBase),),}
  self.M3port_converters = {'inputSum': 'keyboard.inputSum', 'returnCard': 'cardSlot.returnCard', 'emitCash': 'cashSlot.emitCash', 'inputPIN': 'keyboard.inputPIN', 'withdraw': 'accounting.withdraw', 'insertCard': 'cardSlot.insertCard'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return ATMSafe(level,hName)
if __name__ == '__main__': runcap()
