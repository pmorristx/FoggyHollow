#
# TripleToggleMonitor.py
#
class TripleToggleMonitor(jmri.jmrit.automat.AbstractAutomaton) :
    def init(self):
        #
        # Buttons being initialized and tracked.
        ButtonList = [107]

        #
        # DeviceList will contain one TrackDevice instance for each of the devices
        #
        DeviceList = {}

        #
        #  Get a handle to the panel
        windowsList = jmri.util.JmriJFrame.getFrameList()

        self.panelEditor = None
        self.windowsList = jmri.util.JmriJFrame.getFrameList()
        self.layoutEditor = None
        for i in range(windowsList.size()) :
            window = windowsList.get(i)
            windowClass = str(window.getClass())
            if (windowClass.endswith(".PanelEditor")) :
                if (window.getTitle().endswith("Lights Editor")) :
                    self.panelEditor = window
                    print "FOund panel editor " + window.getTitle()
                    break

        #
        # Set up the DeviceList entries for buttons
        #
        for i in range(len(ButtonList)) :
            ButtonNumber = ButtonList[i]
            DeviceList[ButtonNumber] = self.TrackDevice()
            DeviceList[ButtonNumber].init(ButtonNumber, self.panelEditor)
            DeviceList[ButtonNumber].setInitialDeviceState()
        return


    def handle(self):
        self.waitMsec(1)         # time is in milliseconds

    #
    # TrackDevice class, one instance for each device.
    #
    class TrackDevice(java.beans.PropertyChangeListener) :
        import java
        import javax.swing
        from jmri.jmrit.display import SensorIcon

        buttonClick = None
        ON = 1
        OFF = 0
        TIMER = 2

        # TrackDevice.init - Initialize a TrackDevice instance for a particular device
        #
        # aName          : Device name
        # aDevice        : JMRI device instance
        # aAllowedStates : Array of states we want to track, other states are ignored
        #
        def init(self, btnNumber, panelEditor) :
            self.DeviceNumber = btnNumber
            self.Light = lights.getLight("CL" + str(btnNumber-100))
            self.OnButton = sensors.getSensor("IS" + str(btnNumber) + ":BO")
            self.OffButton = sensors.getSensor("IS" + str(btnNumber) + ":BF")
            self.TimerButton = sensors.getSensor("IS" + str(btnNumber) + ":BT")
            self.buttonClick = jmri.jmrit.Sound("resources/sounds/Signal-normal.wav")

            self.OnIcon = self.findPanelIcon(panelEditor, "IS" + str(btnNumber) + ":BO")
            self.OffIcon = self.findPanelIcon(panelEditor, "IS" + str(btnNumber) + ":BF")
            self.TimerIcon = self.findPanelIcon(panelEditor, "IS" + str(btnNumber) + ":BT")

            self.sendTimeoutListener = self.TimeoutReceiver()
            self.sendTimeoutListener.setCallBack(self.sendTimeoutHandler)
            delaySecs = 300 +  java.util.Random().nextInt(300) # Code transmission delay
            self.sendTimer = javax.swing.Timer(delaySecs*1000, self.sendTimeoutListener)
            self.sendTimer.stop()
            self.sendTimer.setRepeats(True)

            return

        def setInitialDeviceState(self) :
            self.DeviceState = self.OFF
            self.OnButton.addPropertyChangeListener(self)
            self.OffButton.addPropertyChangeListener(self)
            self.TimerButton.addPropertyChangeListener(self)
            return

        def findPanelIcon(self, panelEditor, targetName) :
            if (panelEditor != None) :
                contents = panelEditor.getContents()
                for i in range(contents.size()) :
                    object = contents.get(i)
                    objectClass = str(object.getClass())
                    if (objectClass.endswith("SensorIcon")) :
                        src = object.getTooltip().getText()
                        if (src == targetName) :
                            print "TripleMonitor found " + targetName
                            return object


        # TrackDevice.propertyChange - Record state changes as a result of activities
        #                              elsewhere in JMRI
        #
        # aEvent : Event triggering the change (we don't actually look at the event...)
        #
        def propertyChange(self, aEvent) :
            source =  aEvent.getSource().getSystemName()
            print "Triple change from " + source
            if (source.endswith(":BO")) :
                if (self.DeviceState != self.ON and aEvent.getNewValue() == ACTIVE) : # Request on and not already on
                    self.buttonClick.play()
                    self.OffButton.setState(INACTIVE)
                    self.TimerButton.setState(INACTIVE)
                    self.Light.setState(jmri.Light.ON)
                    self.DeviceState = self.ON
                    self.OnIcon.setControlling(False)
                    self.OffIcon.setControlling(True)
                    self.TimerIcon.setControlling(True)
                    

            elif (source.endswith(":BF")) :
                if (self.DeviceState != self.OFF and aEvent.getNewValue() == ACTIVE) : # Request off and not already off
                    self.buttonClick.play()
                    self.DeviceState = self.OFF
                    self.Light.setState(jmri.Light.OFF)
                    self.OnButton.setState(INACTIVE)
                    self.TimerButton.setState(INACTIVE)
                    self.OnIcon.setControlling(True)
                    self.OffIcon.setControlling(False)
                    self.TimerIcon.setControlling(True)

            elif (source.endswith(":BT")) :
                if (self.DeviceState != self.TIMER and aEvent.getNewValue() == ACTIVE) : # Request timer and not already timed
                    self.buttonClick.play()
                    self.DeviceState = self.TIMER
                    self.OnButton.setState(INACTIVE)
                    self.OffButton.setState(INACTIVE)
                    self.OnIcon.setControlling(True)
                    self.OffIcon.setControlling(True)
                    self.TimerIcon.setControlling(False)

                    self.Light.setState(jmri.Light.ON)
                    delaySecs = 300 +  java.util.Random().nextInt(300) # Code transmission delay
                    self.sendTimer.setInitialDelay(delaySecs * 1000)
                    self.sendTimer.start()

            return

        class TimeoutReceiver(java.awt.event.ActionListener):
            cb = None

            def actionPerformed(self, event) :
                if (self.cb != None) :
                    self.cb(event)
                return

            def setCallBack(self, cbf) :
                self.cb = cbf
                return

        def sendTimeoutHandler(self, event) :
            print "In send timeout handler"
#            self.sendTimer.stop()
            
            if (self.TimerButton.getState() == ACTIVE) :
                if (self.Light.getState() == jmri.Light.ON) :
                    self.Light.setState(jmri.Light.OFF)
                else :
                    self.Light.setState(jmri.Light.ON)
            elif (self.OnButton.getState() == ACTIVE) :
                self.Light.setState(jmri.Light.ON)
            else :
                self.Light.setState(jmri.Light.OFF)
            return

TripleToggleMonitor().start()          # create one of these, and start it running

