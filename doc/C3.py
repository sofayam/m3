import RTSTypes
class C3(RTSTypes.M3CapsuleRuntimeType):
    def c3act(self):
        self.send(self, self.level, 'response', )
    def __init__(self,level):
        self.level = level
        RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
