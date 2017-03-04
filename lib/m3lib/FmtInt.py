import M3Objects
import M3Types
import M3Predefined
import M3TypeLib
import M3ProcLib
M3TL=M3TypeLib.internaliseTypes(r'/home/mark/m3/lib/m3lib/FmtInt')

def Bool(b):
    import FmtMod
    return FmtMod.Bool(b)
M3ProcLib.enter('Fmt.i3o:7',Bool)

def Char(c):
    import FmtMod
    return FmtMod.Char(c)
M3ProcLib.enter('Fmt.i3o:35',Char)

def Int(n):
    import FmtMod
    return FmtMod.Int(n)
M3ProcLib.enter('Fmt.i3o:63',Int)
