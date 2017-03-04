MODULE MixUser;
IMPORT Mixin;
IMPORT Part1;
PROCEDURE Use(t : Part1.T) =
BEGIN
  t.touch()
END Use;

BEGIN
END MixUser.
