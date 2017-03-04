CAPSULE INTERFACE CapConj ;
  IMPORT CapConjTypes AS CT;
  PORT p1 : CT.aInbOut ;
  PORT p2 : CT.aOutbIn ;
PORT test : PROTOCOL
   INCOMING MESSAGE init() ;
   INCOMING MESSAGE summary() ;
END
END CapConj.
