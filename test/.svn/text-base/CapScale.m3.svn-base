CAPSULE CapScale ;
IMPORT ScaleTypes AS ST;
IMPORT Regress;

  ACTIVITY set (v : ST.Volts; t : ST.Time) = 
  BEGIN 
    Regress.init("Scaled Inputs and Outputs");
    volts := v;
    time := t;
    SEND scaleOut(2 seconds * v , t );
    SEND scaleOut(v := v - 1 mV, t := t - 1 seconds); (* TBD cannot test this yet *)
    SEND scaleOut(v := 2 seconds * v * 1 seconds , t := t - 1 seconds); (* TBD cannot test this yet *)
  END set ;
  ACTIVITY expect (v : INTEGER; t : INTEGER) = 
  BEGIN 
    Regress.assertPass(v = volts AND t = time);
    Regress.summary()
  END expect ;
  VAR volts : INTEGER ;
  VAR time : INTEGER ;


BEGIN

END CapScale.
