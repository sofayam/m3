MODULE Multi3;
IMPORT Regress;
TYPE
PROCEDURE confirm(x,y :INTEGER) =
BEGIN
  Regress.assertPass(x = y);
END confirm;
BEGIN
END Multi3.
