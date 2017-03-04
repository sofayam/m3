CAPSULE CapAgrKid2 ;
IMPORT Timer;
  ACTIVITY start () =
  BEGIN 
    SEND p2.endMsg()
  END start ;
  CONNECT
    p1.startMsg -> start;
BEGIN

END CapAgrKid2.
