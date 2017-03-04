CAPSULE CapReply2 ;
IMPORT CapReplyTypes;
IMPORT Timer;
  ACTIVITY start () = 
  BEGIN 
     SEND ask(p3);
  END start ;
  ACTIVITY signalSuccess (i : INTEGER) = 
  BEGIN 
     SEND success(); 
  END signalSuccess ;
  CONNECT
    p3.callMe -> signalSuccess;
BEGIN

END CapReply2.
