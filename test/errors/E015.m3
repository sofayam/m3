MODULE E015;

TYPE rref = REF RECORD 
  i : INTEGER ;
END ;


VAR a := NEW(rref,1); <*ERROR 015*>
BEGIN

END E015.
