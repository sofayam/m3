MODULE OpaqueUser;
IMPORT  Opaque, Regress;
VAR

  h : Opaque.hidden;
  i : INTEGER;

BEGIN
  Regress.init("Opaque");
  h := Opaque.makeHidden(99);
  (* h.i := 77; *)
  i := Opaque.openHidden(h);
  Regress.assertPass(i = 99);
  Regress.summary()
END OpaqueUser.
