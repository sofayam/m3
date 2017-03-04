INTERFACE CapReplyTypes;

  TYPE callingBack = PROTOCOL
    INCOMING MESSAGE callMe (i : INTEGER);
  END ;

  TYPE askForCallBack = PROTOCOL 
    OUTGOING MESSAGE ask (returnAddress : callingBack);
  END ;

  TYPE testProto =  PROTOCOL
    INCOMING MESSAGE start() ;
    OUTGOING MESSAGE success() ;
  END;

END CapReplyTypes.
