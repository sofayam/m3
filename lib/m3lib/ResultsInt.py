import M3Objects
import M3Types
import M3Predefined
import M3TypeLib
import M3ProcLib
M3TL=M3TypeLib.internaliseTypes(r'/home/mark/m3/lib/m3lib/ResultsInt')

def Write(msg):
    import ResultsMod
    return ResultsMod.Write(msg)
M3ProcLib.enter('Results.i3o:7',Write)

def WriteProtocol(msg):
    import ResultsMod
    return ResultsMod.WriteProtocol(msg)
M3ProcLib.enter('Results.i3o:33',WriteProtocol)
