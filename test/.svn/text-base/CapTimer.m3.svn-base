CAPSULE CapTimer;
IMPORT Timer, IO, Regress, Fmt;

  TYPE wp = RECORD
    who : TEXT ;
    when : INTEGER
  END ;

  CONST max = 14; (* TBD do code generation for constants *)

  TYPE waypoints = ARRAY [1..max] OF wp;

  VAR 
      t1 : PERIODIC FIXED TIMER DELAY 100 ms;
      t2 : PERIODIC CHANGEABLE TIMER; (*By default changeable and oneshot*)
      i,j : INTEGER := 0;
      
      ctr : INTEGER := 1;
    
      actualWaypoints : waypoints;

      expectedWaypoints := waypoints 
      {wp{"start",0 ms},
       
       wp{"act1",100 ms}, wp{"act1",200 ms}, wp{"act1",300 ms},
       wp{"act1",400 ms}, wp{"act1",500 ms}, 
       
       wp{"act2",510 ms}, wp{"act2",520 ms}, wp{"act2",530 ms}, 

       wp{"act1",600 ms}, wp{"act1",700 ms}, wp{"act1",800 ms}, 
       wp{"act1",900 ms}, wp{"act1",1000 ms}
      };

  PROCEDURE setWaypoint (caller : TEXT) =
  BEGIN
    actualWaypoints[ctr] := wp{who := caller, when := Timer.GetElapsed()};
    ctr := ctr + 1;
  END setWaypoint ;

  ACTIVITY act1 () =
    WRITES ctr ;
    READS ctr ;
    WRITES actualWaypoints ;
  BEGIN
    i := i + 1;
    IF i = 5 THEN
      Timer.Change(t2, 10 ms);
      Timer.Start(t2);
      SEND firet1();
      i := 0;
    END;
    setWaypoint("act1");
  END act1;

  ACTIVITY act2 () =
    WRITES ctr ;
    READS ctr ;
    WRITES actualWaypoints ;
  BEGIN
    j := j + 1;
    SEND firet2();
    IF j = 3 THEN
      Timer.Stop(t2);
    END;
    setWaypoint("act2");
  END act2;

  ACTIVITY start() =
    WRITES actualWaypoints ;
  BEGIN
    Regress.init("CapTimer");
    Timer.Start(t1);
    setWaypoint("start");
  END start;

  ACTIVITY summary () = 
     VAR passed : BOOLEAN;
      rec : wp;
  BEGIN 
     (*
     FOR idx := FIRST(actualWaypoints) TO LAST(actualWaypoints) DO
       rec := actualWaypoints[idx];
       IO.Put(rec.who & " : " & Fmt.Int(rec.when) & "\n");
     END;
     *)
     passed := actualWaypoints = expectedWaypoints;
     
     Regress.assertPass(passed);
     Regress.summary();
  END summary ;

CONNECT 
  t1 -> act1;
  t2 -> act2;
BEGIN

END CapTimer.
