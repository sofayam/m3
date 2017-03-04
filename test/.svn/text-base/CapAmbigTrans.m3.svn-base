CAPSULE CapAmbigTrans IMPLEMENTS CapAmbig ;
IMPORT Regress;
  VAR first := TRUE;
  
  ACTIVITY start () = 
  BEGIN 
     Regress.init("Ambiguous Ports for Transitions");
  END start ;
  ACTIVITY summary () = 
  BEGIN 
     Regress.summary();
  END summary ;
  STATE s1
    ON p1t() =
      BEGIN
        Regress.assertPass(first);
        first := NOT first;
        NEXT s2;
      END p1t;
  START = BEGIN
    NEXT s1
  END;
  STATE s2
    ON p2t() =
      BEGIN
        Regress.assertPass(NOT first);
        NEXT s1;
      END p2t;
  CONNECT
      p1.a -> p1t;
      p2.a -> p2t;

BEGIN


END CapAmbigTrans.
