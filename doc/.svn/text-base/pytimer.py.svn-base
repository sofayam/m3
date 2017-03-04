import Time
import RTSTypes
# Defining a capsule
class pytimer(RTSTypes.M3CapsuleRuntimeType):
    
    # Defining an activity (which is simply a method of the capsule)
    def timeact(self):
        # Application code
        self.i += 1
        print "Timer Demo %s" % self.i
        # Sending a message
        self.send(originator=self,
                  level=self.level,
                  msgName='foo',
                  myParam=self.i)

    # Defining the capsule contents and structure in the constructor 
    def __init__(self,level):
        # Call parent constructor
        RTSTypes.M3CapsuleRuntimeType.__init__(self,level)
        # Defining a timer
        self.myTimer=RTSTypes.M3TimerRuntimeType(delay=10*Time.F_psec,
                                                 periodic=True,
                                                 changeable=False).createObject()
        # Connecting the timer to an activity/message
        self.myTimer.connect(context=self,         
                             srcMsg ='',  # not needed by timer         
                             destMsg = 'timeact',  
                             destObj = self,
                             level = level)
        # Start the timer
        self.myTimer.start()
        # Store level for use by "send" later
        self.level = level
        # Application specific data
        self.i = 0
if __name__ == '__main__':
    import Simulator
    Simulator.run(pytimer(1))
