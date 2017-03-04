CAPSULE CapType ;

IMPORT CapTypes, Timer, Regress;

  ACTIVITY actInt (i : INTEGER) = 
  BEGIN 
    SEND resInt(i+1);
  END actInt ;

  ACTIVITY actRec (rec : CapTypes.CapRec) = 
    VAR locRec : CapTypes.CapRec;
  BEGIN 
    locRec := rec;
    locRec.x := rec.x + 1;
    locRec.b := NOT rec.b;
    SEND resRec(locRec);
  END actRec ;

  ACTIVITY actArr (arr : CapTypes.CapArray) = 
    VAR locArr : CapTypes.CapArray;
    TYPE transform = ARRAY CapTypes.Color OF CapTypes.Color;
    CONST transformVector = transform{CapTypes.Color.Green, CapTypes.Color.Blue, CapTypes.Color.Red};
  BEGIN 
    FOR idx := FIRST(arr) TO LAST(arr) DO
       locArr[idx] := transformVector[arr[idx]]
    END ;
    SEND resArr(locArr);
  END actArr ;

  ACTIVITY actSet(set : CapTypes.CapSet) = 
  BEGIN
    SEND resSet(set := CapTypes.FullSet - set);
  END actSet ;

  ACTIVITY actOpen(open : CapTypes.CapOpen) = 
    VAR sum : INTEGER := 0;
  BEGIN
    FOR idx := FIRST(open) TO LAST(open) DO
       sum := sum + open[idx].x
    END ;
    SEND resOpen(sum := sum);
  END actOpen;
  ACTIVITY init () = 
  BEGIN 
    Regress.init("TypedParameters");
  END init ;
  ACTIVITY summary () = 
  BEGIN 
    Regress.summary();
  END summary ;
  ACTIVITY actReal (real : REAL) = 
  BEGIN 
     SEND resReal(real / 3.0);
  END actReal ;
  ACTIVITY actDict(dict : CapTypes.CapDict) = 
  BEGIN 
    SEND resDict(dict);
  END actDict ;
  ACTIVITY actList(list : CapTypes.CapList) = 
  BEGIN 
    SEND resList(list);
  END actList ;

BEGIN
END CapType.
