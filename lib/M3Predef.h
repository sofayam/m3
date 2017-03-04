/* 
   A lot of this is provisional just to get tests working
   maybe some of the predefineds need to be ruled out for c code generation 
*/
#define M3Predef__NEW(x) (x*)malloc(sizeof(x))
#define M3Predef__TRUNC(x) (int) x
#define M3Predef__FIRST(x) 0

typedef int M3Predef__BOOLEAN ;

#define ENUMLIT__M3Predef__BOOLEAN__FALSE 0
#define ENUMLIT__M3Predef__BOOLEAN__TRUE 1

typedef float M3Predef__REAL ;
typedef int M3Predef__INTEGER ;
