
CAPSULE CapRTC21 ;
  IMPORT Log;
  ACTIVITY a21 () = 
  BEGIN 
      Log.addEvent("a21");
      SEND s1();
      SEND s2();
      SEND s3();
  END a21 ;
  ACTIVITY s3 () = 
  BEGIN
    Log.addEvent("s3")
  END s3 ;

BEGIN

END CapRTC21.
