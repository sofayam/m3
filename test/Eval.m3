MODULE Eval;
IMPORT Regress;
PROCEDURE IncX(VAR x : INTEGER) : INTEGER =
BEGIN
  x := x + 1;
  RETURN x;
END IncX;
VAR x := 1;
BEGIN
  Regress.init("Eval");
  EVAL IncX(x);
  Regress.assertPass(x = 2);
  Regress.summary();
END Eval.
