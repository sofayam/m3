CAPSULE ATMSafe ;
FROM BankTypes IMPORT Card;
  VAR cardInfo : Card ;
  TRIGGER shadyCustomer ON failureCount = 3;
  VAR failureCount : INTEGER := 0;
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
        ELSE
           failureCount := failureCount + 1;
        END 
      END inputPIN;
    ON reject() =
      BEGIN
         failureCount := 0;
      NEXT empty;
      END reject;
  CONNECT
    shadyCustomer -> reject;
 
BEGIN

END ATMSafe.
