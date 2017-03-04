import os
import os.path
import string
for file in open("libs.dat").readlines():
    print os.popen("m3 -s %s" % file).read()
#    if os.path.splitext(file)[1] not in [".m3\n",".i3\n",".mg\n",".ig\n"]:
#        print "found an odd one"
#    elif string.find(file,"unix") != -1:
#        print "found unix stuff"
#    else:

