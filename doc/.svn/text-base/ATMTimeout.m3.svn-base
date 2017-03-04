CAPSULE ATMTimeout ;
FROM BankTypes IMPORT Card;
  IMPORT Timer;
  VAR cardInfo : Card ;
  VAR inputTimeout : ONESHOT FIXED TIMER  DELAY 15 s ;
  START = BEGIN
    NEXT empty
  END;
  STATE empty
    ON insertCard(card : Card) =
      BEGIN
         cardInfo := card;
         Timer.Start(inputTimeout);
         NEXT inserted;
      END insertCard;
  STATE authorized
    ON inputSum(sum : INTEGER) =
      BEGIN
         SEND withdraw(sum);	
         SEND emitCash();
         SEND returnCard();
         NEXT empty;
      END inputSum;
    ON giveUp() =
      BEGIN
         SEND returnCard();
         NEXT empty;
      END giveUp;
  STATE inserted
    ON inputPIN(pin : INTEGER) =
      BEGIN
        Timer.Start(inputTimeout);
        IF pin = cardInfo.encodedPIN THEN
           NEXT authorized;
        END 
      END inputPIN;
    ON giveUp() =
      BEGIN
         SEND returnCard();
         NEXT empty;
      END giveUp;
  
  CONNECT
    inputTimeout -> giveUp;
BEGIN

END ATMTimeout.
