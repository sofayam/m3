import os
#
# Global settings 
#

systemFileExtension   = ".sys"
macroFileExtension    = ".mac"
inputFileExtension    = ".inp"
preproFileExtension   = ".pre"
protocolFileExtension = ".pro"
resultFileExtension   = ".res"
traceFileExtension   = ".trc"

# TBD set up paths here
outputPath = "res" + os.sep      # TBD deal with system dependent path seperators


sysFile = ""
scriptFile = ""
resFile = ""

#
# Ragbag of options information and 
#
assertRaises = True

failure = False

trace = False

graphicalTrace = None
tracePort = 9998
stepCommand = "STEP"

results = None
