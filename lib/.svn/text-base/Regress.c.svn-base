#include "Regress.h"
#include <stdio.h>
char* testname;
int passed = 1;
int testctr = 0;
void Regress__init(char* Regress__name) {
  testname = Regress__name;
}
void Regress__assertPass(int Regress__cond) {
  testctr++;
  if (!Regress__cond) {
    passed = 0;
    printf("%sFAILED on test %d\n", testname,testctr);
  }
}
void Regress__summary() {
  char *verdict = passed ? "PASSED" : "FAILED";
  printf("%s (C) : %s (%d)\n",testname,verdict,testctr);
}
