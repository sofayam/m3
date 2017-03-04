MODULE OpRef;
(*
REVEAL T = BRANDED REF RECORD
  x : INTEGER ;
END;
*)
PROCEDURE Use(t : T) =
BEGIN
  t.x := 99;
END Use;
PROCEDURE Get():T = 
BEGIN
  RETURN T{};
END Get;

BEGIN

END OpRef.
