MODULE Dispose;
IMPORT Regress;
TYPE O = OBJECT x : INTEGER END;

VAR o := NEW(O, x := 1);

BEGIN
  Regress.init("Dispose");

  DISPOSE(o);
  Regress.assertPass(o = NIL);

  Regress.summary();

END Dispose.
