MODULE TryFinally ;
IMPORT Regress;
EXCEPTION hell;

PROCEDURE hellRaiser (doit : BOOLEAN)  RAISES {hell} =
BEGIN
  IF doit THEN
    RAISE hell;
  END
END hellRaiser; 

VAR 
  caught := FALSE;
  finalRan := FALSE;

BEGIN

  Regress.init("TryFinally");

  TRY
    TRY
      hellRaiser(TRUE);
    FINALLY
      finalRan := TRUE;
    END
  EXCEPT
    | hell => caught := TRUE; 
  END;

  Regress.assertPass(finalRan AND caught);

  caught := FALSE;
  finalRan := FALSE;
  
  TRY
    TRY
      hellRaiser(FALSE);
    FINALLY
      finalRan := TRUE;
    END
  EXCEPT
    | hell => caught := TRUE; 
  END;

  Regress.assertPass(finalRan AND NOT caught);

  Regress.summary()

END TryFinally.
