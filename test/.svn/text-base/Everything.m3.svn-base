
CAPSULE Everything ; 
  USECAPSULE EverythingSub ;
  START = BEGIN
    NEXT s2    
  END;
  ACTIVITY a () =
    VAR x : INTEGER;
  BEGIN 
    x := int1;
  END a ;
  ACTIVITY b () =
    READS y ;      
    READS arr ;
  BEGIN 
    int1 := int2;
  END b ;
  ACTIVITY c () =
    SENDS aa;
  BEGIN 
    int1 := 10;
    arr[2] := 11;
  END c ;
  VAR int1, int2 : INTEGER ;
  VAR arr : ARRAY [1..10] OF INTEGER ;
  STATE s1    
    ON t() =
    SENDS om;
      BEGIN
        arr[1] := 20;
        NEXT s2;
      END t;
    ON t3() =
      BEGIN
      NEXT s2;
      END t3;
  STATE s2
    ON t2() =
      BEGIN
      NEXT s1;
      END t2;
  TRIGGER trig ON int1 = 9 ;
  VAR tim : ONESHOT CHANGEABLE TIMER ;
  VAR kid : EverythingSub ;
  VAR x : INTEGER ;
  VAR y : INTEGER ;
  ACTIVITY aa () =
    WRITES x ;
    WRITES arr ;
    WRITES int1 ;
    WRITES x1 ; 
  BEGIN 
  END aa ;
  VAR x1 : INTEGER ;
  ACTIVITY abc () =
    SENDS kid.b; 
  BEGIN 
    x := 99;
  END abc ;
  CONNECT
    tim -> b;
    trig -> a;
    kid.tiddlypom -> om;
    kid.tiddlypom -> t3;
    tim -> t2;
BEGIN

END Everything.
