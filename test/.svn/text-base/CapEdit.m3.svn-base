CAPSULE CapEdit;
  USECAPSULE PingPong;
  VAR pp : PingPong;
  ACTIVITY foo () = BEGIN END foo ;
  VAR x : INTEGER;
  VAR y : INTEGER;
  VAR z : INTEGER;
  VAR o : INTEGER;
  ACTIVITY foo1 () = BEGIN END foo1 ;
  VAR o1 : INTEGER;
  ACTIVITY act23 () = BEGIN END act23 ;
  ACTIVITY bababoom () = BEGIN END bababoom ;
  ACTIVITY b1 () =
    WRITES y ; BEGIN END b1 ;
  ACTIVITY fff () = BEGIN END fff ;
  ACTIVITY ff () = BEGIN END ff ;
  ACTIVITY aaa () = BEGIN END aaa ;
  ACTIVITY foofoo () = BEGIN END foofoo ;
  ACTIVITY f12 () = BEGIN END f12 ;
  ACTIVITY f13 () = BEGIN END f13 ;
  ACTIVITY sssss () = BEGIN END sssss ;
  TRIGGER t7 ON TRUE ;
  VAR t9 : TIMER ;
CONNECT
  ping -> pp.ping;
  pong -> pp.pong;
  pp.innerreply -> outerreply;
    t7 -> foo;
BEGIN
END CapEdit.
