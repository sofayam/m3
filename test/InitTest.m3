MODULE InitTest;
IMPORT Regress;

VAR
  I := 10;
  F := 10.0;
BEGIN
  Regress.init("Init");
  I := I + 1;
  F := F + 1.0;
  Regress.assertPass(NOT ((I # 11) OR (F > 11.1)));
  Regress.summary();
END InitTest.
