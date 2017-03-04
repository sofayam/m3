CAPSULE PingPong;
IMPORT Regress, IO;
START = 
BEGIN
  NEXT s1;
END;

STATE s1 
   ON ping() =
     VAR starting : BOOLEAN;
   BEGIN
      starting := x = 0;
      Regress.assertPass(starting);
      x := 1;
      NEXT s2
   END ping;
STATE s2 
   ON pong() =
     VAR pinged : BOOLEAN;
   BEGIN
      pinged := x = 1;
      Regress.assertPass(pinged);
      SEND innerreply();
      x := 2;
      NEXT s1
   END pong;
  VAR x : INTEGER := 0;
  ACTIVITY check () = 
     VAR ponged := FALSE;
  BEGIN 
     ponged := x = 2;
     Regress.assertPass(ponged)
  END check ;

BEGIN

END PingPong.
