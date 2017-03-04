testname = ""
testctr = 0

def init(name):
    global testname, passed
    testname = name.val
    passed = True
    
def assertPass(cond):
    global passed, testctr
    testctr += 1
    passed = passed and cond.toBool()
    if not cond.toBool():
        raise "FAIL"

def summary():
    verdict = {True: "PASSED", False: "FAILED"}
    print "%s : %s (%d)" % (testname, verdict[passed], testctr) #OK
    
