INTERFACE Traffic;

TYPE 
  vk = {car, truck, motorcycle};
  MetricWeight = SCALED INTEGER  {g * 1000 = kg * 1000 = tonne};
  vehicle = RECORD 
    CASE kind : vk OF
    |  vk.truck => 
         axels : [2..10] := 2 ;
         weight : MetricWeight ;
    |  vk.car => 
         doors : [2..5] ;
    ELSE (* mandatory, shows we have not forgotten *) 
    END;
    topSpeed : [30 .. 300];
  END;

VAR
  myCar   := vehicle{vk.car, doors := 3, topSpeed := 210};
  myTruck := vehicle{vk.truck, weight := 5 tonne}; 
  myBike  := vehicle{vk.motorcycle, topSpeed := 200};
END Traffic.
