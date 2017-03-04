import os
import os.path
import tkFileDialog
import Pmw
from Tkinter import *
from ScrolledText import ScrolledText
class InputFile:
    def __init__(self,drawing):
        self.drawing = drawing
        self.toplevel = Toplevel()
        self.dirty = False
        self.filename = drawing.name + ".inp"
        self.toplevel.title(self.filename)
        self.inputText = ScrolledText(self.toplevel)
        self.inputText.pack()

        self.popup = Menu(self.toplevel, tearoff=0)
        self.popup.add_command(label="Dismiss", command=self.nothing)
        self.popup.add_command(label="Abort", command=self.abort)
        self.popup.add_command(label="Accept", command=self.accept)
        self.popup.add_command(label="Feedback", command=self.feedback)
        self.popup.add_command(label="Other File", command=self.changeFile)                
        self.popup.add_command(label="Run", command=self.run)
        self.popup.add_command(label="Debug", command=self.debug)                
        
        def popupMenu(event):
            self.popup.post(event.x_root,event.y_root)
        self.toplevel.bind('<Button-3>', popupMenu)
        Widget.bind(self.inputText,'<Any-KeyPress>',self.setDirty)        
        self.refreshSource()
    def nothing(self): pass
    def abort(self):
        self.refreshSource()
        self.setClean()
        print "aborted"
    def accept(self):
        inptext = self.getSource()
        handle = open(self.filename,"w")
        handle.write(inptext)
        self.setClean()
    def run(self):
        self.accept()
        self.drawing.doRun()
    def debug(self):
        self.drawing.doDebug()
    def changeFile(self):
        self.filename = tkFileDialog.asksaveasfilename(initialdir=os.getcwd(),
                                      parent=self.toplevel, title="Select Input file",
                                      filetypes=[("Input files", ".inp")],
                                      defaultextension='.inp')
        self.filename = os.path.basename(self.filename)
        self.refreshSource()
        self.drawing.setInpFile(os.path.splitext(self.filename)[0])
    def refreshSource(self):
        inptext = ""
        if os.path.exists(self.filename):
            inptext = open(self.filename).read()
        self.setSource(inptext)
        self.toplevel.title(self.filename)
    def setSource(self,txt):
        self.inputText.delete('1.0',END)
        self.inputText.insert(END,txt)        
    def getSource(self):
        return self.inputText.get("1.0",END)
    def feedback(self):
        resFile = "res" + os.sep + os.path.splitext(os.path.basename(self.filename))[0] + ".res"
        if os.path.exists(resFile):
            resText = open(resFile).read()
            self.setSource(resText)
            self.setDirty()
    def setClean(self):
        if self.dirty:
            self.dirty = False
            self.toplevel.title(self.filename)
    def setDirty(self,event=None):
        if event and (event.keysym in ['Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Win_L', 'Win_R']):
            return 
        if not self.dirty:
            self.dirty = True
            self.toplevel.title(self.filename+"*")

