
CAPSULE CapRTC221 ;
  IMPORT Log;
  ACTIVITY s1 () = 
  BEGIN 
    Log.addEvent("s1");
    SEND s4();
  END s1 ;
  

BEGIN

END CapRTC221.
