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
M3TL=M3TypeLib.internaliseTypes(r'm3lib/ATMCapMod')
class ATM(RTSTypes.M3CapsuleRuntimeType):
 def inputPIN(self, pin):
  M3incStat('RECEIVE','inputPIN')
  if self.cardState.equals(self.CardState.withVal('Inserted')).opand(pin.equals(self.cardInfo.getField('encodedPIN'))).toBool():
   self.cardState.assign(self.CardState.withVal('Authorized'))
 def insertCard(self, card):
  M3incStat('RECEIVE','insertCard')
  self.cardState.assign(self.CardState.withVal('Inserted'))
  self.cardInfo.assign(card)
 def inputSum(self, sum):
  M3incStat('RECEIVE','inputSum')
  if self.cardState.equals(self.CardState.withVal('Authorized')).toBool():
   M3incStat('SEND','accounting.withdraw')
   self.sendAfter(self, self.__level, 'accounting.withdraw', 0, sum)
   M3incStat('SEND','cashSlot.emitCash')
   self.sendAfter(self, self.__level, 'cashSlot.emitCash', 0, )
   M3incStat('SEND','cardSlot.returnCard')
   self.sendAfter(self, self.__level, 'cardSlot.returnCard', 0, )
   self.cardState.assign(self.CardState.withVal('Empty'))
 def __init__(self,level,runtimeName):
  self.runtimeName = runtimeName
  self.__level = level
  RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
  self.CardState=M3TL[2].finalTipe
  self.cardInfo=Card.createObject()
  self.cardState=self.CardState.createObject(self.CardState.withVal('Empty').val)
  self.__init_capsule_connect()
  self.__init_capsule_begin_end()
  self.__init_param_converters()
 def __init_capsule_connect(self): pass
 def __init_capsule_begin_end(self): pass # capsule BEGIN .. END
 def __init_param_converters(self):
  self.M3param_converters = {'cardSlot.insertCard' : (('card', Card),),'keyboard.inputPIN' : (('pin', M3Types.M3IntegerBase),),'keyboard.inputSum' : (('sum', M3Types.M3IntegerBase),),'cashSlot.emitCash' : (),'cardSlot.returnCard' : (),'accounting.withdraw' : (('sum', M3Types.M3IntegerBase),),}
  self.M3port_converters = {'inputSum': 'keyboard.inputSum', 'returnCard': 'cardSlot.returnCard', 'emitCash': 'cashSlot.emitCash', 'inputPIN': 'keyboard.inputPIN', 'withdraw': 'accounting.withdraw', 'insertCard': 'cardSlot.insertCard'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return ATM(level,hName)
if __name__ == '__main__': runcap()
