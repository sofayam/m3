MODULE AnonTest;
IMPORT IO, Regress;
TYPE
  enum = {a,b,c,d};
  arr1 = ARRAY [1..10] OF [1..10]; 
  arr2 = ARRAY [1..10] OF [enum.a .. enum.b]; 
  rec = RECORD 
    i : [1..10] := 1;
    a : ARRAY [1..5] OF [enum.a .. enum.b]; 
  END;
VAR 
  r : rec ;
  i1 : [1..10];
  r1 : RECORD i : [1..10]; END;

BEGIN
  Regress.init("Anon");
  r.i := 1;
  r.a[3] := enum.b;
(*  IO.PutInt(r.i); *)
  i1 := 4;
  r1.i := 4;
  Regress.assertPass(i1 = r1.i);
  Regress.summary();
END AnonTest.
