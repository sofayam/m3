MODULE Set;
IMPORT Regress, IO, Fmt, Text;
TYPE 
  r = RECORD i : INTEGER END;
  enum = {red,orange,yellow,green,blue,indigo,violet};
  range = [1..10];
  eset = SET OF enum;
  iset = SET OF range;
(*  rset = SET OF r;*)
VAR
  colors := ARRAY enum OF TEXT  
                {"red","orange","yellow","green","blue","indigo","violet"};
  es1 := eset{enum.red};
  es2 := eset{enum.indigo, enum.green};
  es3 : eset;
  is1 := iset{4};
  is2 := iset{2..6, 8, 10};
  is3 : iset;

PROCEDURE ESetImage(set : eset) : TEXT =
  VAR
    res : TEXT := "";
  BEGIN
    FOR color := FIRST(enum) TO LAST(enum) DO
      IF color IN set THEN
        res := res & colors[color] & " "
      END
    END;
    RETURN res
  END ESetImage; 

PROCEDURE ISetImage(set : iset) : TEXT =
  VAR
    res : TEXT := "";
  BEGIN
    FOR int := FIRST(range) TO LAST(range) DO
      IF int IN set THEN
        res := res & Fmt.Int(int) & " "
      END
    END;
    RETURN res
  END ISetImage; 

BEGIN
  Regress.init("Set");
  IF 1 IN is1 THEN
      Regress.assertPass(TRUE);
  END;
  
  es3 := es1 + es2;
  Regress.assertPass(Text.Equal(ESetImage(es3),"red green indigo "));

  is3 := is2 - is1;
  Regress.assertPass(Text.Equal(ISetImage(is3),"2 3 5 6 8 10 "));

  Regress.assertPass(Text.Equal(ESetImage(eset{enum.red, enum.green} * eset{enum.green, enum.orange}), "green "));

  Regress.assertPass(Text.Equal(ESetImage(eset{enum.red, enum.green} / eset{enum.green, enum.orange}), "red orange "));

  Regress.assertPass(eset{enum.red, enum.violet} = eset{enum.violet, enum.red});
  Regress.assertPass(eset{enum.red, enum.violet} # eset{enum.red});
  Regress.assertPass(eset{enum.red, enum.violet} > eset{enum.red});
  Regress.assertPass(eset{enum.red, enum.violet} >= eset{enum.red});
  Regress.assertPass(eset{enum.violet} < eset{enum.red, enum.blue, enum.violet});
  Regress.assertPass(eset{enum.red, enum.violet} <= eset{enum.red, enum.violet});


  Regress.summary();

END Set.
