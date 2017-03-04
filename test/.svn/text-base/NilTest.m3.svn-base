MODULE NilTest;
IMPORT Regress;
TYPE iref = REF INTEGER;
VAR irefvar : iref;
    b : BOOLEAN;
    i : INTEGER;
    caught := FALSE;
BEGIN
  Regress.init("NilTest");
  Regress.assertPass(irefvar = NIL);
  TRY
    irefvar^ := 1;
  EXCEPT
  | NullPointerError => 
    caught := TRUE
  END;
  Regress.assertPass(caught);
  irefvar := NEW(iref);
  Regress.assertPass(irefvar # NIL);
  irefvar^ := 1;
  i := irefvar^; 
  Regress.assertPass(irefvar^ = i);
  Regress.summary();
END NilTest.
