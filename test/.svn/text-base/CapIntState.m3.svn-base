CAPSULE CapIntState ;
  IMPORT Regress,IO;
  USECAPSULE CapIntStateSub ;
  VAR trace : TEXT := "";
  STATE s1
    ON t1() =
      BEGIN
      trace := trace & "1";
      NEXT s2;
      END t1;
  START = BEGIN
    NEXT s1
  END;
  STATE s2
    ON t1() =
      BEGIN
      trace := trace & "2";
      NEXT s1;
      END t1;
  VAR capIntStateSub : CapIntStateSub ;
  ACTIVITY start () =
  BEGIN 
    SEND capIntStateSub.windup();
    Regress.init("InternalState");
  END start ;
  ACTIVITY summary () = 
  BEGIN
     Regress.assertPass(trace = "12121");
     Regress.summary();
  END summary ;
 
  CONNECT 
     capIntStateSub.alarm -> t1;
BEGIN
END CapIntState.
