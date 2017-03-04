MODULE ExprTest;
IMPORT Regress, IO;
TYPE
  enum = {a,b,c};
VAR
  I := 2;
  J : INTEGER;
  B : BOOLEAN;
  e : enum;
  
BEGIN
  Regress.init("Expr");
  J := I * (2 + 1);
  Regress.assertPass(J = 6);
  J := J + J + J;
  Regress.assertPass(J = 18);
  J := - J;
  Regress.assertPass(J = -18);
  B := J = I;
  Regress.assertPass(NOT B);
  B := J < I;
  Regress.assertPass(B);
  B := J > I;
  Regress.assertPass(NOT B);
 
  Regress.assertPass(NOT (10 = 9));

  Regress.assertPass(NOT (10 # 10));

  Regress.assertPass(NOT (10 < 9));

  Regress.assertPass(NOT (10 <= 9));

  Regress.assertPass(NOT (9 >= 10));

  Regress.assertPass(NOT (3 > 9));

  Regress.assertPass((3 > 9) OR (10 = 10 AND 9 > 8));
  Regress.summary();

END ExprTest.
