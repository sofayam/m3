CAPSULE ATM ;
FROM BankTypes IMPORT Card;

  TYPE CardState = {Empty, Inserted, Authorized} ;

  VAR cardInfo : Card ;
  VAR cardState : CardState := CardState.Empty;

  ACTIVITY inputPIN (pin : INTEGER) =
  BEGIN
     IF cardState = CardState.Inserted  AND 
        pin = cardInfo.encodedPIN 
     THEN
        cardState := CardState.Authorized;
     END 
  END inputPIN ;

  ACTIVITY insertCard (card : Card) = 
  BEGIN 
     cardState := CardState.Inserted;
     cardInfo := card;
  END insertCard ;

  ACTIVITY inputSum (sum : INTEGER) = 
  BEGIN 
    IF cardState = CardState.Authorized THEN
       SEND withdraw(sum);	
       SEND emitCash();
       SEND returnCard();
       cardState := CardState.Empty;
    END;
  END inputSum ;
BEGIN

END ATM.
