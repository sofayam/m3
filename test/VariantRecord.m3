MODULE VariantRecord;
IMPORT Regress;
TYPE sub = [1..200];

TYPE r = RECORD i : INTEGER END; (* You cannot use this as a tag *)

TYPE intTag = RECORD 
  CASE tag : sub OF
     1, 99..101 =>  
        x : INTEGER;
   | 2, 3..10 => 
        y,b : BOOLEAN;
  ELSE
    z : INTEGER;
  END;
  a : INTEGER;
END;
TYPE color = {red, blue, green};
TYPE enumTag = RECORD
  CASE col : color OF
    | color.green => 
        greenInt : INTEGER ;
    | color.blue =>
        blueInt : INTEGER ;
    ELSE
      redInt : INTEGER ;
  END
END;
TYPE defTag = RECORD
  CASE col : color := color.green OF 
   | color.blue =>
       blueInt : INTEGER ;
   | color.green => 
       greenInt : INTEGER ;
   ELSE
      redInt : INTEGER ;
  END
END;

VAR i : INTEGER;
    it := intTag{x := 22, tag:=100};
    et1 := enumTag{col := color.green, greenInt := 99};
    et2 := enumTag{col := color.red};
    caught := FALSE;
    dt := defTag{greenInt := 101};
BEGIN
  Regress.init("Variant Records");
  it.tag := 1;
  it.x := 23;
  TRY
    it.y := FALSE
  EXCEPT
    | ConstraintError => 
         caught := TRUE
  END;
  Regress.assertPass(caught);

  et1.greenInt := et1.greenInt + 1;
  Regress.assertPass(et1.greenInt = 100);

  caught := FALSE;
  TRY
     et1.blueInt := 0;
  EXCEPT
   | ConstraintError =>
        caught := TRUE
  END;
  Regress.assertPass(caught);

  et1 := et2;
  et1.redInt := 99;

  Regress.assertPass(dt.col = color.green);

  Regress.summary()
END VariantRecord.
