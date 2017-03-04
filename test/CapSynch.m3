CAPSULE CapSynch ;
IMPORT Regress;
  USECAPSULE CapSynchChild1 ;
  USECAPSULE CapSynchChild2 ;
  VAR c1 : CapSynchChild1 ;
  VAR c2 : CapSynchChild2 ;

  ACTIVITY asyn1 () = 
  BEGIN 
     SEND c1.asyn();
     CALL c2.sCheck(0);
  END asyn1 ;

  ACTIVITY asyn2 () = 
  BEGIN 
     CALL c2.sCheck(4);
  END asyn2 ;

  ACTIVITY varCheck() =
     VAR x : INTEGER := 0;
  BEGIN
     CALL c2.varCheck(x);
     Regress.assertPass(x = 5);
  END varCheck;

  ACTIVITY init () = 
  BEGIN 
     Regress.init("Synchronous Messages");
  END init ;
  ACTIVITY summary () = 
  BEGIN 
     Regress.summary();
  END summary ;
  CONNECT
    c1.p2 <=> c2.p1;
BEGIN

END CapSynch.
