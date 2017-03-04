from Tkinter import *

class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"

scalemax = 100
canvasWidth = 300
canvasHeight = 300
circWidth = 10


#
# create scrolled canvas


class ScaledCanvas:
    def __init__(self):
        root = Toplevel()
        self.magscale = Scale(root, from_=0, to=scalemax)
        self.vscrollbar = AutoScrollbar(root)
        self.vscrollbar.grid(row=0, column=1, sticky=N+S)
        self.magscale.grid(row=0, column=2)
        self.hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
        self.hscrollbar.grid(row=1, column=0, sticky=E+W)

        self.canvas = Canvas(root, 
                        yscrollcommand=self.vscrollbar.set, 
                        xscrollcommand=self.hscrollbar.set,
                        bg="white")
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)

        # make the canvas expandable
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        Widget.bind(self.canvas, "<Button-1>", self.drawcirc)
        Widget.bind(self.magscale, "<B1-Motion>", self.doscale)
        self.magscale.set(scalemax) # bump to max


    def getScaleFactor(self):
        return 1.0+(self.magscale.get()/30.0)
    def doScale(self,coords):
        fact = self.getScaleFactor()
        return [coord * fact for coord in coords]

    def drawcirc(self,event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        #print event.x,event.y,x,y
        fact = self.getScaleFactor()
        x = x / fact
        y = y / fact
        c = circ(x,y,x+circWidth,y+circWidth)
        c.render(self)
        bba = self.canvas.bbox("all")
        self.canvas.config(scrollregion=(0,0,bba[2],bba[3]))

    def doscale(self,event):
        for circ in circs:
            circ.resize()
        bba = self.canvas.bbox("all")
        if not bba:
            bba = (0,0,canvasWidth,canvasHeight)
        self.canvas.config(scrollregion=(0,0,bba[2],bba[3]))

circs = []

class circ:
    def __init__(self, sx, sy, ex, ey):
        self.sx,self.sy,self.ex,self.ey = sx,sy,ex,ey
        circs.append(self)
    def coords(self):
        return (self.sx,self.sy,self.ex,self.ey)
    def render(self,scanvas):
        self.scanvas=scanvas
        fact = self.scanvas.getScaleFactor()        
        self.handle=self.scanvas.canvas.create_oval(self.scanvas.doScale(self.coords()))
    def resize(self):
        fact = self.scanvas.getScaleFactor()
        #print fact, self.sx*fact
        self.scanvas.canvas.coords(self.handle, *self.scanvas.doScale(self.coords()))

if __name__ == "__main__":
    def newsc():
        ScaledCanvas()
    root = Tk()
    Button(root,text="New Canvas", command=newsc).pack()
    root.mainloop()
