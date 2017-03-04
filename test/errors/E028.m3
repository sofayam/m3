MODULE E028;

TYPE r = RECORD I : INTEGER END ;

VAR r1, r2 := r{i:= 99};
    i := MAX(r1, r2); <*ERROR 028*>

BEGIN
  
END E028.
