import java
import jmri
#
#  Monitors a memory variable containing an ascii representation of the current time.  Updates
#  MemoryIcons on the control panel when the time changes.
class NixiePanelClock(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        #
        # Set up the DeviceList entries for turnouts
        #

        clock = self.TrackDevice()
        time =  memories.getMemory("IMCURRENTTIME").getValue()

        clock.init("IMCURRENTTIME",  memories.getMemory("IMCURRENTTIME"))
        memories.getMemory("IM20:H3").setValue(":")

        #
        #  Initialize to the current time so we don't wait a minute for the time to update
        memories.getMemory("IM20:H3").setValue(":")
        if (time.__len__() == 8) :
            memories.getMemory("IM20:H1").setValue(time[0:1])
            memories.getMemory("IM20:H2").setValue(time[1:2])
            memories.getMemory("IM20:M1").setValue(time[3:4])
            memories.getMemory("IM20:M2").setValue(time[4:5])
        else :
            memories.getMemory("IM20:H1").setValue(0)
            memories.getMemory("IM20:H2").setValue(time[0:1])
            memories.getMemory("IM20:M1").setValue(time[2:3])
            memories.getMemory("IM20:M2").setValue(time[3:4])

        return


    def handle(self):
        ###self.waitMsec(1)         # time is in milliseconds
        return False


    #
    # TrackDevice class, one instance for each device.
    #
    import java
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
            return

        # TrackDevice.propertyChange - Record state changes as a result of activities
        #                              elsewhere in JMRI
        #
        # aEvent : Event triggering the change (we don't actually look at the event...)
        #
        def propertyChange(self, aEvent) :
            newTime = str(self.Device.getValue())
            memories.getMemory("IM20:H3").setValue(":")
            if (newTime.__len__() == 8) :
                memories.getMemory("IM20:H1").setValue(newTime[0:1])
                memories.getMemory("IM20:H2").setValue(newTime[1:2])
                memories.getMemory("IM20:M1").setValue(newTime[3:4])
                memories.getMemory("IM20:M2").setValue(newTime[4:5])
            else :
                memories.getMemory("IM20:H1").setValue(0)
                memories.getMemory("IM20:H2").setValue(newTime[0:1])
                memories.getMemory("IM20:M1").setValue(newTime[2:3])
                memories.getMemory("IM20:M2").setValue(newTime[3:4])
            return

NixiePanelClock().start()          # create one of these, and start it running
