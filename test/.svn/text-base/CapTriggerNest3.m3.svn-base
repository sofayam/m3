CAPSULE CapTriggerNest3 ;
  TRIGGER t ON loc = 100 ;
  VAR loc : INTEGER := 99 ;
  ACTIVITY startInner () = 
  BEGIN 
    loc := 100;
  END startInner ;
  CONNECT
    t -> reply;
BEGIN

END CapTriggerNest3.
