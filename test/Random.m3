MODULE Random;
IMPORT IO;
VAR
  IM := 139968 ;
  IA := 3877 ;
  IC := 29573 ;
  last := 42 ;

PROCEDURE next(max : INTEGER) : INTEGER =
  VAR res : INTEGER;
  BEGIN
    last := (last * IA + IC) MOD IM  ;
    res := max * last DIV IM ;
    (* IO.PutInt(res); *)
    RETURN res
  END next;


BEGIN

(*

Here is the python code for the above which you can use
to verify the results for the tree insert test if you don't
believe me

im = 139968
ia = 3877
ic = 29573
last = 42

def next(max):
    global last
    last = (last * ia + ic) % im
    return max * last / im

for i in range(100):
    print next(100)

*) 

END Random.
