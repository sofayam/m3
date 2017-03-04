import m3
import Options
from CapsuleEntity import CapsuleEntity
Options.setOptions()

args = Options.args
Options.options.generate = False

if len(args) != 1:
    print "invoke with one argument"
else:
    top = CapsuleEntity("top",specnode=m3.compile(args[0] + ".ci3o"),bodynode=m3.compile(args[0] + ".cm3o"))
    
    top.elabChildren()

    top.createMessagePoints(top=True)

    top.installConnections()

    top.findActivities()

    top.printtree()
