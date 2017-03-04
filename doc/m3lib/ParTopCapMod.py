import M3Objects
import M3Types
import RTSTypes
import M3Predefined
import TimerInt as Timer
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/ParTopCapMod')
class ParTop(RTSTypes.M3CapsuleRuntimeType):
 def __init__(self,level,runtimeName):
  self.runtimeName = runtimeName
  self.__level = level
  RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
  self.par1=CapsuleMap.createCapsule(self.__level+1,'SimplePar',self.runtimeName+'.'+'par1')
  self.par2=CapsuleMap.createCapsule(self.__level+1,'SimplePar2',self.runtimeName+'.'+'par2')
  self.__init_capsule_connect()
  self.__init_capsule_begin_end()
  self.__init_param_converters()
 def __init_capsule_connect(self):
  self.connect(self,'p1.getBusy','p1.getBusy',self.par1,self.__level)
  self.par1.connect(self,'p1.delegate','p1.delegate',self.par2,self.__level)
  self.par2.connect(self,'p2.done','p1.done',self,self.__level)
 def __init_capsule_begin_end(self): pass # capsule BEGIN .. END
 def __init_param_converters(self):
  self.M3param_converters = {'p1.getBusy' : (),'p1.done' : (),}
  self.M3port_converters = {'getBusy': 'p1.getBusy', 'done': 'p1.done'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return ParTop(level,hName)
if __name__ == '__main__': runcap()
