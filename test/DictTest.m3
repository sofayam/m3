MODULE DictTest;
IMPORT Regress, IO;

TYPE 
  color = {red,blue,green};
  colorDictType = DICT color OF INTEGER;
  ridx = RECORD
    c : color;
    b : TEXT;
  END;
  recDictType = DICT ridx OF INTEGER;


VAR myDict := DICT OF INTEGER{};
    res := 0;
    ctr := 0;
    colorDict : colorDictType;
    col : color;
    rdict : recDictType;
BEGIN
  Regress.init("DictTest");
  FOR I := 1 TO 4 DO
    myDict[IMAGE(I)] := I
  END ;  
  
  FOREACH k IN KEYS(myDict) DO
    res := res + myDict[k]
  END;
  Regress.assertPass(res = 10);

  myDict := DICT OF INTEGER{};

  FOREACH k IN LIST OF TEXT{"foo", "bar", "baz", "bla"} DO
    myDict[k] := ctr;
    ctr := ctr + 1;
  END;

  DEL(myDict, "foo");
  DEL(myDict, "bar");

  ctr := 0;
  FOREACH k IN KEYS(myDict) DO
    ctr := ctr + myDict[k] 
  END;
  Regress.assertPass(ctr = 5);

  Regress.assertPass(myDict = DICT OF INTEGER{"baz" := 2, "bla" := 3});

  TRY
    DEL(myDict,"foo");
    Regress.assertPass(FALSE)
  EXCEPT 
    ConstraintError => Regress.assertPass(TRUE)
  ELSE
    Regress.assertPass(FALSE)
  END;


  Regress.assertPass(INDEX(myDict, 3) = "bla");

  TRY
    IF INDEX(myDict, 1) = "" THEN
      Regress.assertPass(FALSE);
    END
  EXCEPT ConstraintError =>
    Regress.assertPass(TRUE);
  END;

  colorDict[color.green] := 1;

  FOREACH key IN KEYS(colorDict) DO
    col := key
  END;

  Regress.assertPass(col IN KEYS(colorDict));

  rdict[ridx{c := color.blue, b := "foo"}] := 1; 
  rdict[ridx{c := color.red, b := "bla"}] := 2; 

  res := 0;
  FOREACH k IN KEYS(rdict) DO
    res := res + rdict[k]
  END;

  Regress.assertPass(res = 3);

  DEL(rdict,ridx{c := color.blue, b := "foo"});

  Regress.assertPass(LAST(KEYS(rdict)) = 1);

  Regress.summary()

  

END DictTest.
