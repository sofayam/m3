CAPSULE CapConjKid2 ;
IMPORT Timer;
  ACTIVITY routea () = 
  BEGIN 
     SEND p2.a() 
  END routea ;
  ACTIVITY routeB () = 
  BEGIN 
     SEND p1.b()
  END routeB ;
  CONNECT
    p1.a -> routea;
  p2.b -> routeB;
BEGIN

END CapConjKid2.
