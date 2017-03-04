from Tkinter import *
import types
import sys
import ScriptRecorder
import TkWorkaround
import Options
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

class ZoomDrawing:
    def __init__(self,name):
        root = Toplevel()
        root.title(name)
        self.name = name
        self.root = root
        self.magscale = Scale(root, from_=0, to=scalemax,width=8)
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

        Widget.bind(self.magscale, "<B1-Motion>", self.doZoom)

        self.allShapes = {}

        self.addPopup(root)
        self.addHandlers(self.canvas)
        # ------------- scripting support ------------------
        root.bind('<Configure>', self.windowConfig)
        root.bind('<FocusIn>', self.focusIn)
        root.protocol ("WM_DELETE_WINDOW",self.deleteCallBack)
        self.oldgeom = ""

    def deleteCallBack(self):
        sys.exit()

    def setTitle(self,title):
        self.root.title(title)

    def clear(self):
        self.allShapes = {}
        self.canvas.delete(ALL)

    def makeTop(self):
        TkWorkaround.raiseWindow(self.root)
    def addHandlers(self,canvas):
        pass
    def getScaleFactor(self):
        return float(1.0+(self.magscale.get()/30.0))
    def scaleInt(self,val):
        fact = self.getScaleFactor()
        return int(float(val) / fact)
    def translateEvent(self,event):
        fact = self.getScaleFactor()        
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)        
        x = x * fact
        y = y * fact
        return x,y
    def scaleCoords(self,coords):
        fact = self.getScaleFactor()
        return [coord / fact for coord in coords]
    def unScaleCoords(self,coords):
        fact = self.getScaleFactor()
        return [coord * fact for coord in coords]
    def rebound(self):
        bba = self.canvas.bbox("all")
        if bba:
            self.canvas.config(scrollregion=(0,0,bba[2],bba[3]))
        else:
            self.canvas.config(scrollregion=(0,0,canvasWidth,canvasHeight))
    def doZoom(self,event,scr=False):
        print "zooming"
        if not scr:
            ScriptRecorder.write("setZoom(%s)" % self.magscale.get())
        for shape in self.allShapes.values():
            shape.doZoom()
        self.rebound()

    def coords(self, handle, *xsandys):
        if handle in self.allShapes:
            self.allShapes[handle].coords(*xsandys)
            self.rebound()
        else:
            if True: print "lost handle", handle
    def config(self, handle, *args, **kwargs):
        h = self.allShapes[handle]
        if h:
            h.config(**kwargs)
    def create_oval(self, xsandys, *args, **kwargs):
        zo = ZoomOval(self, xsandys, *args, **kwargs)
        self.allShapes[zo.handle] = zo
        self.rebound()
        return zo.handle

    def create_rectangle(self, xsandys, *args, **kwargs):
        zr = ZoomRectangle(self, xsandys, *args, **kwargs)
        self.allShapes[zr.handle] = zr
        self.rebound()
        return zr.handle

    def create_line(self, xsandys, *args, **kwargs):
        zl = ZoomLine(self, xsandys, *args, **kwargs)
        self.allShapes[zl.handle] = zl
        self.rebound()
        return zl.handle
    
    def create_text(self, x, y, text, font, *args, **kwargs):
        zt = ZoomText(self, (x,y), text, font, *args, **kwargs)
        x,y = self.scaleCoords((x,y))
        self.allShapes[zt.handle] = zt
        self.rebound()
        return zt.handle

    def bbox(self, textHandle):
        return self.allShapes[textHandle].bbox()
    def create_polygon(self, xsandys, *args, **kwargs):
        zp = ZoomPolygon(self, xsandys, *args, **kwargs)
        self.allShapes[zp.handle] = zp
        self.rebound()
        return zp.handle

    def delete(self, handle):
        if handle in self.allShapes:
            self.allShapes[handle].delete()

    def move(self, handle, dx, dy):
        self.allShapes[handle].move(dx,dy)

    def lift(self, item):
        self.canvas.lift(item)

    def lower(self, item):
        self.canvas.lower(item)

    # ------------------- scripting support ----------------------

    def windowConfig(self, env):
        geom = self.root.geometry()
        if self.oldgeom == geom: return 
        self.oldgeom = geom
        ScriptRecorder.write("setGeom('%s')" % geom)

    def setGeom(self,geom):
        self.root.geometry(geom)

    def rescueResource(self):
        return (self.magscale.get(), self.root.geometry())

    def setZoom(self, setting):
        self.magscale.set(setting)
        self.doZoom(None, True)

    def focusIn(self, env):
        ScriptRecorder.write("setFocus('%s.m3')" % self.name)
    
class ZoomShape:
    def __init__(self, zcanvas, xsandys):
        self.zcanvas = zcanvas
        self.canvas = zcanvas.canvas
        self.xsandys = xsandys
    def doZoom(self):
        self.canvas.coords(self.handle, *self.zcanvas.scaleCoords(self.xsandys))
    def coords(self,xsandys):
        self.xsandys = xsandys
        self.doZoom()
    def delete(self):
        self.canvas.delete(self.handle)
    def config(self, **kwargs):
        self.canvas.itemconfigure(self.handle, **kwargs)


class ZoomOval(ZoomShape):
    def __init__(self, zcanvas, xsandys, *args, **kwargs):
        ZoomShape.__init__(self, zcanvas, xsandys)
        self.handle = self.canvas.create_oval(zcanvas.scaleCoords(xsandys), *args, **kwargs)

class ZoomRectangle(ZoomShape):
    def __init__(self, zcanvas, xsandys, *args, **kwargs):
        ZoomShape.__init__(self, zcanvas, xsandys)
        self.handle = self.canvas.create_rectangle(zcanvas.scaleCoords(xsandys), *args, **kwargs)

class ZoomLine(ZoomShape):
    def __init__(self, zcanvas, xsandys, *args, **kwargs):
        ZoomShape.__init__(self, zcanvas, xsandys)
        self.handle = self.canvas.create_line(zcanvas.scaleCoords(xsandys), *args, **kwargs)
    
class ZoomText(ZoomShape):
    def __init__(self, zcanvas, xsandys, text, font, *args, **kwargs):
        ZoomShape.__init__(self, zcanvas, xsandys)
        x,y = xsandys
        if type(font) != types.TupleType:
            self.font = font
            self.fontsize = 8
        else:
            self.font, self.fontsize = font
        self.handle = self.canvas.create_text(x, y, text=text,
                                              font=(self.font, self.fontsize),
                                              *args, **kwargs)
    def doZoom(self):
        ZoomShape.doZoom(self)
        self.canvas.itemconfigure(self.handle, font=(self.font, self.zcanvas.scaleInt(self.fontsize)))

    def bbox(self):
        return self.canvas.bbox(self.handle)
        
class ZoomPolygon(ZoomShape):
    def __init__(self, zcanvas, xsandys, *args, **kwargs):
        ZoomShape.__init__(self, zcanvas, xsandys)
        self.handle = self.canvas.create_polygon(zcanvas.scaleCoords(xsandys), *args, **kwargs)

    
if __name__ == "__main__":
    def newzc():
        ZoomDrawing()
    root = Tk()
    root.mainloop()
