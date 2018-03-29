import jmri

#Created on Jan 29, 2017

class HoistCage(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):
        #
        print "Hoist Cage Init"
        
        self.hoistL4 = sensors.provideSensor("IS Call Hoist To L4")
        self.hoistL3 = sensors.provideSensor("IS Call Hoist To L3")
        self.hoistL2 = sensors.provideSensor("IS Call Hoist To L2")
        self.hoistL1 = sensors.provideSensor("IS Call Hoist To L1")
        self.hoistS1 = sensors.provideSensor("IS Call Hoist To S1")
        self.hoistS2 = sensors.provideSensor("IS Call Hoist To S2")
        self.hoistS3 = sensors.provideSensor("IS Call Hoist To S3") 


        self.hoistButtons = []          
        self.hoistButtons.append(self.hoistL4)
        self.hoistButtons.append(self.hoistL3)
        self.hoistButtons.append(self.hoistL2)
        self.hoistButtons.append(self.hoistL1)
        self.hoistButtons.append(self.hoistS1)
        self.hoistButtons.append(self.hoistS2)   
        self.hoistButtons.append(self.hoistS3)

        for i in range(len(self.hoistButtons)) :
             self.hoistButtons[i].setState(INACTIVE)
        
        self.hoistCommands = []
        self.hoistCommands.append(sensors.provideSensor("Call Hoist To L4"))
        self.hoistCommands.append(sensors.provideSensor("Call Hoist To L3"))
        self.hoistCommands.append(sensors.provideSensor("Call Hoist To L2"))
        self.hoistCommands.append(sensors.provideSensor("Call Hoist To L1"))
        self.hoistCommands.append(sensors.provideSensor("Call Hoist To S1"))
        self.hoistCommands.append(sensors.provideSensor("Call Hoist To S2"))
        self.hoistCommands.append(sensors.provideSensor("Call Hoist To S3"))
        
        self.hoistIndicators = []
        self.hoistIndicators.append(sensors.provideSensor("Hoist L4 Indicator"))
        self.hoistIndicators.append(sensors.provideSensor("Hoist L3 Indicator"))
        self.hoistIndicators.append(sensors.provideSensor("Hoist L2 Indicator"))
        self.hoistIndicators.append(sensors.provideSensor("Hoist L1 Indicator"))
        self.hoistIndicators.append(sensors.provideSensor("Hoist S1 Indicator"))
        self.hoistIndicators.append(sensors.provideSensor("Hoist S2 Indicator"))
        self.hoistIndicators.append(sensors.provideSensor("Hoist S3 Indicator"))

        self.raiseHoistSound = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Short-Short-Long-Signal.wav"))
        self.lowerHoistSound = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Short-Long-Signal.wav"))
        self.stopHoistSound = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/SingleLongSignal.wav"))
        
        self.hoistBells = []
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/QuadShortSignal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/TripleShortSignal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/DoubleShortSignal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/SingleShortSignal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Long-Short-Signal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Long-Short-Short-Signal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Long-Short-Short-Short-Signal.wav")))        
        
        self.currentLevel = 0 # Default at sump      

    def handle (self):
        print "Hoist Cage Handle"

        #  Find current level
        for i in range(len(self.hoistIndicators)) :
            if (self.hoistIndicators[i].getState() == ACTIVE) :
                self.currentLevel = i
        print "current level: " + str(self.currentLevel)        
        self.waitChange(self.hoistButtons)
        print "Button changed"


        
        for i in range(len(self.hoistButtons)) :
            if (self.hoistButtons[i].getState() == ACTIVE and self.currentLevel != i) :

                print "currentLevel " + str(self.currentLevel) + " requestedLevel = " + str(i)

                if (self.currentLevel < i) :
                    self.raiseHoistSound.play()
                else :
                    self.lowerHoistSound.play()
                self.waitMsec(8000)
                self.hoistBells[i].play()
                self.waitMsec(8000) 
                self.hoistCommands[i].setState(ACTIVE)
                sensors.provideSensor("Hoist Moving").setState(jmri.Sensor.ACTIVE)
                if (self.currentLevel < i) :
                    sensors.provideSensor("Hoist Moving Up").setState(jmri.Sensor.ACTIVE)
                else :
                    sensors.provideSensor("Hoist Moving Down").setState(jmri.Sensor.ACTIVE)

                #  Wait for arduino to turn on sensor at requested level
                self.waitSensorActive(self.hoistIndicators[i])
                
                self.hoistCommands[i].setState(INACTIVE)
                self.stopHoistSound.play()
                sensors.provideSensor("Hoist Moving").setState(jmri.Sensor.INACTIVE)
                if (self.currentLevel < i) :
                    sensors.provideSensor("Hoist Moving Up").setState(jmri.Sensor.INACTIVE)
                else :
                    sensors.provideSensor("Hoist Moving Down").setState(jmri.Sensor.INACTIVE)

        return True

HoistCage().start()
