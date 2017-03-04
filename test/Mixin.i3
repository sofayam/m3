INTERFACE Mixin;
IMPORT Part1;

TYPE Mixer = OBJECT
METHODS
  touch() := TouchMe;
END;

PROCEDURE TouchMe(m : Mixer);

REVEAL Part1.T <: Mixer;

END Mixin.
