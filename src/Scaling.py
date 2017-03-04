from Message import error
scalings = {}

class Scale:
    def __init__(self, mult, type=None):
        self.mult = mult
        self.type = None
    def getMult(self):
        return self.mult
    def getType(self):
        if not self.type:
            raise "compiler error: untyped scaling"
        else:
            return self.type
    def setType(self,type):
        self.type = type


errorScaling = Scale(1,None)

def addScaling(n,i,obj):
    if n in scalings and i != scalings[n].getMult():
        error("Conflicting scaling definition for %s" % n, obj)
    else:
        scalings[n] = Scale(i)

def setScalingType(scale,type):
    for name, factor in scale:
        scalings[name].setType(type)

def getScaling(n):
    if n not in scalings:
        error("Scaling %s does not exist" % n)
        return None
    else:
        return scalings[n]

def image(scale, val):
    img = ""
    sign = ""
    if val < 0:
        sign = "-"
        val = -val
    if val == 0:
        unitName, unitFactor = scale[-1]
        img = "...0 %s" % unitName
    else:
        for name,factor in scale:
            quot = val / factor
            if quot:
                img += " + %s %s" % (quot, name)
                val -= quot * factor
    return sign + img[3:]

def flush():
    global scalings
    scalings = {}

