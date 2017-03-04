import M3Types

def Bool(b):
    return M3Types.M3Text.createObject(b.val)

def Char(c):
    return M3Types.M3Text.createObject(c.val)

def Int(n):
    return M3Types.M3Text.createObject("%s" % n.val)
