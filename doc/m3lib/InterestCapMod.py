import M3Objects
import M3Types
import RTSTypes
import M3Predefined
import TimerInt as Timer
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/InterestCapMod')
class Interest(RTSTypes.M3CapsuleRuntimeType):
 def setInterestRate(self, rate):
  M3incStat('RECEIVE','setInterestRate')
  self.interestRate.assign(rate)
 def updateAccount(self, sum):
  M3incStat('RECEIVE','updateAccount')
  accrued=M3Types.M3RealBase.createObject()
  accrued.assign(M3Predefined.M3FLOAT(sum).times(self.interestRate).divide(M3Types.M3RealBase.createObject(100.0)))
  M3incStat('SEND','account.deposit')
  self.sendAfter(self, self.__level, 'account.deposit', 0, M3Predefined.M3TRUNC(accrued))
  M3incStat('SEND','mail.statement')
  self.sendAfter(self, self.__level, 'mail.statement', 0, sum.plus(M3Predefined.M3TRUNC(accrued)))
 def __init__(self,level,runtimeName):
  self.runtimeName = runtimeName
  self.__level = level
  RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
  self.auditTimer=RTSTypes.M3TimerRuntimeType(delay=M3Types.M3IntegerBase.createObject(1 * 31536000000000000000),periodic=True,changeable=False).createObject()
  self.interestRate=M3Types.M3RealBase.createObject(M3Types.M3RealBase.createObject(10.0).val)
  self.__init_capsule_connect()
  self.__init_capsule_begin_end()
  self.__init_param_converters()
 def __init_capsule_connect(self):
  self.auditTimer.connect(self,'','account.requestBalance',self,self.__level)
 def __init_capsule_begin_end(self): # capsule BEGIN .. END
  Timer.Start(self.auditTimer)
 def __init_param_converters(self):
  self.M3param_converters = {'admin.setInterestRate' : (('rate', M3Types.M3RealBase),),'account.updateAccount' : (('sum', M3Types.M3IntegerBase),),'account.deposit' : (('sum', M3Types.M3IntegerBase),),'mail.statement' : (('sum', M3Types.M3IntegerBase),),'account.requestBalance' : (),}
  self.M3port_converters = {'setInterestRate': 'admin.setInterestRate', 'requestBalance': 'account.requestBalance', 'updateAccount': 'account.updateAccount', 'statement': 'mail.statement', 'deposit': 'account.deposit'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return Interest(level,hName)
if __name__ == '__main__': runcap()
