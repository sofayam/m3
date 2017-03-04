ECHO OFF
rem IF ERRORLEVEL 1 GOTO EndofScript 
IF NOT ."%M3_HOME%"==. GOTO m3homefound

ECHO You have not  set M3_HOME
GOTO :EndofScript

:m3homefound

call "%M3_HOME%"\bin\setcaprunpath.bat

rem python m3lib\%1CapMod.py %2 %3 %4 %5 %6 %7
python "%M3_HOME%"\src\runcap.py %*
:EndofScript