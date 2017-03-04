CAPSULE CapTimeReset ;
IMPORT Timer, Regress;

  VAR t1 : ONESHOT FIXED TIMER  DELAY 10 s ;

  VAR t4 : ONESHOT FIXED TIMER  DELAY 40 s ;

  ACTIVITY initTime () = 
  BEGIN 
    Timer.Start(t1);
 
    Timer.Start(t4);
  END initTime ;

  ACTIVITY failTimeDeep () = 
  BEGIN 
     RESET ;
  END failTimeDeep ;

  ACTIVITY failTimeShallow () = 
  BEGIN 
     RESET 1;
  END failTimeShallow ;

  ACTIVITY happens () = 
  BEGIN 
     Regress.assertPass(TRUE)
  END happens ;

  ACTIVITY neverhappens () = 
  BEGIN 
      Regress.assertPass(FALSE)
  END neverhappens ;

  CONNECT
    t1 -> happens;
    t4 -> neverhappens;

BEGIN

END CapTimeReset.
