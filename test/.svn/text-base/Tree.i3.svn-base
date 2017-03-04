INTERFACE Tree;
TYPE 
  Node = REF RECORD 
    val : INTEGER ;
    less, more : Node;
  END;
PROCEDURE enter (val : INTEGER; n : Node) : Node ;
PROCEDURE dump (n : Node);
PROCEDURE collect(n : Node; READONLY collector : ARRAY OF INTEGER; ctr : INTEGER) : INTEGER ;
END Tree.
