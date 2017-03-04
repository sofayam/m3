MODULE Part1;
IMPORT IO;
IMPORT Mixin;
REVEAL T = Mixin.Mixer BRANDED OBJECT  
  i : INTEGER; 
END;
VAR
  ctr : INTEGER := 99;
PROCEDURE make() : T =
VAR t := NEW(T);
BEGIN
  t.i := ctr;
  ctr := ctr + 1;
  RETURN t;
END make;
PROCEDURE get(t : T) : INTEGER =
BEGIN
  RETURN t.i;
END get;
BEGIN
END Part1.
