MODULE ComplExp;
IMPORT IO, Regress;
TYPE 
  enum = {a,b,c};
  rec = RECORD
    e : enum;
  END;
  arr = ARRAY [1..3] OF rec;
VAR
  a : arr;
  e : enum;
  i : INTEGER;
BEGIN
  Regress.init("ComplExp");
  e := enum.a;
  i := 1;
  a[1].e := e;
  Regress.assertPass(a[i].e = enum.a);
  Regress.summary();
END ComplExp.
