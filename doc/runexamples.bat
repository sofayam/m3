call runcap ATM -cpro -s3
call runcap Interest -cpro -s3
call runcap Account -cpro -s3
call runcap Bank -cpro -s3
call runcap BankInterest -cpro -s3
call runcap ATMTimeout -cpro -s3
call runcap SimplePar -cpro -s3
call runcap BankInterest Withdrawals -cpro -s3
call runcap ParTop -cpro -s3
call runcap ParTop -cpro -ppar1=proca,par2=procb -s3 -rpar
call runcap ParTop -cpro -ppar1=proca,par2=procb --system-architecture=Arch -s3 -rparsys
call python pyact.py pyact --raw-python -cpro -s3
call python pytimer.py pytimer --raw-python -cpro -s3
call python pytrigger.py pytrigger --raw-python -cpro -s3
call python C1.py C1 --raw-python -cpro -s3
