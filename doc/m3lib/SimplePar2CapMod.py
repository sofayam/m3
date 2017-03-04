import M3Objects
import M3Types
import RTSTypes
import M3Predefined
import TimerInt as Timer
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/SimplePar2CapMod')
class SimplePar2(RTSTypes.M3CapsuleRuntimeType):
 def delegate(self, ):
  M3incStat('RECEIVE','delegate')
  M3incStat('SEND','p2.done')
  self.sendAfter(self, self.__level, 'p2.done', M3Types.M3IntegerBase.createObject(3 * 1000000000000).val, )
  self.M3LockProcessor(max(M3Types.M3IntegerBase.createObject(3 * 1000000000000).val,M3Types.M3IntegerBase.createObject(6 * 1000000000000).val))
 def __init__(self,level,runtimeName):
  self.runtimeName = runtimeName
  self.__level = level
  RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
  self.__init_capsule_connect()
  self.__init_capsule_begin_end()
  self.__init_param_converters()
 def __init_capsule_connect(self): pass
 def __init_capsule_begin_end(self): pass # capsule BEGIN .. END
 def __init_param_converters(self):
  self.M3param_converters = {'p1.delegate' : (),'p2.done' : (),}
  self.M3port_converters = {'done': 'p2.done', 'delegate': 'p1.delegate'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return SimplePar2(level,hName)
if __name__ == '__main__': runcap()
