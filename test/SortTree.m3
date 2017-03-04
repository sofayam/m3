MODULE SortTree;
IMPORT Random, IO, Tree;
IMPORT Regress ;
CONST
  limit = 10;
TYPE 
  collection = ARRAY [1..limit] OF INTEGER;
VAR
  top : Tree.Node;
  expected := collection{0, 14, 31, 37, 53, 53, 57, 63, 72, 79};
  collector : collection ;
  length : INTEGER ;
  success := TRUE ;
BEGIN
  Regress.init("SortTree");
  FOR i := 1 TO limit DO
    top := Tree.enter(Random.next(100), top);
  END;
  (* Tree.dump(top); *)
  length := Tree.collect(top, collector, 1);
  FOR i := 1 TO limit DO
    success := success AND (collector[i] = expected[i])
  END;
  Regress.assertPass(success);
  Regress.assertPass(collector = expected); 
  Regress.summary();
  
END SortTree.
