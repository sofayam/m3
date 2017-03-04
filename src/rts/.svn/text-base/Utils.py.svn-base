import os.path
def makebackup(fn):
    if os.path.exists(fn):
        ctr = 1
        while True:
            bckname = "%s.%d.bck" % (fn, ctr)
            if not os.path.exists(bckname): break
            ctr += 1
        os.rename(fn,bckname)

        
