CAPSULE INTERFACE CapSwapper ;
PORT p1 : PROTOCOL
   INCOMING MESSAGE ask(expected : TEXT) ;
   INCOMING MESSAGE init(testName : TEXT) ;
   INCOMING MESSAGE summary() ;
END;
END CapSwapper.
