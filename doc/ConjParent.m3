CAPSULE ConjParent ;
IMPORT Timer;
  USECAPSULE ConjC1 ;
  USECAPSULE ConjC2 ;
  VAR c1 : ConjC1 ;
  VAR c2 : ConjC2 ;
  CONNECT
    c2.p1 <=> c1.p1;
BEGIN

END ConjParent.
