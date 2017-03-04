INTERFACE Fmt;

(* Converts basic data types into text, for use with the IO package 
   Present to provide rudimentary compatibility with standard Modula-3 
   It is recommended that you use the more powerful new built-in IMAGE
   procedure instead *)

PROCEDURE Bool (b: BOOLEAN) : TEXT;

PROCEDURE Char (c : CHAR) : TEXT;

(*TYPE Base = [2..16];*)

PROCEDURE Int (n : INTEGER) : TEXT ;

END Fmt.
