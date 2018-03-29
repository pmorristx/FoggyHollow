import jarray
import jmri
import java.util.Random
from MineTrain import MineTrain

class Level1OreTrain(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.

        locoNumber = memories.provideMemory("L1 Loco Number").getValue()
        self.mineTrain = MineTrain()
        self.mineTrain.init(locoNumber, 1)


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

        self.tippleLights = sensors.provideSensor("Tipple Lights")
        self.bridgeLights = sensors.provideSensor("Lake Cavern Bridge")
        self.stoppingAtTipple = sensors.provideSensor("Stopping at Tipple")
        self.stoppingAtLake = sensors.provideSensor("Stopping at Lake")

        self.rightTunnelSignal = masts.getSignalMast("SM-L1-RT-E")
        self.hoistCavernEntranceSignal = masts.getSignalMast("SM-L1-HCE-E")
        self.backTunnelSignal = masts.getSignalMast("SM-L1-E-Back Tunnel")

        #
        #  Get the shutdown switch
        self.shutdownSwitch = sensors.getSensor("IS:L1AUTO")

        #
        #  Initialize the hoist cavern turnout to the main track
        self.hoistCavernTurnout = turnouts.provideTurnout("Hoist Cavern Turnout")
        self.hoistCavernTurnoutSwitchN = sensors.provideSensor("Hoist Cav Turnout Int Normal")
        self.hoistCavernTurnoutSwitchR = sensors.provideSensor("Hoist Cav Turnout Int Reverse")        
        self.throwTurnout(CLOSED)

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

        
        self.turnoutSound = self.mineTrain.loadSoundFile("preference:resources/sounds/SingleTurnout.wav")        

        self.mineTrain.singleToot = self.mineTrain.loadSoundFile("preference:resources/sounds/ShortSingleTootA.wav")
        self.mineTrain.longSingleToot = self.mineTrain.loadSoundFile("preference:resources/sounds/LongtSingleTootA.wav")        
        self.mineTrain.doubleToot = self.mineTrain.loadSoundFile("preference:resources/sounds/LongDoubleTootA.wav")
        self.mineTrain.tripleToot = self.mineTrain.loadSoundFile("preference:resources/sounds/TripleTootA.wav")                                                


        self.pee = self.mineTrain.loadSoundFile("preference:resources/sounds/peeing.wav")
        
        self.splash = []        
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash.wav"))
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash2.wav"))
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash3.wav"))
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash4.wav"))               
        
        self.backTunnelSound = []
        self.backTunnelSound.append(self.mineTrain.loadSoundFile("preference:resources/sounds/SingleRumble.wav"))        
        self.backTunnelSound.append(self.mineTrain.loadSoundFile("preference:resources/sounds/sleeping-giant.wav"))  
        self.backTunnelSound.append(self.mineTrain.loadSoundFile("preference:resources/sounds/BatsInCave.wav")) # bats

        self.backCavernBlock = blocks.provideBlock("L1 Back Cavern")
        self.leftTunnelBlock = blocks.provideBlock("L1 Left Tunnel")
        self.frontTunnelBlock = blocks.provideBlock("L1 Front Tunnel")
        self.tippleBlock = blocks.provideBlock("L1 Tipple")

        self.tippleProb = 0

        self.mineTrain.random = java.util.Random()
        self.mineTrain.findTrain()

        self.firstTime = True
        self.mineTrain.startTrain(True)

        return



    def waitBlockOccupied(self, sensor):
        self.ostate = sensor.getState()
        self.waitChange([sensor], 10000)
        if (self.ostate == sensor.getState()) :
            print "Sensor timed out " + sensor.getUserName()
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
            print "chance of entering hoist cavern = " + str(cavProb) + " out of 60"
            self.enterHoistCavern = cavProb < 60
            if (self.enterHoistCavern) :
                self.throwTurnout(THROWN)
                self.waitMsec(4000)

            self.mineTrain.startTrain(False)

            if (self.enterHoistCavern) :
                self.waitBlockOccupied(self.hoistCavernSensor)
                self.mineTrain.throttle.setSpeedSetting(0.1)  # Slow down so we don't overrun EOT
                self.waitBlockOccupied(self.hoistCavernEOTSensor)
                self.waitMsec(2000)  # wait half a second to get a little farther into hoist cavern
            else :
                self.waitBlockOccupied(self.leftTunnelSensor)
                self.waitMsec(2500)

            self.mineTrain.stopTrain()

            self.waitMsec(10000)

        #
        #  Turn the flag off to stop at the tipple.  This frees the signal to function normally.
        self.stoppingAtTipple.setState(INACTIVE)
        self.waitMsec(1000)
        
        self.mineTrain.startTrainByAspect(True, self.rightTunnelSignal.getAspect())
            
        self.waitMsec(1000)
        self.tippleLights.setState(INACTIVE)


        return

    #
    #  Stop the train at the back lake cavern.
    def stopAtLake(self):
        try:
            self.waitMsec(1200)
            self.mineTrain.stopTrain()

            peeProb = java.util.Random().nextInt(100)
            if (peeProb < 75):
                self.pee.play();
                self.waitMsec(16000)

            for i in range(0,4) :
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
            self.waitBlockOccupied(self.leftTunnelSensor)
        self.setBlockContent(self.leftTunnelBlock)
        
        #
        #  Wait until we get to the front of the left tunnel near the signal.
        self.waitMsec(4500)

        #  We are coming around the left tunnel, check the signal
        if (self.hoistCavernEntranceSignal.getAspect() == "Stop") :
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
            self.mineTrain.throttle.setSpeedSetting(0.1)
            self.tippleLights.setState(ACTIVE)
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
        if ((java.util.Random().nextInt(100) < 60) and (self.tippleLights.getState == INACTIVE) and (self.l2RightBridgeSensor.getState() == ACTIVE)) :
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
            self.bridgeLights.setState(ACTIVE)

        self.waitBlockOccupied(self.backCavernSensor)
        self.setBlockContent(self.backCavernBlock)

        if (self.backTunnelSignal.getAspect() == "Stop") :
            self.stopAtLake()

            self.mineTrain.startTrain(True)

            self.waitMsec(3000)
            self.bridgeLights.setState(INACTIVE)
        else :
            self.waitBlockOccupied(self.backTunnelSensor) 

        if (java.util.Random().nextInt(100) < 60) :
            self.backTunnelSound[java.util.Random().nextInt(3)].play()

        return True
# end of class definition

# start one of these up
Level1OreTrain().start()
