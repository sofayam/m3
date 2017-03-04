CAPSULE CapCmdReset ;
IMPORT Regress;
 
  ACTIVITY neverhappens () = 
  BEGIN 
     Regress.assertPass(FALSE)
  END neverhappens ;

  ACTIVITY failCmdDeep () = 
  BEGIN 
     SEND neverhappens();
     RESET ;
  END failCmdDeep ;
  ACTIVITY failCmdShallow () = 
  BEGIN 
     SEND neverhappens();
     RESET 1;
  END failCmdShallow ;
BEGIN
END CapCmdReset.
