// Persistence of Vision Ray Tracer Scene Description File
// Vers: 3.5
// TBD :
// themes

#version 3.5;

#include "colors.inc"
#include "textures.inc"                       
#include "shapes.inc"
                       
global_settings {
  assumed_gamma 1.0
}

// ----------------------------------------

#declare Maxx = <<maxX>>;
#declare Maxy = <<maxY>>;


camera {
  location  <Maxx/2, Maxy/2, -Maxx>
  look_at   <Maxx/2, Maxy/2,  0.0>
}

#ifdef(Foo)
sky_sphere {
  pigment {
    gradient y
    color_map {
      [0.0 rgb <0.6,0.7,1.0>]
      [0.7 rgb <0.0,0.1,0.8>]
    }
  }
}
#end

background { color White }
light_source {
  <Maxx, Maxy, -Maxx>            // light's position (translated below)
  color rgb <1, 1, 1>  // light's color
}

#macro Arrow(sx,sy,ex,ey,col)
   #declare VN = vnormalize ( <sx,sy,0> - <ex,ey,0> )  ;
   cylinder { <sx,sy,0> + VN*10,<ex,ey,0> + VN*10 ,3 texture { pigment { color col } finish { Shiny } }}
   cone { 0,0,10 * VN,10 texture { pigment { color col } finish { Shiny } } translate <ex,ey,0>}
#end   
 
#macro Block(sx,sy,ex,ey,sz,ez)
   object {
      Round_Box( <sx,sy,sz>, <ex,ey,ez>, 15, yes)  
      texture { PinkAlabaster }}	
#end
 
#macro Label(cx,cy,name)
   #local TS = 20;
   object {
    text {
     ttf "timrom.ttf" name 1, 0
     pigment { Yellow }
     scale <TS,TS,1>
    }
    #local TW = Text_Width("timrom.ttf" name, TS, 0);
    translate <cx-(TW/2),cy-10,-6>
   }
#end

#macro MidLabel(sx,sy,ex,ey,name)
   #local CX = (sx + ex) / 2;
   #local CY = (sy + ey) / 2;
   Label(CX,CY,name)
#end 

#macro Message(sx,sy,ex,ey,name)
   box { <sx,sy,-5> <ex,ey,5>  
      texture { pigment { Red } finish { Shiny } } }
   MidLabel(sx,sy,ex,ey,name)
#end

#macro Port(sx,sy,ex,ey)
   object {
      Round_Box( <sx,sy,0>, <ex,ey,30>, 5, yes)  
      texture { pigment { Grey } finish { Shiny } } }
#end
    

#macro Capsule(sx,sy,ex,ey,name)
   object {
      Round_Box( <sx,sy,40>, <ex,ey,50>, 30, yes)  
      texture { Glass }}  
   MidLabel(sx,sy,sx,sy,name)
#end
#macro Child(sx,sy,ex,ey,name)
   object {
      Round_Box( <sx,sy,10>, <ex,ey,15>, 5, yes)  
      texture { pigment { color White } finish { Shiny } }}
   MidLabel(sx,sy,ex,ey,name)
#end

    
#macro Activity(cx,cy,r,name)
   sphere { <cx, cy, 0> r   
   scale <1,1,0.2>
   texture { pigment { color Black } finish { Shiny } }}
   Label(cx,cy,name)
#end
    
#macro State(cx,cy,r,name)
   #local O = 6;
   torus { r-O, O
       rotate -90*x
       translate <cx,cy,0>
       texture { pigment { color Blue } finish { Shiny } }}
    Label(cx,cy,name)
#end

#macro Transition(sx,sy,ex,ey,name)
   object {
      Round_Box( <sx,sy,20>, <ex,ey,0>, 5, yes)  
      texture { pigment { color Blue } finish { Shiny } }}	
   box { <sx+5,sy-5,-5> <ex-5,ey+5,5>    
      texture { pigment { color Black } finish { Shiny } }}	
   MidLabel(sx,sy,ex,ey,name)   
#end

#macro TransitionProxy(sx,sy,ex,ey)
   object {
      Round_Box( <sx,sy,5>, <ex,ey,-5>, 2, yes)  
      texture { pigment { color Blue } finish { Shiny } }}	
#end

#macro DataStore(sx,sy,ex,ey,name)
   object {
      Round_Box( <sx,sy,-5>, <ex,sy+5,30>, 5, yes)  
      texture { pigment { color Brown } finish { Shiny } }}	
   object {
      Round_Box( <sx,ey+5,-5>, <ex,ey,30>, 5, yes)  
      texture { pigment { color Brown } finish { Shiny } }}	
   #local O = 5;
   cylinder { <sx+O,sy,0>, <sx+O,ey,0>, 2 texture { pigment { color White } finish { Shiny }}}
   cylinder { <sx+O,sy,25>, <sx+O,ey,25>, 2 texture { pigment { color White } finish { Shiny }}}
   cylinder { <ex-O,sy,0>, <ex-O,ey,0>, 2 texture { pigment { color White } finish { Shiny }}}
   cylinder { <ex-O,sy,25>, <ex-O,ey,25>, 2 texture { pigment { color White } finish { Shiny }}}
   MidLabel(sx,sy,ex,ey,name)
#end

#macro Trigger(sx,sy,ex,ey,name)
   object {
      Round_Box( <sx,sy,10>, <ex,ey,15>, 5, yes)  
      texture { pigment { color Gold } finish { Shiny } }}
   MidLabel(sx,sy,ex,ey,name)
#end

#macro Timer(sx,sy,ex,ey,name)
   object {
      Round_Box( <sx,sy,10>, <ex,ey,15>, 5, yes)  
      texture { pigment { color Silver } finish { Shiny } }}
   MidLabel(sx,sy,ex,ey,name)
#end

#macro Start(cx,cy,r)
   sphere { <cx, cy, 0> r 
   texture { pigment { color Red } finish { Shiny } }}
#end

#macro Globe(cx,cy,r)
   sphere { <cx, cy, 0> r 
   texture { Glass }}  
#end

