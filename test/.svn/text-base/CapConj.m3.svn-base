CAPSULE CapConj ;
IMPORT Regress;

  USECAPSULE CapConjKid1 ;
  USECAPSULE CapConjKid2 ;
  VAR c1 : CapConjKid1 ;
  VAR c2 : CapConjKid2 ;
      bOut, aOut := FALSE;
  ACTIVITY init () = 
  BEGIN 
    Regress.init("Protocol Conjugation");
  END init ;
  ACTIVITY summary () = 
  BEGIN 
    Regress.assertPass(bOut AND aOut);
    Regress.summary()
  END summary ;
  ACTIVITY checkA () = 
  BEGIN 
    aOut := TRUE;
    SEND p2.a();
  END checkA ;
  ACTIVITY checkB () = 
  BEGIN 
    bOut := TRUE;
    SEND p1.b()
  END checkB ;
  CONNECT
    c1.p2 <=> c2.p1;
    p1.a -> c1.p1.a;
    p2.b -> c2.p2.b;
    c2.p2.a -> checkA;
    c1.p1.b -> checkB;
BEGIN

END CapConj.
