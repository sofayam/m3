MODULE IfTest;
IMPORT Regress;
VAR 
  A, B := 1;
  C := 2;

BEGIN
  Regress.init("If");
  IF A = B
   THEN
    Regress.assertPass(A = B)
  ELSE
    Regress.assertPass(A # B)
  END;
  IF A = C 
   THEN
    Regress.assertPass(A = C)
  ELSIF C = B 
   THEN
    Regress.assertPass(B # C)
  ELSE
    Regress.assertPass(A # C)
  END;
  Regress.summary();
END IfTest.
