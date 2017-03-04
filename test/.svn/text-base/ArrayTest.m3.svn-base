MODULE ArrayTest ;
IMPORT IO, Regress;
TYPE
  index = {a,b,c,d};
  arr1 = ARRAY [1..3] OF INTEGER;
  arr2 = ARRAY index OF INTEGER;
  arrdots = ARRAY [1..100] OF INTEGER; 
  arrmulti = ARRAY [1..100],[1..10],[5..8] OF INTEGER;
  arrpoly = ARRAY [index.b .. index.c],[3..10] OF INTEGER;
VAR
  a1 : arr1;
  a2 := arr1{1,2,3};
  a3, a4 : arr2;
  dotuser := arrdots{1,5,99,..};  
  arm : arrmulti;
  ap : arrpoly ;
BEGIN
  Regress.init("Array");
   ap[index.b][3] := 1;
   arm[1,4,8] := 4;
   Regress.assertPass(arm[1][4][8] = 4); 
   arm[4][5][6] := 99;
   Regress.assertPass(arm[4,5,6] = 99); 
   a3[index.a] := 1;
   a3[index.d] := 1;
   a1[1] := 1;
   a1[2] := 2;
   a1[3] := 3; 
   FOR i := 1 TO 3 DO
     Regress.assertPass(a2[i] = a1[i]);
     (* IO.PutInt(a1[i]);   *)
   END;
   Regress.assertPass(a2 = a1); 
   Regress.assertPass(a3[index.a] = a3[index.d]);
   Regress.assertPass(dotuser[66] = 99); 
   a3 := arr2{1,2,3,4};
   a4 := a3;
   
  FOR idx := index.a TO index.d DO
     IF a3[idx] # a4[idx] THEN
       Regress.assertPass(a3[idx] = a4[idx])
     END 
   END; 
   (*  a4[1] := 99; *) 
   a4[index.a] := 99;
   Regress.assertPass(a3 # a4);
  Regress.summary();
END ArrayTest.
