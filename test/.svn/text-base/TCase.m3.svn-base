MODULE TCase;
IMPORT Fmt, IO, Regress, Text;
TYPE 
  iref = REF INTEGER;
  rref = REF RECORD
    x : INTEGER;
  END;
  O = OBJECT
    x : INTEGER := 99;
  END;
  P = O OBJECT END ;
    
VAR
  ir := NEW (iref);
  rr := NEW (rref, x := 99);
  o := NEW(O);
  p := NEW(P);

PROCEDURE tellMe(ref : REFANY) : TEXT =
  VAR res : TEXT;
BEGIN
  TYPECASE ref OF 
  | NULL => res := "NULL";
(*  | P, O => res := "blalbl"; *)
  | P (p) => res := "P";
  | O (o) => res := "O" & Fmt.Int(o.x); 
  | iref (ir) => res := "iref";
  | rref (rr) => res := "rref";
    ELSE
      res := "other";
  END;
  RETURN res
END tellMe;

BEGIN
  Regress.init("TCase");
  Regress.assertPass(Text.Equal(tellMe(NIL),"NULL"));
  Regress.assertPass(Text.Equal(tellMe(p), "P"));
  Regress.assertPass(Text.Equal(tellMe(o), "O99"));
  Regress.assertPass(Text.Equal(tellMe(ir), "iref"));
  Regress.assertPass(Text.Equal(tellMe(rr), "rref"));
  Regress.summary()


END TCase.
