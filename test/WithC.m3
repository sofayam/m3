(* Changed to reflect C Code Gen inability to deal with bindings to r-values *)
MODULE WithC;
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
intarr = ARRAY[1..3] OF INTEGER;
VAR
  r1 := rec1{f := rec2{f := 99}};
  res : INTEGER;
  ca := colarr{color.red, color.blue, color.green};
  ia := intarr{2,3,4};
BEGIN
  Regress.init("WithSt");
  WITH x = r1.f.f DO
    x := 101;
  END;
  Regress.assertPass(r1.f.f = 101);
  WITH a = ia[1], b = ia[2], c = ia[3] DO
    res := (b*c) DIV a
  END;
  Regress.assertPass(res = 6);
  WITH c1 = ca[color.red], c2 = ca[c1] DO
    Regress.assertPass(c1 = c2);
  END;

  Regress.summary()
END WithC.
