import RTSTypes
class C2(RTSTypes.M3CapsuleRuntimeType):
    def c2act(self):
        self.send(self, self.level, 'messageFromC2', )
    def __init__(self,level):
        self.level = level
        RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
