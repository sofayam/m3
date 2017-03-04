import M3Objects
import M3Types
import RTSTypes
import M3Predefined
import TimerInt as Timer
import IOInt as IO
import M3TypeLib
import M3ProcLib
import CapsuleMap
from Statistics import M3incStat
M3TL=M3TypeLib.internaliseTypes(r'm3lib/pytimerCapMod')
class pytimer(RTSTypes.M3CapsuleRuntimeType):
 def timeact(self, ):
  M3incStat('RECEIVE','timeact')
  IO.Put(M3Types.M3Text.createObject("timeact\n"))
  self.i.assign(self.i.plus(M3Types.M3IntegerBase.createObject(1)))
  M3incStat('SEND','p1.foo')
  self.sendAfter(self, self.__level, 'p1.foo', 0, self.i)
 def __init__(self,level,runtimeName):
  self.runtimeName = runtimeName
  self.__level = level
  RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
  self.myTimer=RTSTypes.M3TimerRuntimeType(delay=M3Types.M3IntegerBase.createObject(10),periodic=True,changeable=False).createObject()
  self.i=M3Types.M3IntegerBase.createObject(M3Types.M3IntegerBase.createObject(0).val)
  self.__init_capsule_connect()
  self.__init_capsule_begin_end()
  self.__init_param_converters()
 def __init_capsule_connect(self):
  self.myTimer.connect(self,'','timeact',self,self.__level)
 def __init_capsule_begin_end(self): # capsule BEGIN .. END
  Timer.Start(self.myTimer)
 def __init_param_converters(self):
  self.M3param_converters = {'p1.foo' : (('i', M3Types.M3IntegerBase),),}
  self.M3port_converters = {'foo': 'p1.foo'}
def runcap():
 import Simulator
 Simulator.run(createCapsule(1,'top'))
def createCapsule(level,hName):
 return pytimer(level,hName)
if __name__ == '__main__': runcap()
