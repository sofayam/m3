import string
import os
import FileUtils
import Message
class ResourceFile:
    def __init__(self,name,read=False):
        self.name = os.path.splitext(name)[0] + ".rsc"
        self.dict = {}
        if read:
            try:
             f = open(self.name,"r")
             for line in f.readlines():
                 k,v = string.split(line,"=")
                 # snip the \r s (to help Unix)
                 v = v.replace('\r','')
                 self.dict[k] = eval(v)
            except:
                Message.info("No resource File %s" % self.name)
#                raise
    def reset(self):
        self.dict={}

    def read(self,key):
        if key in self.dict:
            res = self.dict[key]
        else:
            res = None
#        print "reading key %s with res <%s>" % (key,res)
        return res

    # Notes are comments in a graphical context
    # they are kept as resources rather than in the source code
    # (which they would make ugly if they are multiline - unless we
    # laboriously pretty printed them which I wont)
    # Format for a note entry in the resource file
    # { ... *note<number> = ("note string", (sx,sy), [(arrow1ex, arrow1ey), ..]), .. } 
    # externally store all \n's as %0A

    def writeNote(self, name, text, topLeft, arrowList):
        text = text.replace("\n",'%0A')
        self.dict[name] = (text, topLeft, arrowList) 

    def getNotes(self):
        notes = []
        for key in self.dict:
            if (len(key) > 5) and key[0:6] == "**Note":
                notes.append(key)
        return notes

    def write(self,key,val):
        self.dict[key] = val

    def flush(self):
        FileUtils.makebackup(self.name)
        f=open(self.name,"w")
        sortkeys = self.dict.keys()
        sortkeys.sort()
        for k in sortkeys:
            f.write("%s=%s\n" % (k,str(self.dict[k])))
        f.close()
