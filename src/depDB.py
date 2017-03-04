import cPickle
import Options
import os

def dataBaseFileName():
    return Options.options.library + os.sep + "dependencies"

def add(name, depList):    
    depList = [str(item) for item in depList]
    depends = read()
    depends[name] = depList
    f = open(dataBaseFileName(),"w")
    cPickle.dump(depends,f)
    
def read():
    if os.path.exists(dataBaseFileName()):
        f = open(dataBaseFileName(),"r")
        depends = cPickle.load(f)
        f.close()
    else:
        depends = {}
    return depends
    
