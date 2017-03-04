MODULE ObjectFields;
IMPORT IO, Regress;
TYPE 
  O = 
   OBJECT 
    i : INTEGER := 1; 
    j : INTEGER := 77 
  END;
  P = 
   O OBJECT 
    j : INTEGER := 99 
  END;
VAR 
  o, osave : O;
  p : P;
  caught := FALSE;
BEGIN
  Regress.init("ObjectFields");
  (* Base Object with no Inheritance *)
  o := NEW(O);
  Regress.assertPass(o.i = 1);
  o.i := 101;
  Regress.assertPass(o.i = 101);
  (* Inheritance *)
  p := NEW(P);
  Regress.assertPass(p.i = 1);
  p.i := 101;
  Regress.assertPass(p.i = 101);
  (* Base Object with no Inheritance *)
  Regress.assertPass(p.j = 99);
  p.j := 909;
  Regress.assertPass(p.j = 909);

  (* Implicit Narrow leads to visibility of masked j *)
  osave := o;
  o := p;
  Regress.assertPass(o.j = 77);

  o.j := 707;
  p := o;
  Regress.assertPass(p.j = 909);

  TRY
    (* Explicit narrow is unnecessary here but test it anyway *)
    p := NARROW(osave,P);
  EXCEPT
    | ConstraintError => caught := TRUE;
  END;
  Regress.assertPass(caught);
  Regress.summary();

END ObjectFields.
