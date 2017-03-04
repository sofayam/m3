CAPSULE CapAgrKid1 ;
IMPORT Regress;
  VAR finished : BOOLEAN;
  ACTIVITY start () = 
  BEGIN 
    Regress.init("Protocol Aggregation");
    SEND p1.startMsg();
    (* miss out p1 here and you will get an error *) 
  END start ;
  ACTIVITY end () = 
  BEGIN 
    finished := TRUE;
  END end ;
  ACTIVITY summary() =
  BEGIN
     Regress.assertPass(finished);
     Regress.summary()
  END summary;
  CONNECT
    p2.endMsg -> end;
BEGIN

END CapAgrKid1.
