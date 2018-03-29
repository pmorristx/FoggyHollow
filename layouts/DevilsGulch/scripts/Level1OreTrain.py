import jarray
import jmri
import java.util.Random
from time import sleep
from MineTrain import MineTrain
import  AOSBackgroundSound

class Level1OreTrain(jmri.jmrit.automat.AbstractAutomaton) :

    class HoistTopListener(java.beans.PropertyChangeListener) :

        def init (self, hoistMovingSensor, boilerIntensity) :
            self.boilerIntensity = boilerIntensity
            self.hoistMovingSensor = hoistMovingSensor
            
        def propertyChange(self, event) :
            if (event.source.getState() == ACTIVE) :
                self.boilerIntensity.setState(INACTIVE)
                #self.roofSign.setState(INACTIVE)
                self.hoistMovingSensor.setState(INACTIVE)
                print "Hoist Top Listener fired"

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration
        locoNumber = memories.provideMemory("L1 Loco Number").getValue()
        self.mineTrain = MineTrain()
        self.mineTrain.init(locoNumber, 1)

        self.waitingFor = memories.provideMemory("L1 Wait")
        
        #  Get DCC control of the hoist
        self.hoist = self.getThrottle(99, False)         


        #  Get occupancy sensors
        self.tippleSensor = sensors.provideSensor("OS:L1:Tipple")
        self.leftTunnelSensor = sensors.provideSensor("OS:L1:Left Tunnel")
        self.frontTunnelSensor = sensors.provideSensor("OS:L1:Front Tunnel")
        self.rightTunnelSensor = sensors.provideSensor("OS:L1:Right Tunnel")
        self.backTunnelSensor = sensors.provideSensor("OS:L1:Back Tunnel")
        self.backCavernSensor = sensors.provideSensor("OS:L1:Back Cavern")
        self.hoistCavernEntranceSensor = sensors.provideSensor("OS:L1:Hoist Cavern Entrance")
        self.hoistCavernEOTSensor = sensors.provideSensor("OS:L1:Hoist EOT")
        self.hoistCavernSensor = sensors.provideSensor("OS:L1:Hoist Cavern")
        self.l2RightBridgeSensor = sensors.provideSensor("OS:L2:Right Bridge")
        self.indicator = sensors.provideSensor("L1 Auto Indicator")

        self.useHoistTurnout = sensors.provideSensor("Use Hoist Turnout")        
        
        self.hoistTopSensor = sensors.provideSensor("Hoist S2 Indicator")
        self.hoistBottomSensor = sensors.provideSensor("Hoist L3 Indicator")          
        self.hoistCallButtonL3 = sensors.provideSensor("IS Call Hoist To L3")
        self.hoistCallButtonS2 = sensors.provideSensor("IS Call Hoist To S2")        
        self.hoistMovingSensor = sensors.provideSensor("Hoist Moving")
        self.boilerIntensity = sensors.provideSensor("Winding House Boiler Intensity")
#        self.roofSign = lights.provideLight("NL78") # Mine Bldg Roof Sign


        
        self.tippleLights = lights.provideLight("L3 Tipple Lanterns")
        self.bridgeLights = lights.provideLight("L3 Lake Cavern Bridge")
        self.stoppingAtTipple = sensors.provideSensor("Stopping at Tipple")
        self.stoppingAtLake = sensors.provideSensor("Stopping at Lake")

        self.rightTunnelSignal = masts.getSignalMast("SM-L1-RT-E")
        self.hoistCavernEntranceSignal = masts.getSignalMast("SM-L1-HCE-E")
        self.backTunnelSignal = masts.getSignalMast("SM-L1-E-Back Tunnel")

        signals.getSignalHead("Left Tunnel Signal East").setLit(True)
        signals.getSignalHead("Left Tunnel Signal West").setLit(True)
        signals.getSignalHead("Right Tunnel Signal East").setLit(True)
        

        #
        #  Get the shutdown switch
        self.shutdownSwitch = sensors.getSensor("IS:L1AUTO")

        #
        #  Initialize the hoist cavern turnout to the main track
        self.hoistCavernTurnout = turnouts.provideTurnout("Hoist Cavern Turnout")
        self.hoistCavernTurnoutSwitchN = sensors.provideSensor("Hoist Cav Turnout Int Normal")
        self.hoistCavernTurnoutSwitchR = sensors.provideSensor("Hoist Cav Turnout Int Reverse")        
        self.throwTurnout(CLOSED)

        self.useHoistTurnout.setState(INACTIVE)

        self.probBackTunnelBats = int(memories.provideMemory("Prob L1 Back Tunnel Bats").getValue())
        self.probTippleStop = int(memories.provideMemory("Prob L1 Tipple Stop").getValue())
        self.probLakeStop = int(memories.provideMemory("Prob L1 Lake Stop").getValue())
        self.probLeftTunnelStop = int(memories.provideMemory("Prob L1 Left Tunnel Stop").getValue())
        self.probHoistStop = int(memories.provideMemory("Prob L1 Hoist Stop").getValue())

        # get loco address. For long address change "False" to "True"

        self.mineTrain.throttle = self.getThrottle(int(self.mineTrain.locoNumber), False)  # short address 14

        self.chainPulley = self.mineTrain.loadSoundFile("preference:resources/sounds/ChainPulley.wav")  # 0.2
#        self.rocks = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/MineRockFall.wav"))  # 19
        self.rocks = []
        self.rocks.append(self.mineTrain.loadSoundFile("preference:resources/sounds/rocks.wav"))  # 7
        self.rocks.append(self.mineTrain.loadSoundFile("preference:resources/sounds/RockChute1.wav"))  
        self.rocks.append(self.mineTrain.loadSoundFile("preference:resources/sounds/RockChute2.wav"))  
        self.rocks.append(self.mineTrain.loadSoundFile("preference:resources/sounds/RockChute3.wav")) 
        self.rocks.append(self.mineTrain.loadSoundFile("preference:resources/sounds/MineRockFall.wav"))

        self.raiseHoistSignal = self.mineTrain.loadSoundFile("preference:resources/sounds/Short-Short-Long-Signal.wav")                

        
        self.turnoutSound = self.mineTrain.loadSoundFile("preference:resources/sounds/SingleTurnout.wav")        

        self.mineTrain.singleToot = self.mineTrain.loadSoundFile("preference:resources/sounds/ShortSingleTootA.wav")
        self.mineTrain.longSingleToot = self.mineTrain.loadSoundFile("preference:resources/sounds/LongtSingleTootA.wav")        
        self.mineTrain.doubleToot = self.mineTrain.loadSoundFile("preference:resources/sounds/LongDoubleTootA.wav")
        self.mineTrain.tripleToot = self.mineTrain.loadSoundFile("preference:resources/sounds/TripleTootA.wav")                                                


        self.pee = self.mineTrain.loadSoundFile("preference:resources/sounds/peeing.wav")
        
        self.splash = []
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/singleSwimmer.wav"))        
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash.wav"))
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash2.wav"))
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash3.wav"))
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash4.wav"))               
        
        self.backTunnelSound = []
        self.backTunnelSound.append(self.mineTrain.loadSoundFile("preference:resources/sounds/SingleRumble.wav"))        
        self.backTunnelSound.append(self.mineTrain.loadSoundFile("preference:resources/sounds/sleeping-giant.wav"))  
        self.backTunnelSound.append(self.mineTrain.loadSoundFile("preference:resources/sounds/BatsInCave.wav")) # bats
        
        #
        #  Hoist sounds
#        self.signalBell = self.mineTrain.loadSoundFile("preference:resources/sounds/SingleElectricBell.wav") # 0.11        
#        self.hoistWav = self.mineTrain.loadSoundFile("preference:resources/sounds/Hoist1Minute.wav") # 1.16                

        self.backCavernBlock = blocks.provideBlock("L1 Back Cavern")
        self.leftTunnelBlock = blocks.provideBlock("L1 Left Tunnel")
        self.frontTunnelBlock = blocks.provideBlock("L1 Front Tunnel")
        self.tippleBlock = blocks.provideBlock("L1 Tipple")

        self.tippleProb = 0


#        self.hoistUpSensor = sensors.provideSensor("Hoist Moving Up")
#        self.hoistDownSensor = sensors.provideSensor("Hoist Moving Down")                
#        self.hoistTopListener = self.HoistTopListener()
#        self.hoistTopListener.init(self.hoistMovingSensor, self.boilerIntensity)
#        self.hoistTopSensor.addPropertyChangeListener(self.hoistTopListener)

        self.mineTrain.random = java.util.Random()
        self.mineTrain.findTrain()

        self.firstTime = True
        self.mineTrain.startTrain(True)


        return


    def waitBlockOccupied(self, sensor):
        self.ostate = sensor.getState()
        self.waitingFor.setValue(sensor.getUserName())
        self.waitChange([sensor], 30000)
        if (self.ostate == sensor.getState()) :
            print "Sensor timed out " + sensor.getUserName()
        self.waitingFor.setValue("")
        return


#    def setHoistDirection(self, direction) :
#        if (direction == "DOWN") :
#            self.hoist.setIsForward(True)
#        else:
#            self.hoist.setIsForward(False)
    #
    #  Run the hoist when the train    enters the hoist cavern
    def doHoist(self):

        self.waitMsec(1200)
        
        #
        #  Ring bell to call hoist down
        self.hoistCallButtonL3.setState(ACTIVE)
#        self.roofSign.setState(ACTIVE)
        self.boilerIntensity.setState(ACTIVE)

        self.hoistMovingSensor.setState(ACTIVE)
        #
        #  Lower cage to main level
        self.waitSensorActive(self.hoistBottomSensor)
        self.hoistMovingSensor.setState(INACTIVE)

        self.waitMsec(1000)

        self.mineTrain.startTrain(False)
        self.waitMsec(2400)
        self.mineTrain.stopTrain()
        
        self.waitMsec(30000)
        
        #  Ring bell to call to raise cage
        self.raiseHoistSignal.play()
        self.waitMsec(7000)
        self.hoistCallButtonS2.setState(ACTIVE)
        self.hoistMovingSensor.setState(ACTIVE)
        self.waitMsec(12000)

        self.mineTrain.startTrainSlow(True)
        return
    #
    #  Depart the tipple after stopping there.
    def leaveTipple(self):
        self.enterHoistCavern = False
        
        #
        #  Sometimes we back up.
        if ((self.mineTrain.random.nextInt(100) < 65) and (self.shutdownSwitch.getState() == ACTIVE)) :
            #
            #  Sometimes we enter the hoist cavern
            cavProb = java.util.Random().nextInt(100)
#            print "chance of entering hoist cavern = " + str(cavProb) + " out of 60"
            self.enterHoistCavern = (cavProb < 60) and (self.hoistTopSensor.getState() == ACTIVE) and (self.shutdownSwitch.getState() == ACTIVE and (self.useHoistTurnout.getState() == ACTIVE))
            if (self.enterHoistCavern) :
                self.throwTurnout(THROWN)
                self.waitMsec(4000)

            self.mineTrain.startTrain(False)

            if (self.enterHoistCavern) :
                self.waitBlockOccupied(self.hoistCavernSensor)
                self.mineTrain.throttle.setSpeedSetting(0.1)  # Slow down so we don't overrun EOT
                self.waitBlockOccupied(self.hoistCavernEOTSensor)
                self.waitMsec(750)  # wait half a second to get a little farther into hoist cavern
                self.mineTrain.stopTrain()                
                self.doHoist()
                
            else :
                self.waitBlockOccupied(self.leftTunnelSensor)
                self.waitMsec(2500)
                self.mineTrain.stopTrain()


            self.waitMsec(5000)

        #
        #  Turn the flag off to stop at the tipple.  This frees the signal to function normally.
        self.stoppingAtTipple.setState(INACTIVE)
        self.waitMsec(1000)
        
        self.mineTrain.startTrainByAspect(True, self.rightTunnelSignal.getAspect())
            
        self.waitMsec(1000)
        self.tippleLights.setState(OFF)


        return

    #
    #  Stop the train at the back lake cavern.
    def stopAtLake(self):
        try:
            self.waitMsec(1200)
            self.mineTrain.stopTrain()
            
            self.changeMessage()
            
            peeProb = java.util.Random().nextInt(100)
            if (peeProb < 75):
                self.pee.play();
                self.waitMsec(16000)

            for i in range(0,5) :
                splashProb = java.util.Random().nextInt(100)
                delay = java.util.Random().nextInt(3)
                if (splashProb > 50):
                    self.splash[i].play();
                    self.waitMsec(2000 * delay)
                    
        
            self.waitMsec(20000)  #  Delay at lake bridge
                    
            #
            #  Backup to the tipple once in a while
            if (java.util.Random().nextInt(100) < 25) :
                self.mineTrain.startTrain(False)
                self.waitBlockOccupied(self.frontTunnelSensor)
                self.mineTrain.stopTrain()
                self.waitMsec(3000)
                
            self.stoppingAtLake.setState(INACTIVE)            

        except:
            print "Error stopping at lake"


        return

    #
    #  Clean shutdown when switch is turned off.  Return train to the front of the layout (Hoist Cavern Entrance)
    #  and shut the train down.
    def shutdown(self):
        #
        #  Clean shutdown...move train to HCE and stop
#                        self.mineTrain.throttle.setSpeedSetting(0.4)
#                        self.waitBlockOccupied(self.hoistCavernEntranceSensor)
        self.mineTrain.throttle.setSpeedSetting(0)
        self.mineTrain.throttle.setF0(False)
        self.mineTrain.throttle.setF1(False)
        self.mineTrain.throttle.setF2(False)
        self.throwTurnout(CLOSED)
        jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/VeryLongSingleTootA.wav")).play()
        self.indicator.setState(INACTIVE)

    #
    #  Throw the hoist cavern turnout to either "CLOSED" or "THROWN".  Check current state before
    #  either moving turnout or playing sound.
    def throwTurnout(self, state):
        if (self.hoistCavernTurnout.getState() != state) :
            self.turnoutSound.play()
            if (state == CLOSED) :
                self.hoistCavernTurnoutSwitchN.setState(ACTIVE)       
            else :
                self.hoistCavernTurnoutSwitchR.setState(ACTIVE)        
    def setBlockContent(self, block):
        try:
            block.setValue("AoS #" + str(self.mineTrain.locoNumber))
        except:
            print "Failed setting block label for block " + block.getUserName()
        return

    #
    #  Main loop repeatedly called until False is returned.
    def handle(self):
        print "<<< Level1OreTrain >>>"
        self.indicator.setState(ACTIVE) # Turn on blue light on control panel

        #
        #  Decide if we are going to stop at the tipple.  If so, we will keep the speed down.
        self.tippleProb = java.util.Random().nextInt(100)
        print "Stopping at tipple prob = " + str(self.tippleProb) + " out of " + str(self.probTippleStop)
        if ((self.tippleProb < self.probTippleStop) and (self.shutdownSwitch.getState() == ACTIVE)) :
            self.stoppingAtTipple.setState(ACTIVE)
        else :
            self.stoppingAtTipple.setState(INACTIVE)

        # If the loco isn't already moving, start it, otherwise leave it alone so we don't change the speed.
        if (self.mineTrain.throttle.getSpeedSetting() == 0) :
            self.mineTrain.startTrain(True)

        #
        #  Let train run to left tunnel
        if (self.firstTime) :
            self.waitSensorActive(self.leftTunnelSensor)
            self.firstTime = False
        else:
            self.waitSensorActive(self.leftTunnelSensor)
        self.setBlockContent(self.leftTunnelBlock)
        
        #
        #  Wait until we get to the front of the left tunnel near the signal.
        self.waitMsec(4500)

        #  We are coming around the left tunnel, check the signal
        if (self.hoistCavernEntranceSignal.getAspect() == "Stop" or self.shutdownSwitch.getState() == INACTIVE) :
            if (self.shutdownSwitch.getState() == INACTIVE) :
                self.shutdown()
                return self.shutdownSwitch.getState() == ACTIVE

            self.mineTrain.throttle.setSpeedSetting(0)
            self.mineTrain.throttle.setF4(True)
            self.waitMsec(5000)

            #
            #  Throw the turnout for us to proceed
            self.throwTurnout(CLOSED)
            self.waitMsec(4000)

            #
            #  After waiting for turnout the move, undim the headlight and start forward
            self.mineTrain.throttle.setF4(False)

        #
        #  The signal will be yellow if we are going to stop at the tipple.  If so, turn on the tipple lights
        #  and proceed slow
        if (self.hoistCavernEntranceSignal.getAspect() == "Approach") :
            self.tippleLights.setState(ON)
            currentSpeed = self.mineTrain.throttle.getSpeedSetting()
            step = (currentSpeed - 0.1) / 3.0
            print " At hoistCavEntrance Signal , speed = " + str(currentSpeed) + " step = " + str(step)
            for s in range (1,3) :
                self.mineTrain.throttle.setSpeedSetting(currentSpeed - (step*s))
                self.waitMsec(20)

        elif (self.hoistCavernEntranceSignal.getAspect() == "Clear") :
            if (self.mineTrain.throttle.getSpeedSetting() < 0.1) :
                self.mineTrain.throttle.setSpeedSetting(self.mineTrain.getSpeed(True))  # was 0.3

        #
        #  Front Tunnel
        #
        if (self.mineTrain.throttle.getSpeedSetting() < 0.1) :
            print "Not running before frontTunnelSensor ... applying band-aid"
            self.mineTrain.throttle.setSpeedSetting(0.1)
        else:
            print "Waiting for frontTunnelSensor, speed = " + str(self.mineTrain.throttle.getSpeedSetting())

        self.waitBlockOccupied(self.frontTunnelSensor)
        self.setBlockContent(self.frontTunnelBlock)
        
        # Before we pass the tipple, determine if we will stop at the lake cavern.
        if ((java.util.Random().nextInt(100) < self.probLakeStop) and (self.shutdownSwitch.getState() == ACTIVE)) :
            self.stoppingAtLake.setState(ACTIVE)
        else :
            self.stoppingAtLake.setState(INACTIVE)        

        # wait for tipple sensor to trigger, then stop
        self.waitBlockOccupied(self.tippleSensor)
        self.setBlockContent(self.tippleBlock)

        # Greet a train on the upper bridge 60% of the time unless we are busy stopping at the tipple
        if ((java.util.Random().nextInt(100) < 60) and (self.tippleLights.getState == OFF) and (self.l2RightBridgeSensor.getState() == ACTIVE)) :
            try :
                    self.longSingleToot.play()
            except:
                    print "Error playing longSingleToot"  

        if (self.rightTunnelSignal.getAspect() == "Stop"):
            try:
                self.waitMsec(2200)
                self.mineTrain.stopTrain()
                self.waitMsec(2000)

                self.chainPulley.play();
                self.waitMsec(2000)
                rockIdx = java.util.Random().nextInt(5)
                self.rocks[rockIdx].play();
                self.changeMessage()
                self.waitMsec(12000)  # was 18000
                self.chainPulley.play();
                self.waitMsec(1000)
            except:
                print "Error stopping at tipple"

            self.waitMsec(15000)  # wait for 15 seconds at the tipple
                          
            #
            #  Leave Tipple
            self.leaveTipple()
            self.waitMsec(500)  # wait 1 second for Xpressnet to catch up

        # wait for back cavern sensor  to trigger
        if (self.stoppingAtLake.getState() == ACTIVE) :
            self.waitBlockOccupied(self.rightTunnelSensor)
            self.bridgeLights.setState(ON)

        self.waitBlockOccupied(self.backCavernSensor)
        self.setBlockContent(self.backCavernBlock)
        if (java.util.Random().nextInt(100) > 80 and self.useHoistTurnout.getState() == INACTIVE) :
            #self.hoistCavernEntranceSignal.setAspect("Stop")
            self.throwTurnout(THROWN)            
        if (self.backTunnelSignal.getAspect() == "Stop") :
            self.stopAtLake()

            self.mineTrain.startTrain(True)

            self.waitMsec(3000)
            self.bridgeLights.setState(OFF)
        else :
            self.waitBlockOccupied(self.backTunnelSensor) 

        if (java.util.Random().nextInt(100) < 60) :
            self.backTunnelSound[java.util.Random().nextInt(3)].play()

        return True
# end of class definition

# start one of these up
Level1OreTrain().start()
