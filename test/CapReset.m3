CAPSULE CapReset ;
IMPORT Timer, Regress;

  USECAPSULE CapTimeReset ;
  USECAPSULE CapCmdReset ;

  VAR timechild : CapTimeReset ;
  VAR cmdchild : CapCmdReset ;

  VAR t : ONESHOT FIXED TIMER  DELAY 50 s ;

  VAR happened : BOOLEAN ;
  
  ACTIVITY startTimeShallow () =
  BEGIN 
     happened := FALSE;
     Timer.Start(t);
     SEND timechild.p1.initTime();
  END startTimeShallow ;

  ACTIVITY startTimeDeep () =
  BEGIN 
     happened := FALSE ;
     Timer.Start(t);
     SEND timechild.p1.initTime();
  END startTimeDeep ;

  ACTIVITY sometimeshappens () =    
  BEGIN 
     happened := TRUE;
  END sometimeshappens ;

  ACTIVITY doCmdDeep () = 
  BEGIN 
     happened := FALSE;
     SEND cmdchild.failCmdDeep();
     SEND sometimeshappens();
  END doCmdDeep ;

  ACTIVITY doCmdShallow () = 
  BEGIN 
     happened := FALSE;
     SEND cmdchild.failCmdShallow();
     SEND sometimeshappens();
  END doCmdShallow ;

  ACTIVITY checkCmdShallow () = 
  BEGIN 
     Regress.assertPass(NOT happened)
  END checkCmdShallow ;

  ACTIVITY checkCmdDeep () = 
  BEGIN 
     Regress.assertPass(happened)
  END checkCmdDeep ;


  ACTIVITY checkTimeDeep () = 
  BEGIN 
     Regress.assertPass(happened)
  END checkTimeDeep ;

  ACTIVITY checkTimeShallow () = 
  BEGIN 
     Regress.assertPass(NOT happened)
  END checkTimeShallow ;

  ACTIVITY init () = 
  BEGIN 
      Regress.init("Subsystem Reset")
  END init ;

  ACTIVITY summary () = 
  BEGIN 
      Regress.summary()
  END summary ;

  CONNECT    
    t -> sometimeshappens;
    p1 <=> timechild.p1 ; 
BEGIN

END CapReset.
