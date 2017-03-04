MODULE Case;
IMPORT Regress, Text;
FROM IO IMPORT Put;
TYPE enum = {red, orange, yellow, green, blue, indigo, violet};
PROCEDURE caseInt(x : INTEGER):TEXT =
  VAR
    res : TEXT;
  BEGIN
    CASE x OF
       1 =>       res := "one"
     | 2..5 =>    res := "two..five"
     | 6 =>       res := "six"
     | 7..9 =>    res := "seven..nine"
    ELSE
      res := "other" 
    END ;
    RETURN res
  END caseInt;
PROCEDURE caseChar(c : CHAR):TEXT =
  VAR
    res : TEXT;
  BEGIN
    CASE c OF
       'a' =>       res := "ay"
     | 'b'..'d' =>  res := "bee..dee"
     | 'e' =>       res := "ee"
     | 'x' =>       res := "ecks"
    ELSE
      res := "other" 
    END ;
    RETURN res
  END caseChar;
PROCEDURE caseEnum(e : enum):TEXT =
  VAR
    res : TEXT;
  BEGIN
    CASE e OF
       enum.red =>     res := "red"
     | enum.orange =>  res := "orange"
     | enum.yellow..
       enum.indigo =>  res := "yellow..indigo"
    ELSE
      res := "other" 
    END ; 
    RETURN res
  END caseEnum;

BEGIN
  Regress.init("Case");
  (*Put(caseInt(3));*)
  Regress.assertPass(Text.Equal(caseInt(3),"two..five"));
(*  Put(caseChar('c'));*)
  Regress.assertPass(Text.Equal(caseChar('c'),"bee..dee"));
  (*Put(">>" & caseEnum(enum.blue) & "<<");*)
(*  Put(caseEnum(enum.blue));*)
  Regress.assertPass(Text.Equal(caseEnum(enum.blue),"yellow..indigo"));

  Regress.summary()
END Case.
