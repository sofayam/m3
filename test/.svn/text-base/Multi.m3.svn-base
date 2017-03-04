MODULE Multi EXPORTS Multi1, Multi2; 

IMPORT Multi3, Regress;

PROCEDURE doTest() =
  BEGIN
    x := 9;
    y := 11;
    Multi3.confirm(x+y,20);
  END doTest;
BEGIN
  Regress.init("Multi");
  doTest();
  Regress.summary();
END Multi. 
  
