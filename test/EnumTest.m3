MODULE EnumTest;
IMPORT IO, Regress;
TYPE
  enum1 = {a,b,c};
  enum2 = [enum1.a .. enum1.b];
VAR
  e1,e2 : enum1;
  e4 := enum1.c;
  e5 : enum2 := enum1.b;
CONST
  e3 = enum1.c;
BEGIN
  Regress.init("Enum");
  e1 := enum1.b;
  e2 := enum1.a;
  Regress.assertPass(e1 # e2);
  e2 := e1;
  Regress.assertPass(e1 = e2);
  Regress.assertPass(e3 = e4);
  Regress.summary();
END EnumTest.
