CAPSULE ATMState ;
FROM BankTypes IMPORT Card;
  VAR cardInfo : Card ;
  START = BEGIN
    NEXT empty
  END;
  STATE empty
    ON insertCard(card : Card) =
      BEGIN
         cardInfo := card;
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
  STATE inserted
    ON inputPIN(pin : INTEGER) =
      BEGIN
        IF pin = cardInfo.encodedPIN THEN
           NEXT authorized;
        END 
      END inputPIN;
BEGIN

END ATMState.
