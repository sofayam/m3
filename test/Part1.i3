INTERFACE Part1;
TYPE T <: ROOT;
PROCEDURE make() : T;
PROCEDURE get(t:T) : INTEGER;
VAR touched : BOOLEAN := FALSE;
END Part1.
