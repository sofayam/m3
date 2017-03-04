totlen = 0
for fname in open("allm3s.txt").readlines():
    if fname[0] == "%":
        continue
    if fname[0] == "#":
        print "SKIPPING %s" % fname #OK
        continue
    fname = fname[:-1]
    l = len(open(fname).readlines())
    totlen += l
    print "%d, %d : %s" % (totlen, l, fname) #OK



