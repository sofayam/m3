MODULE AlgolNasty;
(* Nasty Algol-scope traps - TBD make these even nastier *)
IMPORT Regress;
PROCEDURE foo(r : rec) : INTEGER= 
BEGIN
  RETURN r.x
END foo;

TYPE 
  rec = RECORD
    x : INTEGER;
  END;
  st = [1..LAST(arr)];
VAR
  a := c;

CONST 
  c = 7;
TYPE
  arr = ARRAY[1..c] OF INTEGER ;
VAR 
  s := arr{1,2,3,4,5,6,7};
  passed := TRUE;
BEGIN
  Regress.init("AlgolNasty");
  a := foo(rec{x:=1});
  
  FOR i := 1 TO LAST(st) DO
    passed := passed AND s[i] = i
  END;
  Regress.assertPass(passed);
  Regress.summary()
END AlgolNasty.
