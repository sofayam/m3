import M3Objects
import M3Types
import RTSTypes
import M3Predefined
import ConjTypesInt as CT
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/ConjC1CapMod')
class ConjC1(RTSTypes.M3CapsuleRuntimeType):
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
  self.M3param_converters = {'p1.a' : (),'p1.b' : (),}
  self.M3port_converters = {'a': 'p1.a', 'b': 'p1.b'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return ConjC1(level,hName)
if __name__ == '__main__': runcap()
