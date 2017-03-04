F_psec = 1L
F_nsec = F_psec * 1000L
F_usec = F_nsec * 1000L
F_msec = F_usec * 1000L
F_sec  = F_msec * 1000L
F_min  = F_sec  * 60L
F_hour = F_min  * 60L
F_day  = F_hour * 24L
F_year = F_day * 365L
    
FactorNames = {}

FactorList = [('year', F_year),
              ('day', F_day),
              ('hour', F_hour),
              ('min', F_min),
              ('s', F_sec),
              ('ms', F_msec),
              ('us', F_usec),
              ('ns', F_nsec),
              ('ps', F_psec)]

for abbrev, tickval in FactorList:
    FactorNames[abbrev] = tickval

class Time:

    def __init__(self, quantity=0, factor=None):
        if factor:
            self.ticks = quantity * FactorNames[factor]
        else:
            self.ticks = 0
    def __add__(self, other):
        if other.__class__ is not self.__class__:
            raise "TimeError"
        t = Time()
        t.ticks = self.ticks + other.ticks
        return t
    def __sub__(self, other):
        if other.__class__ is not self.__class__:
            raise "TimeError"
        t = Time()
        t.ticks = self.ticks - other.ticks
        return t
    def __str__(self):
        img = ""
        ticker = long(self.ticks)
        for name, factor in FactorList:
            quot = ticker / factor
            if quot:
                img += (" + %s " % quot) + name
                ticker -= quot * factor
        return img[2:]

# TBD
# These functions expose me as an 'object cheater' : fixing this will mean crawling
# all over the scheduler code in Timer. Wait a while to see whether we really
# need to do that

def timeString(delta):
    t = Time()
    t.ticks = delta
    return str(t)

def convertToDelta(quantity, factor):
    t = Time(quantity, factor)
    return t.ticks

def makeTime(timeList):
    res = 0
    for number, name in timeList:
        res += FactorNames[name] * int(number)
    return res

