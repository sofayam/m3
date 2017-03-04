import M3Objects
import M3Types
import M3Predefined
import M3TypeLib
import M3ProcLib
M3TL=M3TypeLib.internaliseTypes(r'/home/mark/m3/lib/m3lib/MathInt')
pi=M3Types.M3RealBase.createObject(3.1415926535897931)
e=M3Types.M3RealBase.createObject(2.7182818284590451)

def acos(x):
    import MathMod
    return MathMod.acos(x)
M3ProcLib.enter('Math.i3o:39',acos)

def asin(x):
    import MathMod
    return MathMod.asin(x)
M3ProcLib.enter('Math.i3o:67',asin)

def atan(x):
    import MathMod
    return MathMod.atan(x)
M3ProcLib.enter('Math.i3o:95',atan)

def atan2(x):
    import MathMod
    return MathMod.atan2(x)
M3ProcLib.enter('Math.i3o:123',atan2)

def ceil(x):
    import MathMod
    return MathMod.ceil(x)
M3ProcLib.enter('Math.i3o:151',ceil)

def cos(x):
    import MathMod
    return MathMod.cos(x)
M3ProcLib.enter('Math.i3o:179',cos)

def cosh(x):
    import MathMod
    return MathMod.cosh(x)
M3ProcLib.enter('Math.i3o:207',cosh)

def degrees(x):
    import MathMod
    return MathMod.degrees(x)
M3ProcLib.enter('Math.i3o:235',degrees)

def exp(x):
    import MathMod
    return MathMod.exp(x)
M3ProcLib.enter('Math.i3o:263',exp)

def fabs(x):
    import MathMod
    return MathMod.fabs(x)
M3ProcLib.enter('Math.i3o:291',fabs)

def floor(x):
    import MathMod
    return MathMod.floor(x)
M3ProcLib.enter('Math.i3o:319',floor)

def fmod(x,y):
    import MathMod
    return MathMod.fmod(x,y)
M3ProcLib.enter('Math.i3o:347',fmod)

def fmantisse(x):
    import MathMod
    return MathMod.fmantisse(x)
M3ProcLib.enter('Math.i3o:377',fmantisse)

def fexp2(x):
    import MathMod
    return MathMod.fexp2(x)
M3ProcLib.enter('Math.i3o:405',fexp2)

def hypot(x):
    import MathMod
    return MathMod.hypot(x)
M3ProcLib.enter('Math.i3o:433',hypot)

def ldexp(x):
    import MathMod
    return MathMod.ldexp(x)
M3ProcLib.enter('Math.i3o:461',ldexp)

def log(x,base):
    import MathMod
    return MathMod.log(x,base)
M3ProcLib.enter('Math.i3o:489',log)

def log10(x):
    import MathMod
    return MathMod.log10(x)
M3ProcLib.enter('Math.i3o:528',log10)

def modf(x):
    import MathMod
    return MathMod.modf(x)
M3ProcLib.enter('Math.i3o:556',modf)

def pow(x,y):
    import MathMod
    return MathMod.pow(x,y)
M3ProcLib.enter('Math.i3o:584',pow)

def radians(x):
    import MathMod
    return MathMod.radians(x)
M3ProcLib.enter('Math.i3o:614',radians)

def sin(x):
    import MathMod
    return MathMod.sin(x)
M3ProcLib.enter('Math.i3o:642',sin)

def sinh(x):
    import MathMod
    return MathMod.sinh(x)
M3ProcLib.enter('Math.i3o:670',sinh)

def sqrt(x):
    import MathMod
    return MathMod.sqrt(x)
M3ProcLib.enter('Math.i3o:698',sqrt)

def tan(x):
    import MathMod
    return MathMod.tan(x)
M3ProcLib.enter('Math.i3o:726',tan)

def tanh(x):
    import MathMod
    return MathMod.tanh(x)
M3ProcLib.enter('Math.i3o:754',tanh)
