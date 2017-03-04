import Simulator
import RTSTypes
class pytrigger(RTSTypes.M3CapsuleRuntimeType):
    def triggerChecker(self):
        return self.counter == 0
    def dec(self):
        self.counter -= 1
    def handler(self):
        self.send(self, self.level, 'alarm', )
    def __init__(self,level):
        self.level = level
        RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
        self.isZero = RTSTypes.M3TriggerType(self.triggerChecker)
        self.counter = 2
        self.isZero.connect(self,'','handler',self,self.level)

Simulator.run(pytrigger(1))
