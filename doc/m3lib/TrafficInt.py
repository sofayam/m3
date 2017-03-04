import M3Objects
import M3Types
import M3Predefined
import M3TypeLib
import M3ProcLib
M3TL=M3TypeLib.internaliseTypes(r'm3lib/TrafficMod')
vk=M3TL[28].finalTipe
MetricWeight=M3Types.M3IntegerBase.makeScaledType([(u'tonne', 1000000), (u'kg', 1000), (u'g', 1)])
vehicle=M3TL[30].finalTipe
myCar=vehicle.construct(vk.withVal('car'),doors=M3Types.M3IntegerBase.createObject(3),topSpeed=M3Types.M3IntegerBase.createObject(210))
myTruck=vehicle.construct(vk.withVal('truck'),weight=M3Types.M3IntegerBase.createObject(5 * 1000000))
myBike=vehicle.construct(vk.withVal('motorcycle'),topSpeed=M3Types.M3IntegerBase.createObject(200))
