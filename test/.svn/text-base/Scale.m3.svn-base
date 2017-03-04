MODULE Scale;
IMPORT Regress,IO;
IMPORT ScaleTypes AS ST;

VAR v : ST.Volts := 10V;
VAR t : ST.Time := (1 years) - (1 seconds);
VAR NoVolts : ST.Volts := 0V;

BEGIN
  Regress.init("Scaling");
  Regress.assertPass(v = 10 V);
  Regress.assertPass(IMAGE(NoVolts) = "0 mV");
  Regress.assertPass(IMAGE(-v) = "-10 V");
  Regress.assertPass(IMAGE(v) = "10 V");
  v := v + 1 mV;
  Regress.assertPass(IMAGE(v) = "10 V + 1 mV");
  Regress.assertPass(IMAGE(t) = "364 days + 23 hours + 59 minutes + 59 seconds");

  v := 10 V * 10 years; (* will not cause a warning *)
  Regress.summary();

END Scale.
