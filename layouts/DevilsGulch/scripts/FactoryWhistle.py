#
#  Monitors a memory variable containing an ascii representation of the current time.  Updates
#  MemoryIcons on the control panel when the time changes.
class FactoryWhistle(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        #
        # Set up the DeviceList entries for turnouts
        #

        clock = self.TrackDevice()
        time =  memories.getMemory("IMCURRENTTIME").getValue()
        clock.init("IMCURRENTTIME",  memories.getMemory("IMCURRENTTIME"))
        return


    def handle(self):
        ###self.waitMsec(1)         # time is in milliseconds
        return False


    #
    # TrackDevice class, one instance for each device.
    #
    class TrackDevice(java.beans.PropertyChangeListener) :
        # TrackDevice.init - Initialize a TrackDevice instance for a particular device
        #
        # aName          : Device name
        # aDevice        : JMRI device instance
        #
        def init(self, aName, aDevice) :
            self.DeviceName = aName
            self.Device = aDevice
            self.Device.addPropertyChangeListener(self)
            self.factoryWhistle  = jmri.jmrit.Sound( jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/FactoryWhistle.wav"))
            return

        # TrackDevice.propertyChange - Record state changes as a result of activities
        #                              elsewhere in JMRI
        #
        # aEvent : Event triggering the change (we don't actually look at the event...)
        #
        def propertyChange(self, aEvent) :
            newTime = str(self.Device.getValue())
            onhour = False
#            switchOn = (sensors.getSensor("IS1:HW").getState() == ACTIVE)
            if (newTime.__len__() == 8) :
               onhour = newTime[3:4] == "0" and newTime[4:5] == "0"
#               quarterhour = newTime[3:4] == "1" and newTime[4:5] == "5"
#               halfhour = newTime[3:4] == "3" and newTime[4:5] == "0"
            else :
               onhour = newTime[2:3] == "0" and newTime[3:4] == "0"
#              quarterhour = newTime[2:3] == "1" and newTime[3:4] == "5"
#               halfhour = newTime[2:3] == "3" and newTime[3:4] == "0"
#            if (onhour or quarterhour or halfhour) :
            if (onhour) :
                self.factoryWhistle.play()
            return

FactoryWhistle().start()          # create one of these, and start it running
