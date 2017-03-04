import M3Objects
import M3Types
import M3Predefined
from TrafficInt import *
import IOInt as IO
import M3TypeLib
import M3ProcLib
M3TL=M3TypeLib.internaliseTypes(r'm3lib/TrafficMod')
from Statistics import M3incStat
def TrafficMain():
 IO.Put(M3Predefined.M3IMAGE(myCar))
 IO.Put(M3Predefined.M3IMAGE(myTruck))
 IO.Put(M3Predefined.M3IMAGE(myBike))
TrafficMain()
