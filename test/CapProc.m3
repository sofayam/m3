CAPSULE CapProc;
  IMPORT Regress;

  PROCEDURE doubleIt(x:INTEGER) : INTEGER =
    PROCEDURE negateIt(x:INTEGER) : INTEGER =
      BEGIN
        RETURN x * -1;
      END negateIt;
    BEGIN
      RETURN negateIt(negateIt(x * 2));
    END doubleIt;

  VAR localx,localy : INTEGER;

  ACTIVITY ask (x:INTEGER) =
  VAR
    y : INTEGER;
  BEGIN
    y := doubleIt(x);
    localx := x;
    localy := y;
    SEND answer(y);
  END ask;
  ACTIVITY summary () = 
     VAR YisTwiceX : BOOLEAN;
  BEGIN 
     YisTwiceX := localy = 2 * localx; 
     Regress.assertPass(YisTwiceX);
     Regress.summary();
  END summary ;

BEGIN
   Regress.init("CapProc");
END CapProc.
