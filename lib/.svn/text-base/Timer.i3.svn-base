INTERFACE Timer;


TYPE Time = SCALED INTEGER {ps * 1000 = ns  * 1000 = us 
                               * 1000 = ms  * 1000 = s 
                               * 60   = min * 60   = hour 
                               * 24   = day * 365  = year};

PROCEDURE Start(VAR T : TIMER);
PROCEDURE Stop(VAR T : TIMER);
PROCEDURE Change(VAR T : TIMER; newValue : Time);
PROCEDURE GetElapsed() : Time;
END Timer.
