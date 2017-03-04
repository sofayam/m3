import string

globalMappings = {} # implementations to be used for all occurences of a given interface
instanceMappings = {} #       "           "        for specific instances 


def setGlobalMappingsFromOption(option):
    setMappingsFromOption(option,globalMappings)    

def setInstanceMappingsFromOption(option):
    setMappingsFromOption(option,instanceMappings)

def setMappingsFromOption(option,mappings):
    mapPairs = string.split(option,",")
    for pair in mapPairs:
        specImpl = string.split(pair,"=")
        if len(specImpl) != 2:
            raise "error in capsule implementation mapping option %s" % option
        else:
            spec, impl = specImpl
            mappings[spec] = impl
            #print "%s->%s"%(spec,impl)

def createCapsule(level,spec,hierarchicalName):
    if hierarchicalName in instanceMappings:
        impl = instanceMappings[hierarchicalName]
    elif spec in globalMappings:
        impl = globalMappings[spec]
    else:
        impl = spec
    return __import__("%sCapMod" % impl).createCapsule(level,hierarchicalName)
    # TBD FIXME do more checking here that we are getting the right kind of capsule
