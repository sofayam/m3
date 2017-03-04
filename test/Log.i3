INTERFACE Log;
TYPE log = ARRAY OF TEXT ;
PROCEDURE setLength(l : INTEGER);
PROCEDURE addEvent(event : TEXT);
PROCEDURE equalsLog(expected : log) : BOOLEAN;

END Log.
