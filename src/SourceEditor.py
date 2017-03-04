import re
import string
import Lexis
import Colors
import Pmw
from Tkinter import *
from ScrolledText import ScrolledText
import TkWorkaround
class SourceEditor:
    def __init__(self,central,name,bodyTopNode,specTopNode):
        self.dirty = False
        self.central = central
        self.name = name
        self.toplevel = Toplevel()
        self.toplevel.title(name)
        self.pw = Pmw.PanedWidget(self.toplevel, orient='vertical')

        specpane = self.pw.add("spec")
        bodypane = self.pw.add("body")
        self.specText = ScrolledText(specpane,font=("monaco",10),height=5,background=Colors.background)
        self.specText.pack(expand=YES,fill=BOTH)
        self.bodyText = ScrolledText(bodypane,font=("monaco",10),height=15,background=Colors.background)
        self.bodyText.pack(expand=YES,fill=BOTH)        
        self.nodeMap = {bodyTopNode: self.bodyText, specTopNode: self.specText}
        self.textMap = {self.bodyText: bodyTopNode, self.specText: specTopNode}
        Widget.bind(self.bodyText,'<Any-KeyPress>',self.setDirty)
        Widget.bind(self.specText,'<Any-KeyPress>',self.setDirty)
        self.popup = Menu(self.toplevel,tearoff=0)
        self.popup.add_command(label="Dismiss", command=self.nothing)
        self.popup.add_command(label="Diagram", command=self.goDiagram)
        self.popup.add_command(label="Abort", command=self.abort)
        self.popup.add_command(label="Accept", command=self.accept)
        self.popup.add_command(label="Recolor", command=self.recolor)        
        def popupMenu(event):
            self.popup.post(event.x_root,event.y_root)
        self.toplevel.bind('<Button-3>', popupMenu)
        self.pw.pack(expand=YES,fill=BOTH)
        self.toplevel.protocol("WM_DELETE_WINDOW",self.central.doQuit)
        self.refresh()
    def nothing(self): pass
    def setClean(self):
        if self.dirty:
            self.dirty = False
            self.toplevel.title(self.name)
            self.central.unlockGraphics(self.name)
    def setDirty(self,event):
        if event.keysym in ['Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Win_L', 'Win_R']:
            return 
        if not self.dirty:
            self.dirty = True
            self.toplevel.title(self.name+"*")
            self.central.lockGraphics(self.name)
    def abort(self):
        if self.dirty:
            self.setClean()
            self.setSource()
    def getSource(self):
        return (self.specText.get("1.0",END),
                self.bodyText.get("1.0",END))
    def accept(self):
        if self.dirty:
            self.bodyText.config(cursor="watch")
            self.specText.config(cursor="watch")
            self.bodyText.update() # so that the cursor will show
            self.specText.update()
            self.central.update(self.name, self.specText.get("1.0",END),
                                self.bodyText.get("1.0",END),saveOutput=False)
            self.central.setChanged(self.name)
            self.setClean()
            self.bodyText.config(cursor="xterm")
            self.specText.config(cursor="xterm")
    def recolor(self):
        stext,btext = self.getSource()
        self.colorize(self.specText,stext)
        self.colorize(self.bodyText,btext)
    def show(self, specTopNode, bodyTopNode):
        self.nodeMap = {bodyTopNode: self.bodyText, specTopNode: self.specText}
        self.textMap = {self.bodyText: bodyTopNode, self.specText: specTopNode}        
        self.setSource()
    def setSource(self):
        oldScroll,dummy = self.specText.yview()
        self.specText.delete('1.0',END)
        stext = self.textMap[self.specText].regen(forDisplay=True)
        self.specText.insert(END,stext)
        self.colorize(self.specText,stext)
        self.specText.yview("moveto", oldScroll)

        oldScroll,dummy = self.bodyText.yview()
        self.bodyText.delete('1.0',END)
        btext = self.textMap[self.bodyText].regen(forDisplay=True)
        self.bodyText.insert(END,btext)
        self.colorize(self.bodyText,btext)
        self.bodyText.yview("moveto", oldScroll)
    def colorize(self,textWidget,progText):
        def colorizeSub(color,wordList):
            textWidget.tag_remove(color,'1.0',END)
            textWidget.tag_configure(color,foreground=color)
            keywords = re.compile(r'\b(' + string.join(wordList,"|") + r')\b')
            iter = keywords.finditer(progText)
            for match in iter:
                start, stop = match.span()
                textWidget.tag_add(color,"1.0+%dc" % start, "1.0+%dc" % stop)
        textWidget.tag_remove('hilite','1.0',END)
        colorizeSub(Colors.keyword, Lexis.keywords)
        colorizeSub(Colors.reserved, Lexis.reservedWords)
    def refresh(self):
        self.setSource()
    def goDiagram(self):
        self.central.showDiagram(self.name)
    def showSource(self,node):
        self.makeTop()
        topNode = node.getTopNode()
        self.text = self.nodeMap[topNode]
        self.text.tag_remove('hilite','1.0',END)
        start, end =  node.lineRange()
        startIdx = '%d.0' % int(start)
        endIdx = '%d.0' % (int(end)+1)
        self.text.tag_configure('hilite',background=Colors.locatecolor,foreground='black')
        self.text.see(startIdx)
        self.text.tag_add('hilite',startIdx,endIdx)

    def coolSource(self):
        self.text.tag_configure('hilite',background='white',foreground=Colors.locatecooledcolor)
    def makeTop(self):
        TkWorkaround.raiseWindow(self.toplevel)
    def rescueResource(self):
        return repr(self.toplevel.geometry())
    def setGeom(self,geom):
        self.toplevel.geometry(geom)

    def showError(self, unitType, lineNo):
        text = {'m': self.bodyText, 'i': self.specText}[unitType]
        startIdx = '%s.0' % int(lineNo)
        endIdx = '%s.0' % (int(lineNo)+1)
        text.tag_remove('hilite','1.0',END)
        text.tag_configure('hilite',background=Colors.locatecolor,foreground='black')
        text.see(startIdx)
        text.tag_add('hilite',startIdx,endIdx)
        self.makeTop()
