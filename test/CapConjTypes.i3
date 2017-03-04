INTERFACE CapConjTypes ;

TYPE aInbOut = PROTOCOL
  INCOMING MESSAGE a ();
  OUTGOING MESSAGE b ();
END;

TYPE aOutbIn = ~ aInbOut;

END CapConjTypes.
