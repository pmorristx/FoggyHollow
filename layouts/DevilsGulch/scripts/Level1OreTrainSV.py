import jarray
import jmri
import java.util.Random
from MineTrain import MineTrain

class Level1OreTrain(jmri.jmrit.automat.AbstractAutomaton) :
        
#	class shutdownListener(java.beans.PropertyChangeListener) :	
#		def init(self, mast):
#                        self.signalMast = mast
#			return		
#		
#		def propertyChange(self, event) :
#			if (event.source.getState() == INACTIVE) :
#				try:
 #                                       self.signalMast.setAspect("Stop")
#				except :
#					print "Error setting signal mast to stop ", sys.exc_info()[0], sys.exc_info()[1]				

	def init(self):
		# init() is called exactly once at the beginning to do
		# any necessary configuration.
	
		locoNumber = memories.provideMemory("L1 Loco Number").getValue()	
		self.mineTrain = MineTrain()
		self.mineTrain.init(locoNumber, 1)
		
		#self.stoppingAtLake = False
		#self.stoppingAtTipple = False
	
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
#		shutdownListener = self.shutdownListener()
#		shutdownListener.init(self.hoistCavernEntranceSignal)
#		self.shutdownSwitch.addPropertyChangeListener(shutdownListener)
		#
		#  Get the hoist cavern turnout
		self.hoistCavernTurnout = turnouts.provideTurnout("Hoist Cavern Turnout")
		self.hoistCavernTurnoutSwitchN = sensors.provideSensor("Hoist Cav Turnout Int Normal")
		self.hoistCavernTurnoutSwitchR = sensors.provideSensor("Hoist Cav Turnout Int Reverse")				
		self.hoistCavernTurnoutSwitchN.setState(ACTIVE)
				
		self.probBackTunnelBats = int(memories.provideMemory("Prob L1 Back Tunnel Bats").getValue())
	   	self.probTippleStop = int(memories.provideMemory("Prob L1 Tipple Stop").getValue())
		self.probLakeStop = int(memories.provideMemory("Prob L1 Lake Stop").getValue())
		self.probLeftTunnelStop = int(memories.provideMemory("Prob L1 Left Tunnel Stop").getValue())
		self.probHoistStop = int(memories.provideMemory("Prob L1 Hoist Stop").getValue())

		# get loco address. For long address change "False" to "True"


		self.mineTrain.throttle = self.getThrottle(int(self.mineTrain.locoNumber), False)  # short address 14

		self.chainPulley = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/chaindoor.wav"))  # 0.2
#		self.rocks = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/MineRockFall.wav"))  # 19
		self.rocks = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/rocks.wav"))  # 7												
		self.bats = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/BatsInCave.wav"))

		self.mineTrain.singleToot = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ShortSingleTootA.wav"))
		self.longSingleToot = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/LongSingleTootA.wav"))				
		self.mineTrain.doubleToot = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/LongDoubleTootA.wav"))
		self.mineTrain.tripleToot = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/TripleTootA.wav"))

		self.rocks = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/MineRockFall.wav"))
		self.pee = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/peeing.wav"))
		self.splash1 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Splash.wav"))
		self.splash2 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Splash2.wav"))

		self.backCavernBlock =  blocks.provideBlock("L1 Back Cavern")
		self.leftTunnelBlock =  blocks.provideBlock("L1 Left Tunnel")
		self.frontTunnelBlock =  blocks.provideBlock("L1 Front Tunnel")				
		self.tippleBlock = blocks.provideBlock("L1 Tipple")

		self.tippleProb = 0
				
		self.mineTrain.random = java.util.Random()
		self.mineTrain.findTrain()

                self.firstTime = True
		if (self.mineTrain.throttle.getSpeedSetting() == 0) :
			self.mineTrain.startTrain(True)                
				
		return
	


        def waitBlockOccupied(self, sensor):
                self.ostate = sensor.getState()
              #  if (sensor.getState() == ACTIVE):
              #          print "WaitBlockOccupied - original state Active, sensor = " + sensor.getUserName()
              #  else:
              #          print "WaitBlockOccupied - original state Not Active, sensor = " + sensor.getUserName()                        
                self.waitChange([sensor], 10000)
              #  if (sensor.getState() != self.ostate) :
              #          print "Triggered on sensor change"
                return

        def leaveTipple(self):

                self.enterHoistCavern = False
                if ((self.mineTrain.random.nextInt(100) < 70) and (self.shutdownSwitch.getState() == ACTIVE)) :
                        #
                        #  backup sometimes

                        self.enterHoistCavern = self.mineTrain.random.nextInt(100) < 70

                        if (self.enterHoistCavern) :
                                self.hoistCavernTurnoutSwitchR.setState(ACTIVE)
                                self.waitMsec(4000)

                        self.mineTrain.startTrain(False)

                        if (self.enterHoistCavern) :
                                self.waitBlockOccupied(self.hoistCavernSensor)
                                self.mineTrain.throttle.setSpeedSetting(0.1) # Slow down so we don't overrun EOT
                                self.waitBlockOccupied(self.hoistCavernEOTSensor)
                                self.waitMsec(750) # wait half a second to get a little farther into hoist cavern                                        
                        else :
                                self.waitBlockOccupied(self.leftTunnelSensor)
                                self.waitMsec(2500)

                        self.mineTrain.stopTrain()

                        self.waitMsec(10000)



                self.stoppingAtTipple.setState(INACTIVE)
                self.waitMsec(1000)
                self.mineTrain.startTrain(True)
                self.waitMsec(1000)
                self.tippleLights.setState(INACTIVE)
                

                return

        def stopAtLake(self):
                try:
                        self.waitMsec(1200)
                        self.mineTrain.stopTrain()

                        peeProb = java.util.Random().nextInt(100)
                        if (peeProb > 85):
                                self.pee.play();
                                self.waitMsec(16000)

                        splashProb = java.util.Random().nextInt(100)
                        if (splashProb > 65):
                                self.splash1.play();
                                self.waitMsec(3000)
                                splash2Prob = java.util.Random().nextInt(100)
                                if (splash2Prob > 65):
                                        self.splash2.play();
                                        self.waitMsec(3000)													  
                except:
                        print "Error stopping at lake"

                # delay for a time (remember loco could still be moving
                # due to simulated or actual inertia). Time is in milliseconds
                self.waitMsec(20000)  # wait for 20 seconds

                self.stoppingAtLake.setState(INACTIVE)                
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
                        self.hoistCavernTurnoutSwitchN.setState(ACTIVE)										
                        jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/VeryLongSingleTootA.wav")).play()
                        self.indicator.setState(INACTIVE)


        def setBlockContent(self, block):
                try:
                        block.setValue("AoS #" + str(self.mineTrain.locoNumber))								
                except:
                        print "Failed setting block label for block " + block.getUserName()
                return
                        
        def handle(self):
		self.indicator.setState(ACTIVE)
		# handle() is called repeatedly until it returns false.

		#
		#  Decide if we are going to stop at the tipple.  If so, we will keep the speed down.
		self.tippleProb = java.util.Random().nextInt(100)
		if ((self.tippleProb < self.probTippleStop) and (self.shutdownSwitch.getState() == ACTIVE)) :
			self.stoppingAtTipple.setState(ACTIVE)
		else :
			self.stoppingAtTipple.setState(INACTIVE)

						
		# set loco to forward 
		if (self.mineTrain.throttle.getSpeedSetting() == 0) :
			self.mineTrain.startTrain(True)

		#
		#  Let train run around to left tunnel
                if (self.firstTime) :
                        self.waitSensorActive(self.leftTunnelSensor)
                        self.firstTime = False
                else:
                        self.waitBlockOccupied(self.leftTunnelSensor)
                        
                self.setBlockContent(self.leftTunnelBlock)
                self.waitMsec(4500)
                print "HCE Aspect = " + self.hoistCavernEntranceSignal.getAspect()                

                if (self.hoistCavernEntranceSignal.getAspect() == "Stop") :                        
                        if (self.shutdownSwitch.getState() == INACTIVE) :
                                self.shutdown()
                                return self.shutdownSwitch.getState() == ACTIVE                                
			#self.waitMsec(4500)
		
			self.mineTrain.throttle.setSpeedSetting(0)
			self.mineTrain.throttle.setF4(True)
			self.waitMsec(5000)

			#self.hoistCavernTurnout.setState(CLOSED)
			self.hoistCavernTurnoutSwitchN.setState(ACTIVE)						
			self.waitMsec(5000)
						
			self.mineTrain.throttle.setF4(False)
			self.waitMsec(1500)

			# self.mineTrain.doubleToot.play()
			self.waitMsec(1500)
			self.mineTrain.throttle.setSpeedSetting(0.12)
			if (self.stoppingAtTipple.getState() != ACTIVE):
                                self.waitMsec(500)
                                self.mineTrain.throttle.setSpeedSetting(0.2)
                                
		if (self.hoistCavernEntranceSignal.getAspect() == "Approach") :
                        print "Approaching tipple slow"
			self.mineTrain.throttle.setSpeedSetting(0.1)
			self.tippleLights.setState(ACTIVE)
		elif (self.hoistCavernEntranceSignal.getAspect() == "Clear") :
                        if (self.mineTrain.throttle.getSpeedSetting() < 0.1) :
                                 self.mineTrain.throttle.setSpeedSetting(self.mineTrain.getSpeed(True)) # was 0.3                               

		#
		#  Front Tunnel
		#
                if (self.mineTrain.throttle.getSpeedSetting() < 0.1) :
                        print "Not running before frontTunnelSensor ... applying band-aid"
                        self.mineTrain.throttle.setSpeedSetting(0.1)
                else:
                        print "Waiting for frontTunnelSensor, speed = " + str(self.mineTrain.throttle.getSpeedSetting())
                       # self.mineTrain.throttle.setSpeedSetting(0.120) 
		self.waitBlockOccupied(self.frontTunnelSensor)
                self.setBlockContent(self.frontTunnelBlock)

		#if (self.stoppingAtTipple.getState() == ACTIVE) :
		#	self.mineTrain.throttle.setSpeedSetting(0.1)
		#	self.tippleLights.setState(ACTIVE)
                #else :
		#	self.tippleLights.setState(INACTIVE)
		#	self.mineTrain.throttle.setSpeedSetting(0.3)

		# wait for tipple sensor to trigger, then stop
		self.waitBlockOccupied(self.tippleSensor)

                self.setBlockContent(self.tippleBlock)
				

		# Greet a train on the upper bridge
		if (self.l2RightBridgeSensor.getState() == ACTIVE) :
                        try :
                                self.longSingleToot.play()
                        except:
                                print "Error playing longSingleToot"

                if (self.rightTunnelSignal.getAspect() == "Stop"):                  
#		if (self.stoppingAtTipple.getState() == ACTIVE) :
                        try:
                                self.waitMsec(2200)
                                self.mineTrain.stopTrain()
                                self.waitMsec(2000)

                                self.chainPulley.play();
                                self.waitMsec(2000)
                                self.rocks.play();
                                self.waitMsec(7000) # was 18000						
                                self.chainPulley.play();
                                self.waitMsec(1000)
                        except:
                                print "Error stopping at tipple"
                                
			# delay for a time (remember loco could still be moving
			# due to simulated or actual inertia). Time is in milliseconds
			self.waitMsec(15000)  # wait for 20 seconds

						#
						#  Leave Tipple
			self.leaveTipple()
			self.waitMsec(500)  # wait 1 second for Xpressnet to catch up

		# wait for back cavern sensor  to trigger
		if ((java.util.Random().nextInt(100) < self.probLakeStop) and (self.shutdownSwitch.getState() == ACTIVE)) :
			self.stoppingAtLake.setState(ACTIVE)
			self.waitBlockOccupied(self.rightTunnelSensor)
			self.bridgeLights.setState(ACTIVE)
		else :
			self.stoppingAtLake.setState(INACTIVE)

		self.waitBlockOccupied(self.backCavernSensor)
#		self.tippleLights.setState(INACTIVE)
                self.setBlockContent(self.backCavernBlock)

		if (self.backTunnelSignal.getAspect() == "Stop") :
                        self.stopAtLake()

			self.mineTrain.startTrain(True)

			self.waitMsec(3000)
			self.bridgeLights.setState(INACTIVE)

			# Scare the bats
			if (self.mineTrain.random.nextInt(100) < self.probBackTunnelBats) :						
				self.bats.play()

		# and continue around again
		print "End of Loop"
	#	if (self.shutdownSwitch.getState() != ACTIVE) :
	#		self.shutdown()
						
		return True # self.shutdownSwitch.getState() == ACTIVE
		# (requires JMRI to be terminated to stop - caution
		# doing so could leave loco running if not careful)

# end of class definition

# start one of these up
Level1OreTrain().start()
