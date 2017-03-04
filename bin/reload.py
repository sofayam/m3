import sys
import xmlrpclib
import string
print "calling reload.py with argv", sys.argv
s = xmlrpclib.Server("http://localhost:%s" % sys.argv[1])
bufferName = sys.argv[2]
capsuleName = string.split(bufferName,".")[0]
s.reloadCapsule(capsuleName)

print "reload called for capsule ", capsuleName
