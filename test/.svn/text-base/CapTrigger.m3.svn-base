CAPSULE CapTrigger;
  IMPORT Log, Regress;
  VAR
    x := 0;

  TRIGGER t1 ON x = 3;  

  ACTIVITY act1 () =
  BEGIN
    SEND firet1();
    Log.addEvent("t1");
    x := x + 1;
  END act1;

  ACTIVITY act2 () =
  BEGIN
    SEND firet2();
    Log.addEvent("t2");
  END act2;
  ACTIVITY setup () = 
  BEGIN 
     Regress.init("Trigger");
     Log.setLength(5);
  END setup ;
  ACTIVITY summary () = 
     VAR expected := Log.log{"t1","t1","t1","t2","t1"};
  BEGIN 
      Regress.assertPass(Log.equalsLog(expected));
      Regress.summary()
  END summary ;

CONNECT 
  t1 -> act2;
BEGIN

END CapTrigger.
