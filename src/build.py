import depDB
import sys
import string

depends = depDB.read()

def closure(unit):
    # This is cheap (to program), inefficient but doesn't suffer from loops
    startUnitName = unit
    units = {}
    units[startUnitName] = True
    finished = False
    oldlen = 0
    while oldlen != len(units.keys()):
        oldlen = len(units.keys())
        keys = units.keys()
        for unit in keys:
            def getdepends(uname):
                if uname in depends.keys():
                    return depends[uname]
                else:
                    return []
            for dep in getdepends(unit + '.m3o'):
                units[dep] = True
            for dep in getdepends(unit + '.i3o'):
                units[dep] = True
    return units.keys()

def colorList(list):
    return [color(unit) for unit in list]
            
def color(unit):
    if unit + '.i3o' in depends.keys():
        return unit
    else:
        return "*" + unit + "*"
    
def alldeps():
    for dep in depends:
        print "%s : %s" % (dep, string.join(colorList(depends[dep]), ", ")) #OK

if __name__ == "__main__":
    if len(sys.argv) == 1:
        alldeps()
    else:
        print closure(sys.argv[1]) #OK
