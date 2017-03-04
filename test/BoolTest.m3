MODULE BoolTest;
IMPORT Regress;

VAR
  c1 : BOOLEAN ;
  c2 := BOOLEAN.FALSE;
  a : ARRAY BOOLEAN OF BOOLEAN;
  aa : ARRAY BOOLEAN,BOOLEAN OF BOOLEAN;
  aaa := ARRAY [1..4] OF BOOLEAN {FALSE, FALSE, FALSE, TRUE};
  ctr := 1;
BEGIN
  Regress.init("Bool");
  c1 := BOOLEAN.TRUE;
  IF c1 AND NOT c2 THEN
    Regress.assertPass(TRUE);
  ELSE
    Regress.assertPass(FALSE);
  END;
  FOR j := FALSE TO TRUE DO
    a[j] := NOT j;
  END ;
  FOR i := FALSE TO TRUE DO
    FOR j := FALSE TO TRUE DO
      aa[i,j] := i AND j;
    END;
  END;
  FOR i := FALSE TO TRUE DO
    FOR j := FALSE TO TRUE DO
      Regress.assertPass(aa[i,j]=aaa[ctr]);
      ctr := ctr + 1;
    END;
  END;
  Regress.summary();
END BoolTest.
