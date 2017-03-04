import M3Objects
import M3Types
import M3Predefined
import M3TypeLib
import M3ProcLib
M3TL=M3TypeLib.internaliseTypes(r'/home/mark/m3/lib/m3lib/TimerInt')
Time=M3Types.M3IntegerBase.makeScaledType([('year', 31536000000000000000L), ('day', 86400000000000000L), ('hour', 3600000000000000L), ('min', 60000000000000L), ('s', 1000000000000L), ('ms', 1000000000), ('us', 1000000), ('ns', 1000), ('ps', 1)])

def Start(T):
    import TimerMod
    return TimerMod.Start(T)
M3ProcLib.enter('Timer.i3o:95',Start)

def Stop(T):
    import TimerMod
    return TimerMod.Stop(T)
M3ProcLib.enter('Timer.i3o:124',Stop)

def Change(T,newValue):
    import TimerMod
    return TimerMod.Change(T,newValue)
M3ProcLib.enter('Timer.i3o:153',Change)

def GetElapsed():
    import TimerMod
    return TimerMod.GetElapsed()
M3ProcLib.enter('Timer.i3o:193',GetElapsed)
