MODULE Exception;
IMPORT Regress, IO;
EXCEPTION Error;
VAR
  caught := FALSE;
  const := FALSE;
  n := 0;
  smallint : [1..10] ;
BEGIN
  Regress.init("Exception");
  TRY
    RAISE Error;
  EXCEPT
  | Error =>
    caught := TRUE;
  END;
  Regress.assertPass(caught);

  caught := FALSE;
  TRY
    n := 1 DIV 0;
  EXCEPT
  | DivideByZeroError =>
    caught := TRUE;
  END;
  Regress.assertPass(caught);

  caught := FALSE;
  TRY
    TYPE enum = {red, blue, green, yellow};
    VAR e : [enum.blue .. enum.yellow];
    BEGIN
      e := enum.red;
    END;
  EXCEPT
    | ConstraintError =>
      caught := TRUE
  END;
  Regress.assertPass(caught);

  caught := FALSE;
  TRY
    VAR smallint : [1..10];
    BEGIN
      smallint := 11;
    END;
  EXCEPT
    | ConstraintError =>
      caught := TRUE
  END;
  Regress.assertPass(caught);

  caught := FALSE;
  TRY
    VAR ref : REF INTEGER;
    BEGIN
      ref^ := 0;
    END;
  EXCEPT
    | NullPointerError =>
      caught := TRUE
  END;
  Regress.assertPass(caught);


  Regress.summary();
END Exception.
