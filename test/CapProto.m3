CAPSULE CapProto ;
IMPORT Regress, Proto;

ACTIVITY m1(param : Proto.ParamType) =
BEGIN
   Regress.assertPass(param.b AND param.c = Proto.Color.red)
END m1;
  ACTIVITY init () = 
  BEGIN 
     Regress.init("Protocol Type");
  END init ;
  ACTIVITY summary () = 
  BEGIN 
      Regress.summary();
  END summary ;

BEGIN
END CapProto.
