
CAPSULE EverythingSub ;
  ACTIVITY a () =
    READS d ; 
  BEGIN 
  END a ;
  ACTIVITY b () =
    WRITES d ; 
  BEGIN 
  END b ;
  ACTIVITY c () =
    WRITES d ; 
  BEGIN 
  END c ;
  VAR d : INTEGER ;

BEGIN

END EverythingSub.
