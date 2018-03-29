#
# TurnoutMonitor.py

#

import java
import javax.swing
import javax.swing.Timer

class TurnoutMonitor(jmri.jmrit.automat.AbstractAutomaton) :

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
#        logFileName = "C:\\Users\\pmorris.PETROLITE\\JMRI\TurnoutMonitor.log"
        logFileName = jmri.util.FileUtil.getExternalFilename("preference:BBTurnoutMonitor.log")


        #
        # Turnouts being initialized and tracked.
        # Turnouts not found while processing the existing tracking file are initialized to the
        # first entry in the allowable states list for turnouts - CLOSED.
        #
        #SignalList = ["IM21:TV", "IM25:TV"]
        SignalList = ["IM1:TV", "IM9:TV", "IM3:TV", "IM11:TV"]        

        signalStates = ["N", "R"]

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
        shutdown.register(self.SignalMonitorShutdown("Turnout Monitor"))

        #
        # Initialize the JMRI turnout devices and log their states
        #
        for i in range(len(SignalList)) :
            DeviceList[SignalList[i]].setInitialDeviceState(logFile, self)

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
        from javax.swing import Timer

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
            self.DeviceName = aName
            self.Device = aDevice
            self.DeviceNumber = self.DeviceName[2:self.DeviceName.find(":")]
            self.AllowedStates = aAllowedStates
            self.parent = aParent
            self.DeviceValue = self.AllowedStates[0]
            self.LogFile = aLogFile

            self.timeoutListener = self.TimeoutReceiver()
            self.timeoutListener.setCallBack(self.receiveTimeoutHandler)


            self.receiveTimer = Timer(100, self.timeoutListener)
            self.receiveTimer.setInitialDelay(10);

            self.receiveTimer.stop()
            self.receiveTimer.setRepeats(False)

            self.sendTimeoutListener = self.TimeoutReceiver2()
            self.sendTimeoutListener.setCallBack(self.sendTimeoutHandler)

            self.sendTimer = Timer(100, self.timeoutListener)            
            self.sendTimer.setInitialDelay(10);
            self.sendTimer.stop()
            self.sendTimer.setRepeats(False)

            self.pauseTimeoutListener = self.TimeoutReceiver()
            self.pauseTimeoutListener.setCallBack(self.pauseTimeoutHandler)
            
            self.pauseTimer = Timer(100, self.pauseTimeoutListener)
            self.pauseTimer.setInitialDelay(10);            
            
            self.pauseTimer.stop()
            self.pauseTimer.setRepeats(False)

            self.finalTimeoutListener = self.TimeoutReceiver()
            self.finalTimeoutListener.setCallBack(self.finalTimeoutHandler)
            self.finalTimer = Timer(100, self.finalTimeoutListener)
            self.finalTimer.setInitialDelay(10);            
            self.finalTimer.stop()
            self.finalTimer.setRepeats(False)


#            self.relayClicks = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/EnhancedCTCRelayTrimmed.wav"))
            self.relayClicks = jmri.jmrit.Sound("resources/sounds/Code-receive.wav")
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
            print 'updateState ' + self.DeviceName + " to state = " + aNewState
            for i in range(len(self.AllowedStates)) :
                if (aNewState == self.AllowedStates[i]) :
                    self.DeviceValue = aNewState
                    self.Device.setValue(aNewState)
                    break

        # TrackDevice.propertyChange - Record state changes as a result of activities
        #                              elsewhere in JMRI
        #
        # aEvent : Event triggering the change (we don't actually look at the event...)
        #
        def propertyChange(self, aEvent) :
            newValue = self.Device.getValue()
            print ("***** In propertyChange")
            memories.getMemory("IM5:TVC").setValue("1")

            #
            #  Turn on Control Code indicator light
            codeSendSensor = sensors.getSensor("Code Send Indicator")
            codeSendSensor.setState(ACTIVE)

            #
            #  Start relay clicking sound
            self.relaySend.loop()

            #
            #  Start timer to keep code send light on and relays clicking for a while.
            ccdl = 15 #+  java.util.Random().nextInt(1) # Code transmission delay
            self.sendTimer.setDelay(ccdl * 1000)
            #self.sendTimer.start()
            
            
            self.parent.waitMsec(ccdl*1000);
            
            self.relaySend.stop()
            codeSendSensor.setState(INACTIVE)
            

            if (newValue == self.DeviceValue) :
                return
                
            for i in range(len(self.AllowedStates)) :
                if (newValue == self.AllowedStates[i]) :
                    self.DeviceValue = newValue
                    self.LogFile.write(self.DeviceName + " " + self.DeviceValue + "\n")
                    self.LogFile.flush()
                    break
            return


        # TrackDevice.setInitialDeviceState - After reading all of the old tracking file we
        #                                     now initialize the actual devices to their last
        #                                     known states and log these states into the new
        #                                     log file.
        #
        def setInitialDeviceState(self, logFile, parent) :
            #       Uncomment the following print statement to display the list of devices being tracked.
            print "In setInitDeviceState, name = " + self.DeviceName + " value = " + self.DeviceValue
            self.LogFile = logFile
###            self.Device.setState(self.DeviceValue)
            self.Device.addPropertyChangeListener(self)
            #logStateChange2(self.DeviceName, self.DeviceState, False)
            logFile.write(self.DeviceName + " " + self.DeviceValue + "\n")
            

            signalId = "IS:" + self.DeviceNumber
            # Move the switch lever to the correct position
            sensors.getSensor( signalId + ":CB").setState(INACTIVE)
            if (self.DeviceValue == "N") :
                turnouts.provideTurnout("NT" + self.DeviceNumber).setState(CLOSED)
                self.parent.waitMsec(100)
                sensors.getSensor( signalId + ":NK").setState(ACTIVE)
                sensors.getSensor( signalId + ":L").setState(ACTIVE)
                sensors.getSensor( signalId + ":RK").setState(INACTIVE)

            else :
                turnouts.provideTurnout("NT" + self.DeviceNumber).setState(THROWN)
                self.parent.waitMsec(100)
                sensors.getSensor( signalId + ":NK").setState(INACTIVE)
                sensors.getSensor( signalId + ":RK").setState(ACTIVE)
                sensors.getSensor( signalId + ":L").setState(INACTIVE)

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

        def sendTimeoutHandler(self, event) :
            print "In send timeout handler"
            self.sendTimer.stop()
            self.relaySend.stop()
            sensors.getSensor("IS16:CCK").setState(INACTIVE)


            smdl = 5 #+  java.util.Random().nextInt(2) # Switch motor delay - 

            self.pauseTimer.setInitialDelay(smdl * 100)
            self.pauseTimer.start()
            return
        #
        #  Timeout handler between send & receive.
        #  Turn panel indicators off & start indication code relay clicks.
        def pauseTimeoutHandler(self, event) :
            self.pauseTimer.stop()


            sensors.getSensor("Code Receive Indicator").setState(ACTIVE)
            self.relayClicks.loop()
            newName = "IS:" + self.DeviceNumber
            sensors.getSensor( newName + ":NK").setState(INACTIVE)
            sensors.getSensor( newName + ":RK").setState(INACTIVE)
            signals.getSignalHead("VH:T" + str(self.DeviceNumber) + "N").setAppearance(DARK)
            signals.getSignalHead("VH:T" + str(self.DeviceNumber) + "R").setAppearance(DARK)

            icdl = 5 #+  java.util.Random().nextInt(3) # Indicator code delay

            self.receiveTimer.setInitialDelay(icdl * 100)
            self.receiveTimer.start()
            return

        #
        #  Final timeout handler....turn off Indication Code relay clicks and change indicator lights on panel.
        def receiveTimeoutHandler(self, event) :
            # see which phase we think we are in
            self.receiveTimer.stop()

            sensors.getSensor("Code Receive Indicator").setState(INACTIVE)

            #
            #  Throw the turnout.  We should do this in an earlier timeout handler, but with the CTC panel lights hardwired to the tortoise motor,
            #  the lights change too soon.
            if (memories.getMemory("IM1:FB").getValue() == 0) :
                if (self.Device.getValue() == "N") :
                    turnouts.provideTurnout("NT" + self.DeviceNumber).setState(CLOSED)
                else :
                    turnouts.provideTurnout("NT" + self.DeviceNumber).setState(THROWN)

            self.finalTimer.setInitialDelay(6000)
            self.finalTimer.start()

            return

        #
        #  Final timeout handler....turn off Indication Code relay clicks and change indicator lights on panel.
        def finalTimeoutHandler(self, event) :
            # see which phase we think we are in
            self.finalTimer.stop()

            self.relayClicks.stop()
            sensors.getSensor("Code Receive Indicator").setState(INACTIVE)
            memories.getMemory("IM5:TVC").setValue("0")
            memories.getMemory("IM1:FB").setValue(0)
            return

    #return False              # all done, don't repeat 
TurnoutMonitor().start()          # create one of these, and start it running

