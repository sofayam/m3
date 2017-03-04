import Global
import string
import re

macroPattern = re.compile(r"@\s*(\w*)((\s\w*\=\w*)*)\s*$") # TBD FIXME this is not good enough for passing complex values

def process(inpLines):
    resLines = []
    for line in inpLines:
        found = lookMacroCall(line)
        if found:
            call, params = found
            newLines = doMacroCall(call, params)
            for line in newLines:
                resLines.append(line)
        else:
            resLines.append(line)
    return resLines


def lookMacroCall(line):
    # either return none or the name of the macro and the parameter list as a dictionary
    m = macroPattern.match(line)
    if m:
        macroName = m.group(1)
        kvps = m.group(2)
        params = splitKVPs(kvps)
        return macroName, params
    return None

def splitKVPs(kvps):
    dict = {}
    for kvp in string.split(kvps):
        (key, val) = re.compile(r"(\w*)\=(\w*)").match(kvp).groups()
        dict[key]=val
    return dict

def doMacroCall(macroName, params):
    #print "doing a macro call on %s with params %s" % (macroName, params)
    # TBD you should really add type checking here
    resultLines = []
    macroFileName = ""
    macroLines = []
    try:
        macroFileName = macroName + Global.macroFileExtension
        macroFile = open(macroFileName)
        macroLines = macroFile.readlines()
        macroFile.close()
    except:
        # TBD warning strategy here
        raise "problem opening macro file %s" % macroFileName
    for line in macroLines:
        for k in params.keys():
            formal = "$(%s)" % k
            actual = params[k]
            line = string.replace(line, formal, actual)
        resultLines.append(line)
    #for k in params.keys():
    #    print "%s->%s" % (k,params[k])
    if resultLines[-1:] != "\n":
        resultLines.append("\n")
    return resultLines

def test(fileName):
    linesIn = open(fileName).readlines()
    return process(linesIn)

if __name__ == "__main__":
    test(sys.argv[1])
