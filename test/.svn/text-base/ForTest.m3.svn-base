MODULE ForTest;
(* IMPORT IO; *)
IMPORT Regress;
VAR accum : INTEGER;
BEGIN
  Regress.init("For");
  accum := 0;
  FOR I := 1 TO 10 BY 2
   DO
    accum := accum + I;
    (* IO.PutInt(I); *) 
    FOR I := 100 TO 103 DO
      (*IO.PutInt(I); *)
      accum := accum + I;
      (*IO.PutInt(accum);*)
   END;
  END;
  (*IO.PutInt(accum);*)
  Regress.assertPass(accum = 2055);
  Regress.summary();
END ForTest.
