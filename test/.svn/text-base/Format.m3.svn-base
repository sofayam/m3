MODULE Format;
IMPORT Fmt, Text, Regress;

VAR

ca := ARRAY OF CHAR{'h','a','l','l','o'};

t : TEXT;

BEGIN
  Regress.init("Format");

  t := Fmt.Bool(FALSE) & " " & Fmt.Int(999);

  Regress.assertPass(Text.Equal(t, "FALSE 999"));

  t := Text.FromChars(ca);

  Regress.assertPass(Text.Equal(t,"hallo"));

  Regress.summary();

END Format.
