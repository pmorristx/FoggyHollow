import jarray
import jmri
import java.util.Random
from MineTrain import MineTrain

class Hoist(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        #  Get occupancy sensors
        self.topSensor = sensors.provideSensor("Hoist Top")
        self.bottomSensor = sensors.provideSensor("Hoist Bottom")        
        #
        #  Get the shutdown switch
        self.shutdownSwitch = sensors.getSensor("Hoist Auto")

        #
        #  Initialize the hoist cavern turnout to the main track
        self.throttle = self.getThrottle(99, False) 

        return
    #
    #  Clean shutdown when switch is turned off.  Return train to the front of the layout (Hoist Cavern Entrance)
    #  and shut the train down.
    def shutdown(self):
        #
        self.throttle.setSpeedSetting(0.0)

    def setDirection(self, direction) :
        if (direction == "DOWN") :
            self.throttle.setIsForward(True)
        else:
            self.throttle.setIsForward(False)
    
    def doBottom(self) :
        self.throttle.setSpeedSetting(0.0)
        self.waitMsec(5000 + java.util.Random().nextInt(3000))
        if (java.util.Random().nextInt(100) < 50) :
            self.setDirection("DOWN")
            self.throttle.setSpeedSetting(0.1)
            self.waitMsec(4000)
            self.throttle.setSpeedSetting(0.0)
            self.waitMsec(4000 + java.util.Random().nextInt(1000))
        self.setDirection("UP")
        self.throttle.setSpeedSetting(0.1)

    def doTop(self) :
        self.throttle.setSpeedSetting(0.0)
        self.waitMsec(5000 + java.util.Random().nextInt(3000))
        self.setDirection("DOWN") #this is redundant
        
            
    #  Main loop repeatedly called until False is returned.
    def handle(self):

        self.setDirection("DOWN")
        self.throttle.setSpeedSetting(0.1)

        self.waitSensorActive(self.bottomSensor)

        if (self.shutdownSwitch.getState() != ACTIVE) :
            self.shutdown()
            return False        

        self.doBottom()

        if (self.shutdownSwitch.getState() != ACTIVE) :
            self.shutdown()
            return False        

        self.waitSensorActive(self.topSensor)

        if (self.shutdownSwitch.getState() != ACTIVE) :
            self.shutdown()
            return False        

        self.doTop()

        if (self.shutdownSwitch.getState() != ACTIVE) :
            self.shutdown()
            return False
        
        return self.shutdownSwitch.getState() == ACTIVE
# end of class definition

# start one of these up
Hoist().start()
