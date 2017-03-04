MODULE E022;

TYPE o1 = OBJECT i : INTEGER := 1 END;
TYPE o2 = OBJECT j : INTEGER := 1 END;

VAR o2ref : o2 := NEW(o2, j := 1);
    o1ref : o1;
BEGIN
  
  o1ref := NARROW(o2ref,o1) <*ERROR 022*>


END E022.
