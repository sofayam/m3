import M3Objects
import M3Types
import RTSTypes
import M3Predefined
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/AccountCapMod')
class Account(RTSTypes.M3CapsuleRuntimeType):
 def deposit(self, sum):
  M3incStat('RECEIVE','deposit')
  newtotal=M3Types.M3IntegerBase.createObject()
  newtotal.assign(self.money.plus(sum))
  self.money.assign(newtotal)
 def withdraw(self, sum):
  M3incStat('RECEIVE','withdraw')
  newtotal=M3Types.M3IntegerBase.createObject()
  newtotal.assign(self.money.minus(sum))
  self.money.assign(newtotal)
 def requestBalance(self, ):
  M3incStat('RECEIVE','requestBalance')
  M3incStat('SEND','information.balance')
  self.sendAfter(self, self.__level, 'information.balance', 0, sum=self.money)
 def __init__(self,level,runtimeName):
  self.runtimeName = runtimeName
  self.__level = level
  RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
  self.money=M3Types.M3IntegerBase.createObject(M3Types.M3IntegerBase.createObject(0).val)
  self.__init_capsule_connect()
  self.__init_capsule_begin_end()
  self.__init_param_converters()
 def __init_capsule_connect(self): pass
 def __init_capsule_begin_end(self): pass # capsule BEGIN .. END
 def __init_param_converters(self):
  self.M3param_converters = {'movement.withdraw' : (('sum', M3Types.M3IntegerBase),),'movement.deposit' : (('sum', M3Types.M3IntegerBase),),'information.requestBalance' : (),'information.balance' : (('sum', M3Types.M3IntegerBase),),}
  self.M3port_converters = {'requestBalance': 'information.requestBalance', 'balance': 'information.balance', 'deposit': 'movement.deposit', 'withdraw': 'movement.withdraw'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return Account(level,hName)
if __name__ == '__main__': runcap()
