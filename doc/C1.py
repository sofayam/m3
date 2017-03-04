import RTSTypes
import Simulator

import C2
import C3
class C1(RTSTypes.M3CapsuleRuntimeType):
    def __init__(self,level):
        self.level = level
        RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
        self.c2=C2.C2(level+1)
        self.c3=C3.C3(level+1)
        self.connect(context=self,
                     srcMsg='input',
                     destMsg='c2act',
                     destObj=self.c2,
                     level=level)
        self.c2.connect(self,'messageFromC2','c3act',self.c3,level)
        self.c3.connect(self,'response','response',self,level)
Simulator.run(C1(1))
