CAPSULE CapReply3 ;
IMPORT CapReplyTypes;
IMPORT Timer;
  ACTIVITY replier (returnAddress : CapReplyTypes.callingBack) = 
  BEGIN 
     REPLY returnAddress.callMe(99);
  END replier ;
  CONNECT
    p1.ask -> replier;
BEGIN

END CapReply3.
