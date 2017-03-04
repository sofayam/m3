ECHO OFF
IF ERRORLEVEL 1 GOTO EndofScript 
IF NOT ."%M3_HOME%"==. GOTO m3homefound

ECHO You have not set M3_HOME
GOTO :EndofScript

:m3homefound

call "%M3_HOME%"\bin\setcaprunpath.bat

python m3lib\%1Mod.py %*

:EndofScript