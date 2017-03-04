MODULE Const;
IMPORT ConstInt, IO, Regress;

TYPE 
  arr1 = ARRAY[LAST(CARDINAL)-10..LAST(CARDINAL)] OF INTEGER;
  arr2 = ARRAY[FIRST(CARDINAL)..FIRST(CARDINAL)+10] OF INTEGER;
  arr3 = ARRAY [ORD(FALSE) .. 10] OF INTEGER ;
  color = {red,blue,green} ;
CONST
   verbose : INTEGER = 10 ;
   nine = 9 ;
   nineteen = ConstInt.ten + nine ;
   false = 9 = 10 ;
   true = NOT false ;
   puzzle = true OR false;
   one = ABS(-1);
   two = one + one;
   three = CEILING(2.6);
   six = three + three;
   four = FLOOR(4.1);
   eight = four + four;
   PI = 3.14156;
   truncPI = TRUNC(PI);
   almost = 99.9;
   full = ROUND(almost);
   threePointO = FLOAT(3);
   minfour = MIN(four,eight);
   maxeight = MAX(four,eight);
   arr3length = NUMBER(arr3);
   arr2length = NUMBER(arr2);
   twentytwo = arr3length + arr2length;
   red = VAL(ORD(color.red),color);
   blueOrd = ORD(color.blue);
   redAsWell = VAL(blueOrd - 1, color);


VAR v : INTEGER;
    a1 := arr1{1,2,3,4,5,6,7,8,9,10,11}; 
    a2 := arr2{1,2,3,4,5,6,7,8,9,10,11}; 
BEGIN
  Regress.init("Const");
  v := nine;
  v := nineteen;
  v := nineteen + nine;
  Regress.assertPass(verbose * 2 = 20); 
  Regress.assertPass(v = 28); 
(*  Regress.assertPass(a1[LAST(CARDINAL)-7] = 4); won't work for C *)
  Regress.assertPass(a2[3] = 4);
  Regress.assertPass(FIRST(arr3) = 0);
  Regress.assertPass(two = 2);
  Regress.assertPass(six = 6);
  Regress.assertPass(eight = 8);
  Regress.assertPass(truncPI = TRUNC(PI));
  Regress.assertPass(full = 100);
  Regress.assertPass(threePointO = 3.0);
  Regress.assertPass(minfour = 4);
  Regress.assertPass(maxeight = 8);
  Regress.assertPass(twentytwo = 22);
  Regress.assertPass(red = color.red);
  Regress.assertPass(redAsWell = color.red);

  Regress.summary();
END Const.
