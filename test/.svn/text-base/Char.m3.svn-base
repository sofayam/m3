MODULE Char;
IMPORT IO, Regress;

TYPE
    subchar = ['a' .. 'b'];
VAR 
    sc : subchar ;
    ch : CHAR ;
    i : INTEGER;
    charOfInt : ARRAY ['A' .. 'Z'] OF INTEGER;
    intOfChar : ARRAY [1 .. 26] OF CHAR;
    caught := FALSE;
    ok := TRUE;

BEGIN
  Regress.init("Char");
  i := ORD('A');
  FOR ch := 'A' TO 'Z' DO
(*    IO.PutChar(ch); *)
    charOfInt[ch] := i;
    i := i + 1;
  END;
  ch := 'A';
  FOR i := 1 TO 26 DO
(*    IO.PutInt(i); *)
    intOfChar[i] := ch;
    ch := VAL(ORD(ch) + 1, CHAR);
  END;
  FOR i := 1 TO 26 DO
    ch := VAL(i + ORD('A') - 1,CHAR);
(*    IO.PutChar(ch);
    IO.PutInt(charOfInt[ch]);
    IO.PutInt(ORD(intOfChar[i])); *)
    ok := ok AND (ORD(intOfChar[i]) = charOfInt[ch])
  END;
  Regress.assertPass(ok);

  TRY
    sc := 'A';
  EXCEPT
  | ConstraintError => caught := TRUE;
  END;
  Regress.assertPass(caught);

  (* Control Characters *)

  ch := '\n' ;
  ch := '\"' ;
  ch := '\'' ;

  (* TBD more tests here when (if ever) we get back to string handling *)

  Regress.summary()
END Char.
