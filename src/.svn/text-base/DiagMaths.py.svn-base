import math
def findEdgeCirc(cx, cy, r, mx, my):
    #
    # Find the point on the edge of a circle with centre cx,cy and radius r
    # corresponding to mouse position mx, my treated as a vector from that
    # centre
    #
    xoff = mx - cx
    yoff = my - cy
    xsig = 1; ysig = 1
    if xoff < 0:
        xsig = -1
        xoff = -xoff
    if yoff < 0:
        ysig = -1
        yoff = -yoff
    if xoff == 0: xoff = 1 # avoid div by zero errors
    if yoff == 0: yoff = 1

    mdist = math.sqrt((xoff**2)+(yoff**2))    
    rat = float(r)/mdist

    resx = cx + ((xoff * rat) * xsig)
    resy = cy + ((yoff * rat) * ysig)
    return (resx, resy)


def findEdgeOval(cx, cy, rx, ry, mx, my):
    #
    # Find the point on the edge of an oval with centre cx,cy, xradius rx and yradius ry
    # corresponding to mouse position mx, my treated as a vector from that
    # centre
    #
    xoff = mx - cx
    yoff = my - cy
    xsig = 1; ysig = 1
    if xoff < 0:
        xsig = -1
        xoff = -xoff
    if yoff < 0:
        ysig = -1
        yoff = -yoff
    if xoff == 0: xoff = 1 # avoid div by zero errors
    if yoff == 0: yoff = 1

    mdist = math.sqrt((xoff**2)+(yoff**2))    
    rat = float(rx)/mdist

    resx = cx + ((xoff * float(rx) / mdist) * xsig)
    resy = cy + ((yoff * float(ry) / mdist) * ysig)
    return (resx, resy)


    
def findEdgeRect(cx, cy, rx, ry, mx, my):
    #
    # Find the point on the edge of a rect with centre cx,cy and radius rx,ry
    # corresponding to mouse position mx, my treated as a vector from that
    # centre
    #
    xoff = mx - cx
    yoff = my - cy
    xsig = 1; ysig = 1
    if xoff < 0:
        xsig = -1
        xoff = -xoff
    if yoff < 0:
        ysig = -1
        yoff = -yoff
    if xoff == 0: xoff = 1 # avoid div by zero errors
    if yoff == 0: yoff = 1
    if ry == 0: ry = 1
    mouseVector = float(xoff)/yoff
    containerVector = float(rx)/ry
    if mouseVector > containerVector:
        gdx = rx
        gdy = (1/mouseVector) * rx
    else:
        gdx = mouseVector * ry
        gdy = ry
    x = cx + (gdx * xsig)
    y = cy + (gdy * ysig)
    return (x,y, (mouseVector,xsig,ysig))

def useVector(cx, cy, rx, ry, v):
    mouseVector, xsig, ysig = v
    containerVector = float(rx)/ry
    if mouseVector > containerVector:
        gdx = rx
        gdy = (1/mouseVector) * rx
    else:
        gdx = mouseVector * ry
        gdy = ry
    x = cx + (gdx * xsig)
    y = cy + (gdy * ysig)
    return (x,y)

def dist(x1,y1,x2,y2,mx,my):
    #
    # Distance of a point my,my from the line x1,y1-x2,y2
    # - well alright not exactly but good enough
    dx = x2 - x1
    dy = y2 - y1
    base = math.sqrt((dx**2)+(dy**2))
    mdxa = mx - x1
    mdya = my - y1
    al = math.sqrt((mdxa**2)+(mdya**2))
    mdxb = mx - x2
    mdyb = my - y2
    bl = math.sqrt((mdxb**2)+(mdyb**2))
    return (al + bl) - base 

    
def roundedRectCoords(sx,sy,ex,ey,bump):
        b = bump
        return (sx+b,sy,ex-b,sy,ex,sy,
                ex,sy+b,ex,ey-b,ex,ey,
                ex-b,ey,sx+b,ey,sx,ey,
                sx,ey-b, sx,sy+b, sx,sy)

def isUnder(x,y,outline):
        sx,sy,ex,ey = outline
        #print "isUnder", x,y,outline
        res = (x >= sx) and (x <= ex) and (y >= sy) and (y <= ey)
        return res

def isInside(avatarOutline, selectCoords):
    sx,sy,ex,ey = avatarOutline
    return isUnder(sx,sy,selectCoords) and isUnder(ex,ey,selectCoords)
    
def addOffset(coords,dx,dy):
    shifted = []
    for idx,coord in enumerate(coords):
        if idx % 2:
            coord += dy
        else:
            coord += dx
        shifted.append(coord)
    return shifted

def middle(coords):
    sx,sy,ex,ey = coords
    return ((sx+ex)/2),((sy+ey)/2)

def scaleXY(coords, x, y):
    # original coords are %s of final x and y
    scaled = []
    for idx,coord in enumerate(coords):
        if idx % 2:
            res = (coord / 100.0) * y
        else:
            res = (coord / 100.0) * x
        scaled.append(res)
    return scaled
    
def setYFlip(maxy):
    global yflip
    yflip = maxy

def flipYCoord(coord):
    return yflip - coord

def flipYCoords(coords):
    if len(coords) == 4:
        newcoords =  [coords[0],flipYCoord(coords[1]),coords[2],flipYCoord(coords[3])]
    else:
        raise "hell"
    return newcoords
                      
def fattenUp(bbox,dy):
    return bbox[0], bbox[1]-dy, bbox[2], bbox[3]+dy

def inset(xsandys, off):
    sx,sy,ex,ey = xsandys
    return [sx+off,sy+off,ex-off,ey-off]

def constrain(xsandys, capOutline, constraints):
    res = []
    osx,osy,oex,oey = capOutline
    oldWidth = oex-osx
    oldHeight = oey-osy
    sx,sy,ex,ey = constraints
    newWidth = ex - sx
    newHeight = ey - sy
    for idx,coord in enumerate(xsandys):
        if idx % 2:
            res.append((((coord - osy)/ oldHeight) * newHeight) + sy)
        else:
            res.append((((coord - osx)/ oldWidth) * newWidth) + sx)             
    return res

def Vector(a,b):
    def sign(x):
        if x > 0: return 1
        if x < 0: return -1
        return 0
    sx,sy = b.middle()
    ex,ey = a.middle()
    if sx==ex or sy==ey:
        return sign(ex-sx),sign(ey-sy)
    hyp = math.sqrt(((ex-sx)**2)+((ey-sy)**2))
    vx = 1.0/hyp*(ex-sx)
    vy = 1.0/hyp*(ey-sy)
    return vx,vy
