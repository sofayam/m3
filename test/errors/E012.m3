MODULE E012;

TYPE aref = REF ARRAY OF INTEGER;

VAR a := NEW(aref,foo := 1); <*ERROR 012*>
BEGIN

END E012.