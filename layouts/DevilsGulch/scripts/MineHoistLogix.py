import jmri

class MineHoistLogix(jmri.jmrit.automat.AbstractAutomaton) :
    def init(self):
        print "Initializine Mine Hoist"
        self.hoist = self.getThrottle(99, False)
        
        self.hoistTopSensor = sensors.provideSensor("Hoist Top")
        self.hoistBottomSensor = sensors.provideSensor("Hoist Bottom") 

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

        return

    def stopHoist(self, goingDown) :
        self.hoist.setSpeedSetting(0.0)
        self.movingUp.setState(jmri.Sensor.INACTIVE)
        self.movingDown.setState(jmri.Sensor.INACTIVE)
        self.moving.setState(jmri.Sensor.INACTIVE)                                                
        #
        #  Only turn off the lights at the top of the headframe if the hoist just came up.
        self.waitMsec(10000)
        if (not goingDown) :
            self.hoist.setF0(False)
            
        return
    
    def handle(self):

        goingDown = self.hoistTopSensor.getState() == ACTIVE
        
        self.signalBell.play()
        self.waitMsec(5000)
        
        if (goingDown) :
            self.hoist.setF0(True) # Light is already on if we are at the bottom going up.
            self.waitMsec(4000)
            
            self.hoist.setIsForward(True)
            self.movingUp.setState(INACTIVE)
            self.movingDown.setState(ACTIVE)
            waitSensor = self.hoistBottomSensor
        else :
            self.hoist.setIsForward(False)
            self.movingDown.setState(INACTIVE)
            self.movingUp.setState(ACTIVE)
            waitSensor = self.hoistTopSensor
            
        self.moving.setState(ACTIVE)
        self.hoistSound.play()
        self.hoist.setSpeedSetting(0.9)

        self.waitSensorActive(waitSensor)
        self.stopHoist(goingDown)
        
        return False

MineHoistLogix().start()
