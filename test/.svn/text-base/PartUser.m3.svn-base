MODULE PartUser;
IMPORT Part1, MixUser;
IMPORT Regress;

VAR 
  t : Part1.T;
  x : INTEGER;
BEGIN
  Regress.init("Partial");
  t := Part1.make();
  x := Part1.get(t);
  Regress.assertPass(x = 99);
  t := Part1.make();
  x := Part1.get(t);
  Regress.assertPass(x = 100);
  MixUser.Use(t);
  Regress.assertPass(Part1.touched);
  Regress.summary()
END PartUser.
