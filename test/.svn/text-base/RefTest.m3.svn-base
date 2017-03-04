MODULE RefTest;
IMPORT Regress, IO;

TYPE 
  ri = REF INTEGER ;
  rec = RECORD
    i : INTEGER ; 
  END;
  refInRec = RECORD
    i : REF INTEGER ; 
  END;
  ra = REF ARRAY [1..4] OF BOOLEAN;
  refRec = REF rec ;
  refToRefInRec = REF refInRec ;
VAR 
  r1, r2 : ri ;
  r3, r4 : refRec ;
  r5 : refToRefInRec ;
  r6 := NEW(ra);
  i : INTEGER ; 
PROCEDURE BoolText(b : BOOLEAN) : TEXT =
  BEGIN
    IF b THEN
      RETURN "TRUE"
    ELSE
      RETURN "FALSE"
    END
  END BoolText ;
BEGIN
  Regress.init("Ref");
  r1 := NEW(ri);
  r2 := r1;
  r1^ := 99;
  Regress.assertPass(r2^ = 99);

  r3 := NEW(refRec);
  r4 := r3;
  r3^.i := 101;

  Regress.assertPass(r4.i = 101);
  (*  IO.PutInt(r3^.i); *)
  
  r5 := NEW(refToRefInRec);
  r5^.i := NEW(REF INTEGER);  
  r5^.i^ := 999 ;
  i := r5.i^;
  Regress.assertPass(i = 999);
  r6[1] := FALSE;
  FOR i := 2 TO 4 DO
    r6[i] := NOT r6[i-1];
  END;
  Regress.assertPass(r6[4] = TRUE);
(*  r6[10] := FALSE;
  r6 := NIL;
  r6[1] := FALSE;  
TBD do some tests to catch nullpointer exceptions here eventually *)
  Regress.summary();
END RefTest.
