procLib = {}

def enter(code, fun):
#    print "Enter", code
    procLib[code] = fun

def lookup(code):
#    print "Lookup ", code
    return procLib[code]


    
