MODULE OpenArray;
IMPORT IO, Regress;

TYPE 
  oa = ARRAY  OF INTEGER;
  mat = ARRAY OF ARRAY OF INTEGER ;
  oar = REF oa ;
  (*  matref = REF mat ; *)
  matref = REF ARRAY OF ARRAY OF INTEGER ;
VAR 
  oa1 := oa{101,202,303} ;
  oar1 : oar;
  matref1 : matref ;

PROCEDURE InitMatrix(matrefpar : matref) =
  VAR inner := matrefpar[FIRST(matrefpar^)];
BEGIN
  FOR i := FIRST(matrefpar^) TO LAST(matrefpar^) DO
    FOR j := FIRST(inner) TO LAST(inner) DO
      matrefpar[i,j] := i*j ;
    END
  END;
END InitMatrix;

PROCEDURE SumMatrix(matrefpar : matref) : INTEGER =
  VAR 
    inner := matrefpar[FIRST(matrefpar^)];
    sum := 0;
BEGIN
  FOR i := FIRST(matrefpar^) TO LAST(matrefpar^) DO
    FOR j := FIRST(inner) TO LAST(inner) DO
      sum := sum + matrefpar[i,j] ;
    END
  END;
  RETURN sum
END SumMatrix;


VAR res := 0 ;
BEGIN
  Regress.init("OpenArray");

  FOR i := FIRST(oa1) TO LAST(oa1) DO
    res := res + oa1[i]
  END;
  Regress.assertPass(res = 606);

  oar1 := NEW(oar, 10);
  oar1[5] := 101; 
  matref1 := NEW(matref, 9, 8); (* don't change this otherwise you won't get 1008 out at the end *)

  InitMatrix(matref1);
  res := SumMatrix(matref1);
  Regress.assertPass(res = 1008);
  Regress.summary();

END OpenArray.
