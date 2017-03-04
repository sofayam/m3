CAPSULE INTERFACE Bank ;
IMPORT BankTypes;
PORT wall : PROTOCOL
    INCOMING MESSAGE inputPIN(pin : INTEGER) ;
    INCOMING MESSAGE inputSum(sum : INTEGER) ;
    INCOMING MESSAGE insertCard(card : BankTypes.Card) ;
    OUTGOING MESSAGE returnCard();
    OUTGOING MESSAGE emitCash();
END;
PORT counter : PROTOCOL
    INCOMING MESSAGE deposit(sum : INTEGER) ;
END
END Bank.
