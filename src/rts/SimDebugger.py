import string
import sys
import CommandQueue

gonext = False
stepmode = False
ar = []
timeQueue = None
ctr = 0
traceLevel = 0

def trc(level=1):
    # 0 traces everything
    return traceLevel > level
    

def setTimeQueue(tq):
    global timeQueue
    timeQueue = tq
    
def s():
    global gonext
    gonext = True

def q():
    print "Und weg ..."
    sys.exit()

def g():
    global stepmode, gonext
    stepmode = False
    gonext = True
    print "Running to end ..."

def cq():
    CommandQueue.dump()

def tq():
    timeQueue.dumpTQ()

def t(val=10):
    global traceLevel
    traceLevel = val

def h():
    print """
    q - (quit) stop altogether
    g - (go) run to end without debugger
    s - (step) one step - run till next invocation of debugger
    cq - dump command queue
    tq - dump time queue
    t - (trace) switch on global traceing (masses of output)
    """

def activate():
    global stepmode
    stepmode = True
        

def interpret():
    global ctr
    global gonext
    ctr += 1
    if stepmode:
        gonext = False
        while not gonext:
            sys.stdout.write("DBG(%d)> " % ctr)
            inp = sys.stdin.readline()
            if len(inp) >= 1:
                inp = inp[:-1]
                wrds = string.split(inp)
                if len(wrds) == 1:
                    cmd = inp + "()"
                else:
                    if len(wrds) == 2:
                        args = wrds[1]
                    else:
                        args = string.join(wrds[1:],",")
                    cmd = wrds[0] + "(" + args + ")"
                try:
                    eval(cmd)
                except NameError:
                    print "Oops - this raised %s" % sys.exc_info()[0]
                    print "command '%s' [%s] not understood" % (inp,cmd)
                    h()
