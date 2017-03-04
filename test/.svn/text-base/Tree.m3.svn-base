MODULE Tree ;
IMPORT IO;

PROCEDURE enter (val : INTEGER; n : Node) : Node =
BEGIN
  IF n = NIL THEN
(*    IO.Put("Entering");
    IO.PutInt(val); *)
    RETURN NEW(Node, val := val); 
  ELSIF val < n.val THEN
    n.less := enter(val, n.less)
  ELSE
    n.more := enter(val, n.more)
  END;
  RETURN n;
END enter ;

PROCEDURE dump (n : Node) =
BEGIN
  IF n # NIL THEN 
    dump(n.less);
    IO.PutInt(n.val);
    dump(n.more);
  END;
END dump;

PROCEDURE collect(n : Node; READONLY collector : ARRAY OF INTEGER; ctr : INTEGER) : INTEGER = 
BEGIN
  IF n # NIL THEN
    ctr := collect(n.less, collector, ctr);
    (* IO.PutInt(ctr); *)
    collector[ctr] := n.val;
    ctr := ctr + 1;
    ctr := collect(n.more, collector, ctr);
  END;
  RETURN ctr;
END collect;
 
BEGIN
END Tree.
