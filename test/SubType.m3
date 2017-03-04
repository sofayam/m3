MODULE SubType;
IMPORT Regress;
IMPORT EnumInt;
TYPE 
  enum = {a, b, c, d};
  shortie = [10 .. 20];
  enumsub = [enum.b .. enum.c];
  enumsubtricky = [EnumInt.intenum.w .. EnumInt.intenum.y];
  enumsubsupertricky = [EnumInt.intx .. EnumInt.inty];
CONST
  cenumb = enum.b;
  cenumsubb = enumsub.b;
  cenumsubtx = enumsubtricky.x;
  cenumsubstx = enumsubsupertricky.x;
VAR 
  s1, s2, s3 : shortie;
  es1, es2 : enumsub;
  est1, est2 : enumsubtricky;
  esst1, esst2 : enumsubsupertricky;
BEGIN
  Regress.init("SubType");
  s1 := 11;
  s2 := 12;
  s3 := s1 * s2 DIV 10;
(*  es1 := enum.a; *)
  es1 := enumsub.b;
  (* TBD This test will only start making sense when we have exception handlers - numerics are shakey too !!!*)
  Regress.assertPass(s3 = 13);
  Regress.assertPass(es1 = enum.b);
  Regress.assertPass(cenumb = cenumsubb);
  Regress.assertPass(cenumsubtx = cenumsubstx);
 (* esst1 := enum.b; *)
  Regress.summary();
END SubType.
