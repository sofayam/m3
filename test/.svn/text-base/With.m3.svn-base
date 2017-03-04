MODULE With;
IMPORT Regress;
TYPE
rec2 = RECORD
  f : INTEGER;
END;
rec1 = RECORD
  f : rec2;
END;
color = {red, blue, green};
colarr = ARRAY color OF color;

VAR
  r1 := rec1{f := rec2{f := 99}};
  res : INTEGER;
  ca := colarr{color.red, color.blue, color.green};

BEGIN
  Regress.init("WithSt");
  WITH x = r1.f.f DO
    x := 101;
  END;
  Regress.assertPass(r1.f.f = 101);
  WITH a = 2, b = 3, c = 4 DO
    res := (b*c) DIV a
  END;
  Regress.assertPass(res = 6);
  WITH c1 = ca[color.red], c2 = ca[c1] DO
    Regress.assertPass(c1 = c2);
  END;

  Regress.summary()
END With.
