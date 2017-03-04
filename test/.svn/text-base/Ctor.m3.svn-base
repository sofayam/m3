MODULE Ctor;
IMPORT Regress;
TYPE 
  rec1 = RECORD
    i : INTEGER := 99;
  END;
  rec2 = RECORD
    r : rec1 := rec1{};
  END;

VAR
  r1 : rec1 := rec1{i := 1};
  r2 : rec2 := rec2{r := rec1{i := 2}};
  r3 : rec2 ;
BEGIN
  Regress.init("Ctor");
  Regress.assertPass(r3.r.i = 99);
  Regress.summary();
END Ctor.
