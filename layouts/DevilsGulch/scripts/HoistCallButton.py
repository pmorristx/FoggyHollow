import jmri
import java.util.Random
from time import sleep

class HoistCallButton(jmri.jmrit.automat.AbstractAutomaton) :

    class HoistCallButtonListener(java.beans.PropertyChangeListener) :
        def init(self, hoist, topSensor, bottomSensor, sensors):
            self.hoist = hoist
            self.topSensor = topSensor
            self.bottomSensor = bottomSensor
            self.movingUp = sensors.provideSensor("Hoist Moving Up")
            self.movingDown = sensors.provideSensor("Hoist Moving Down")
            self.moving = sensors.provideSensor("Hoist Moving")
            
            path = "preference:resources/sounds/SingleElectricBell.wav"
            hoistSound = "preference:resources/sounds/Hoist1Minute.wav"
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
            if (event.source.getState() == ACTIVE) :
                self.signalBell.play()
                sleep(5)
                event.source.setState(INACTIVE)
                if (self.topSensor.getState() == ACTIVE) :
                    self.hoist.setIsForward(True)
                    self.movingUp.setState(INACTIVE)                                                
                    self.movingDown.setState(ACTIVE)
                else :
                    self.hoist.setIsForward(False)
                    self.movingDown.setState(INACTIVE)
                    self.movingUp.setState(ACTIVE)                                                                                                
                self.hoist.setF0(True)
                sleep(1)
                self.moving.setState(ACTIVE)
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
            if (event.source.getState() == ACTIVE and not self.hoist.getIsForward()) :
                self.hoist.setSpeedSetting(0.0)
                self.hoist.setF0(False)
                self.movingUp.setState(INACTIVE)
                self.movingDown.setState(INACTIVE)
                self.moving.setState(INACTIVE)                                                
                #sleep(1) 
                #event.source.setState(ACTIVE)
#                print "Hoist Top Listener fired"

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
            if (event.source.getState() == ACTIVE and self.hoist.getIsForward()) :
                self.hoist.setSpeedSetting(0.0)
                self.hoist.setF0(False)
                self.movingUp.setState(INACTIVE)
                self.movingDown.setState(INACTIVE)
                self.moving.setState(INACTIVE)                                                                            

#    def init(self):
#        self.hoist = self.getThrottle(99, False) 
        
#        self.hoistTopSensor = sensors.provideSensor("Hoist Top")
#        self.hoistBottomSensor = sensors.provideSensor("Hoist Bottom") 
#        self.hoistCallButton = sensors.provideSensor("Hoist Call Button")   
        
        #
        #  Hoist sounds

        
#        self.hoistTopListener = self.HoistTopListener()
#        self.hoistTopListener.init(self.hoist, sensors)
#        self.hoistTopSensor.addPropertyChangeListener(self.hoistTopListener)
        
#        self.hoistBottomListener = self.HoistBottomListener()
#        self.hoistBottomListener.init(self.hoist, sensors)
#        self.hoistBottomSensor.addPropertyChangeListener(self.hoistBottomListener)  
        
#        self.hoistCallButtonListener = self.HoistCallButtonListener()
#        self.hoistCallButtonListener.init(self.hoist, self.hoistTopSensor, self.hoistBottomSensor, sensors)
#        self.hoistCallButton.addPropertyChangeListener(self.hoistCallButtonListener)
        
#    def setHoistDirection(self, direction) :
#        if (direction == "DOWN") :
#            self.hoist.setIsForward(True)
#        else:
#            self.hoist.setIsForward(False)
    
#    def handle(self):
        
#        self.waitMsec(1500)
#        return True               
    
     
# start one of these up
#HoistCallButton().start()
