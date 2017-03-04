import time

finish = time.time()
start = float(open("stamp.tmp").read())

print "Time taken %s seconds" % (finish - start)
