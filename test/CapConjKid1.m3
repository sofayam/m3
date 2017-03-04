CAPSULE CapConjKid1 ;
IMPORT Timer;
  ACTIVITY routeA () =
   
  BEGIN 
    SEND p2.a();
  END routeA ;
  ACTIVITY routeB () = 
  BEGIN 
     SEND p1.b()
  END routeB ;
  CONNECT
    p1.a -> routeA;
  p2.b -> routeB;
BEGIN

END CapConjKid1.
