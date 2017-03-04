import Simulator
import RTSTypes
class act1(RTSTypes.M3CapsuleRuntimeType):
    def a1(self, foo, bar):
        print "activity a1 called with foo %s and bar %s" % (foo, bar) 
    def __init__(self,level):
        RTSTypes.M3CapsuleRuntimeType.__init__(self,level)

Simulator.run(act1(1))
