INTERFACE Text;

(* Basic operations on TEXT type *)

TYPE T = TEXT;

PROCEDURE Equal(t,u : T) : BOOLEAN;

PROCEDURE FromChars (READONLY a : ARRAY OF CHAR) : T ;

END Text.
