call cleanup
call m3 -c --main IfTest.m3
call ccomp IfTest
call m3 -c --main ForTest.m3
call ccomp ForTest
call m3 -c --main ImpAs.m3
call ccomp ImpAs ..\lib\Text.obj ..\lib\Fmt.obj 
call m3 -c --main ArrayTest.m3
call ccomp ArrayTest ..\lib\Text.obj ..\lib\Fmt.obj
call m3 -c RecInt.i3
call m3 -c --main RecTest.m3
call ccomp RecTest
call m3 -c --main RefCTest.m3
call ccomp RefCTest
call m3 -c --main ExprTest.m3
call ccomp ExprTest
call m3 -c --main EnumTest.m3
call ccomp EnumTest
call m3 -c --main Complexp.m3
call ccomp ComplExp
call m3 -c ConstInt.i3
call m3 -c --main Const.m3
call ccomp Const
call m3 -c --main Proc.m3
call ccomp Proc
call m3 -c EnumInt.*3 
call m3 -c --main SubType.m3
call ccomp SubType EnumInt.c
call m3 -c --main AnonTest.m3
call ccomp AnonTest
call m3 -c --main ArrayCTest.m3
call ccomp ArrayCTest
call m3 -c ElabSub1.i3
call m3 -c ElabSub2.i3
call m3 -c ElabSub1.m3
call m3 -c ElabSub2.m3
call m3 -c --main ElabTest.m3
call ccomp ElabTest ElabSub1.c ElabSub2.c
call m3 -c --main BoolCTest.m3
call ccomp BoolCTest
call m3 -c --main WithC.m3
call ccomp WithC
call m3 -c --main Case.m3 
call ccomp Case ..\lib\Text.obj
call m3 -c --main Exit.m3
call ccomp Exit 

IfTest.exe
ForTest.exe
ImpAs.exe
ArrayTest.exe
RecTest.exe
RefCTest.exe
ExprTest.exe
EnumTest.exe
Complexp.exe
Const.exe
Proc.exe
SubType.exe
AnonTest.exe
ArrayCTest.exe
ElabTest.exe
BoolCTest.exe
WithC.exe
Case.exe
Exit.exe