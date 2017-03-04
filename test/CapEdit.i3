CAPSULE INTERFACE CapEdit;
  PORT p1 : PROTOCOL
    INCOMING MESSAGE ping();
             MESSAGE pong();
    OUTGOING MESSAGE outerreply();
    INCOMING MESSAGE foo();
    INCOMING MESSAGE foo1();
    INCOMING MESSAGE act23();
    INCOMING MESSAGE bababoom();
    INCOMING MESSAGE b1();
    INCOMING MESSAGE fff();
    INCOMING MESSAGE ff();
    INCOMING MESSAGE aaa();
    INCOMING MESSAGE foofoo();
    INCOMING MESSAGE f12() ;
    INCOMING MESSAGE f13() ;
    INCOMING MESSAGE sssss() ;
  END;
END CapEdit.