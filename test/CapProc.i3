CAPSULE INTERFACE CapProc;
PORT p1 : PROTOCOL
   INCOMING MESSAGE ask(x:INTEGER);
   OUTGOING MESSAGE answer(x:INTEGER);
    INCOMING MESSAGE summary() ;
 
END;
END CapProc.
