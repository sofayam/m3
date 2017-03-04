@ECHO OFF
call err0.bat
IF ERRORLEVEL 1 GOTO EndofScript 
IF NOT ."%M3_HOME%"==. GOTO m3homefound

ECHO You have not set M3_HOME
GOTO EndofScript

:m3homefound

call "%M3_HOME%"\bin\setcomppath.bat

python "%M3_HOME%\src\m3.py" %1 %2 %3 %4 %5 %6

:EndofScript

