import PSUtils
import LoadSrc
import Colors
import DiagMaths
import CompilationUnit
import Options
import os
import random
import time
import string
defaultCapsuleDims = 100,100
defaultAvatarDims = 40,40
defaultDataStoreDims = 40,40
defaultTriggerDims = 40,40
defaultTimerDims = 40,40
defaultActivityDims = 40,40
defaultProcedureDims = 40,40
defaultStateDims = 40,40
defaultChildDims = 80,100
defaultTransitionDims = 60,30
defaultStartDims = 10,10
defaultPortDims = 40,40
defaultChildPortDims = 20,20
defaultMessageDims = 60,15
defaultTransitionProxyDims = 15,15
capsuleTopLeft = 50,50
capsuleInset = 50
childBump = 20
stateBump = 20
capsuleBump = 30
transitionBump = 5
messageInterval = 5
messageSpace = defaultMessageDims[1] + messageInterval
messageStart = 10
portLabelOff = -5
shadowOff = 5 # proportion of radius used for shadow
stateConcOff = 5 # offset between concentric rings of state
hotCorner = 10
noteInset = 10
highlightValueMaxLen =  20
connLabelArrowLen = 20
class Resizable:
    # Mixin for classes which can be resized by means of hotspots at the four corners
    # Note: you need to call initResizing in the setup of the avatar you choose to make
    # resizable
    def initResizing(self):
        self.scorchMark = None
        self.scorchSection = None
    def heat(self,x,y):
        self.showHotSpot(x,y)
    def cool(self):
        if self.scorchMark:
            self.canvas.delete(self.scorchMark)
            self.scorchMark = None
            self.scorchSection = None
    def moveScorch(self,dx,dy):
        sx,sy,ex,ey = self.scorchCoords
        sx += dx ; ex += dx
        sy += dy ; ey += dy
        self.scorchCoords = sx,sy,ex,ey 
        self.canvas.coords(self.scorchMark,self.scorchCoords)
    def showHotSpot(self,x,y):
        section,coords = self.getHotSpot(x,y)
        if not section:
            self.cool()
        if section and section != self.scorchSection:
            self.cool()
            self.scorchMark = self.canvas.create_rectangle(coords,fill=Colors.scorchcolor)
            self.scorchCoords = coords
            self.scorchSection = section
    def getHotSpot(self,x,y):
        sx,sy,ex,ey = self.outline
        hc = hotCorner
        for section, coords in (("TOPLEFT", (sx,sy,sx+hc,sy+hc)),
                                ("TOPRIGHT", (ex-hc,sy,ex,sy+hc)),
                                ("BOTTOMLEFT", (sx,ey-hc,sx+hc,ey)),
                                ("BOTTOMRIGHT", (ex-hc,ey-hc,ex,ey))):
            if DiagMaths.isUnder(x,y,coords):
                return section,coords # tbd maybe return a polygon outline to light up
        return None,None
    def hotMove(self,dx,dy):
        def flip(outline):
            sx,sy,ex,ey = self.outline
            if sx > ex:
                tmp = ex
                ex = sx
                sx = tmp
            if sy > ey:
                tmp = ey
                ey = sy
                sy = tmp
            return sx,sy,ex,ey
            
        sx,sy,ex,ey = self.outline

        if self.scorchSection:
            sx,sy,ex,ey = self.outline
            self.outline = {"TOPLEFT": (sx+dx,sy+dy,ex,ey),
                            "TOPRIGHT": (sx,sy+dy,ex+dx,ey),
                            "BOTTOMLEFT": (sx+dx,sy,ex,ey+dy),
                            "BOTTOMRIGHT": (sx,sy,ex+dx,ey+dy)}[self.scorchSection]
            self.outline = flip(self.outline) # stop creation of inverted unmovable avatars
            self.setShape()
            self.moveScorch(dx,dy)
            return True
        return False
    
class Circle:
    def drawCameo(self, canvas, parentDrawing, childAvatar,cameos):
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline
        cameos.append(Cameo(canvas, self,
                            parentDrawing, childAvatar,
                            canvas.create_oval(DiagMaths.constrain(self.xsandys,capOutline,constraints))))

    def drawCameoPS(self, canvas, parentDrawing, childAvatar,psfile):
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline
        outline = DiagMaths.constrain(self.xsandys,capOutline,constraints)
        cx, cy = DiagMaths.middle(outline)
        xr = cx - outline[0]
        yr = cy - outline[1]
        ovality = float(yr) / xr
        psfile.write("%s %s %s %s oval\n" % (ovality, xr, cx, cy))
    def getPov(self,f):
        cx,cy = self.middle()
        r = cx - self.outline[0]
        f.write("Globe(%d,%d,%d)\n" % (cx,DiagMaths.flipYCoord(cy),r))
    def shapeGetPostscript(self,psfile, fill="1 1 1"):
        cx,cy = self.middle()
        xr = cx - self.outline[0]
        yr = cy - self.outline[1]
        ovality = float(yr) / xr
        psfile.write("%s %s %s %s oval\n" % (ovality, xr, cx, cy))

    def shapeDraw(self, **kwargs):
        if Options.options.shadows and self.shadowed:
#            shadowOff = shadowFactor * min(self.xyRadii())
            self.shadow = self.canvas.create_oval(DiagMaths.addOffset(self.xsandys,shadowOff,shadowOff), outline="white", fill="grey")
        self.oval = self.canvas.create_oval(self.xsandys, **kwargs)
    def shapeMove(self):
        if Options.options.shadows and self.shadowed:
#            shadowOff = shadowFactor * min(self.xyRadii())
            self.canvas.coords(self.shadow,DiagMaths.addOffset(self.xsandys,shadowOff,shadowOff))
        self.canvas.coords(self.oval,self.xsandys)        
    def shapeEdge(self, point):
        x,y = point
        sx,sy,ex,ey = self.outline
        cx, cy =  self.middle()
        rx = ex - cx
        ry = ey - cy
        return  DiagMaths.findEdgeOval(cx,cy,rx,ry,x,y)

class ConcCircle(Circle):
    def shapeDraw(self, **kwargs):
        Circle.shapeDraw(self, **kwargs)
        self.inneroval = self.canvas.create_oval(DiagMaths.inset(self.xsandys,stateConcOff), **kwargs)
    def shapeMove(self):
        Circle.shapeMove(self)
        self.canvas.coords(self.inneroval, DiagMaths.inset(self.xsandys,stateConcOff))

class Rectangle:
    def drawCameoPS(self, canvas, parentDrawing, childAvatar,psfile):
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline
        outline = DiagMaths.constrain(self.xsandys,capOutline,constraints)
        psfile.write("gsave %s setrgbcolor\n" % PSUtils.makeColor(self.avatarColor()))
        psfile.write("%s %s %s %s square\n" % tuple(outline))
        psfile.write("grestore\n")        
                     
    def drawCameo(self, canvas, parentDrawing, childAvatar,cameos):
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline
        cameos.append(Cameo(canvas, self,
                            parentDrawing, childAvatar,
                            canvas.create_rectangle(DiagMaths.constrain(self.xsandys,capOutline,constraints),
                                                    outline=self.avatarColor())))
    def shapeGetPostscript(self,psfile,fill=None):
        psfile.write("gsave %s setrgbcolor\n" % PSUtils.makeColor(self.avatarColor()))
        psfile.write("%s %s %s %s square\n" % tuple(self.outline))
        psfile.write("grestore\n")
    def shapeDraw(self, **kwargs):
        if Options.options.shadows and self.shadowed:
#            shadowOff = shadowFactor * min(self.xyRadii())
            self.shadow = self.canvas.create_rectangle(
                DiagMaths.addOffset(self.xsandys,shadowOff,shadowOff), outline="white", fill="grey")
        self.rect = self.canvas.create_rectangle(self.xsandys, **kwargs)        
    def shapeMove(self):
        if Options.options.shadows and self.shadowed:
#            shadowOff = shadowFactor * min(self.xyRadii())
            self.canvas.coords(self.shadow,DiagMaths.addOffset(self.xsandys,shadowOff,shadowOff))
        self.canvas.coords(self.rect,self.xsandys)
    def shapeEdge(self, point):
        x,y = point
        sx,sy,ex,ey = self.outline
        cx, cy =  self.middle()
        rx = ex - cx
        ry = ey - cy
        x,y,_ = DiagMaths.findEdgeRect(cx,cy,rx,ry,x,y)
        return x,y
    def topRightCorner(self):
        sx,sy,ex,ey = self.outline
        cx, cy =  self.middle()
        return cx,sy,ex,cy
class TwoLines(Rectangle):
    def drawCameoPS(self, canvas, parentDrawing, childAvatar,psfile):
        sx,sy,ex,ey = self.outline        
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline

        psfile.write("newpath %s %s moveto %s %s lineto stroke\n" % tuple(
            DiagMaths.constrain((sx,sy,ex,sy),capOutline,constraints)))

        psfile.write("newpath %s %s moveto %s %s lineto stroke\n" % tuple(
            DiagMaths.constrain((sx,ey,ex,ey),capOutline,constraints)))


        
    def drawCameo(self, canvas, parentDrawing, childAvatar,cameos):
        sx,sy,ex,ey = self.outline        
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline
        cameos.append(Cameo(canvas,self,
                            parentDrawing, childAvatar,                            
                            (canvas.create_line(
            DiagMaths.constrain((sx,sy,ex,sy),capOutline,constraints)),
                             canvas.create_line(
            DiagMaths.constrain((sx,ey,ex,ey),capOutline,constraints))),
                            cameoType=Cameo.twolines))
    def shapeGetPostscript(self,psfile):
        sx,sy,ex,ey = self.outline
        psfile.write("newpath %s %s moveto %s %s lineto stroke\n" % (sx,sy, ex,sy))
        psfile.write("newpath %s %s moveto %s %s lineto stroke\n" % (sx,ey, ex,ey))
    def shapeDraw(self):
        sx,sy,ex,ey = self.outline
        self.topLine = self.canvas.create_line((sx,sy,ex,sy),width=2)
        self.botLine = self.canvas.create_line((sx,ey,ex,ey),width=2)
    def shapeMove(self): 
        sx,sy,ex,ey = self.outline
        self.canvas.coords(self.topLine,(sx,sy,ex,sy))
        self.canvas.coords(self.botLine,(sx,ey,ex,ey))


class RoundedRect(Rectangle):
    def shapeGetCameo(self,canvas, parentDrawing, childAvatar, cameos, color):
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline
        cameos.append(Cameo(canvas, self,
                            parentDrawing, childAvatar,
                            canvas.create_polygon(DiagMaths.constrain(
            self.xsandys,capOutline,constraints),smooth=1,fill="white",outline=color)))
        
    def drawCameoPS(self, canvas, parentDrawing, childAvatar,psfile):
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline
        sx,sy,ex,ey = DiagMaths.constrain(self.outline,capOutline,constraints)
        psfile.write(PSUtils.roundedRectPS(sx,sy,ex,ey,self.bump,self.avatarColor()))        
    def drawCameo(self, canvas, parentDrawing, childAvatar,cameos):
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline
        cameos.append(Cameo(canvas, self,
                            parentDrawing, childAvatar,
                            canvas.create_polygon(DiagMaths.constrain(
            self.xsandys,capOutline,constraints),smooth=1,fill="white",outline="black")))

    def shapeGetPostscript(self,psfile,thickness=1):
        sx,sy,ex,ey = self.outline        
        psfile.write(PSUtils.roundedRectPS(sx,sy,ex,ey,self.bump,self.avatarColor(),thickness))
    def shapeCreate(self):
        sx,sy,ex,ey = self.outline
        self.xsandys = DiagMaths.roundedRectCoords(sx,sy,ex,ey,bump=self.bump)
    def shapeDraw(self, **kwargs):
        if Options.options.shadows and self.shadowed:
#            shadowOff = shadowFactor * min(self.xyRadii())
            self.shadow = self.canvas.create_polygon(DiagMaths.addOffset(self.xsandys,shadowOff,shadowOff), smooth=1, fill="grey")
        self.rect = self.canvas.create_polygon(self.xsandys,smooth=1,**kwargs)
    def shapeMove(self):
        if Options.options.shadows and self.shadowed:
#            shadowOff = shadowFactor * min(self.xyRadii())
            self.canvas.coords(self.shadow,DiagMaths.addOffset(self.xsandys,shadowOff,shadowOff))        
        self.canvas.coords(self.rect,self.xsandys)


class Avatar:
    def addConnLabel(self, cl):
        self.connLabels.append(cl)    
    def avatarColor(self):
        return "black"    
    def Highlight(self,phase):
        color = {"in": Colors.highlight, "out": Colors.visited}[phase]
        if self.highlight:
            self.canvas.delete(self.highlight)
        self.highlight = self.canvas.create_rectangle(self.outline,outline=color,width=2)
    def HighlightExclusive(self):
        if hasattr(self.canvas, "exclusiveHighlight"):
            self.canvas.delete(self.canvas.exclusiveHighlight)
        self.canvas.exclusiveHighlight = self.canvas.create_rectangle(self.outline,outline=Colors.exclusive,width=2)
    def HighlightValue(self,newValue):
        global highlightValueMaxLen
        if not self.visited:
            self.visited = self.canvas.create_rectangle(DiagMaths.inset(self.outline,-5),outline=Colors.visited, width=2)
        if self.debugValue:
            self.canvas.delete(self.debugValue)
        mx, my = self.middleUpper()
        highlightValueMaxLen = Options.options.highlightValueMaxLen or highlightValueMaxLen
        if len(newValue) > highlightValueMaxLen:
            newValue = newValue[0:highlightValueMaxLen-3] + "..."
        self.debugValue = self.canvas.create_text(mx,my,newValue,("times",15))
    def drawCameo(self, canvas, parentDrawing, childAvatar,cameos):
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline
        cameos.append(Cameo(canvas, self,
                            parentDrawing, childAvatar,
                            canvas.create_rectangle(DiagMaths.constrain(self.xsandys,capOutline,constraints))))
    def getPov(self, povFile):
        povFile.write("Block (%s, %s, %s, %s, -10, 10)\n" % tuple(DiagMaths.flipYCoords(self.outline)))
    def xyRadii(self):
        sx,sy,ex,ey = self.outline
        return ((ex-sx)/2.0,(ey-sy)/2.0)
    def hotMove(self,dx,dy): return False
    def heat(self,x,y): pass
    def cool(self): pass
    def getPSColor(self):
        return PSUtils.makeColor("black")
    def getPostscriptTitle(self,(x,y),psfile):
        psfile.write("%s %s moveto (%s) showmiddle\n" % (x,y,self.titleText))
    def __init__(self,name,node,title=None): # This is called for avatars being created from the original parse tree
        self.name = name
        if node:
            self.node = node
            node.avatar = self
        self.connections = []
        if title == None:
            self.titleText = name
        else:
            self.titleText = title
        self.defaultDims = defaultAvatarDims
        self.shadowed = True
        self.cameos = []
        self.visited = False
        self.highlight = False
        self.debugValue = False
        self.setup()
        self.connLabels = []
        self.portLabels = []
    def setup(self):
        pass # hook for subclasses to do something if they need to
    def setRandom(self):
        dw,dh = defaultCapsuleDims
        sx = random.random() * dw
        sy = random.random() * dh
        self.setOutline((sx,sy))
    def setXY(self,x,y):
        self.setOutline((x,y))
    def setOutline(self, outline):
        # outline is just top left and bottom right, stored as resource and used
        # for calculating mouse hits, edges etc
        if len(outline) == 2:
            sx,sy = outline
            dw,dh = self.defaultDims
            ex = sx + dw
            ey = sy + dh
            outline = sx,sy,ex,ey
        if len(outline) != 4:
            #print "!!!!!!!!bad outline"
            raise "bad outline"
        self.outline = outline
        self.setShape()
    def setShape(self):
        # shape is potentially more detailed though based on the outline (e.g. rounded edges)
        # these are the actual coordinates sent to the ZoomCanvas
        self.xsandys = self.outline[:] # default is just a copy
    def setResource(self,resource):
        self.setOutline(resource)
    def getResource(self):
        return self.outline
    def middle(self):
        return DiagMaths.middle(self.outline)
    def middleTop(self):
        sx,sy,ex,ey = self.outline
        return ((sx+ex)/2),sy
    def middleUpper(self):
        sx,sy,ex,ey = self.outline
        return ((sx+ex)/2),(((sy + ey) / 2) + sy) / 2
    def middleTopPS(self):
        sx,sy,ex,ey = self.outline
        return ((sx+ex)/2),sy+4
    def between(self, other):
        myx, myy = self.middle()
        othx, othy = other.middle()
        return (((myx + othx) /2), ((myy +othy) / 2))
    def setCanvas(self,canvas):
        self.canvas = canvas
    def shiftWithConstraints(self,dx,dy,constrainer):
        # where is my middle
        mx,my = self.middle()
        # apply dx,dy to it
        smx = mx + dx
        smy = my + dy
        # find the edge on the constrainer
        emx,emy = constrainer.edgeRect((smx,smy))
        # work out the dx,dy to the original middle
        ndx = emx - mx
        ndy = emy - my
        # use that to really shift me
        self.shift(ndx,ndy)
        return ndx,ndy # this is needed by any contained objects
    def shift(self,dx,dy):
        if self.hotMove(dx,dy): return
        self.xsandys = DiagMaths.addOffset(self.xsandys,dx,dy)
        self.outline = DiagMaths.addOffset(self.outline,dx,dy)        
    def moveConnections(self,dx,dy):
        for conn in self.connections:
            conn.move()
        for cl in self.connLabels:
            cl.move(0,0,self,dx,dy) # this makes them move their arrows
        self.move
        
    def isUnder(self,x,y):
        return DiagMaths.isUnder(x,y,self.outline)
    def isInside(self,selectCoords):
        return DiagMaths.isInside(self.outline, selectCoords)
    def drawTitle(self,yoff = 0,bg=False):
        mx,my = self.middle()
        my += yoff
        self.title = self.canvas.create_text(mx,my,self.titleText,("times",10))
        coords = self.canvas.bbox(self.title)
        if bg: 
            self.canvas.delete(self.title)
            self.titlebg = self.canvas.create_rectangle(coords,outline="white",fill=Colors.titlebgcolor)
            self.title = self.canvas.create_text(mx,my,self.titleText,("times",10))
    def moveTitle(self,yoff=0,bg=False):
        mx,my = self.middle()
        my += yoff
        self.canvas.coords(self.title,(mx,my))
        if bg:
            self.canvas.coords(self.titlebg, self.canvas.bbox(self.title))
    def edge(self, (x, y)):
        # The point on my edge bisected by a line drawn from my middle to x,y on the outside
        return self.middle()
    def edgeRect(self,(x,y)):
        sx,sy,ex,ey = self.outline
        cx, cy =  self.middle()
        rx = ex - cx
        ry = ey - cy
        x,y,_ = DiagMaths.findEdgeRect(cx,cy,rx,ry,x,y)
        return x,y
    def avatarType(self):
        return self.__class__.__name__
    def addConnections(self, conn):
        self.connections.append(conn)
    def changeOutline(self,ol):
        self.outline = ol
        self.setShape()
        self.move(0,0)

class Capsule(Resizable, Rectangle ,Avatar):
    def drawCameo(self, canvas, parentDrawing, childAvatar,cameos):
        pass
    def drawCameoPS(self, canvas, parentDrawing, childAvatar,psfile):
        pass
    
    def getPov(self, povFile):
        povFile.write('Capsule (%s, %s, %s, %s,"%s")\n' % tuple(DiagMaths.flipYCoords(self.outline) + [self.name]))
    def getPostscript(self, psfile):
        self.shapeGetPostscript(psfile)
    def setup(self):
        self.initResizing()
        self.defaultDims = defaultCapsuleDims
        self.bump = capsuleBump
        self.shadowed = False
        self.ports = []
    def setRandom(self):
        self.setOutline(capsuleTopLeft)
#    def setShape(self):
#        self.shapeCreate()
    def draw(self):
        self.shapeDraw(outline="black",fill="white",width=2)
    def move(self,dx,dy):
        self.shift(dx,dy)
        self.shapeMove()
        self.movePorts(dx,dy)
    def movePorts(self,dx,dy):
        for port in self.ports:
            port.move(0,0)
    def addPort(self, port):
        self.ports.append(port)
    def extend(self,(nex,ney)):
        sx,sy,ex,ey = self.outline
        self.setOutline((sx,sy,nex+capsuleInset,ney+capsuleInset))
        self.move(0,0)

class DataStore(Resizable,TwoLines,Avatar):
    def getPov(self, povFile):
        povFile.write('DataStore(%s, %s, %s, %s, "%s")\n' % tuple(DiagMaths.flipYCoords(self.outline) + [self.name]))
    def getPostscript(self,psfile):
        self.shapeGetPostscript(psfile)
        self.getPostscriptTitle(self.middle(),psfile)        
    def setup(self):
        self.defaultDims = defaultDataStoreDims
        self.initResizing()
    def edge(self,point):
        return self.shapeEdge(point)
    def move(self,dx,dy):
        self.shift(dx,dy)
        self.shapeMove()
        self.moveTitle()
        self.moveConnections(dx,dy)
    def draw(self):
        self.shapeDraw()
        self.drawTitle()

class Trigger(Resizable,RoundedRect,Avatar):
    def getPov(self, povFile):
        povFile.write('Trigger (%s, %s, %s, %s, "%s")\n' % tuple(DiagMaths.flipYCoords(self.outline) + [self.name]))

    def getPostscript(self,psfile):
        self.shapeGetPostscript(psfile)
        mx,my = self.middle()
        my += 10
        self.getPostscriptTitle((mx,my),psfile)
        self.getPostscriptAmp(psfile)
    def setup(self):
        self.initResizing()
        self.bump = childBump
        self.defaultDims = defaultTriggerDims
        
    def edge(self,point):
        return self.shapeEdge(point)
    def draw(self):
        self.shapeDraw(outline="black", fill="white")
        self.drawAmp()
        self.drawTitle(10)
    def move(self,dx,dy):
        self.shift(dx,dy)        
        self.shapeMove()
        self.moveTitle(10)
        self.moveAmp()
        self.moveConnections(dx,dy)        
    def setShape(self):
        self.shapeCreate()
    def getPostscriptAmp(self,psfile):
        mx,my = DiagMaths.middle(self.topRightCorner())
        psfile.write("%s %s moveto (@) showmiddle\n" % (mx,my))         # TBD make the size better
    def drawAmp(self):
        mx,my = DiagMaths.middle(self.topRightCorner())
        self.amp = self.canvas.create_text(mx,my,"@",("times", 20))        
    def moveAmp(self):
        mx,my = DiagMaths.middle(self.topRightCorner())
        self.canvas.coords(self.amp,(mx,my))


class Timer(Resizable,RoundedRect, Avatar):
    def getPov(self, povFile):
        povFile.write('Timer (%s, %s, %s, %s, "%s")\n' % tuple(DiagMaths.flipYCoords(self.outline) + [self.name]))
    def getPostscript(self,psfile):
        self.shapeGetPostscript(psfile)
        mx,my = self.middle()
        my += 10
        self.getPostscriptTitle((mx,my),psfile)
        self.getPostscriptClock(psfile)
    def setup(self):
        self.initResizing()
        self.defaultDims = defaultTimerDims
        self.bump = childBump
    def setShape(self):
        self.shapeCreate()
    def edge(self,point):
        return self.shapeEdge(point)
    def draw(self):
        self.shapeDraw(outline="black",fill="white")
        mx,my = self.middle()
        # calculate top left corner
        self.drawClock()
        self.drawTitle(10)
    def clockHands(self,clockFace):
        clockMiddlex,clockMiddley = DiagMaths.middle(clockFace)
        twelveOclockx, twelveOclocky = clockMiddlex,clockFace[1] 
        threeOclockx, threeOclocky = clockFace[2] - 4,clockMiddley
        return clockMiddlex, clockMiddley, twelveOclockx, twelveOclocky, threeOclockx, threeOclocky 
    def drawClock(self):
        clockFace = self.topRightCorner()
        clockMiddlex, clockMiddley, twelveOclockx, twelveOclocky, threeOclockx, threeOclocky = self.clockHands(clockFace)
        self.face = self.canvas.create_oval(clockFace)
        self.bigHand = self.canvas.create_line((clockMiddlex,clockMiddley,twelveOclockx,twelveOclocky))
        self.smallHand = self.canvas.create_line((clockMiddlex,clockMiddley,threeOclockx,threeOclocky))
    def move(self,dx,dy):
        self.shift(dx,dy)
        self.shapeMove()        
        self.moveTitle(10)
        self.moveClock()
        self.moveConnections(dx,dy)
    def moveClock(self):
        clockFace = self.topRightCorner()
        clockMiddlex, clockMiddley, twelveOclockx, twelveOclocky, threeOclockx, threeOclocky = self.clockHands(clockFace)
        self.canvas.coords(self.face,clockFace)
        self.canvas.coords(self.bigHand, (clockMiddlex,clockMiddley,twelveOclockx,twelveOclocky))
        self.canvas.coords(self.smallHand, (clockMiddlex,clockMiddley,threeOclockx,threeOclocky))
    def getPostscriptClock(self,psfile):
        clockFace = self.topRightCorner()
        clockMiddlex, clockMiddley, twelveOclockx, twelveOclocky, threeOclockx, threeOclocky = self.clockHands(clockFace)
        r = clockMiddlex - clockFace[0]
        fill = "1 1 1"
        psfile.write("newpath %s %s %s 0 360 arc closepath gsave %s setrgbcolor fill grestore stroke\n" % (
            clockMiddlex,clockMiddley,r,fill))
        psfile.write("newpath %s %s moveto %s %s lineto stroke\n" % (clockMiddlex, clockMiddley, twelveOclockx, twelveOclocky))
        psfile.write("newpath %s %s moveto %s %s lineto stroke\n" % (clockMiddlex, clockMiddley, threeOclockx, threeOclocky))        
        
class Activity(Resizable,Circle,Avatar):
    def getPov(self,f):
        cx,cy = self.middle()
        r = cx - self.outline[0]
        f.write('Activity(%d,%d,%d,"%s")\n' % (cx,DiagMaths.flipYCoord(cy),
                                             r,self.name))
    def getPostscript(self,psfile):
        self.shapeGetPostscript(psfile)
        self.getPostscriptTitle(self.middle(),psfile)        
    def setup(self):
        self.initResizing()
        self.defaultDims = defaultActivityDims
    def edge(self,point):
        return self.shapeEdge(point)
    def draw(self):
        self.shapeDraw(fill="white")
        self.drawTitle()
    def move(self,dx,dy):
        self.shift(dx,dy)
        self.shapeMove()
        self.moveTitle()
        self.moveConnections(dx,dy)

class State(Resizable, RoundedRect,Avatar):
    def avatarColor(self):
        return Colors.statecolor
    def drawCameo(self, canvas, parentDrawing, childAvatar, cameos):
        self.shapeGetCameo(canvas, parentDrawing, childAvatar, cameos, self.avatarColor())
        
    def getPov(self,f):
        cx,cy = self.middle()
        r = cx - self.outline[0]
        f.write('State(%d,%d,%d,"%s")\n' % (cx,DiagMaths.flipYCoord(cy),r,self.name))
    def getPostscript(self,psfile):
        self.shapeGetPostscript(psfile,thickness=2)
        self.getPostscriptTitle(self.middle(),psfile)        
    def setup(self):
        self.initResizing()
        self.defaultDims = defaultStateDims
        self.bump = stateBump
    def draw(self):
        self.shapeDraw(fill="white", outline=self.avatarColor(), width=2)
        self.drawTitle(bg=True)
        mx,my = self.middle()
        #self.icon = self.canvas.create_text(mx,my,"S",("times",20),fill="grey")
    def move(self,dx,dy):
        self.shift(dx,dy)
        self.shapeMove()
        self.moveTitle(bg=True)
        self.moveConnections(dx,dy)
        #self.canvas.coords(self.icon,self.middle())
    def edge(self,point):
        return self.shapeEdge(point)
    def setShape(self):
        self.shapeCreate()
        
class Child(Resizable, Rectangle, Avatar):
    def getPostscript(self, psfile):
        self.shapeGetPostscript(psfile)
        self.getPostscriptTitle(self.middle(),psfile)
        
    def getPov(self, povFile):
        povFile.write('Child (%s, %s, %s, %s, "%s")\n' % tuple(DiagMaths.flipYCoords(self.outline) + [self.name]))
        
#    def setShape(self):
#        self.shapeCreate()
    def setup(self):

        self.initResizing()
        self.bump = childBump
        import m3
        self.defaultDims = defaultChildDims
        if hasattr(self,"node"):
            # TBD this is a mess
            # This is the topNode of the interface of which this child is an instance
            self.specNode = m3.compile(fileName=self.node.tipe.qualId.image() + ".ci3o")
            self.bodyNode = m3.compile(fileName=self.node.tipe.qualId.image() + ".cm3o")
            # TBD we get to choose this later if we want something other than the default implementation
    def draw(self):
        self.shapeDraw(outline="black",fill="white",width=1)
        self.drawTitle(bg=True)
    def createCameos(self, parentDrawing, childAvatar):
        import Connection
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline
        for avatar in parentDrawing.allAvatars():
            avatar.drawCameo(self.canvas,parentDrawing,childAvatar,self.cameos)
        self.cameos += Connection.createCameoConnections(self.canvas, parentDrawing, childAvatar)
    def createCameosPS(self, parentDrawing, childAvatar, psfile):
        import Connection
        capOutline=parentDrawing.capsule.outline
        constraints=childAvatar.outline
        for avatar in parentDrawing.allAvatars():
            avatar.drawCameoPS(self.canvas,parentDrawing,childAvatar,psfile)
        Connection.createCameoConnectionsPS(self.canvas, parentDrawing, childAvatar,psfile)
    def updateCameos(self):
        for cameo in self.cameos:
            cameo.update()
    def move(self,dx,dy):
        self.shift(dx,dy)
        self.shapeMove()
        self.moveTitle(bg=True)
        self.moveConnections(dx,dy)
        self.movePorts(dx,dy)
    
    def movePorts(self,dx,dy):
        for port in self.childPorts:
            port.move(dx,dy)
    def capName(self):
        # TBD This is a cheap and nasty way of finding the capsule but it works
        # TBD Doesn't work if you want to find source
        capName = self.node.tipe.qualId.image()
        return "%s.m3" % capName
    def interfaceUnitName(self):
        # TBD slightly better than the above
        capName = self.node.tipe.qualId.image()
        return CompilationUnit.CompilationUnit(capName,"CapsuleInterface")
    def createChildPorts(self):
        #print self.node
        res = []
        for port in self.specNode.portList.kidsNoSep():
            portname = self.name + "." + port.id.idname
            cp = ChildPort(portname,port,title=port.id.idname)
            cp.setChild(self)
            res.append(cp)
        self.childPorts = res
        return res
    def getChildPorts(self):
        return self.childPorts

class Transition(RoundedRect,Avatar):
    def avatarColor(self):
        return Colors.transitioncolor
    def drawCameo(self, canvas, parentDrawing, childAvatar, cameos):
        self.shapeGetCameo(canvas, parentDrawing, childAvatar, cameos, self.avatarColor())
        
    def getPov(self, povFile):
        povFile.write('Transition (%s, %s, %s, %s, "%s")\n' % tuple(DiagMaths.flipYCoords(self.outline) + [self.name]))
    def getPostscript(self, psfile):
        self.shapeGetPostscript(psfile)
        self.getPostscriptTitle(self.middle(),psfile)
    def setup(self):
        self.defaultDims = defaultTransitionDims
        self.bump = transitionBump
    def edge(self,point):
        return self.shapeEdge(point)
    def setShape(self):
        self.shapeCreate()
    def draw(self):
        self.drawTitle()
        sx,sy,ex,ey = self.canvas.bbox(self.title)
        bb = self.canvas.bbox(self.title)
        width = ex - sx
        #print "set width to ", width
        #self.xsandys = bb
        self.setOutline(DiagMaths.fattenUp(bb,10))
        #self.xsandys[2] = ex
        self.canvas.delete(self.title)
        self.shapeDraw(fill=Colors.cancolor,outline=self.avatarColor())
        self.drawTitle()
    def setOwningState(self,state):
        self.owningState = state
    def move(self,dx,dy):
        self.shift(dx,dy)
        self.shapeMove()
        self.moveTitle()
        self.moveConnections(dx,dy)

class Start(Circle,Avatar):
    def avatarColor(self):
        return Colors.startcolor
    def getPov(self,f):
        cx,cy = self.middle()
        r = cx - self.outline[0]
        f.write("Start(%d,%d,%d)\n" % (cx,DiagMaths.flipYCoord(cy),r))
    def getPostscript(self,psfile):
        self.shapeGetPostscript(psfile,fill="0 0 0")
    def setup(self):
        self.defaultDims = defaultStartDims    
    def draw(self):
        self.shapeDraw(fill=self.avatarColor())
    def moveTitle(self): pass
    def edge(self,point):
        return self.shapeEdge(point)
    def move(self,dx,dy):
        self.shift(dx,dy)
        self.shapeMove()
        self.moveConnections(dx,dy)

class Procedure(Resizable,Rectangle,Avatar):
    def avatarColor(self):
        return Colors.procedurecolor
    def getPov(self,f):
        cx,cy = self.middle()
        r = cx - self.outline[0]
        f.write("Start(%d,%d,%d)\n" % (cx,DiagMaths.flipYCoord(cy),r))
    def getPostscript(self,psfile):
        self.shapeGetPostscript(psfile,fill="0 0 0")
        self.getPostscriptTitle(self.middle(),psfile)        
    def setup(self):
        self.initResizing()
        self.defaultDims = defaultProcedureDims
        self.shadowed = False
    def draw(self):
        self.shapeDraw(outline=self.avatarColor())
        self.drawTitle()
    def edge(self,point):
        return self.shapeEdge(point)
    def move(self,dx,dy):
        self.shift(dx,dy)
        self.shapeMove()
        self.moveConnections(dx,dy)
        self.moveTitle()

class PortCommon:
#    def avatarColor(self):
#        return Colors.portcolor
    def setResource(self,resource):
        sx,sy,ex,ey = resource
        ex = sx + self.defaultDims[0]
        ey = sy + self.defaultDims[1]
        self.setOutline((sx,sy,ex,ey))
    def draw(self):
        self.shapeDraw(fill=Colors.portcolor)
        self.drawTitle(yoff=portLabelOff)        
    def moveCommon(self,dx,dy,home):
        dx,dy = self.shiftWithConstraints(dx,dy,home)        
        self.shapeMove()
        self.moveTitle(yoff=portLabelOff)
        self.moveConnections(dx,dy)
        self.moveLabels(dx,dy)
    def edge(self,point):
        return self.shapeEdge(point)
    def getPov(self, povFile):
        povFile.write("Port(%s, %s, %s, %s)\n" % tuple(DiagMaths.flipYCoords(self.outline)))
    def getPostscript(self,psfile):
        self.shapeGetPostscript(psfile)
        self.getPostscriptTitle(self.middleTopPS(),psfile)
    def getSynchFor(self, otherPort):
        return self.node.getType().getSynchFor(otherPort.node.getType())
    def addPortLabel(self,pl):
        self.portLabels.append(pl)
    def moveLabels(self,dx,dy):
        for portLabel in self.portLabels:
            portLabel.move(dx,dy)
    
class Port(PortCommon,Rectangle,Avatar):
    def drawCameo(self, canvas, parentDrawing, childAvatar, cameos):
        pass
    def drawCameoPS(self, canvas, parentDrawing, childAvatar,psfile):
        pass
    
    def setup(self):
        self.defaultDims = defaultPortDims

    def setCapsule(self,capsule):
        self.capsule = capsule
        self.capsule.addPort(self)
    def move(self,dx,dy):
        self.moveCommon(dx,dy,self.capsule)
    def getMessagesFor(self,otherPort):
        if otherPort.avatarType() != "ChildPort": print "internal error, Port to Port connection"
        return self.node.getType().getMessagesFor(otherPort.node.getType(),"up")

class ChildPort(PortCommon,Rectangle,Avatar):
    def setup(self):
        self.defaultDims = defaultChildPortDims
        self.connLabels = []
    def setChild(self,child):
        self.child = child
    def move(self,dx,dy):
        self.moveCommon(dx,dy,self.child)
    def getMessagesFor(self,otherPort):
        #print otherPort
        if otherPort.avatarType() == "ChildPort":
            dir = "across"
        else:
            dir = "down"
        return self.node.getType().getMessagesFor(otherPort.node.getType(),dir)

class TransitionProxy(Rectangle,Avatar):
    def avatarColor(self):
        return Colors.transitioncolor
    def getPov(self, povFile):
        povFile.write("TransitionProxy(%s, %s, %s, %s)\n" % tuple(DiagMaths.flipYCoords(self.outline)))    
    def getPostscript(self,psfile):
        self.shapeGetPostscript(psfile)
        self.getPostscriptTitle(self.middle(),psfile)        
    def setup(self):
        self.defaultDims = defaultTransitionProxyDims
    def edge(self,point):
        return self.shapeEdge(point)
    def draw(self):
        mx,my = self.middle()
        self.drawTitle()
        self.setOutline(self.canvas.bbox(self.title))
        self.canvas.delete(self.title)
        self.shapeDraw(fill=Colors.cancolor, outline=self.avatarColor())
        self.drawTitle()
    def move(self,dx,dy):
        self.shift(dx,dy)        
        self.shapeMove()
        mx,my = self.middle()
        self.moveConnections(dx,dy)
        self.moveTitle()

class PSWords:
    def getPostscriptWords(self,psfile):
        x,y,_,_ = self.outline
        wordarray = string.split(self.words,"\n")
        y = y + 10
        for line in wordarray:
            psfile.write("%s %s moveto (%s) show\n" % (x,y,line))
            y = y + 10
        
class Note(Rectangle,Avatar,PSWords):
    def getPostscript(self,psfile):
        self.shapeGetPostscript(psfile)
        self.getPostscriptWords(psfile)
    def avatarColor(self):
        return Colors.notecolor
    def edge(self, coord):
        return self.edgeRect(coord)
    def setup(self):
        self.arrows = []
    def draw(self):
        sx,sy,ex,ey = self.outline
        self.text = self.canvas.create_text(sx,sy,self.words,("times",10),anchor='nw')
        self.setOutline(self.canvas.bbox(self.text))
        self.canvas.delete(self.text)
        self.shapeDraw(fill=self.avatarColor())
        self.text = self.canvas.create_text(sx,sy,self.words,("times",10),anchor='nw')
    def setResource(self, noteDetails):
        self.node = None
        self.words, (x,y), self.arrowCoords = noteDetails
        self.words = self.words.replace("%0A",'\n')
        self.setOutline((x,y,x+100,y+100))
    def move(self,dx,dy):
        self.shift(dx,dy)
        self.shapeMove()
        sx,sy,ex,ey = self.outline
        self.canvas.coords(self.text,(sx,sy))
        self.moveConnections(dx,dy)
    def getResource(self):
        sx,sy,ex,ey = self.outline
        return self.words, (sx,sy), [(arrow.outline[0], arrow.outline[1]) for arrow in self.arrows]
    def addArrow(self,arrow):
        self.arrows.append(arrow)
    def addArrowXY(self,x,y):
        na = NoteArrow("**Arrow%s" % time.time(), None)
        na.create(x,y)
        self.addArrow(na)



class NoteArrow(Circle,Avatar):
    def getPostscript(self, psfile):
        pass
    def draw(self): pass
    def setup(self):
        self.defaultDims = 20,20
    def create(self,x,y):
        self.setOutline((x,y))
    def move(self,dx,dy):
        self.shift(dx,dy)
        self.moveConnections(dx,dy)
        # TBD move the arrow as well
    def getResource(self):
        return None

class Label(Rectangle,Avatar,PSWords):
    def setInvisible(self):
        if not len(self.words): return
        if Options.options.arrowsOff: return
        self.canvas.config(self.pointer,fill=Colors.cancolor)
        self.canvas.config(self.text, fill=Colors.cancolor)
        self.canvas.lower(self.pointer)
        self.canvas.lower(self.text)
    def setVisible(self):
        if not len(self.words): return
        if Options.options.arrowsOff: return
        self.canvas.config(self.pointer,fill=self.avatarColor())
        self.canvas.config(self.text,fill=self.avatarColor())        
        self.canvas.lift(self.pointer)
        self.canvas.lift(self.text)
            
    def drawCameo(self, canvas, parentDrawing, childAvatar,cameos):
        pass
    def drawCameoPS(self, canvas, parentDrawing, childAvatar,psfile):
        pass
    def getPostscript(self, psfile):
        if Options.options.arrowsOff: return 
        if len(self.words):
            self.getPostscriptWords(psfile)
            psfile.write("newpath %s 1 5 7 arrow stroke\n" % PSUtils.arrayAsString(self.arrowCoords()))
    def draw(self):
        if Options.options.arrowsOff:
            color = Colors.cancolor
        else:
            color = self.avatarColor()
        #print "drawing connlabel", self.name
        x,y = self.middle()
        if len(self.words):
            self.text = self.canvas.create_text(x,y,self.words,("times",10),fill=color)
            self.outline = self.canvas.bbox(self.text)
            self.pointer = self.canvas.create_line(self.arrowCoords(),arrow="last",fill=color)
        if Options.options.arrowsOff and len(self.words):
            self.canvas.lower(self.pointer)
            self.canvas.lower(self.text)
            
    def setup(self):
        self.defaultDims = 20,20
    def create(self,x,y):
        self.setOutline((x,y))
    def move(self, dx,dy, endAvatar=None, adx=None, ady=None):
        if endAvatar:
            dx, dy = self.calcAdditionalShift(dx, dy, endAvatar, adx, ady)
        self.shift(dx,dy)
        if len(self.words):
            sx, sy, ex, ey = self.outline
            self.canvas.coords(self.text, self.middle())
            self.canvas.coords(self.pointer, self.arrowCoords())
    def setWords(self, words):
        self.words = string.join(words,"\n")

class ConnLabel(Label):
    def setPorts(self,a,b):
        self.fromPort = a
        self.toPort = b
        a.addConnLabel(self)
        b.addConnLabel(self)
    def arrowCoords(self):
        mx,my = self.middle()
        vx,vy = DiagMaths.Vector(self.toPort, self.fromPort)
        xoff = connLabelArrowLen*vx
        yoff = connLabelArrowLen*vy        
        sx,sy = self.shapeEdge((mx+xoff, my+yoff))
        return (sx,sy,sx+xoff,sy+yoff)
    def calcAdditionalShift(self,dx,dy, endAvatar, adx, ady):
        if endAvatar == self.fromPort:
            startAvatar = self.toPort
        else:
            startAvatar = self.fromPort
        samx,samy = startAvatar.middle()
        eamx,eamy = endAvatar.middle()
        # return how much the middle has moved by
        nmx,nmy = DiagMaths.middle((samx,samy,eamx,eamy))
        omx,omy = DiagMaths.middle((samx,samy,eamx-adx,eamy-ady))
        return nmx-omx,nmy-omy
class PortLabel(Label):
    def setPort(self,p,dir):
        self.port = p
        self.dir = {"INCOMING": -1, "OUTGOING": 1}[dir]
    def arrowCoords(self):
        mx,my = self.middle()
        vx,vy = DiagMaths.Vector(self, self.port)
        xoff = connLabelArrowLen*vx*self.dir
        yoff = connLabelArrowLen*vy*self.dir
        if(abs(xoff)) > (abs(yoff)):
            yoff = 0
        else:
            xoff = 0
        sx,sy = self.shapeEdge((mx+xoff, my+yoff))
        return (sx,sy,sx+xoff,sy+yoff)
    def calcAdditionalShift(dx,dy, endAvatar, adx, ady):
        print "additionalshift"
        return adx, ady
class Cameo:
    normal,connection,twolines = range(3) # fake enum
    def __init__(self, canvas, parent, parentDrawing, childAvatar, handle, cameoType=normal):
        self.canvas = canvas # what the cameo is drawn on
        self.parent = parent # the full size object on the original canvas
        self.parentDrawing = parentDrawing # the full size drawing
        self.childAvatar = childAvatar # the child containing the cameos
        self.handle = handle # what Tk created when the cameo was drawn
        self.cameoType = cameoType # do we need to calculate xsandys each time
    def update(self):
        if self.cameoType in (self.normal, self.connection):
            if self.cameoType == self.normal:
                xsandys = self.parent.xsandys
            else:
                xsandys = self.parent.xsandys()

            self.canvas.coords(
                self.handle, DiagMaths.constrain(xsandys,
                                                     self.parentDrawing.capsule.outline,
                                                     self.childAvatar.outline))
        elif self.cameoType == self.twolines:
            sx,sy,ex,ey = self.parent.outline
            handleTop,handleBottom = self.handle
            self.canvas.coords(
                handleTop, DiagMaths.constrain((sx,sy,ex,sy),
                                                 self.parentDrawing.capsule.outline,
                                                 self.childAvatar.outline))
            self.canvas.coords(
                handleBottom, DiagMaths.constrain((sx,ey,ex,ey),
                                                 self.parentDrawing.capsule.outline,
                                                 self.childAvatar.outline))
            
        else:
            raise "run time bug : wrong cameo type"
