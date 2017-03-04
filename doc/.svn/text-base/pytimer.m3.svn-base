CAPSULE pytimer ;
IMPORT Timer, IO;
  VAR myTimer : PERIODIC FIXED TIMER  DELAY 10 ps ;
      i : INTEGER := 0;
  ACTIVITY timeact () = 
  BEGIN 
      IO.Put("timeact\n");
      i := i + 1;
      SEND foo(i);
  END timeact ;
  CONNECT
    myTimer -> timeact;
BEGIN

   Timer.Start(myTimer);

END pytimer.
