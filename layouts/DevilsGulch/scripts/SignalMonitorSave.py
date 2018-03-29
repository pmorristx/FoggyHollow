#
# SignalMonitor.py

#
from time import sleep


import java
import javax.swing

class SignalMonitor(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        #########################################################################
        #
        # The first part of the script defines a variety of values and procedures
        #
        #########################################################################

        # logFileName - name of the file being used to record device states.
        #
        # Note that the log file MUST exist each time that the script is invoked.  The
        # file can be zero length (ie., the first time the script is run), which results
        #in all turnouts being set to CLOSED and all lights being set to OFF.
        #
        logFileName = "C:\\Users\\pmorris.PETROLITE\\JMRI\SignalMonitor.log"


        #
        # Turnouts being initialized and tracked.
        # Turnouts not found while processing the existing tracking file are initialized to the
        # first entry in the allowable states list for turnouts - CLOSED.
        #
        SignalList = ["IM8:TOV", "IM9:TOV"]

        signalStates = ["P", "S", "C"]

        #
        # DeviceList will contain one TrackDevice instance for each of the devices
        #
        DeviceList = {}

        logFile = -1

        #########################################################################
        #
        # The remainder of the script defines code which is executed immediately
        # as the script is being processed initially.
        #
        #########################################################################


        #
        # Set up the DeviceList entries for turnouts
        #
        for i in range(len(SignalList)) :
            SignalName = SignalList[i]
            print "Creating device entry Signal " + SignalName
            DeviceList[SignalName] = self.TrackDevice()
            sensor = memories.getMemory(SignalName)
            print "Memory state = " + str(sensor.getValue())

            DeviceList[SignalName].init(SignalName, memories.provideMemory(SignalName), signalStates, logFile, self)

        #
        # Process the existing log file, reading each line and updating our internal
        # states as appropriate.
        #
        # Note that the log file MUST exist each time that the script is invoked.  The
        # file can be zero length, which results in all turnouts being set to CLOSED and
        # all lights being set to OFF.
        #
        logFile = open(logFileName, "r")

        while True:
            line = logFile.readline()
            if (len(line) == 0) :
                break
            line = line.strip() 
            i = line.find(" ")
            if (i < 0) :
                print 'Invalid line format: ' + line
            else :
                k = line[0:i].strip()                         # k is the device name
                try :
                    v = line[i+1:len(line)].strip()      # v is the device state
                except ValueError:
                    print "Log file contains invalid device state value: " + line
                else :
                    try :
                        handler = DeviceList[k]
                    except KeyError:
                        print "Log file contains status for unknown device: " + line
                    else:
                        handler.updateState(v)

        logFile.close()

        #
        # Recreate the log file and register our shutdown handler
        #
        logFile = open(logFileName, "w")
        shutdown.register(self.SignalMonitorShutdown("Device Tracker"))

        #
        # Initialize the JMRI turnout devices and log their states
        #
        for i in range(len(SignalList)) :
            DeviceList[SignalList[i]].setInitialDeviceState(logFile)

        logFile.flush()

        return


    def handle(self):
        self.waitMsec(1)         # time is in milliseconds


    #
    # logStateChange - Add a state change line to the tracking file
    #
    # We normally "flush" the file after each state change...but not
    # during initialization.
    #
    def logStateChange2 (name, value, flush) :
        logFile.write(name + " " + value + "\n")
        if (flush) :
            logFile.flush()
        
    #
    # TrackDevice class, one instance for each device.
    #
    class TrackDevice(java.beans.PropertyChangeListener) :
        import java
        import javax.swing

        delayTimer = None
        relayClicks = None
        # TrackDevice.init - Initialize a TrackDevice instance for a particular device
        #
        # aName          : Device name
        # aDevice        : JMRI device instance
        # aAllowedStates : Array of states we want to track, other states are ignored
        #
        def init(self, aName, aDevice, aAllowedStates, aLogFile, aParent) :
            print ('init ' + aName )
            self.DeviceName = aName
            self.Device = aDevice
            self.AllowedStates = aAllowedStates
            self.parent = aParent
            self.DeviceValue = self.AllowedStates[0]
            self.LogFile = aLogFile
            self.timeoutListener = self.TimeoutReceiver()
            self.timeoutListener.setCallBack(self.timeoutHandler)
            self.delayTimer = javax.swing.Timer(10000, self.timeoutListener)
            self.delayTimer.stop()
            self.delayTimer.setRepeats(False)
            self.relayClicks = jmri.jmrit.Sound("resources/sounds/Code-receive.wav")

        # TrackDevice.updateState - Track the device state while reading the old log
        #                           file.  Note the state but don't change the device
        #                           itself and don't log the changes to the new log file
        #                           (yet).
        #
        # aNewState : New device state.
        #
        def updateState(self, aNewState) :
            print 'updateState ' + self.DeviceName
            for i in range(len(self.AllowedStates)) :
                if (aNewState == self.AllowedStates[i]) :
                    self.DeviceValue = aNewState
                    break

        # TrackDevice.propertyChange - Record state changes as a result of activities
        #                              elsewhere in JMRI
        #
        # aEvent : Event triggering the change (we don't actually look at the event...)
        #
        def propertyChange(self, aEvent) :
            newValue = self.Device.getValue()

            print "Property change " + self.DeviceName
            codeSendSensor = sensors.getSensor("IS18:CCK")
            #codeSendSensor.setState(ACTIVE)
            self.parent.waitMsec(400)
            #codeSendSensor.setState(INACTIVE)
            
            if (codeSendSensor.getState() == ACTIVE) :
                self.parent.waitSensorInactive(codeSendSensor)
            # Click the relay, then light the appropriate indicator light
            sensors.getSensor("IS17:ICK").setState(ACTIVE)
            print "Turning on IC light"

            self.relayClicks.loop()
            newName = "IS" + self.DeviceName[2:3]
            sensors.getSensor( newName + ":WKC").setState(INACTIVE)
            sensors.getSensor( newName + ":WKL").setState(INACTIVE)
            sensors.getSensor( newName + ":WKR").setState(INACTIVE)

            delay = 3 +  java.util.Random().nextInt(4) # Minimum 3 seconds, max of 7 seconds
            self.delayTimer.setInitialDelay(delay * 1000)
            self.delayTimer.start()

            if (newValue == self.DeviceValue) :
                return
                
            for i in range(len(self.AllowedStates)) :
                if (newValue == self.AllowedStates[i]) :
                    self.DeviceValue = newValue
                    #logStateChange2(self.DeviceName, self.DeviceValue, True)
                    print "state change " + self.DeviceName + " " + str(self.DeviceValue)
                    self.LogFile.write(self.DeviceName + " " + self.DeviceValue + "\n")
                    self.LogFile.flush()
                    break
            return


        # TrackDevice.setInitialDeviceState - After reading all of the old tracking file we
        #                                     now initialize the actual devices to their last
        #                                     known states and log these states into the new
        #                                     log file.
        #
        def setInitialDeviceState(self, logFile) :
            #       Uncomment the following print statement to display the list of devices being tracked.
            print "In setInitDeviceState, name = " + self.DeviceName + " value = " + self.DeviceValue
            self.LogFile = logFile
###            self.Device.setState(self.DeviceValue)
            self.Device.addPropertyChangeListener(self)
            #logStateChange2(self.DeviceName, self.DeviceState, False)
            logFile.write(self.DeviceName + " " + self.DeviceValue + "\n")
            
            signalId = "IS" + self.DeviceName[2:3]
            # Move the switch lever to the correct position
            if (self.DeviceValue == "P") :
                sensors.getSensor( signalId + ":WLL").setState(INACTIVE)
                sensors.getSensor( signalId + ":WLR").setState(INACTIVE)
                sensors.getSensor( signalId + ":WLC").setState(ACTIVE)
                sensors.getSensor( signalId + ":WKR").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKL").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKC").setState(ACTIVE)
                sensors.getSensor( signalId + ":TOC").setState(INACTIVE)
                sensors.getSensor( signalId + ":TOS").setState(INACTIVE)
                sensors.getSensor( signalId + ":TOP").setState(ACTIVE)
            elif (self.DeviceValue == "C") :
                sensors.getSensor( signalId + ":WLL").setState(ACTIVE)
                sensors.getSensor( signalId + ":WLR").setState(INACTIVE)
                sensors.getSensor( signalId + ":WLC").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKR").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKL").setState(ACTIVE)
                sensors.getSensor( signalId + ":WKC").setState(INACTIVE)
                sensors.getSensor( signalId + ":TOC").setState(ACTIVE)
                sensors.getSensor( signalId + ":TOS").setState(INACTIVE)
                sensors.getSensor( signalId + ":TOP").setState(INACTIVE)

            else :
                sensors.getSensor( signalId + ":WLL").setState(INACTIVE)
                sensors.getSensor( signalId + ":WLR").setState(ACTIVE)
                sensors.getSensor( signalId + ":WLC").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKR").setState(ACTIVE)
                sensors.getSensor( signalId + ":WKL").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKC").setState(INACTIVE)
                sensors.getSensor( signalId + ":TOC").setState(INACTIVE)
                sensors.getSensor( signalId + ":TOS").setState(ACTIVE)
                sensors.getSensor( signalId + ":TOP").setState(INACTIVE)


        class TimeoutReceiver(java.awt.event.ActionListener):
            cb = None

            def actionPerformed(self, event) :
                if (self.cb != None) :
                    self.cb(event)
                return

            def setCallBack(self, cbf) :
                self.cb = cbf
                return

        def timeoutHandler(self, event) :
            # see which phase we think we are in
            print "In timeout Handler"
            self.delayTimer.stop()

            signalNumber = self.DeviceName[2:3]
            print " Signal number = " + str(signalNumber) + " signal state = " + self.Device.getValue()
            if (self.Device.getValue() == "P") :
                sensors.getSensor( "IS" + signalNumber + ":WKC").setState(ACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":WKR").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":WKL").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":TOC").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":TOS").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":TOP").setState(ACTIVE)
            elif (self.Device.getValue() == "C") :
                sensors.getSensor( "IS" + signalNumber + ":WKC").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":WKR").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":WKL").setState(ACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":TOS").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":TOP").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":TOC").setState(ACTIVE)
            elif (self.Device.getValue() == "S") :
                sensors.getSensor( "IS" + signalNumber + ":WKC").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":WKR").setState(ACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":WKL").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":TOC").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":TOP").setState(INACTIVE)
                sensors.getSensor( "IS" + signalNumber + ":TOS").setState(ACTIVE)

            self.relayClicks.stop()
            self.parent.waitMsec(1000)
            sensors.getSensor("IS17:ICK").setState(INACTIVE)

            return
    #
    # Close the log file when JMRI shuts down
    #
    class SignalMonitorShutdown(jmri.implementation.AbstractShutDownTask):
        def execute(self):
            logFile.close()
            return True



    #return False              # all done, don't repeat 
SignalMonitor().start()          # create one of these, and start it running

