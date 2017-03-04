import time

usageFile = "C:\\smlusage.txt"

class UseInstance:
    def __init__(self, descr):
        self.descr = descr
        self.when = time.localtime()
    def __str__(self):
        return "%s|%s" % (time.strftime("%a, %d %b %Y %H:%M:%S",self.when), self.descr)
useInstances = []
def create():
    pass

def save():
    f = open(usageFile,"a")
    for u in useInstances:
        f.write(str(u)+"\n")
    f.close()
    
def add(descr):
    useInstances.append(UseInstance(descr))


    
