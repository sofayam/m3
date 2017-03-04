MODULE TypeCode;
IMPORT Regress;
IMPORT IO;

TYPE O = OBJECT x : INTEGER END;
TYPE P = O OBJECT x : INTEGER END;
     
VAR o := NEW(O, x := 99);
    p := NEW(P, x := 99);

BEGIN

  Regress.init("TypeCode");
  Regress.assertPass(TYPECODE(o) = TYPECODE(O));

  Regress.assertPass(ISTYPE(o,O));

  Regress.assertPass(NOT ISTYPE(o,P));

  Regress.assertPass(ISTYPE(p,O));

  Regress.assertPass(TYPECODE(o) # TYPECODE(p));
  Regress.summary();

END TypeCode.
