CAPSULE INTERFACE CapType ;
IMPORT CapTypes;
PORT p1 : PROTOCOL
    INCOMING MESSAGE init() ;
    INCOMING MESSAGE actInt(i : INTEGER);
    OUTGOING MESSAGE resInt(i : INTEGER);
    INCOMING MESSAGE actRec(rec : CapTypes.CapRec) ;
    OUTGOING MESSAGE resRec(rec : CapTypes.CapRec) ;
    INCOMING MESSAGE actArr(arr : CapTypes.CapArray) ;
    OUTGOING MESSAGE resArr(arr : CapTypes.CapArray) ;
    INCOMING MESSAGE actSet(set : CapTypes.CapSet);
    OUTGOING MESSAGE resSet(set : CapTypes.CapSet);
    INCOMING MESSAGE actOpen(open : CapTypes.CapOpen);
    OUTGOING MESSAGE resOpen(sum : INTEGER);
    INCOMING MESSAGE actReal(real : REAL) ;
    OUTGOING MESSAGE resReal(real : REAL) ;
    INCOMING MESSAGE actDict(dict : CapTypes.CapDict) ;
    OUTGOING MESSAGE resDict(dict : CapTypes.CapDict) ;
    INCOMING MESSAGE actList(list : CapTypes.CapList) ;
    OUTGOING MESSAGE resList(list : CapTypes.CapList) ;
    INCOMING MESSAGE summary() ;
END;
END CapType.
