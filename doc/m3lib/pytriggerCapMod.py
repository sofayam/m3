import M3Objects
import M3Types
import RTSTypes
import M3Predefined
import TimerInt as Timer
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/pytriggerCapMod')
class pytrigger(RTSTypes.M3CapsuleRuntimeType):
 def M3TriggerProc17(self):
  return self.counter.equals(M3Types.M3IntegerBase.createObject(0))
 def dec(self, ):
  M3incStat('RECEIVE','dec')
  self.counter.assign(self.counter.minus(M3Types.M3IntegerBase.createObject(1)))
 def handler(self, ):
  M3incStat('RECEIVE','handler')
  M3incStat('SEND','p1.alarm')
  self.sendAfter(self, self.__level, 'p1.alarm', 0, )
 def __init__(self,level,runtimeName):
  self.runtimeName = runtimeName
  self.__level = level
  RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
  self.isZero = RTSTypes.M3TriggerType(self.M3TriggerProc17)
  self.counter=M3Types.M3IntegerBase.createObject(M3Types.M3IntegerBase.createObject(2).val)
  self.__init_capsule_connect()
  self.__init_capsule_begin_end()
  self.__init_param_converters()
 def __init_capsule_connect(self):
  self.isZero.connect(self,'','handler',self,self.__level)
 def __init_capsule_begin_end(self): pass # capsule BEGIN .. END
 def __init_param_converters(self):
  self.M3param_converters = {'p1.dec' : (),'p1.alarm' : (),}
  self.M3port_converters = {'alarm': 'p1.alarm', 'dec': 'p1.dec'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return pytrigger(level,hName)
if __name__ == '__main__': runcap()
