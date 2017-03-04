rm *.c
rm *.exe
m3.sh -c --main IfTest.m3
ccomp.sh IfTest
m3.sh -c --main ForTest.m3
ccomp.sh ForTest
m3.sh -c --main ImpAs.m3
ccomp.sh ImpAs ../lib/Text.o ../lib/Fmt.o 
m3.sh -c --main ArrayTest.m3
ccomp.sh ArrayTest ../lib/Text.o ../lib/Fmt.o
m3.sh -c RecInt.i3
m3.sh -c --main RecTest.m3
ccomp.sh RecTest
m3.sh -c --main RefCTest.m3
ccomp.sh RefCTest
m3.sh -c --main ExprTest.m3
ccomp.sh ExprTest
m3.sh -c --main EnumTest.m3
ccomp.sh EnumTest
m3.sh -c --main ComplExp.m3
ccomp.sh ComplExp
m3.sh -c ConstInt.i3
m3.sh -c --main Const.m3
ccomp.sh Const
m3.sh -c --main Proc.m3
ccomp.sh Proc
m3.sh -c EnumInt.*3 
m3.sh -c --main SubType.m3
ccomp.sh SubType EnumInt.c
m3.sh -c --main AnonTest.m3
ccomp.sh AnonTest
m3.sh -c --main ArrayCTest.m3
ccomp.sh ArrayCTest
m3.sh -c ElabSub1.i3
m3.sh -c ElabSub2.i3
m3.sh -c ElabSub1.m3
m3.sh -c ElabSub2.m3
m3.sh -c --main ElabTest.m3
ccomp.sh ElabTest ElabSub1.c ElabSub2.c
m3.sh -c --main BoolCTest.m3
ccomp.sh BoolCTest
m3.sh -c --main WithC.m3
ccomp.sh WithC
m3.sh -c --main Case.m3 
ccomp.sh Case ../lib/Text.o
m3.sh -c --main Exit.m3
ccomp.sh Exit 

./IfTest.exe
./ForTest.exe
./ImpAs.exe
./ArrayTest.exe
./RecTest.exe
./RefCTest.exe
./ExprTest.exe
./EnumTest.exe
./ComplExp.exe
./Const.exe
./Proc.exe
./SubType.exe
./AnonTest.exe
./ArrayCTest.exe
./ElabTest.exe
./BoolCTest.exe
./WithC.exe
./Case.exe
./Exit.exe