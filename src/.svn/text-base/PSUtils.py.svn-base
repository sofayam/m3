import string

def arrayAsString(a):
    return string.join([str(x) for x in a], " ")


# TBD is there some easier way to do this ?
def roundedRectPS(sx,sy,ex,ey,bump,color,thickness):
    res = ""
    if color:
        res += "gsave %s setrgbcolor \n" % makeColor(color)
    b = bump
    res += "%s setlinewidth\n" % thickness
    res += "%s %s moveto\n" % (sx, sy+b)
    res += "%s %s %s %s %s %s curveto\n" % (sx,sy,sx,sy,sx+b,sy)
    res += "%s %s lineto\n" % (ex-b, sy)
    res += "%s %s %s %s %s %s curveto\n" % (ex,sy,ex,sy,ex,sy+b)
    res += "%s %s lineto\n" % (ex, ey-b)
    res += "%s %s %s %s %s %s curveto\n" % (ex,ey,ex,ey,ex-b,ey)
    res += "%s %s lineto\n" % (sx+b, ey)
    res += "%s %s %s %s %s %s curveto\n" % (sx,ey,sx,ey,sx,ey-b)
    res += "%s %s lineto\n" % (sx, sy+b)
    res += "closepath stroke\n"
    if color:
        res += "grestore\n"
    # res += psdebug(sx,sy+b, "%s %s" % (sx,sy+b))
    return res

def psdebug(x,y,text):
    res =  "/Times-Roman findfont\n"
    res += "15 scalefont setfont\n"
    res += "%s %s moveto\n" % (x,y)
    res += "(%s) show\n" % text
    return res

def polygonPS(points):
    res = "%s %s moveto\n" % (points[0], points[1])
    for idx in range(1,len(points)/2):
        xoff = idx*2
        yoff = xoff+1
        x = points[xoff]
        y = points[yoff]
        res += "%s %s lineto\n" % (x,y)
    res += "closepath gsave  1 1 1 setrgbcolor fill grestore stroke\n"
    return res

colorMap = {"grey" : (128, 138, 135), "red" : (255,0,0), "purple": (147, 112, 219),
            "lavender": (230, 230, 250), "yellow": (255,255,0),
            "blue" : (0,0,255), "black" : (0,0,0), "white": (255,255,255)}
    
def makeColor(color):
    #convert 3 ints to a string of fractions of 256
    r,g,b = colorMap[color]
    return "%s %s %s" % (r / 255.0, g / 255.0, b / 255.0)
    
