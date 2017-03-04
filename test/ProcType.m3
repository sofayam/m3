MODULE ProcType;
IMPORT Regress;

TYPE Proc = PROCEDURE (x : INTEGER) : INTEGER;

VAR varDouble : Proc := Double;

PROCEDURE Double (x : INTEGER) : INTEGER =
  BEGIN
    RETURN x * 2
  END Double;

PROCEDURE Treble (x : INTEGER) : INTEGER =
  BEGIN
    RETURN x * 3
  END Treble;
PROCEDURE CallProcObj(x : INTEGER; p : Proc) : INTEGER =
  BEGIN
    RETURN p(x);
  END CallProcObj;

BEGIN
  Regress.init("ProcType");
  Regress.assertPass(CallProcObj(1, Double)=2);
  Regress.assertPass(CallProcObj(1, Treble)=3);
  Regress.assertPass(CallProcObj(1, varDouble)=2);
  Regress.summary()
END ProcType.
