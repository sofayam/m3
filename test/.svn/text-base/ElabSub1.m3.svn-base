MODULE ElabSub1;
IMPORT ElabSub2;
IMPORT Regress;
PROCEDURE allClear() = 
BEGIN
  Regress.assertPass(status = statusType.done);
  ElabSub2.tickle(); (* Workaround for Issue No 131 *)
  Regress.assertPass(ElabSub2.status = ElabSub2.statusType.done);
END allClear;
BEGIN
  status := statusType.done;
END ElabSub1.
