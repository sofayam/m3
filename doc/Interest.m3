CAPSULE Interest ;
IMPORT Timer;
  VAR auditTimer : PERIODIC FIXED TIMER  DELAY 1 year ;     
      interestRate : REAL := 10.0;
  ACTIVITY setInterestRate (rate : REAL) = 
  BEGIN 
     interestRate := rate;
  END setInterestRate ;
  ACTIVITY updateAccount (sum : INTEGER) = 
     VAR accrued : REAL;
  BEGIN 
     accrued := FLOAT(sum) * interestRate / 100.0;
     SEND deposit(TRUNC(accrued));
     SEND statement(sum + TRUNC(accrued));
  END updateAccount ;
  CONNECT
    auditTimer -> requestBalance;

BEGIN
   Timer.Start(auditTimer)

END Interest.
