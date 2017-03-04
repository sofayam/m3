import sys
import xmlrpclib

s = xmlrpclib.Server("http://localhost:%s" % sys.argv[1])
s.shutdown()
