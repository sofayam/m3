INTERFACE IO;

(* The following perform simple output to the terminal, for testing 
   purposes it is recommended that you use the features provided by
   the Results Interface *)

PROCEDURE Put(T:TEXT);

PROCEDURE PutInt(I:INTEGER);

PROCEDURE PutReal(f:REAL);

PROCEDURE PutChar(C : CHAR);

END IO.
