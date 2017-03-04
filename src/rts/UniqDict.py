class UniqDict(dict):
    def __setitem__(self, x, y):
        # print "setting %s to %s" % (x,y)
        if self.has_key(x):
            raise "Duplicate Key %s" % x
        else:
            super(UniqDict, self).__setitem__(x,y)
