INTERFACE OpRef;

(*TYPE T <: REFANY; *)
TYPE T = RECORD 
  x : INTEGER
END ;

PROCEDURE Use(t : T);

PROCEDURE Get():T;

END OpRef.
