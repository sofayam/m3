MODULE Numerics;
IMPORT IO, Regress;
VAR
  x : INTEGER := 99;
  f : REAL ;
  epsilon : REAL := 0.001;
  lr : LONGREAL;
TYPE 
  enum = {red, blue, green};
BEGIN

  Regress.init("Numeric");
  Regress.assertPass ((10 DIV 4) = 2);
  Regress.assertPass ((10 MOD 3) = 1);

  Regress.assertPass ((10.0 / 4.0) = 2.5);

  f := FLOAT(x);
  
  Regress.assertPass (f = 99.0); 

  x := ROUND(f);
  Regress.assertPass (x = 99);

  f := 10.0 / 3.0;

  Regress.assertPass (ABS(f - 3.3333) < epsilon) ;

  Regress.assertPass (ROUND(1.6) = 2);
  Regress.assertPass (TRUNC(1.6) = 1);
  Regress.assertPass (FLOOR(-1.1) = -2);
  Regress.assertPass (CEILING(-1.1) = -1);
  Regress.assertPass (FLOOR(1.1) = 1);
  Regress.assertPass (CEILING(1.1) = 2);

  Regress.assertPass (MAX(10,11) = 11);
  Regress.assertPass (MAX(10.0,11.0) = 11.0);
  Regress.assertPass (MIN(10,11) = 10);
  Regress.assertPass (MIN(10.0,11.0) = 10.0);

  Regress.assertPass (MAX(enum.red, enum.green) = enum.green);
  Regress.assertPass (MIN(enum.red, enum.green) = enum.red);

  lr := 99.9;
  Regress.assertPass(TRUNC(lr) = 99);

  Regress.summary()

END Numerics.
