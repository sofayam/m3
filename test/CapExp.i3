CAPSULE INTERFACE CapExp ;
IMPORT CapExpTypes;
PORT p1 : PROTOCOL
 INCOMING MESSAGE question(x : INTEGER) ;
 OUTGOING MESSAGE reply(z : CapExpTypes.bytes) ;
END;
END CapExp.
