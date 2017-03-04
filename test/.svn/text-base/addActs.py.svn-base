from TestScript import *
from random import random
import profile
start()
open('Big.m3')

def doitall(x,y):
    setTurbo()
    goNewActMode()
    for i in range(x):
        for j in range(y):
            if ((i % 3) == 0) and ((j % 3) == 0):  
                msedwn((i*100)+100,(j*100)+100,{'name': 'aa%sx%s' % (i,j), 'port': 'p1'})
                print i,j
    goNewDataMode()
    for i in range(x):
        for j in range(y):
            if (((i + 1) % 3) == 0) and (((j + 1) % 3)  == 0):  
                msedwn((i*100)+100,(j*100)+100,{'name': 'dd%sx%s' % (i,j), 'type': 'INTEGER'})
                print i,j

    for data,act in zip(datastores(),activities()):
        connect(data,act)
setTurbo(False)
doitall(50,40)
#profile.run("doitall()","profile.dat")
doSave()
