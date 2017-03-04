import M3Objects
import M3Types
import M3Predefined
import M3TypeLib
import M3ProcLib
M3TL=M3TypeLib.internaliseTypes(r'/home/mark/m3/lib/m3lib/TextInt')
T=M3Types.M3Text

def Equal(t,u):
    import TextMod
    return TextMod.Equal(t,u)
M3ProcLib.enter('Text.i3o:17',Equal)

def FromChars(a):
    import TextMod
    return TextMod.FromChars(a)
M3ProcLib.enter('Text.i3o:47',FromChars)
