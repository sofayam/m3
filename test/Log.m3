MODULE Log;

VAR
   ctr : INTEGER := 0;
   localLog : REF log; (* This was not giving an error when we had := instead of : FIX ME *)

PROCEDURE setLength(l : INTEGER) =
  BEGIN
    localLog := NEW(REF log,l);
  END setLength;

PROCEDURE addEvent(event : TEXT) = 
  BEGIN
    localLog[ctr] := event;
    ctr := ctr + 1;
  END addEvent;

PROCEDURE equalsLog(expected : log) : BOOLEAN =
  BEGIN
    RETURN localLog^ = expected
  END equalsLog;
BEGIN

END Log.
