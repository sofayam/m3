CAPSULE CapAmbig ;
IMPORT Regress;
  VAR first := TRUE;
  ACTIVITY p1a () = 
  BEGIN 
     Regress.assertPass(first);
     first := NOT first;
  END p1a ;
  ACTIVITY p2a () = 
  BEGIN 
     Regress.assertPass(NOT first);
  END p2a ;
  ACTIVITY start () = 
  BEGIN 
     Regress.init("Ambiguous Ports");
  END start ;
  ACTIVITY summary () = 
  BEGIN 
     Regress.summary();
  END summary ;
  CONNECT
      p1.a -> p1a;
      p2.a -> p2a;

BEGIN


END CapAmbig.
