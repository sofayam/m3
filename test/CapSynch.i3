CAPSULE INTERFACE CapSynch ;
PORT p1 : PROTOCOL
   INCOMING MESSAGE asyn1() ;
   INCOMING MESSAGE asyn2() ;
   INCOMING MESSAGE varCheck();
   INCOMING MESSAGE init() ;
   INCOMING MESSAGE summary() ;
END;
END CapSynch.