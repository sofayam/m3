CAPSULE CapPar ;
IMPORT Timer;
  USECAPSULE CapParChild1 ;
  USECAPSULE CapParChild2 ;
  VAR child1 : CapParChild1 ;
  VAR child2 : CapParChild2 ;
  CONNECT
    p1 <=> child1.p1;
    p1 <=> child2.p1;
BEGIN

END CapPar.
