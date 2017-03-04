import M3Objects
import M3Types
import RTSTypes
import M3Predefined
import TimerInt as Timer
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/ConjParentCapMod')
class ConjParent(RTSTypes.M3CapsuleRuntimeType):
 def __init__(self,level,runtimeName):
  self.runtimeName = runtimeName
  self.__level = level
  RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
  self.c1=CapsuleMap.createCapsule(self.__level+1,'ConjC1',self.runtimeName+'.'+'c1')
  self.c2=CapsuleMap.createCapsule(self.__level+1,'ConjC2',self.runtimeName+'.'+'c2')
  self.__init_capsule_connect()
  self.__init_capsule_begin_end()
  self.__init_param_converters()
 def __init_capsule_connect(self):
  self.c2.connect(self,'p1.a','p1.a',self.c1,self.__level)
  self.c1.connect(self,'p1.b','p1.b',self.c2,self.__level)
 def __init_capsule_begin_end(self): pass # capsule BEGIN .. END
 def __init_param_converters(self):
  self.M3param_converters = {}
  self.M3port_converters = {}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return ConjParent(level,hName)
if __name__ == '__main__': runcap()
