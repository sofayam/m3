MODULE Predef;
IMPORT Regress;
TYPE
  enum = {red, green, blue};
VAR
  ch, oldch : CHAR := 'A';
  i, oldi   : INTEGER := 1;
  e, olde   : enum := enum.green;
  es : [enum.green .. enum.blue];
  caught := FALSE;
BEGIN
  Regress.init("Predef");
  INC(ch); DEC(ch);
  Regress.assertPass(oldch = ch);
  INC(i); DEC(i);
  Regress.assertPass(oldi = i);
  INC(e); DEC(e);
  Regress.assertPass(olde = e); 

  es := e;
  TRY
    DEC(es);
  EXCEPT
  | ConstraintError => caught := TRUE;
  END;
  Regress.assertPass(caught); 

  caught := FALSE;
  TRY
    DEC(e); DEC(e);
  EXCEPT
  | ConstraintError => caught := TRUE;
  END;
  Regress.assertPass(caught); 


  Regress.assertPass(VAL(ORD(ch),CHAR) = ch); 
  Regress.assertPass(VAL(ORD(i),INTEGER) = i); 
  Regress.assertPass(VAL(ORD(e),enum) = e);  

  Regress.summary();
  
END Predef.
