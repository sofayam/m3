GENERIC MODULE Stack(Elem);
IMPORT IO, Fmt;
REVEAL T = BRANDED OBJECT 
  n: INTEGER; 
  a: REF ARRAY OF Elem.T;
END;

PROCEDURE Create(): T = 
  BEGIN 
    RETURN NEW(T, n := 0, a := NIL) 
  END Create;

PROCEDURE Push(VAR s: T; x: Elem.T) = 
  BEGIN
    (*IO.Put("Pushing " & Fmt.Int(x) & "\n");  *)
    IF s.a = NIL THEN
      (*IO.Put("Creating Array\n"); *)
      s.a := NEW (REF ARRAY OF Elem.T, 2);
      (* IO.Put("Created Array size " & Fmt.Int(LAST(s.a^)) & "\n"); *)
    ELSIF s.n > LAST(s.a^) THEN
      WITH temp = NEW(REF ARRAY OF Elem.T, 2*NUMBER(s.a^)) DO 
        FOR i := 0 TO LAST(s.a^) DO 
          (* IO.Put("Copy " & Fmt.Int(s.a[i])); *)
          temp[i] := s.a[i];
        END;
        s.a := temp;
      END 
    END;
    s.a[s.n] := x;
    INC(s.n);
  END Push;

PROCEDURE Pop(VAR s: T) : Elem.T = 
  VAR
    res : INTEGER;
  BEGIN
    DEC(s.n);
    res := s.a[s.n];
    (* IO.Put("Popping " & Fmt.Int(res) & "\n");  *)
    RETURN res;
  END Pop;

BEGIN END Stack.

