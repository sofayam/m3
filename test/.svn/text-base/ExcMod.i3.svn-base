INTERFACE ExcMod;

EXCEPTION hell;
EXCEPTION cain;

TYPE rec = RECORD x : INTEGER END;
EXCEPTION rPackage (rec);
EXCEPTION iPackage (INTEGER);
          
TYPE 
  exceptions = {cain, hell};

PROCEDURE raiseIt(e : exceptions) RAISES {hell, cain} ; 

PROCEDURE raiseiPack(i : INTEGER) RAISES {iPackage} ;

PROCEDURE raiserPack(i : INTEGER) RAISES {rPackage} ;

END ExcMod.
