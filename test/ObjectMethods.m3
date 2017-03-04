MODULE ObjectMethods;
IMPORT Regress;
TYPE 
  O = 
   OBJECT 
    i : INTEGER := 99;
  METHODS
    init(x : INTEGER) : O := Init;
  END;

PROCEDURE Init(self : O; x : INTEGER): O =
  VAR o : O;
BEGIN
  Regress.assertPass(self.i = 999);
  self.i := x;
  RETURN self;
END Init;
VAR
  o : O;
TYPE bla = {a,b,c};
BEGIN
  Regress.init("ObjectMethods"); 
  o := NEW(O);
  o.i := 999;
  o := o.init(77);
  Regress.assertPass(o.i = 77); 
  Regress.summary();
END ObjectMethods.
