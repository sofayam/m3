import M3Objects
import M3Types
import RTSTypes
import M3Predefined
import BankTypesInt as BankTypes
import BankTypesInt as BankTypes
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/BankInterestCapMod')
class BankInterest(RTSTypes.M3CapsuleRuntimeType):
 def __init__(self,level,runtimeName):
  self.runtimeName = runtimeName
  self.__level = level
  RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
  self.atm=CapsuleMap.createCapsule(self.__level+1,'ATM',self.runtimeName+'.'+'atm')
  self.account=CapsuleMap.createCapsule(self.__level+1,'Account',self.runtimeName+'.'+'account')
  self.interest=CapsuleMap.createCapsule(self.__level+1,'Interest',self.runtimeName+'.'+'interest')
  self.__init_capsule_connect()
  self.__init_capsule_begin_end()
  self.__init_param_converters()
 def __init_capsule_connect(self):
  self.connect(self,'counter.deposit','movement.deposit',self.account,self.__level)
  self.connect(self,'wall.inputPIN','keyboard.inputPIN',self.atm,self.__level)
  self.connect(self,'wall.inputSum','keyboard.inputSum',self.atm,self.__level)
  self.connect(self,'wall.insertCard','cardSlot.insertCard',self.atm,self.__level)
  self.atm.connect(self,'cardSlot.returnCard','wall.returnCard',self,self.__level)
  self.atm.connect(self,'cashSlot.emitCash','wall.emitCash',self,self.__level)
  self.connect(self,'admin.setInterestRate','admin.setInterestRate',self.interest,self.__level)
  self.interest.connect(self,'mail.statement','mail.statement',self,self.__level)
  self.atm.connect(self,'accounting.withdraw','movement.withdraw',self.account,self.__level)
  self.interest.connect(self,'account.requestBalance','information.requestBalance',self.account,self.__level)
 def __init_capsule_begin_end(self): pass # capsule BEGIN .. END
 def __init_param_converters(self):
  self.M3param_converters = {'wall.inputSum' : (('sum', M3Types.M3IntegerBase),),'wall.insertCard' : (('card', BankTypes.Card),),'admin.setInterestRate' : (('rate', M3Types.M3RealBase),),'wall.inputPIN' : (('pin', M3Types.M3IntegerBase),),'counter.deposit' : (('sum', M3Types.M3IntegerBase),),'wall.returnCard' : (),'mail.statement' : (('sum', M3Types.M3IntegerBase),),'wall.emitCash' : (),}
  self.M3port_converters = {'inputSum': 'wall.inputSum', 'returnCard': 'wall.returnCard', 'emitCash': 'wall.emitCash', 'inputPIN': 'wall.inputPIN', 'deposit': 'counter.deposit', 'statement': 'mail.statement', 'setInterestRate': 'admin.setInterestRate', 'insertCard': 'wall.insertCard'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return BankInterest(level,hName)
if __name__ == '__main__': runcap()
