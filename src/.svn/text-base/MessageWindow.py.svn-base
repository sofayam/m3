from Tkinter import *
import Pmw
import Message
import TkWorkaround
import string
import Colors
class MessageWindow:
    def __init__(self,central):
        self.central = central
        self.root = Toplevel()
        self.root.title("Messages")
        self.st = Pmw.ScrolledText(self.root)
        self.st.pack(expand=YES,fill=BOTH)   
        Message.setOutStream(self)
        self.root.bind('<Button-1>', self.butPress)
        self.root.protocol("WM_DELETE_WINDOW", self.closeCallBack)
        for color in Colors.mwColors.values():
            self.st.tag_configure(color, foreground=color)
        self.root.geometry('700x150+110+0')
    def writePrimitive(self,txt,traits):
        if traits not in Colors.mwColors:
            self.st.insert(END, "++++++++bad trait %s++++++++" % traits, "red")
        color = Colors.mwColors[traits]
        self.st.insert(END, txt, color)
        if traits == "error":
            TkWorkaround.raiseWindow(self.root)
        self.st.yview("moveto",1.0)
    def write(self,txt,traits="normal"):
        self.root.after_idle(self.writePrimitive, txt, traits)
    def butPress(self,event):
        lineNo = string.split(self.st.index("current"),".")[0]
        lineTxt = self.st.get("%s.0" % lineNo, "%s.999" % lineNo)
        self.central.showError(lineTxt)
    def closeCallBack(self): pass
def start(central):
    myWindow = MessageWindow(central)

    
