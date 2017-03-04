MODULE StackUser;
IMPORT IntStack, Regress, IO, Fmt;
VAR 
  t : IntStack.T;
  success := TRUE;
  tmp : INTEGER;
CONST
  limit = 10;
BEGIN

  Regress.init("Generic");
  t := IntStack.Create();
  FOR i := 1 TO limit DO
    (* IO.Put("Calling Push " & Fmt.Int(i) & "\n");*)
    IntStack.Push(t,i)
  END;
  FOR i := limit TO 1 BY -1 DO
    (*IO.Put("Calling Pop " & Fmt.Int(i) & "\n");*)
    tmp := IntStack.Pop(t);
    success := success AND (tmp = i)
  END; 

  Regress.assertPass(success);
  Regress.summary();

END StackUser.
