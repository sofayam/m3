import Global
expectations = []
timeBase = 0
expectUsed = False
expectFailed = False
def addExpectation(entry):
    #print "appending expectation", entry.image()
    global expectUsed
    expectUsed = True
    entry.timeBase = timeBase
    expectations.append(entry)

def findExpectation(msgName, kwargs):
    #print "looking for expectation", msgName
    for entry in expectations:
        if applies(msgName,entry):
            expectations.remove(entry)
            checkExpTime(entry)            
            checkExpData(kwargs,entry)
            break

def checkEmpty():
    if expectations != []:
        expectFailed = True
        Global.results.putFailure("Noshow : the following messages were expected and never arrived :")
        for expectation in expectations:
            expectation.text = expectation.text[:-1] # chop that trailing cr
            Global.results.putFailure("   " + expectation.text)
        

def applies(msgName, entry):
    return entry.fullName == msgName

def checkExpTime(entry):
    import Files
    import Timer
    import Time
    clock = Timer.timeQueue.wallClock
    passed = False
    #import pdb; pdb.set_trace()
    if entry.timeBase == clock:
        passed = True
    if entry.timeBase < clock:
        if entry.earliest == "*":
            passed = True
        else:
            if entry.timeBase + entry.earliest >= clock:
                passed = True
    else:
        if entry.latest == "*":
            passed = True
        else:
            if entry.timeBase - entry.latest <= clock:
                passed = True
    if not passed:
        expectFailed = True
        Global.results.putFailure("Timing : output expected at %s, output occurred at %s" % (
            Time.timeString(entry.timeBase), Time.timeString(Timer.timeQueue.wallClock)))



def checkExpData(actKwargs, entry):
    import Files
    #print "checking %s against %s" % (actKwargs, entry.image())
    for key,value in entry.params:
        if value == "*":
            #print "wildcard for %s" % key
            continue
        # coerce the expected value to the type of the actual value
        if key not in actKwargs:
            Global.results.putFailure("Parameter %s missing in output" % key)
            continue
        if Global.raw_python:
            wanted = value
            got = actKwargs[key]
            passed = str(got) == str(wanted)
        else:
            actualType = actKwargs[key].tipe
            expectedValue = actualType.coerce(value,allowChoices=True)
            #import pdb; pdb.set_trace()
            # equals might go either to the standard M3objects or to Any/Range/Alternatives
            passed = expectedValue.equals(actKwargs[key]).toBool()
            wanted = expectedValue.image()
            got = actKwargs[key].image()
        if not passed:
            Global.results.putFailure("Parameter : %s - value expected %s, value sent %s " % (
                key, wanted, got))


def  shiftTimeBase(latest):
    import Time
    global timeBase
    timeBase = Time.makeTime(latest)
    #print "timeBase shifted from to %s by %s" % (timeBase, latest)

def expectPassed():
    return expectUsed and not expectFailed
