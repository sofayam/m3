CAPSULE CapMain;
  IMPORT Regress;
  USECAPSULE PingPong;
  VAR pp : PingPong;
  ACTIVITY summary () = 
  BEGIN 
      Regress.summary();
  END summary ;
  
CONNECT
  p1 <=> pp.p1;
  pp.innerreply -> outerreply;

BEGIN
  Regress.init("CapMain")
END CapMain.
