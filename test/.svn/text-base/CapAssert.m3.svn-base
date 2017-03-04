CAPSULE CapAssert ;
IMPORT Regress, Results;
  ACTIVITY start () = 
  VAR caught := FALSE;
  BEGIN 
     Regress.init("Assertions");
     Results.WriteProtocol("Started Assertions Test Program");
     TRY
       ASSERT FALSE OR
          NOT
              TRUE;
     EXCEPT 
     | AssertError =>
       caught := TRUE;
     END; 
     Regress.assertPass(caught);
     Regress.summary()
  END start ;
BEGIN

END CapAssert.
