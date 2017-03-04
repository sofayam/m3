import os
import cPickle
import sys
modname = sys.argv[1]
def showlib(name):
    filename = "m3lib" + os.sep + name + "TypeLib"
    if not os.path.exists(filename):
        print "%s not present" % filename #OK
        return
    print ">>>> %s " % filename #OK
    f = open(filename)
    tt = cPickle.load(f)
    for t in tt.values():
        print t.image() #OK

showlib(modname + "Mod")
showlib(modname + "Int")
                      

    
