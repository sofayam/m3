MODULE Mixin;
IMPORT Part1;
PROCEDURE TouchMe(m : Mixer) =
BEGIN
  Part1.touched := TRUE;
END TouchMe;
BEGIN
END Mixin.
