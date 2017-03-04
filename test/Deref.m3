MODULE Deref;
IMPORT DerefInt;
IMPORT IO, Regress;

(* This contains long dereference chains which code generation has to sort out from qualids *)

TYPE r0 = RECORD a : r1 END;
     r1 = RECORD b : r2 END;
     r2 = RECORD c : r3 END;
     r3 = RECORD d : r4 END;
     r4 = RECORD e : INTEGER := 99 END;

     VAR r : r0; 
         er : DerefInt.r0;

BEGIN

  Regress.init("Deref");

  Regress.assertPass(r.a.b.c.d.e = 99);
  Regress.assertPass(er.a.b.c.d.e = 88);
  Regress.assertPass(DerefInt.er.a.b.c.d.e = 88);

  Regress.summary();
  
END Deref.
