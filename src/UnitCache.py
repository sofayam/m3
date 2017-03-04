loadedUnits = {}

unitListeners = {}

def addListener(unitName, listener):
#    print unitName, " has listener ",listener
    if unitName not in unitListeners:
        unitListeners[unitName] = []
    if listener not in unitListeners[unitName]:
        unitListeners[unitName].append(listener)
        
def add(unitName,unitXML):
#    print "unitCache.add", unitName.image()    
    loadedUnits[unitName] = unitXML
    if unitName in unitListeners:
        for listener in unitListeners[unitName]:
            listener.unitCacheChanged()

def loaded(unitName):
    if unitName in loadedUnits:
#        print "UnitCache.loaded hit", unitName.image()        
        return loadedUnits[unitName]
    else:
#        print "UnitCache.loaded miss", unitName.image()        
        return False
    
def flush():
    global loadedUnits
    loadedUnits = {}
