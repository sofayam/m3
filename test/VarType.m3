(*
  This is meaningless as it stands - and serves only as a reminder that there 
  should be a different category of test: semantic errors detected at compile
  time: TBD how should this be tested
  1) Programmatic interface to compiler to listen for syntax errors
  2) grep results (ugh)
*)

MODULE VarType;
IMPORT Regress;
TYPE 
  R = RECORD
    I : INTEGER;
  END;
VAR
  I : INTEGER;
  J : INTEGER; (* This should only be a type and not a variable *)
BEGIN
  Regress.init("VarType");
  I := 1;
  J := 2;
  Regress.assertPass(I+J = 3);
  Regress.summary();
END VarType.
