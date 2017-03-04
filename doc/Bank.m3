CAPSULE Bank ;
IMPORT BankTypes;
  USECAPSULE ATM ;
  USECAPSULE Account ;
  VAR atm : ATM ;
  VAR account : Account ;
  CONNECT
    counter <=> account.movement;
    wall <=> atm.keyboard;
    wall <=> atm.cardSlot;
    wall <=> atm.cashSlot;
BEGIN

END Bank.
