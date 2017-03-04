import M3Objects
import M3Types
import M3Predefined
import M3TypeLib
import M3ProcLib
M3TL=M3TypeLib.internaliseTypes(r'/home/mark/m3/lib/m3lib/IOInt')

def Put(T):
    import IOMod
    return IOMod.Put(T)
M3ProcLib.enter('IO.i3o:7',Put)

def PutInt(I):
    import IOMod
    return IOMod.PutInt(I)
M3ProcLib.enter('IO.i3o:33',PutInt)

def PutReal(f):
    import IOMod
    return IOMod.PutReal(f)
M3ProcLib.enter('IO.i3o:59',PutReal)

def PutChar(C):
    import IOMod
    return IOMod.PutChar(C)
M3ProcLib.enter('IO.i3o:85',PutChar)
