CAPSULE CapSwapper ;
IMPORT Timer;
IMPORT Regress;
  USECAPSULE CapStandard ;
  VAR kid : CapStandard ;
      expectedReply : TEXT;
  ACTIVITY handleReply (t : TEXT) = 
  BEGIN 
     Regress.assertPass(t = expectedReply);
     
  END handleReply ;
  ACTIVITY init (testName : TEXT) = 
  BEGIN 
     Regress.init(testName);
  END init ;
  ACTIVITY summary () = 
  BEGIN 
      Regress.summary();
  END summary ;
  ACTIVITY ask(expected : TEXT) =
  BEGIN
      expectedReply := expected;
      SEND kid.ask()
  END ask;
  CONNECT
    kid.reply -> handleReply;
BEGIN

END CapSwapper.
