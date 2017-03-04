MODULE ArrayCTest;
IMPORT Regress;
TYPE a10 = ARRAY [1..10] OF INTEGER;

VAR a10v : a10;

PROCEDURE suma10(param : a10) : INTEGER =
  VAR sum := 0;
BEGIN
  FOR i := 1 TO 10 DO
    sum := sum + param[i];
  END;
  RETURN sum;
END;

BEGIN
  Regress.init("ArrayC");
  a10v := a10{1,2,3,..};
  Regress.assertPass(suma10(a10v)=27);
  Regress.summary()
END ArrayCTest.
