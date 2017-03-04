CAPSULE INTERFACE CapDataport ;
IMPORT CapDataPortTypes AS CDT;


PORT p1 : PROTOCOL
   INCOMING MESSAGE expectx(ex : INTEGER) ;
   INCOMING MESSAGE expectr(er : CDT.rec) ;
   INCOMING MESSAGE init() ;
   INCOMING MESSAGE summary() ;
   INCOMING MESSAGE expectInner(einner : INTEGER) ;
END;

END CapDataport.
