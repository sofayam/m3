CAPSULE INTERFACE Interest ;
PORT admin : PROTOCOL
    INCOMING MESSAGE setInterestRate(rate : REAL);
END;
PORT account : PROTOCOL
    OUTGOING MESSAGE deposit(sum : INTEGER);
    OUTGOING MESSAGE requestBalance();
    INCOMING MESSAGE updateAccount(sum : INTEGER);

END;
PORT mail : PROTOCOL
    OUTGOING MESSAGE statement(sum : INTEGER);
END
END Interest.
