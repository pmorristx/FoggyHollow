#
# SignalMonitor.py

#
from time import sleep

import java
import javax.swing
import javax.swing.Timer

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
#        logFileName = "C:\\Users\\pmorris.PETROLITE\\JMRI\SignalMonitor.log"
        logFileName = jmri.util.FileUtil.getExternalFilename("preference:SignalMonitor.log")


        #
        # Turnouts being initialized and tracked.
        # Turnouts not found while processing the existing tracking file are initialized to the
        # first entry in the allowable states list for turnouts - CLOSED.
        #
        SignalList = ["IM8:TOV", "IM6:TOV"]

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
            #print "Creating device entry Signal " + SignalName
            DeviceList[SignalName] = self.TrackDevice()
            sensor = memories.getMemory(SignalName)
            #print "Memory state = " + str(sensor.getValue())

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
    # Close the log file when JMRI shuts down
    #
    class SignalMonitorShutdown(jmri.implementation.AbstractShutDownTask):
        def execute(self):
            logFile.close()
            return True
        
    #
    # TrackDevice class, one instance for each device.
    #
    class TrackDevice(java.beans.PropertyChangeListener) :
        import java
        import javax.swing
        import javax.swing.Timer

        delayTimer = None
        relayClicks = None
        # TrackDevice.init - Initialize a TrackDevice instance for a particular device
        #
        # aName          : Device name
        # aDevice        : JMRI device instance
        # aAllowedStates : Array of states we want to track, other states are ignored
        #
        def init(self, aName, aDevice, aAllowedStates, aLogFile, aParent) :
            from javax.swing import Timer 
            #print ('TrackDevice.init ' + aName )
            self.DeviceName = aName
            self.Device = aDevice
            self.DeviceValue = self.Device.getValue()
            self.AllowedStates = aAllowedStates
            self.parent = aParent
            self.LogFile = aLogFile

            self.timeoutListener = self.TimeoutReceiver()
            self.timeoutListener.setCallBack(self.receiveTimeoutHandler)
            self.receiveTimer = Timer(1, self.timeoutListener)
            self.receiveTimer.stop()
            self.receiveTimer.setRepeats(False)

            self.sendTimeoutListener = self.TimeoutReceiver()
            self.sendTimeoutListener.setCallBack(self.sendTimeoutHandler)
            self.sendTimer = Timer(1, self.sendTimeoutListener)
            self.sendTimer.stop()
            self.sendTimer.setRepeats(False)

            self.pauseTimeoutListener = self.TimeoutReceiver()
            self.pauseTimeoutListener.setCallBack(self.pauseTimeoutHandler)
            self.pauseTimer = Timer(1, self.pauseTimeoutListener)
            self.pauseTimer.stop()
            self.pauseTimer.setRepeats(False)

            self.relayClicks = jmri.jmrit.Sound("resources/sounds/Code-receive.wav")
            #self.relayClicks = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/EnhancedCTCRelay.wav"))
            self.relaySend = jmri.jmrit.Sound("resources/sounds/Code-send.wav")

            return

        # TrackDevice.updateState - Track the device state while reading the old log
        #                           file.  Note the state but don't change the device
        #                           itself and don't log the changes to the new log file
        #                           (yet).
        #
        # aNewState : New device state.
        #
        def updateState(self, aNewState) :
            #print 'updateState ' + self.DeviceName
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
            #print "Property change " + self.DeviceName
            newValue = self.Device.getValue()

            codeSendSensor = sensors.getSensor("IS16:CCK")
            codeSendSensor.setState(ACTIVE)

#            self.relaySend.loop()
            ccdl = 5 +  java.util.Random().nextInt(1) # Code transmission delay
            self.sendTimer.setInitialDelay(ccdl * 10)
            self.sendTimer.start()

            if (newValue == self.DeviceValue) :
                return
                
            for i in range(len(self.AllowedStates)) :
                if (newValue == self.AllowedStates[i]) :
                    self.DeviceValue = newValue
                    #logStateChange2(self.DeviceName, self.DeviceValue, True)
                    #print "state change " + self.DeviceName + " " + str(self.DeviceValue)
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
            #print "In setInitDeviceState, name = " + self.DeviceName + " value = " + self.DeviceValue
            self.LogFile = logFile
            self.Device.setValue(self.DeviceValue)
            self.Device.addPropertyChangeListener(self)
            #logStateChange2(self.DeviceName, self.DeviceState, False)
            logFile.write(self.DeviceName + " " + self.DeviceValue + "\n")
            
            signalId = "IS:" + self.DeviceName[2:3]
            ctcId = "CTC:TO" + self.DeviceName[2:3]
            # Move the switch lever to the correct position
            sensors.getSensor( signalId + ":CB").setState(INACTIVE)
            if (self.DeviceValue == "P") :

                #print " ctcId = " + ctcId + " state = green"
                turnouts.provideTurnout("NT" + self.DeviceName[2:3]).setState(CLOSED)
                sensors.getSensor( signalId + ":WLL").setState(INACTIVE)
                sensors.getSensor( signalId + ":WLR").setState(INACTIVE)
                sensors.getSensor( signalId + ":WLC").setState(ACTIVE)

                sensors.getSensor( signalId + ":WKR").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKL").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKC").setState(ACTIVE)

                sensors.getSensor( ctcId + ":GK").setState(ACTIVE)
                sensors.getSensor( ctcId + ":YK").setState(INACTIVE)
                sensors.getSensor( ctcId + ":RK").setState(INACTIVE)

                sensors.getSensor( ctcId + ":GS").setState(ACTIVE)
                sensors.getSensor( ctcId + ":YS").setState(INACTIVE)
                sensors.getSensor( ctcId + ":RS").setState(INACTIVE)


                sensors.getSensor( signalId + ":TOC").setState(INACTIVE)
                sensors.getSensor( signalId + ":TOS").setState(INACTIVE)
                sensors.getSensor( signalId + ":TOP").setState(ACTIVE)
            elif (self.DeviceValue == "C") :
                #print " ctcId = " + ctcId + " state = yellow"
                sensors.getSensor( signalId + ":WLL").setState(ACTIVE)
                sensors.getSensor( signalId + ":WLR").setState(INACTIVE)
                sensors.getSensor( signalId + ":WLC").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKR").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKL").setState(ACTIVE)
                sensors.getSensor( signalId + ":WKC").setState(INACTIVE)

                sensors.getSensor( ctcId + ":GK").setState(INACTIVE)
                sensors.getSensor( ctcId + ":YK").setState(ACTIVE)
                sensors.getSensor( ctcId + ":RK").setState(INACTIVE)

                sensors.getSensor( ctcId + ":GS").setState(INACTIVE)
                sensors.getSensor( ctcId + ":YS").setState(ACTIVE)
                sensors.getSensor( ctcId + ":RS").setState(INACTIVE)

                sensors.getSensor( signalId + ":TOC").setState(ACTIVE)
                sensors.getSensor( signalId + ":TOS").setState(INACTIVE)
                sensors.getSensor( signalId + ":TOP").setState(INACTIVE)

            else :
                #print " ctcId = " + ctcId + " state = red"
                turnouts.provideTurnout("NT" + self.DeviceName[2:3]).setState(THROWN)
                sensors.getSensor( signalId + ":WLL").setState(INACTIVE)
                sensors.getSensor( signalId + ":WLR").setState(ACTIVE)
                sensors.getSensor( signalId + ":WLC").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKR").setState(ACTIVE)
                sensors.getSensor( signalId + ":WKL").setState(INACTIVE)
                sensors.getSensor( signalId + ":WKC").setState(INACTIVE)

                sensors.getSensor( ctcId + ":GK").setState(INACTIVE)
                sensors.getSensor( ctcId + ":YK").setState(INACTIVE)
                sensors.getSensor( ctcId + ":RK").setState(ACTIVE)

                sensors.getSensor( ctcId + ":GS").setState(INACTIVE)
                sensors.getSensor( ctcId + ":YS").setState(INACTIVE)
                sensors.getSensor( ctcId + ":RS").setState(ACTIVE)

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

        class TimeoutReceiver2(java.awt.event.ActionListener):
            cb = None

            def actionPerformed(self, event) :
                if (self.cb != None) :
                    self.cb(event)
                return

            def setCallBack(self, cbf) :
                self.cb = cbf
                return

        class TimeoutReceiver3(java.awt.event.ActionListener):
            cb = None

            def actionPerformed(self, event) :
                if (self.cb != None) :
                    self.cb(event)
                return

            def setCallBack(self, cbf) :
                self.cb = cbf
                return

        def sendTimeoutHandler(self, event) :
            #print "In send timeout handler"
            self.sendTimer.stop()
#            self.relaySend.stop()
            sensors.getSensor("IS16:CCK").setState(INACTIVE)

            #sleep(2)

            signalNumber = self.DeviceName[2:3]
            if (self.Device.getValue() == "P") :
                turnouts.provideTurnout("NT" + signalNumber).setState(CLOSED)
            elif (self.Device.getValue() == "S") :
                turnouts.provideTurnout("NT" + signalNumber).setState(THROWN)


            smdl = 5 +  java.util.Random().nextInt(2) # Switch motor delay - 

            self.pauseTimer.setInitialDelay(smdl * 10)
            self.pauseTimer.start()
            return

        def pauseTimeoutHandler(self, event) :
            #print "In pause timeout handler"
            self.pauseTimer.stop()


            sensors.getSensor("IS17:ICK").setState(ACTIVE)
            #print "Turning on IC light"

#            self.relayClicks.loop()
            newName = "IS:" + self.DeviceName[2:3]
            sensors.getSensor( newName + ":WKC").setState(INACTIVE)
            sensors.getSensor( newName + ":WKL").setState(INACTIVE)
            sensors.getSensor( newName + ":WKR").setState(INACTIVE)

            ctcName = "CTC:TO" + self.DeviceName[2:3]
            if (sensors.getSensor( ctcName + "YK").getState() == ACTIVE) :
                sensors.getSensor( ctcName + "YK").setState(INACTIVE)
            if (sensors.getSensor( ctcName + "GK").getState() == ACTIVE) :
                sensors.getSensor( ctcName + "GK").setState(INACTIVE)
            if (sensors.getSensor( ctcName + "RK").getState() == ACTIVE) :
                sensors.getSensor( ctcName + "RK").setState(INACTIVE)

            icdl = 5 +  java.util.Random().nextInt(3) # Indicator code delay

            self.receiveTimer.setInitialDelay(icdl * 10)
            self.receiveTimer.start()
            return


        def receiveTimeoutHandler(self, event) :
            # see which phase we think we are in
            #print "In receive timeout Handler"
            self.receiveTimer.stop()

            signalNumber = self.DeviceName[2:3]
            #print " Signal number = " + str(signalNumber) + " signal state = " + self.Device.getValue()
            if (self.Device.getValue() == "P") :
                sensors.getSensor( "IS:" + signalNumber + ":WKC").setState(ACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":WKR").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":WKL").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":TOC").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":TOS").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":TOP").setState(ACTIVE)

                #sensors.getSensor("CTC:TO" + signalNumber + "YK").setState(INACTIVE)
                sensors.getSensor("CTC:TO" + signalNumber + "GK").setState(ACTIVE)
                #sensors.getSensor("CTC:TO" + signalNumber + "RK").setState(INACTIVE)

            elif (self.Device.getValue() == "C") :
                sensors.getSensor( "IS:" + signalNumber + ":WKC").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":WKR").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":WKL").setState(ACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":TOS").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":TOP").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":TOC").setState(ACTIVE)

                sensors.getSensor("CTC:TO" + signalNumber + "YK").setState(ACTIVE)
                #sensors.getSensor("CTC:TO" + signalNumber + "GK").setState(INACTIVE)
                #sensors.getSensor("CTC:TO" + signalNumber + "RK").setState(INACTIVE)
                jmri.jmrit.Sound("resources/sounds/Bell.wav").play()
            elif (self.Device.getValue() == "S") :
                sensors.getSensor( "IS:" + signalNumber + ":WKC").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":WKR").setState(ACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":WKL").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":TOC").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":TOP").setState(INACTIVE)
                sensors.getSensor( "IS:" + signalNumber + ":TOS").setState(ACTIVE)

                #sensors.getSensor("CTC:TO" + signalNumber + "YK").setState(INACTIVE)
                #sensors.getSensor("CTC:TO" + signalNumber + "GK").setState(INACTIVE)
                sensors.getSensor("CTC:TO" + signalNumber + "RK").setState(ACTIVE)

#            self.relayClicks.stop()
            self.parent.waitMsec(1000)
            sensors.getSensor("IS17:ICK").setState(INACTIVE)

            return

    #return False              # all done, don't repeat 
SignalMonitor().start()          # create one of these, and start it running

