CAPSULE INTERFACE CapTypeNestChild ;
IMPORT CapTypeNestTypes;
PORT p1 : PROTOCOL
   INCOMING MESSAGE mess(rec : CapTypeNestTypes.r) ;
   INCOMING MESSAGE setup() ;
   INCOMING MESSAGE summary() ;
END;
END CapTypeNestChild.
