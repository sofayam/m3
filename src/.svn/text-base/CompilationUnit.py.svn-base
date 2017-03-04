# A descriptor for a compilation unit, can also be used as a dictionary key for caching purposes
import os.path


unitTypeNames = {"Interface": "i3o", "Module": "m3o", "CapsuleInterface": "ci3o",
                 "Capsule": "cm3o", "GenericInterface": "gi3o", "Generic": "gm3o",
                 "InterfaceInstantiation": "i3o", "ModuleInstantiation": "m3o"}

extToUnitTypeName = {}
for unitTypeName in unitTypeNames:
    extToUnitTypeName[unitTypeNames[unitTypeName]] = unitTypeName
    
def transformFileToUnit(fileName):
    base = os.path.basename(fileName)
    name, ext = os.path.splitext(base)
    if not ext:
        raise "Compiler anomaly : filename %s has no suffix " % ext
    unitType = extToUnitTypeName[ext[1:]]
    return CompilationUnit(name, unitType)

class CompilationUnit:
    def __init__(self,unitName,unitType):
        if unitType not in unitTypeNames:
            raise "bad compilation unit type"
        self.unitName = unitName
        self.unitType = unitType
    def __eq__(self,other):
        return (self.unitName == other.unitName) and (self.unitType == other.unitType)
    def __hash__(self):
        return hash((self.unitName,self.unitType))
    def image(self):
        return self.unitName + ":" + self.unitType
