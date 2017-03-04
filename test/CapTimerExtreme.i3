CAPSULE INTERFACE CapTimerExtreme ;
PORT p1 : PROTOCOL
    INCOMING MESSAGE start() ;
    OUTGOING MESSAGE smallAlarm() ;
    OUTGOING MESSAGE mediumAlarm() ;
    OUTGOING MESSAGE bigAlarm() ;
    INCOMING MESSAGE summary() ;
END;
END CapTimerExtreme.
