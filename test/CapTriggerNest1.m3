CAPSULE CapTriggerNest1 ;
IMPORT Regress;
  USECAPSULE CapTriggerNest2 ;
  VAR tn2 : CapTriggerNest2 ;
      loc : INTEGER := 0;
      cameBack : INTEGER := 0;
  TRIGGER t ON loc = 1;
  ACTIVITY start () = 
  BEGIN 
    Regress.init("TriggerNest");
    loc := 1
  END start ;
  ACTIVITY comingBack () = 
  BEGIN 
    cameBack := cameBack + 1;
    SEND outerreply();
  END comingBack ;
  ACTIVITY summary () =
     VAR res : BOOLEAN; 
  BEGIN 
     res := cameBack = 1;
     Regress.assertPass(res);
     Regress.summary();
  END summary ;

  CONNECT
    t -> tn2.startInner;
    tn2.reply -> comingBack;
   

BEGIN

END CapTriggerNest1.
