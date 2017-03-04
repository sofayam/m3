CAPSULE CapTimerNest1 ;
IMPORT Timer, Regress;
  USECAPSULE CapTimerNest2 ;
  VAR tn2 : CapTimerNest2 ;
  VAR t : PERIODIC FIXED TIMER DELAY 200 ms ;
  ACTIVITY start () = 
  BEGIN 
    Regress.init("TimerNest");
    Timer.Start(t);
  END start ;
  ACTIVITY comingBack () = 
  BEGIN 
    cameBack := cameBack + 1;
    SEND outerreply();
  END comingBack ;
  ACTIVITY summary () =
     VAR res : BOOLEAN; 
  BEGIN 
     res := cameBack = 4;
     Regress.assertPass(res);
     Regress.summary();
  END summary ;
  VAR cameBack : INTEGER := 0;
  CONNECT
    t -> tn2.startInner;
    tn2.reply -> comingBack;
   

BEGIN

END CapTimerNest1.
