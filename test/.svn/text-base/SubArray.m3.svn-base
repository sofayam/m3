MODULE SubArray;
(* taken from "Programming with Style" p. 148,
   and then turned into a test *)
IMPORT Regress;
IMPORT Fmt, IO;
TYPE
  Array1 = ARRAY [1..30] OF INTEGER;
  Array2 = ARRAY [1..10] OF INTEGER;
VAR
  a1 := Array1{0,..};
  a2 := Array2{1,..};
CONST
  exp1 = Array1{0,0,0,0,0,0,0,0,0,0,
                 1,1,1,1,1,1,1,1,1,1,0,..};
  exp2 = Array2{0,..};
  exp3 = Array1{0,0,0,0,0,0,0,0,0,0,
                0,3,6,9,12,1,1,1,1,1,0,..};
  exp4 = Array1{0,0,0,0,0,0,0,0,0,0,
                0,0,3,6,9,12,1,1,1,1,0,..};

PROCEDURE ArrayImage(VAR a : ARRAY OF INTEGER) : TEXT =
  VAR t : TEXT := "";
BEGIN
  FOR i := FIRST(a) TO LAST(a) DO
    t := t & Fmt.Int(a[i]);
  END;
  RETURN t & "\n";
END ArrayImage;

BEGIN
  Regress.init("SubArray");
  (*  IO.Put(ArrayImage(a1));
      IO.Put(ArrayImage(a2)); *)
  SUBARRAY(a1, 10, NUMBER(a2)) := a2;
  Regress.assertPass(a1 = exp1);
  (*  IO.Put(ArrayImage(a1));
      IO.Put(ArrayImage(a2)); *)
  a2 := SUBARRAY(a1,0,NUMBER(a2));
  Regress.assertPass(a2 = exp2);
  (*IO.Put(ArrayImage(a2));*)
  FOR i := 0 TO 4 DO 
    SUBARRAY(a1,10,5)[i] := 3 * i
  END;
  Regress.assertPass(a1 = exp3);
  (*IO.Put(ArrayImage(a1)); *)
  SUBARRAY(a1,11,5):= SUBARRAY(a1,10,5);
  Regress.assertPass(a1 = exp4);
  (*IO.Put(ArrayImage(a1));*)
  Regress.summary()
END SubArray.
