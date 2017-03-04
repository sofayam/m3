CAPSULE CapStrictState ;
IMPORT Timer;
  STATE s1
    ON t1() =
      BEGIN
         SEND r1();
         NEXT s2;
      END t1;
  START = BEGIN
    NEXT s1
  END;
  STATE s2
    ON t2() =
      BEGIN
         SEND r1();
      NEXT s3;
      END t2;
  STATE s3;
BEGIN

END CapStrictState.
