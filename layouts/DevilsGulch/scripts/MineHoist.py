import jarray
import jmri
import jmri.Sensor
import java.util.Random
from time import sleep
# temporary disable listeners
class MineHoist(jmri.jmrit.automat.AbstractAutomaton) :
    def init(self, sensors):
        print "Initializine Mine Hoist"
        self.hoist = self.getThrottle(99, False)
        
        self.hoistTopSensor = sensors.provideSensor("Hoist Top")
        self.hoistBottomSensor = sensors.provideSensor("Hoist Bottom") 
        self.hoistCallButton = sensors.provideSensor("Hoist Call Button")   
        
        #
        #  Hoist sounds
        self.hoistTopListener = self.HoistTopListener()
        self.hoistTopListener.init(self.hoist, sensors)
#        self.hoistTopSensor.addPropertyChangeListener(self.hoistTopListener)
        
        self.hoistBottomListener = self.HoistBottomListener()
        self.hoistBottomListener.init(self.hoist, sensors)
#        self.hoistBottomSensor.addPropertyChangeListener(self.hoistBottomListener)  
        
        self.hoistCallButtonListener = self.HoistCallButtonListener()
        self.hoistCallButtonListener.init(self.hoist, self.hoistTopSensor, self.hoistBottomSensor, sensors)
#        self.hoistCallButton.addPropertyChangeListener(self.hoistCallButtonListener)
        return

    def toggleLight(self, state) :
        self.hoist.setF0(state)
        return
    
    def getLightState(self) :
        return self.hoist.getF0()

    def handle(self):
        return False

    class HoistCallButtonListener(java.beans.PropertyChangeListener) :
        def init(self, hoist, topSensor, bottomSensor, sensors):
            self.hoist = hoist
            self.topSensor = topSensor
            self.bottomSensor = bottomSensor
            self.movingUp = sensors.provideSensor("Hoist Moving Up")
            self.movingDown = sensors.provideSensor("Hoist Moving Down")
            self.moving = sensors.provideSensor("Hoist Moving")

            path = "preference:resources/sounds/SingleElectricBell.wav"
            hoistSound = "preference:resources/sounds/Hoist45Secs.wav"
            try :
                print "Loading sound file " + path
                self.signalBell = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename(path))
            except :
                print "Error creating sound file ", path, sys.exc_info()[0], sys.exc_info()[1]

            try :
                print "Loading sound file " + hoistSound
                self.hoistSound = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename(hoistSound))
            except :
                print "Error creating sound file ", hoistSound, sys.exc_info()[0], sys.exc_info()[1]                            

        def propertyChange(self, event):
            if (event.source.getState() == jmri.Sensor.ACTIVE) :
                self.signalBell.play()
                sleep(5)
                event.source.setState(jmri.Sensor.INACTIVE)
                if (self.topSensor.getState() == jmri.Sensor.ACTIVE) :
                    self.hoist.setIsForward(True)
                    self.movingUp.setState(jmri.Sensor.INACTIVE)                                                
                    self.movingDown.setState(jmri.Sensor.ACTIVE)
                else :
                    self.hoist.setIsForward(False)
                    self.movingDown.setState(jmri.Sensor.INACTIVE)
                    self.movingUp.setState(jmri.Sensor.ACTIVE)                                                                                                
                self.hoist.setF0(True)
                sleep(1)
                self.moving.setState(jmri.Sensor.ACTIVE)
                self.hoistSound.play()
                self.hoist.setSpeedSetting(0.9)
            return

    class HoistTopListener(java.beans.PropertyChangeListener) :
        def init (self, hoist, sensors) :
            self.hoist = hoist
            self.movingUp = sensors.provideSensor("Hoist Moving Up")
            self.movingDown = sensors.provideSensor("Hoist Moving Down")
            self.moving = sensors.provideSensor("Hoist Moving")                                                

        def propertyChange(self, event) :
            # Stop the hoist if we hit the top sensor AND we are going up.  Don't
            # stop if hoist is going down...false positives prevent the cage from
            # lowering.
            print "Hoist Top Listener called, state = " + str(event.source.getState()) + "desired state = " + str(jmri.Sensor.ACTIVE)
            if (self.hoist.getIsForward()) :
                print "self.hoist.getIsForward() = True"
            else:
                print "self.hoist.getIsForward() = False"
                
            if (event.source.getState() == jmri.Sensor.ACTIVE and not self.hoist.getIsForward()) :
                print "Hoist Top Listener triggered"                
                self.hoist.setSpeedSetting(0.0)
                self.hoist.setF0(False)
                self.movingUp.setState(jmri.Sensor.INACTIVE)
                self.movingDown.setState(jmri.Sensor.INACTIVE)
                self.moving.setState(jmri.Sensor.INACTIVE)                                                

    class HoistBottomListener(java.beans.PropertyChangeListener) :
        def init (self, hoist, sensors) :
            self.hoist = hoist
            self.movingUp = sensors.provideSensor("Hoist Moving Up")
            self.movingDown = sensors.provideSensor("Hoist Moving Down")
            self.moving = sensors.provideSensor("Hoist Moving")

        def propertyChange(self, event) :
            # Stop the hoist if we hit the bottom sensor AND we are going down.  Don't
            # stop if hoist is going up...false positives prevent the cage from
            # raising.
            print "Hoist Bottom Listener called"            
            if (event.source.getState() == jmri.Sensor.ACTIVE and self.hoist.getIsForward()) :
                print "Hoist Bottom Listener triggered"
                self.hoist.setSpeedSetting(0.0)
                self.hoist.setF0(False)
                self.movingUp.setState(jmri.Sensor.INACTIVE)
                self.movingDown.setState(jmri.Sensor.INACTIVE)
                self.moving.setState(jmri.Sensor.INACTIVE)                                                                            
