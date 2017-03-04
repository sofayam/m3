MODULE FirstLast;

IMPORT IO, Regress;
TYPE 
  arr = ARRAY [1..10] OF INTEGER;
  color = {red, blue, green};
VAR 
  arri := arr{1,2,3,..} ; 
  arrc := ARRAY color OF color{color.blue, color.red, color.green} ;
BEGIN

  Regress.init("FirstLast");
  Regress.assertPass(arri[LAST(arr)] = 3);
  Regress.assertPass(FIRST(INTEGER) + LAST(INTEGER) = -1);
  Regress.assertPass(arrc[color.blue] = color.red);
  Regress.assertPass(arrc[LAST(arrc)] = color.green);
  Regress.summary();
  
END FirstLast.
