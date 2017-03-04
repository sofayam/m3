INTERFACE CapAgrTypes ;

TYPE start = PROTOCOL
   INCOMING MESSAGE startMsg () ;
END ;
TYPE middle = PROTOCOL
   INCOMING MESSAGE middleMsg () ;
END ;
TYPE end = PROTOCOL
   INCOMING MESSAGE endMsg () ;
END ;

TYPE wholeLoad = start @ ~ (middle @ end) ;

TYPE wholeLoadConj = ~ wholeLoad ;

TYPE test = PROTOCOL 
   INCOMING MESSAGE start();
   INCOMING MESSAGE summary();
END;
END CapAgrTypes.
