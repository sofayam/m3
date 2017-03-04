IF NOT ."%M3_HOME%"==. GOTO m3homefound


ECHO You have not set M3_HOME
GOTO EndofScript

:m3homefound

set PYTHONPATH=%M3_HOME%\src;%M3_HOME%\src\rts;%M3_HOME%\lib;%M3_HOME%\lib\m3lib;m3lib


:EndofScript
