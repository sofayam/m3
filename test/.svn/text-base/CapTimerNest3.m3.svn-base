
CAPSULE CapTimerNest3 ;
IMPORT Timer;
  VAR t : ONESHOT FIXED TIMER DELAY 100 ms ;
  ACTIVITY startInner () = 
  BEGIN 
     Timer.Start(t);
  END startInner ;
  CONNECT
    t -> reply;
BEGIN

END CapTimerNest3.
