MODULE E034;


VAR  a : ARRAY[1..10] OF INTEGER; 
     r : RECORD i : INTEGER END ;

PROCEDURE p (p1 : ARRAY OF INTEGER) =
BEGIN
END p;
BEGIN
  p(SUBARRAY(a,2,r)); <*ERROR 034*>

END E034.
