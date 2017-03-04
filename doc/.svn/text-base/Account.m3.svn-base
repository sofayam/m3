CAPSULE Account ;
  VAR money : INTEGER := 0;
  ACTIVITY deposit (sum : INTEGER) = 
    VAR newtotal : INTEGER;
  BEGIN
    newtotal := money + sum;
    money := newtotal;
  END deposit ;
  ACTIVITY withdraw (sum : INTEGER) = 
    VAR newtotal : INTEGER;	 
  BEGIN 
    newtotal := money - sum;
    money := newtotal;
  END withdraw ;
  ACTIVITY requestBalance () = 
  BEGIN 
     SEND balance(sum := money);
  END requestBalance ;
  
BEGIN

END Account.
