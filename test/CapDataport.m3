CAPSULE CapDataport ;
IMPORT Regress;
IMPORT CapDataPortTypes AS CDT;
  USECAPSULE CapDataportChild ;

  VAR r : CDT.rec ;
  VAR x : INTEGER := 0;

  ACTIVITY expectx (ex : INTEGER) = 
  BEGIN
     Regress.assertPass(ex = x);
  END expectx ;

  ACTIVITY expectr (er : CDT.rec) = 
  BEGIN
     Regress.assertPass(er = r);
  END expectr ;

  ACTIVITY init () = 
  BEGIN 
     Regress.init("Dataport");
  END init ;
  ACTIVITY summary () = 
  BEGIN 
     Regress.summary();
  END summary ;
  VAR child : CapDataportChild ;
  CONNECT
    p1 <=> child.p1;
BEGIN

END CapDataport.
