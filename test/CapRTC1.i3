CAPSULE INTERFACE CapRTC1 ;
PORT p1 : PROTOCOL
    INCOMING MESSAGE a21();
    INCOMING MESSAGE setup() ;
    INCOMING MESSAGE summary() 
END;
END CapRTC1.
