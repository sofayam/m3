MODULE ExcModUser;
IMPORT Regress, ExcMod;
VAR caught := FALSE;
EXCEPTION shouldntHappen;
BEGIN

  (* TBD test cases involving unhandled exceptions are not in the regression suite yet *)
  (* How would we regress test for them anyway ??? *)

  Regress.init("ExcModUser");
  TRY 
   ExcMod.raiseIt(ExcMod.exceptions.hell); 
  EXCEPT
  | ExcMod.hell =>
    caught := TRUE
  END;
  Regress.assertPass(caught);

  caught := FALSE;
  TRY 
   ExcMod.raiseIt(ExcMod.exceptions.cain);
  EXCEPT
  | ExcMod.cain =>
    caught := TRUE
  | ExcMod.hell =>
    caught := TRUE
  END;
  Regress.assertPass(caught);

  caught := FALSE;
  TRY 
   ExcMod.raiseIt(ExcMod.exceptions.cain);
  EXCEPT
  | ExcMod.hell =>
    RAISE shouldntHappen;
  ELSE
    caught := TRUE
  END;
  Regress.assertPass(caught);

  TRY
    ExcMod.raiseiPack(88)
  EXCEPT
  | ExcMod.iPackage (contents) =>
    Regress.assertPass(contents = 88);
  END; 

  TRY
    ExcMod.raiserPack(99)
  EXCEPT
  | ExcMod.rPackage (contents) =>
    Regress.assertPass(contents.x = 99);
  END; 
  Regress.summary();

END ExcModUser.
