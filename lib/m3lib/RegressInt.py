import M3Objects
import M3Types
import M3Predefined
import M3TypeLib
import M3ProcLib
M3TL=M3TypeLib.internaliseTypes(r'/home/mark/m3/lib/m3lib/RegressInt')

def init(name):
    import RegressMod
    return RegressMod.init(name)
M3ProcLib.enter('Regress.i3o:7',init)

def assertPass(cond):
    import RegressMod
    return RegressMod.assertPass(cond)
M3ProcLib.enter('Regress.i3o:33',assertPass)

def summary():
    import RegressMod
    return RegressMod.summary()
M3ProcLib.enter('Regress.i3o:59',summary)
