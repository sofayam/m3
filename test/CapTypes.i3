INTERFACE CapTypes;

TYPE CapRec = RECORD
   x : INTEGER ;
   b : BOOLEAN ;
END ;
TYPE Color = {Red, Green, Blue};
TYPE CapArray = ARRAY [1..4] OF Color;
TYPE CapSet = SET OF Color;
CONST FullSet = CapSet{Color.Red, Color.Green, Color.Blue};
TYPE CapOpen = ARRAY OF CapRec;
TYPE CapDict = DICT OF CapRec;
TYPE CapList = LIST OF CapRec;
END CapTypes.
