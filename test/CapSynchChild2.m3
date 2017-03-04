CAPSULE CapSynchChild2 ;
IMPORT Regress;

  VAR ctr : INTEGER := 0;

  ACTIVITY aCheck (i : INTEGER) = 
  BEGIN 
     Regress.assertPass(i = ctr);
     ctr := ctr + 1;
  END aCheck ;

  PROCEDURE sCheck(i : INTEGER) =
  BEGIN
     Regress.assertPass(i = ctr);
     ctr := ctr + 1;
  END sCheck;

  PROCEDURE varCheck(VAR i : INTEGER) =
  BEGIN
     i := ctr;
  END varCheck;

BEGIN

END CapSynchChild2.
