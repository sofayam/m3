INTERFACE Opaque;

TYPE hidden <: REFANY ;

PROCEDURE makeHidden(x : INTEGER) : hidden;

PROCEDURE openHidden(h : hidden) : INTEGER;

END Opaque.
