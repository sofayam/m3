import string
import Global
def argsToString(args, kwargs):
    if Global.raw_python:
        return pythonArgsToString(args, kwargs)
    #print args, kwargs
    res = string.join([arg.image() for arg in args], " ")
    res += string.join(["%s = %s" % (k, v.image())  for k,v in kwargs.items()], ", ")
    return res

def pythonArgsToString(args, kwargs):
    res = ""
    for ctr,arg in enumerate(args):
        res += ("arg%d=%s," % (ctr,repr(arg)))
    for k,v in kwargs.items():
        res += ("%s=%s" % (k,repr(v)))
    return res
