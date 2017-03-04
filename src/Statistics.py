SimCycles = 0
TriggersActivated = 0
TimersElapsed = 0

everybody = []
trace = []
globStatistics = {}
objectTypes = {}
allCtrs = {}
com = "% "


def printTrace(event,details):
    import Global
    if Global.trace:
        Global.results.putTrace(event + ":" + details)

def M3incStat(ctrName, name=""):
    if ctrName not in globStatistics:
        globStatistics[ctrName] = 0
    globStatistics[ctrName] += 1
    printTrace(ctrName, name)
    
class Gatherer:
    def __init__(self,name=None):
        if name:
            self.statisticsName = name
        else:
            self.statisticsName = self.__class__.__name__
        self.statisticsCtrs = {}
        addToCensus(self)
    def incStatCtr(self,ctrName):
        if ctrName not in allCtrs:
            allCtrs[ctrName] = 0
        allCtrs[ctrName] += 1
        printTrace(ctrName, self.__class__.__name__)

def addToCensus(M3Object):
    name = M3Object.statisticsName
    if name not in objectTypes:
        objectTypes[name] = 1
    else:
        objectTypes[name] += 1

def fillDots(label, value, width=30):
    valstr = "%s" % value
    return label + ("." * (width - len(label) - len(valstr))) + valstr 
    

def basic():
    res = ""
    res += "%sStatistics for this run\n" % com
    res += "%sBasic:\n" % com
    res += "%s %s\n" % (com, fillDots("Simulation Cycles", SimCycles))
    res += "%s %s\n" % (com, fillDots("Triggers activated", TriggersActivated))
    res += "%s %s\n" % (com, fillDots("Timers elapsed", TimersElapsed))
    return res

def gory():
    res = "%sGory:\n" % com
    res += "%s Modeling element instances created (by type):\n" % com
    for name in objectTypes:
        res += "%s %s\n" % (com, fillDots(name, objectTypes[name]))
    return res

def detailed():
    def makePretty(ctr):
        prettyName = {"ASSIGN": "Assignments",
                      "SUBSCRIPT": "Subscripts",
                      "COMPARE": "Comparisons"}
        if ctr in prettyName:
            return prettyName[ctr]
        return ctr
                  
    res = "%sDetailed:\n" % com
    for ctr in allCtrs:
        res += "%s %s\n" % (com, fillDots(makePretty(ctr), allCtrs[ctr]))
    return res

def report(level):
    res = ""
    if level > 0:
        res += basic()
    if level > 1:
        res += detailed()
    if level > 2:
        res += gory()
    return res
