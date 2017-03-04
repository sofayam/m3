CAPSULE CapExp ;
IMPORT Timer;
  ACTIVITY question (x : INTEGER) = 
  BEGIN 
    buff := x;
    Timer.Start(t);
  END question ;
  ACTIVITY answer () = 
  BEGIN 
     SEND reply(buff * 2);
  END answer ;
  VAR t : ONESHOT FIXED TIMER  DELAY 11 ps ;
  VAR buff : INTEGER ;
  CONNECT
    t -> answer;
BEGIN

END CapExp.
