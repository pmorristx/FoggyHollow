#
# LightMasterPowerMonitor.py
#
class LightMasterPowerMonitor(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        listener  = self.TrackDevice()
        listener.init("100")
        listener.setInitialDeviceState()
        return


    def handle(self):
        self.waitMsec(1)         # time is in milliseconds

    #
    # TrackDevice class, one instance for each device.
    #
    from time import sleep

    class TrackDevice(java.beans.PropertyChangeListener) :
        # TrackDevice.init - Initialize a TrackDevice instance for a particular device
        #
        # aName          : Device name
        # aDevice        : JMRI device instance
        # aAllowedStates : Array of states we want to track, other states are ignored
        #
        def init(self, sensorNumber) :
            self.buttonList = [101,102,103,104,105, 106, 107]
            self.powerOn = sensors.getSensor("IS" + sensorNumber + ":BO")
            self.powerOff = sensors.getSensor("IS" + sensorNumber + ":BF")
            self.powerTimed = sensors.getSensor("IS" + sensorNumber + ":BT")
            self.powerOnSound  = jmri.jmrit.Sound( jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/electricshock.wav"))
            self.powerOffSound = jmri.jmrit.Sound( jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/circuitbreaker.wav"))

            return

        def setInitialDeviceState(self) :
            self.DeviceState = INACTIVE
            self.powerOn.addPropertyChangeListener(self)
            self.powerOff.addPropertyChangeListener(self)
            self.powerTimed.addPropertyChangeListener(self)

            return

        # TrackDevice.propertyChange - Record state changes as a result of activities
        #                              elsewhere in JMRI
        #
        # aEvent : Event triggering the change (we don't actually look at the event...)
        #
        def propertyChange(self, aEvent) :
            from time import sleep

            source =  aEvent.getSource().getSystemName()
            if (source.endswith(":BO") or source.endswith(":BT")) :
                if (self.DeviceState != ACTIVE and aEvent.getNewValue() == ACTIVE) : # Request on and not already on
                    self.powerOnSound.play()
                    self.DeviceState = ACTIVE
                    for i in range(len(self.buttonList)) :
                        buttonNumber = self.buttonList[i]
                        onButton = "IS" + str(buttonNumber) + ":BO"
                        toggleButton = "IS" + str(buttonNumber) + ":T"
                        timedButton = "IS" + str(buttonNumber) + ":BT"
                        timedSensor = sensors.getSensor(timedButton)
                        
                        testButton = sensors.getSensor(onButton)
                        if (testButton is None) :
                            testButton = sensors.getSensor(toggleButton)
                        if (testButton.getState() == ACTIVE) :
                            indicator = sensors.getSensor("IS" + str(buttonNumber) + ":K")
                            if (indicator is not None) :
                                indicator.setState(ACTIVE)
                            light = lights.getLight("CL" + str(buttonNumber-100))
                            if (light is not None) :
                                light.setState(jmri.Light.ON)
                        elif (timedSensor is not None) : # If a timed button exists, toggle it to restart the timer
                            print "Checking timed sensor " + str(buttonNumber)
                            if (timedSensor.getState() == ACTIVE) :
                                print "Resetting timer for sensor " + str(buttonNumber)
                                sensors.getSensor("IS" + str(buttonNumber) + ":BF").setState(ACTIVE)
                                sleep(1)
                                timedSensor.setState(ACTIVE)

            elif (source.endswith(":BF")) :
                if (self.DeviceState != INACTIVE and aEvent.getNewValue() == ACTIVE) : # Request off and not already off
                    self.powerOffSound.play()
                    self.DeviceState = INACTIVE
                    for i in range(len(self.buttonList)) :
                        buttonNumber = self.buttonList[i]
                        indicator = sensors.getSensor("IS" + str(buttonNumber) + ":K")
                        if (indicator is not None) :
                            indicator.setState(INACTIVE)
                        light = lights.getLight("CL" + str(buttonNumber-100))
                        if (light is not None) :
                            light.setState(jmri.Light.OFF)


            return

LightMasterPowerMonitor().start()          # create one of these, and start it running

