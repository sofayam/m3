MODULE E013;

TYPE aref = REF ARRAY OF INTEGER;

VAR a := NEW(aref,1.0); <*ERROR 013*>
BEGIN

END E013.
