import RTSOptions
import Global
RTSOptions.setOptions()
cap = __import__("%sCapMod" % Global.sysFile)
cap.runcap()

