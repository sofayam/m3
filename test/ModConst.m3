MODULE ModConst;
IMPORT IO, Regress;
TYPE
  lit = LIST OF INTEGER ;
  dit = DICT OF INTEGER ;

VAR 
  li := lit{4,3,2,1};
  di := dit{"foo" := 2, "bar" := 4, "baz" := 1, "bla" :=  3};
  res := 0;
BEGIN
  Regress.init("Modeling Type Constructors");
  FOREACH i IN li DO
    res := res + i;
  END ;
  Regress.assertPass(res = 10);
  res := 0;
  FOREACH k IN KEYS(di) DO
    res := res + di[k]
  END ;
  Regress.assertPass(res = 10);
  Regress.summary();
END ModConst.
