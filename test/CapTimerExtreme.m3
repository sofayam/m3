CAPSULE CapTimerExtreme ;
 
IMPORT Timer, Regress, Log;
  ACTIVITY start () = 
  BEGIN 
    Regress.init("Timer Extremes");
    Log.setLength(3);
    Timer.Start(big);
    Timer.Start(medium);
    Timer.Start(small);
  END start ;
  VAR big : ONESHOT FIXED TIMER DELAY 10 year ;
  VAR small : ONESHOT FIXED TIMER DELAY 1 ps ;
  VAR medium : ONESHOT FIXED TIMER DELAY 152 s ;
  ACTIVITY summary () = 
  BEGIN 
     Regress.assertPass(Log.equalsLog(Log.log{"small", "medium", "big"}));
     Regress.summary()
  END summary ;
  ACTIVITY recordSmall () =
  BEGIN 
     Log.addEvent("small");
     SEND smallAlarm(); 
  END recordSmall ;
  ACTIVITY recordMedium () =
  BEGIN 
     Log.addEvent("medium");
     SEND mediumAlarm(); 
  END recordMedium ;
  ACTIVITY recordBig () =  
  BEGIN 
     Log.addEvent("big");
     SEND bigAlarm(); 
  END recordBig ;

  CONNECT
    small -> recordSmall;
    medium -> recordMedium;
    big -> recordBig;
BEGIN
END CapTimerExtreme.
