CAPSULE pytrigger ;
IMPORT Timer;
  TRIGGER isZero ON counter = 0;
  ACTIVITY dec () = 
  BEGIN 
     counter := counter - 1;
  END dec ;
  ACTIVITY handler () = 
  BEGIN 
     SEND alarm();
  END handler ;
  VAR counter : INTEGER := 2;
  CONNECT
    isZero -> handler;
BEGIN

END pytrigger.
