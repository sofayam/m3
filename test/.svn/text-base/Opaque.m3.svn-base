MODULE Opaque;

REVEAL hidden = RECORD
  i : INTEGER;
END;

PROCEDURE makeHidden(x : INTEGER) : hidden =
VAR
  h := hidden{i := x};
BEGIN
  RETURN h
END makeHidden;
  
PROCEDURE openHidden(h : hidden) : INTEGER =
BEGIN
  RETURN h.i;
END openHidden;

BEGIN

END Opaque.
