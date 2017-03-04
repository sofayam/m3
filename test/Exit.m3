MODULE Exit;
IMPORT Regress, IO;
VAR x := 0;
BEGIN
  Regress.init("Exit");
  FOR i := 1 TO 10 DO 
    x := x + 1;  
    IF i = 3 THEN
      EXIT
    END 
  END;
  Regress.assertPass(x = 3);
  LOOP
    IF x = 6 THEN EXIT END;
    x := x + 1
  END;
  Regress.assertPass(x = 6);
  REPEAT
    x := x - 1; 
  UNTIL x = 4;
  Regress.assertPass(x = 4);
  WHILE x < 9 DO
    x := x + 1
  END;
  Regress.assertPass(x = 9);

  Regress.summary();
    
END Exit.
