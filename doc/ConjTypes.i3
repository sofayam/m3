INTERFACE ConjTypes ;

TYPE aInbOut = PROTOCOL
  INCOMING MESSAGE a ();
  OUTGOING MESSAGE b ();
END;

TYPE aOutbIn = ~ aInbOut;

END ConjTypes.
