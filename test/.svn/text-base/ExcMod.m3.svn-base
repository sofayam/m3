MODULE ExcMod;

PROCEDURE raiseCain() RAISES {cain} =
BEGIN
  RAISE cain;
END raiseCain;

PROCEDURE raiseIt (e : exceptions) RAISES {hell, cain} = 
BEGIN
  IF e = exceptions.hell THEN
    RAISE hell;
  ELSIF e = exceptions.cain THEN
    raiseCain();
END ;
END raiseIt;

PROCEDURE raiseiPack(i : INTEGER) RAISES {iPackage} =
BEGIN
  RAISE iPackage (i)
END raiseiPack;

PROCEDURE raiserPack(i : INTEGER) RAISES {rPackage} =
BEGIN
  RAISE rPackage (rec{x := i})
END raiserPack;

BEGIN
END ExcMod.
