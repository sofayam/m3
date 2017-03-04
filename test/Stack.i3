GENERIC INTERFACE Stack (Elem);
TYPE T <: REFANY;
PROCEDURE Create(): T;
PROCEDURE Push(VAR s: T; x: Elem.T);
PROCEDURE Pop(VAR s: T) : Elem.T;
END Stack.
