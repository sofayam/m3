MODULE ListTest;
IMPORT Regress;
CONST limit = 4;
TYPE  
  myList = LIST OF INTEGER;
VAR 
  list1, list2, list3 : myList;
  passed : BOOLEAN := TRUE ;
TYPE
  color = {red,green,blue} ;
  rec = RECORD 
    i : INTEGER ;
    b : BOOLEAN ;
    e : color ;
  END;
VAR
  ctr : INTEGER := 1 ;
  recList : LIST OF rec;
  fooList := LIST OF color{color.blue, color.green};

BEGIN
  Regress.init("ListTest");
  FOR ctr := 1 TO limit DO
    APPEND(list1,ctr);
  END;
  REPEAT
    APPEND(list2,POP(list1))
  UNTIL LAST(list1) = 0;
  Regress.assertPass(limit = LAST(list2));

  FOR ctr := 1 TO limit DO
    APPEND(list3,POP(list2))
  END;
  FOR ctr := 1 TO limit DO
    IF list3[ctr] # ctr THEN
      passed := FALSE;
    END
  END; 
  Regress.assertPass(passed);

  FOR ctr := 1 TO limit DO
    APPEND(recList, rec{ctr,FALSE,color.red})
  END;
  passed := TRUE ;
  FOREACH r IN recList DO
     IF NOT r.i = ctr AND r = recList[ctr] THEN (* Note the nasty use of global ctr *)
       passed := FALSE;
     END;
     ctr := ctr + 1;
  END;

  Regress.assertPass(passed);
  
  fooList := LIST OF color{color.red, color.green} ;

  Regress.assertPass(LAST(fooList) = 2);

  APPEND(fooList,color.green);

  Regress.assertPass(NUMBER(fooList) = 3);

  DEL(fooList,1);

  Regress.assertPass(NUMBER(fooList) = 2);

  Regress.assertPass(fooList = LIST OF color{color.green, color.green});

  TRY
    DEL(fooList,5);
    Regress.assertPass(FALSE)
  EXCEPT 
    ConstraintError => Regress.assertPass(TRUE)
  ELSE
    Regress.assertPass(FALSE)
  END;

  Regress.assertPass(color.green IN fooList);
  Regress.assertPass(NOT color.red IN fooList);

  Regress.assertPass(INDEX(LIST OF INTEGER{1,2,3,4},3) = 3);

  TRY
    IF INDEX(LIST OF INTEGER{1,2,3,4},7) = 0 THEN
      Regress.assertPass(FALSE);
    END
  EXCEPT ConstraintError =>
    Regress.assertPass(TRUE);
  END;


  Regress.summary()

END ListTest.
