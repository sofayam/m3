MODULE RecTest;
IMPORT Regress, IO; 
IMPORT RecInt;
TYPE rec = RECORD
  i1 : INTEGER := 99;
  f1 : REAL;
END;
VAR r := rec{f1 := 1.0};
    rcopy : rec;
    r1 : RecInt.rec1;
    r2 : RecInt.rec3;
  
BEGIN
  Regress.init("Rec");
  r := rec{f1:= 2.9};
  Regress.assertPass(r.i1 = 99);
  r := rec{10,f1:= 2.9};
  rcopy := r;
  r.i1 := 999;
 (* IO.PutInt(r.i1);
  IO.PutInt(rcopy.i1);*)
  Regress.assertPass(r.i1 = 999 AND rcopy.i1 = 10);


  r1.a2 := r.i1;
  Regress.assertPass(r1.a2 = 999);

  r2.r1.f1 := 1.01;
  r.f1 := r2.r1.f1;
  Regress.assertPass((r.f1 > 1.0) AND (r.f1 < 1.02));
  Regress.summary();
END RecTest.
