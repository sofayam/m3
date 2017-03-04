CAPSULE CapTypeNestChild ;
IMPORT CapTypeNestTypes;
IMPORT Regress;
  ACTIVITY mess(rec : CapTypeNestTypes.r) =
  BEGIN
     Regress.assertPass(TRUE)
  END mess;
  ACTIVITY setup () = 
  BEGIN 
     Regress.init("Types in Nested Capsules");
  END setup ;
  ACTIVITY summary () = 
  BEGIN 
     Regress.summary()
  END summary ;
BEGIN
 
END CapTypeNestChild.
