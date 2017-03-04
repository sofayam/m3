import time

stamp = open("stamp.tmp","w")
stamp.write("%s" % time.time())
stamp.close()
