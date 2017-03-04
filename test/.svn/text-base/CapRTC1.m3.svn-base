CAPSULE CapRTC1 ;
  IMPORT Log, Regress;
  USECAPSULE CapRTC21 ;
  USECAPSULE CapRTC22 ;
  VAR capRTC21 : CapRTC21 ;
  VAR capRTC22 : CapRTC22 ;
  ACTIVITY setup () = 
  BEGIN 
    Regress.init("RunToCompletion");
    Log.setLength(5)
  END setup ;
  ACTIVITY summary () = 
    VAR expected := Log.log{"a21","s3","s1","s4","s2"};
  BEGIN 
    Regress.assertPass(Log.equalsLog(expected));
    Regress.summary()
  END summary ;
  CONNECT
    capRTC21.p2 <=> capRTC22.p1;
    p1 <=> capRTC21.p1;

BEGIN

END CapRTC1.
