CAPSULE BankInterest ;
IMPORT BankTypes;
  USECAPSULE ATM ;
  USECAPSULE Account ;
  USECAPSULE Interest ;
  VAR atm : ATM ;
  VAR account : Account ;
  VAR interest : Interest ;
  CONNECT
     counter <=> account.movement;
     wall <=> atm.keyboard;
     wall <=> atm.cardSlot;
     wall <=> atm.cashSlot;
     admin <=> interest.admin;
     mail <=> interest.mail;
     atm.accounting <=> account.movement;
     interest.account <=> account.information;

(*    inputPIN -> atm.inputPIN;
    inputSum -> atm.inputSum;
    insertCard -> atm.insertCard;
    atm.returnCard -> returnCard;
    atm.emitCash -> emitCash;
    atm.withdraw -> account.withdraw;
    deposit -> account.deposit;
    interest.requestBalance -> account.requestBalance;
    account.balance -> interest.updateAccount;
    interest.deposit -> account.deposit;
    setInterestRate -> interest.setInterestRate;
    interest.statement -> statement; *)
BEGIN

END BankInterest.
