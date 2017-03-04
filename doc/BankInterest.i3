CAPSULE INTERFACE BankInterest ;
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
END;
PORT mail : PROTOCOL
    OUTGOING MESSAGE statement(sum : INTEGER);
END;
PORT admin : PROTOCOL
    INCOMING MESSAGE setInterestRate(rate : REAL);
END;
END BankInterest.
