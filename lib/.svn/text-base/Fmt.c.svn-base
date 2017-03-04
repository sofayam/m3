#include <stdio.h>
char* Fmt__Bool(short Fmt__b) {
  if (Fmt__b) {
    return "TRUE";
  } else {
    return "FALSE";
  };
}

char* Fmt__Char( char Fmt__c ) {
  char*  res = (char*)malloc(2);
  sprintf(res,"%c",Fmt__c);
  return res;
}

char* Fmt__Int( int Fmt__n) {
  char* res = (char*)malloc(10);
  sprintf(res, "%d", Fmt__n);
  return res;
}
