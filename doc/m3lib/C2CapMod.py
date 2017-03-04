import M3Objects
import M3Types
import RTSTypes
import M3Predefined
import TimerInt as Timer
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/C2CapMod')
class C2(RTSTypes.M3CapsuleRuntimeType):
 def c2act(self, ):
  M3incStat('RECEIVE','c2act')
  M3incStat('SEND','p2.messageFromC2')
  self.sendAfter(self, self.__level, 'p2.messageFromC2', 0, )
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
  self.M3param_converters = {'p1.c2act' : (),'p2.messageFromC2' : (),}
  self.M3port_converters = {'c2act': 'p1.c2act', 'messageFromC2': 'p2.messageFromC2'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return C2(level,hName)
if __name__ == '__main__': runcap()
