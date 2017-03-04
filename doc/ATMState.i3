CAPSULE INTERFACE ATMState ;
FROM BankTypes IMPORT Card;

PORT keyboard : PROTOCOL
    INCOMING MESSAGE inputPIN(pin : INTEGER) ;
    INCOMING MESSAGE inputSum(sum : INTEGER) ;
END;
PORT cardSlot : PROTOCOL
    INCOMING MESSAGE insertCard(card : Card) ;
    OUTGOING MESSAGE returnCard();
END;
PORT cashSlot : PROTOCOL
    OUTGOING MESSAGE emitCash();
END;
PORT accounting : PROTOCOL
    OUTGOING MESSAGE withdraw(sum : INTEGER);
END;
END ATMState.
