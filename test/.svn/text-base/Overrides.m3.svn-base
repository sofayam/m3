MODULE Overrides;
IMPORT Text;
IMPORT IO;
IMPORT Regress;

TYPE A = OBJECT 
  i : INTEGER;
METHODS
  doit() : TEXT := doitA;
END;

PROCEDURE doitA (self : A) : TEXT =
BEGIN
  RETURN "doitA";
END doitA;

TYPE AB = A OBJECT 
  i : INTEGER;
OVERRIDES
  doit := doitAB;
END;
PROCEDURE doitAB (self : A) : TEXT =
BEGIN
  RETURN "doitAB"
END doitAB;


TYPE AC = A OBJECT 
  i : INTEGER;
METHODS
  doit() : TEXT := doitAC;
END;

PROCEDURE doitAC (self : A) : TEXT =
BEGIN
  RETURN "doitAC"
END doitAC;

PROCEDURE doitAD (self : A) : TEXT =
BEGIN
  RETURN "doitAD"
END doitAD;

VAR
  aa := ARRAY OF A{NEW(A),NEW(AB),NEW(AC),NEW(AB, doit := doitAD)};
BEGIN
  Regress.init("Overrides");  
  Regress.assertPass(Text.Equal(aa[0].doit(),"doitA"));
  Regress.assertPass(Text.Equal(aa[1].doit(),"doitAB"));
  Regress.assertPass(Text.Equal(aa[2].doit(),"doitA"));
  Regress.assertPass(Text.Equal(aa[3].doit(),"doitAD")); 

  Regress.summary();
END Overrides.
