CAPSULE INTERFACE Account ;
PORT movement : PROTOCOL
    INCOMING MESSAGE deposit(sum : INTEGER) ;
    INCOMING MESSAGE withdraw(sum : INTEGER) ;
END;
PORT information : PROTOCOL
    INCOMING MESSAGE requestBalance() ;
    OUTGOING MESSAGE balance(sum : INTEGER) ;
END;
END Account.
