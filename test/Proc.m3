MODULE Proc;
IMPORT Regress;
TYPE
  retrec = RECORD
    i : INTEGER := 98;
  END;
PROCEDURE foo1(I1 : INTEGER := 10; VALUE I2 : INTEGER := 1; expected : INTEGER := 11) =
VAR  j : INTEGER;
BEGIN
  Regress.assertPass(expected = I1+I2);
END foo1;
PROCEDURE foo2(expected : INTEGER; I1 : INTEGER := 1; I2 : INTEGER := -1) =
  VAR  j : INTEGER;
  BEGIN
    Regress.assertPass(expected = I1-I2);
  END foo2;
PROCEDURE changeVAR(VAR changed: INTEGER; target: INTEGER) =
  BEGIN
    changed := target;
  END changeVAR;  
PROCEDURE leaveVALUE(leave: INTEGER; target: INTEGER) =
  BEGIN
    leave := target;
  END leaveVALUE;  
PROCEDURE retInt() : INTEGER =
  VAR
    x := 1;
  BEGIN
    x := x + 1;
    RETURN 1; 
  END retInt;

PROCEDURE retRec(c : BOOLEAN): retrec = 
  VAR  
    r,r1 : retrec;
  BEGIN
    IF c THEN
      r.i := 99;
      RETURN r;
    ELSE
      r1 := retrec{};
      RETURN r1;
    END;
  END retRec ;

VAR 
  changeMe : INTEGER;   
  ret : INTEGER;
BEGIN
  Regress.init("Proc");
  (* defaults *)
  foo1();
  foo1(5,3,8);
  foo2(2);
  foo2(1,5,4);
  (* keywords *)
  foo2(I2 := 1, expected := 0);
  (* modes *)
  changeMe := 100;
  changeVAR(changed:=changeMe, target:=99);
  Regress.assertPass(changeMe=99);
  leaveVALUE(leave:=changeMe, target:=100);
  Regress.assertPass(changeMe=99);
  (* return values *)
  Regress.assertPass(retInt()=1);
  Regress.assertPass(retRec(FALSE).i=98);
  Regress.assertPass(retRec(TRUE).i=99);
  Regress.summary();
END Proc.
