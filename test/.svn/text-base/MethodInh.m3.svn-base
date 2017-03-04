MODULE MethodInh;
IMPORT Regress;
TYPE
  A =  OBJECT 
    i : INTEGER := 99;
  METHODS
    putA(x : INTEGER) := put;
  END;

  AB = A OBJECT 
    i : INTEGER := 88;
    (*  METHODS
        putA() := put; *)
  END;

PROCEDURE put(a : A; x : INTEGER) = 
  BEGIN
    dump(a.i,x)
  END put;

TYPE 
  AC = A OBJECT
    i : INTEGER := 77;
  METHODS
    putA(x : INTEGER) := put;
  END;

PROCEDURE putAD(a : AD; x : INTEGER) = 
  BEGIN
    dump(a.i,x)
  END putAD;
TYPE 
  AD = AC OBJECT
    i : INTEGER := 66;
  METHODS
    putA(x : INTEGER) := putAD;
  END;

PROCEDURE dump(given, expected : INTEGER) = 
  BEGIN
    Regress.assertPass(given=expected);
  END dump;

VAR a : A := NEW(A);
    ab : AB := NEW(AB);
    ac : AC := NEW(AC);
    ad : AD := NEW(AD);
BEGIN
(*  a := NEW(A);*)
  Regress.init("MethodInh");
  a.putA(99);
  ab.putA(99); (*  AB is automatically cast by this call *) 
  A.putA(a,99);
  ac.putA(99);
  A.putA(ac,99);
  ad.putA(66);
  A.putA(ad,99);
  Regress.summary();

END MethodInh.



