#
# ButtonToggleMonitor.py
#
class BeaverBendStationLights(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        #
        # Buttons being initialized and tracked.
        ButtonList = [200]

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
                if (window.getTitle().endswith("Beaver Bend Editor")) :
                    self.panelEditor = window
                    break

        #
        # Set up the DeviceList entries for buttons
        #
        for i in range(len(ButtonList)) :
            ButtonNumber = ButtonList[i]
            DeviceList[ButtonNumber] = self.TrackLightDevice()
            throt = self.getThrottle(3, False)
            DeviceList[ButtonNumber].init(ButtonNumber, self.panelEditor, self)
            DeviceList[ButtonNumber].setInitialDeviceState()
        return


    def handle(self):
        self.waitMsec(1)         # time is in milliseconds

    #
    # TrackDevice class, one instance for each device.
    #
    class TrackLightDevice(java.beans.PropertyChangeListener) :
        import java
        import javax.swing
        from jmri.jmrit.display import SensorIcon

        buttonClick = None
        ON = 1
        OFF = 0

        # TrackDevice.init - Initialize a TrackDevice instance for a particular device
        #
        # aName          : Device name
        # aDevice        : JMRI device instance
        # aAllowedStates : Array of states we want to track, other states are ignored
        #
        def init(self, btnNumber, panelEditor, parent) :
            self.DeviceNumber = btnNumber
            self.parent = parent
            # self.throt = throt
            #self.throt.setF5(True)

            self.onButton = sensors.getSensor("IS" + str(btnNumber))
            self.buttonClick = jmri.jmrit.Sound("resources/sounds/Signal-normal.wav")
            self.electricZap1 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ShortElectricClick.wav"))
            self.electricZap2 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ShortTesla.wav"))
            self.electricZap3 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ElectricSizzle.wav"))
            self.electricZap4 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ElectricSizzle2.wav"))
            self.OnIcon = self.findPanelIcon(panelEditor, "IS" + str(btnNumber) + ":BO")
            return

        def setInitialDeviceState(self) :
            self.DeviceState = self.OFF
            self.onButton.addPropertyChangeListener(self)
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
                            return object

        def randomArc(self) :
            #
            # Play random arcing sound...for long sounds delay before turning light on.
            delay = 50
            prob =  java.util.Random().nextInt(10) # Switch arcing delay
            if (prob > 9) :
                self.electricZap4.play()
                delay = 900
            elif (prob > 8) :
                self.electricZap3.play()
                delay = 750
            elif (prob > 6) :
                self.electricZap2.play()
                delay = 300
            elif (prob > 2) :
                self.electricZap1.play()
                delay = 200

            self.parent.waitMsec(delay)
            return

#        def toggleLight(self) :     
#            throt = self.getThrottle(18, False)
#            throt.setF5(!throt.getF5)  
#            return          
            
            
        # TrackDevice.propertyChange - Record state changes as a result of activities
        #                              elsewhere in JMRI
        #
        # aEvent : Event triggering the change (we don't actually look at the event...)
        #
        def propertyChange(self, aEvent) :
            try :
                source =  aEvent.getSource().getSystemName()
                if (self.DeviceState != self.ON and aEvent.getNewValue() == ACTIVE) : # Request on and not already on
                    self.buttonClick.play()

                    self.DeviceState = self.ON

                    self.randomArc()   
#                    self.toggleLight()                                          

            except:
                print "Unexpected error: "
                raise

            return

BeaverBendStationLights().start()          # create one of these, and start it running
