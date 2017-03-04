MODULE ForEach;
IMPORT Regress;

VAR intArray := ARRAY OF INTEGER{1,2,3,4};
    intList := LIST OF INTEGER{1,2,3,4};
    ctr := 0;
BEGIN
  Regress.init("ForEach");
  FOREACH i IN intArray DO
    ctr := ctr + i
  END;
  Regress.assertPass(ctr = 10);
  ctr := 0;
  FOREACH i IN intList DO
    ctr := ctr + i
  END;
  Regress.assertPass(ctr = 10);
  Regress.summary()
END ForEach.
