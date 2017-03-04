cd ..\lib
call m3 -c Fmt.i3 IO.i3 Regress.i3 Text.i3
cl /c Fmt.c
cl /c IO.c
cl /c Regress.c
cl /c Text.c