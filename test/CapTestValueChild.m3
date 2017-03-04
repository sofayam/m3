CAPSULE CapTestValueChild ;
IMPORT Timer;
  ACTIVITY start () = 
  BEGIN 
     Timer.Start(ticker);
  END start ;
  VAR ticker : PERIODIC FIXED TIMER  DELAY 1 s ;
  ACTIVITY addTick () = 
  BEGIN 
     ticks := ticks + 1;
  END addTick ;
  VAR ticks := 0 ;
  CONNECT
    ticker -> addTick;
BEGIN

END CapTestValueChild.
