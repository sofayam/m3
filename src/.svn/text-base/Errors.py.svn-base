import string
import re

errorPat = re.compile(".*<\*ERROR (.*)\*>")

directive = None
foundError = False

def findDirective(text):
    global directive
    directive = None
    foundError = False
    ctr = 0
    for line in string.split(text,"\n"):
        ctr += 1
        res = errorPat.search(line)
        if res:
            if directive:
                raise "only one error directive allowed"
            directive = (ctr, res.groups()[0])

def checkDirective(lineno, code):
    global foundError
    expectedLine, expectedCode = directive
    #print "expected line %s code %s, actual line %s code %s " % (expectedLine, expectedCode, lineno, code)
    if (lineno == expectedLine) and (code == expectedCode):
        foundError = True

