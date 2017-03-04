INTERFACE DerefInt;

TYPE r0 = RECORD a : r1 END;
     r1 = RECORD b : r2 END;
     r2 = RECORD c : r3 END;
     r3 = RECORD d : r4 END;
     r4 = RECORD e : INTEGER := 88 END;
  
     VAR er : r0;

END DerefInt.
