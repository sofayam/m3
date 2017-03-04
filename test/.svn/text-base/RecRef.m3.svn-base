MODULE RecRef;
IMPORT Regress;
TYPE
  cellref = REF RECORD
    key : INTEGER ;
    next1, next2 : cellref ;
  END;
  cell = RECORD
    key : INTEGER ;
    next : REF cell ;
  END;
VAR
  rootref : cellref;
  root : cell;
BEGIN
  Regress.init("RecRef") ;
  rootref := NEW(cellref, key := 99) ;
  Regress.assertPass(rootref.key = 99) ;
  root := cell{1,NIL} ;
  root.key := 88 ;
  Regress.assertPass(root.key = 88);
  Regress.summary() ;
END RecRef.
