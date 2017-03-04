import os
import os.path

backupdir = "backups"

def makebackup(fn):
    checkBackupDir()
    before,after = os.path.split(fn)
    if before:
        before += os.sep
    bfn = before + backupdir + os.sep + after
    #print bfn
    if os.path.exists(fn):
        ctr = 1
        while True:
            bckname = "%s.%d.bck" % (bfn, ctr)
            if not os.path.exists(bckname): break
            ctr += 1
        #print "renaming %s to %s" % (fn, bckname)
        os.rename(fn,bckname)

def checkBackupDir():
    if not os.path.exists(backupdir):
        os.mkdir(backupdir)

        
    
    
