runcap.sh ATM -cpro -s3
runcap.sh Interest  -cpro -s3
runcap.sh Account  -cpro -s3
runcap.sh Bank  -cpro -s3
runcap.sh BankInterest  -cpro -s3
runcap.sh ATMTimeout  -cpro -s3
runcap.sh SimplePar  -cpro -s3
runcap.sh BankInterest Withdrawals -cpro -s3
runcap.sh TopPar -cpro -s3
runcap.sh TopPar -cpro -ppar1=proca,par2=procb -s3 -rpar
runcap.sh TopPar -cpro -ppar1=proca,par2=procb --system-architecture=Arch -s3 -rparsys

. $M3_HOME/bin/setcaprunpath.sh
python pyact.py pyact --raw-python -cpro -s3
python pytimer.py pytimer --raw-python -cpro -s3
python pytrigger.py pytrigger --raw-python -cpro -s3
python C1.py C1 --raw-python -cpro -s3