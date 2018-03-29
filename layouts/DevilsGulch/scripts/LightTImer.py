#
# LightTimer.py
#

import java
import javax.swing
import jmri.Light.ON as ON
import jmri.Light.OFF as OFF

class LightTimer(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        DeviceList = {}
        DeviceList["IS100"] = self.LayoutLight()
        DeviceList["IS100"].init("CL1", lights.getLight("CL107"))
        DeviceList["IS100"].setInitialDeviceState()

        return


    def handle(self):
        self.waitMsec(1)         # time is in milliseconds


    #
    # LayoutLight class, one instance for each device.
    #
    class LayoutLight(java.beans.PropertyChangeListener) :
        import java
        import javax.swing

        delayTimer = None

        # LayoutLight.init - Initialize a LayoutLight instance for a particular device
        #
        # aName          : Device name
        # aDevice        : JMRI device instance
        # aAllowedStates : Array of states we want to track, other states are ignored
        #
        def init(self, aName, aDevice) :
            print ('LayoutLight.init ' + aName )

            fullname = jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/electricstart.wav")
            self.startSnap = jmri.jmrit.Sound(fullname)

            fullname = jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/circuitbreaker.wav")
            self.stopSnap = jmri.jmrit.Sound(fullname)


            self.DeviceName = aName
            self.Device = aDevice

            self.sendTimeoutListener = self.TimeoutReceiver()
            self.sendTimeoutListener.setCallBack(self.sendTimeoutHandler)
            delaySecs = 120 +  java.util.Random().nextInt(1) # Code transmission delay
            self.sendTimer = javax.swing.Timer(delaySecs*1000, self.sendTimeoutListener)
            self.sendTimer.stop()
            self.sendTimer.setRepeats(True)

            return

        # LayoutLight.propertyChange - Record state changes as a result of activities
        #                              elsewhere in JMRI
        #
        # aEvent : Event triggering the change (we don't actually look at the event...)
        #
        def propertyChange(self, aEvent) :


            if (sensors.getSensor("IS100:BF").getState() == ACTIVE) :
                self.Device.setState(jmri.Light.OFF)
                self.stopSnap.play()
            elif (sensors.getSensor("IS100:BO").getState() == ACTIVE) :
                self.Device.setState(jmri.Light.ON)
                self.startSnap.play()
            else :
                self.startSnap.play()
                self.Device.setState(jmri.Light.ON)
                delaySecs = 120 +  java.util.Random().nextInt(1) # Code transmission delay
                self.sendTimer.setInitialDelay(delaySecs * 1000)
                self.sendTimer.start()

            return


        # LayoutLight.setInitialDeviceState - After reading all of the old tracking file we
        #                                     now initialize the actual devices to their last
        #                                     known states and log these states into the new
        #                                     log file.
        #
        def setInitialDeviceState(self) :
            #       Uncomment the following print statement to display the list of devices being tracked.
            print "In setInitDeviceState, name = " + self.DeviceName
            sensors.getSensor("IS100:BT").addPropertyChangeListener(self)
            sensors.getSensor("IS100:BF").addPropertyChangeListener(self)
            sensors.getSensor("IS100:BO").addPropertyChangeListener(self)


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
            
            if (sensors.getSensor("IS100:BT").getState() == ACTIVE) :
                if (self.Device.getState() == jmri.Light.ON) :
                    self.Device.setState(jmri.Light.OFF)
                else :
                    self.Device.setState(jmri.Light.ON)
            elif (sensors.getSensor("IS100:BO").getState() == ACTIVE) :
                self.Device.setState(jmri.Light.ON)
            else :
                self.Device.setState(jmri.Light.OFF)
            return

    #return False              # all done, don't repeat 
LightTimer().start()          # create one of these, and start it running

