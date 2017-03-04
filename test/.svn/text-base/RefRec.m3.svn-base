MODULE RefRec;
IMPORT Regress;
TYPE
  recref = REF RECORD 
    i : INTEGER;
    j : INTEGER := 99;
    b : BOOLEAN ;
  END;
VAR
  recref1 := NEW(recref, i := 88, b := TRUE);
  recref2 := NEW(recref, b := FALSE);
BEGIN
  Regress.init("RefRec");
  Regress.assertPass(recref1.i = 88);
  Regress.assertPass(recref2.j = 99);
  Regress.assertPass(NOT recref2.b);
  Regress.summary();
END RefRec.
