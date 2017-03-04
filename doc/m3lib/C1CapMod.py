import M3Objects
import M3Types
import RTSTypes
import M3Predefined
import TimerInt as Timer
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/C1CapMod')
class C1(RTSTypes.M3CapsuleRuntimeType):
 def __init__(self,level,runtimeName):
  self.runtimeName = runtimeName
  self.__level = level
  RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
  self.c2=CapsuleMap.createCapsule(self.__level+1,'C2',self.runtimeName+'.'+'c2')
  self.c3=CapsuleMap.createCapsule(self.__level+1,'C3',self.runtimeName+'.'+'c3')
  self.__init_capsule_connect()
  self.__init_capsule_begin_end()
  self.__init_param_converters()
 def __init_capsule_connect(self):
  self.connect(self,'p1.input','p1.c2act',self.c2,self.__level)
  self.c2.connect(self,'p2.messageFromC2','p1.c3act',self.c3,self.__level)
  self.c3.connect(self,'p2.response','p2.response',self,self.__level)
 def __init_capsule_begin_end(self): pass # capsule BEGIN .. END
 def __init_param_converters(self):
  self.M3param_converters = {'p1.input' : (),'p2.response' : (),}
  self.M3port_converters = {'input': 'p1.input', 'response': 'p2.response'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return C1(level,hName)
if __name__ == '__main__': runcap()
