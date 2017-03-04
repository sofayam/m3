CAPSULE CapReply1 ;
IMPORT Timer;
  USECAPSULE CapReply2 ;
  USECAPSULE CapReply3 ;
  VAR sender : CapReply2 ;
  VAR replier : CapReply3 ;
  CONNECT
    p1 <=> sender.p1;
  sender.p2 <=> replier.p1;
BEGIN

END CapReply1.
