CAPSULE INTERFACE CapTrigger;
PORT p1 : PROTOCOL
   OUTGOING MESSAGE firet1();
            MESSAGE firet2();
    INCOMING MESSAGE setup() ;
             MESSAGE act1() ;
             MESSAGE summary() ;
END;
END CapTrigger.
