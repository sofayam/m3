MODULE RecNasty;
IMPORT Regress;
TYPE

  R2 = RECORD
    back : REF R3;
    r3 : R3 := R3{f1 := 99} (* ultra-nasty *)
  END;

  R3 = RECORD
    f1 : INTEGER;
  END;

  R1 = RECORD 
    f1 : INTEGER;
    (*f2 : R2 := R2{}*)
    f3 : REF R1;
    f4 : R3 := R3{f1 := 33};
  END;

VAR
  r3 := R3{f1 := 44};
  r1 := R1{f1 := 99, f3 := NIL};
  r2 := R2{};

BEGIN
  Regress.init("RecNasty");
  Regress.assertPass(r3.f1 = 44);
  r2.back := NEW(REF R3, f1 := 101);
  Regress.assertPass(r2.back.f1 = 101);
  Regress.summary()
END RecNasty.
