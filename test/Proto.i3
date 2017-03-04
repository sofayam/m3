INTERFACE Proto;

TYPE Color = {red, blue, green};

TYPE ParamType = RECORD
   b : BOOLEAN ;
   c : Color ;
END;

TYPE ProtoType = PROTOCOL 
   INCOMING MESSAGE m1 (param : ParamType); 
END;

END Proto.
