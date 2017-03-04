import sys
import m3parser
import tpg.base
import compro
import os
import m3
tpg.base.lexwithdotall = True
p = m3parser.Parser()
skip = True
m3.setOptions()
for fname in open("allm3s.txt").readlines():
    if fname[0] == "%":
        skip = False
        continue
    if skip:
        continue
    fname = fname[:-1]
    if fname[0] == "#":
        print "SKIPPING %s" % fname #OK
        continue
    print fname #OK
    m3.compile(fileName=fname)





    

