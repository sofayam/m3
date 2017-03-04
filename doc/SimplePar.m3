CAPSULE SimplePar ;
  ACTIVITY getBusy () = 
  BEGIN 
     complex1();
     SEND delegate() AFTER 5 s;
     complex2()
  END getBusy AFTER 10 s;
  PROCEDURE complex1 () = 
  BEGIN 
  END complex1 ;
  PROCEDURE complex2 () = 
  BEGIN 
  END complex2 ;
BEGIN
END SimplePar.
