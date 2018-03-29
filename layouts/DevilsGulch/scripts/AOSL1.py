# This is an example script for a JMRI "Automat" in Python
# It is based on the AutomatonExample.
#
# It listens to two sensors, running a locomotive back and
# forth between them by changing its direction when a sensor
# detects the engine. 
#
# Author:  Howard Watkins, January 2007.
# Part of the JMRI distribution
#
# The next line is maintained by CVS, please don't change it
# $Revision: 17977 $

import jarray
import jmri
import java.util.Random

class AoSL1(jmri.jmrit.automat.AbstractAutomaton) :


	def init(self):
		# init() is called exactly once at the beginning to do
		# any necessary configuration.
	
		self.stoppingAtLake = False
		self.stoppingAtTipple = False
	
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
		
                # Get light switch sensors		   
		self.tippleLights = sensors.provideSensor("Tipple Lights")
		self.bridgeLights = sensors.provideSensor("Lake Cavern Bridge")

                #
                #  Get the shutdown switch
                self.shutdownSwitch = sensors.getSensor("IS:L1AUTO")                

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

                self.locoNumber = memories.provideMemory("L1 Loco Number").getValue()
		self.throttle = self.getThrottle(int(self.locoNumber), False)  # short address 14

		self.chainPulley = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/chaindoor.wav"))  # 0.2
#		self.rocks = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/MineRockFall.wav"))  # 19
		self.rocks = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/rocks.wav"))  # 7								                
		self.bats = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/BatsInCave.wav"))

                self.singleToot = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ShortSingleTootA.wav"))
		self.longSingleToot = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/LongSingleTootA.wav"))				
		self.doubleToot = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/LongDoubleTootA.wav"))
		self.tripleToot = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/TripleTootA.wav"))

		self.rocks = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/MineRockFall.wav"))
		self.pee = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/peeing.wav"))
		self.splash1 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Splash.wav"))
		self.splash2 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Splash2.wav"))				


                self.backCavernBlock =  blocks.provideBlock("L1 Back Cavern")
                self.leftTunnelBlock =  blocks.provideBlock("L1 Left Tunnel")
                self.frontTunnelBlock =  blocks.provideBlock("L1 Front Tunnel")                
                self.tippleBlock = blocks.provideBlock("L1 Tipple")

                self.tippleProb = 0
                
		self.random = java.util.Random()
				
		return

        #
        #  Returns a randomized speed.  Reverse speeds are slower than forward
        def getSpeed(self, isForward) :
                if (isForward) :
                        return 0.15 + 0.1 * self.random.nextInt(3)
                else :
                        return 0.15 + 0.1 * self.random.nextInt(2)        

        #
        #  Stop the train.  Put headlight to dim, then turn it off.
        def stopTrain(self) :
                self.throttle.setSpeedSetting(0)
                self.waitMsec((self.random.nextInt(3) + 2) * 1000)								
                self.throttle.setF4(True)
                self.waitMsec((self.random.nextInt(2) + 1) * 1000)								
                #self.throttle.setF0(False)
                #self.waitMsec((self.random.nextInt(2)+1) * 1000)
                self.singleToot.play()

        #
        #  Start the train moving in the requested direction.  Turn the headlight on first, then undim it, then get
        #  a random speed to start moving.
        def startTrain(self, isForward):

                self.throttle.setF1(True) # Turn brake light on
                self.throttle.setIsForward(isForward)
                self.throttle.setF2(True) # Turn on beacon
                self.throttle.setF0(True) # Turn on headlight				
                self.waitMsec((self.random.nextInt(2) + 1) * 1000)				
                self.throttle.setF4(False) # Turn dim off
                self.waitMsec((self.random.nextInt(2) + 1) * 1000)
                #
                #  Signal direction
                if (isForward):
                        self.doubleToot.play()
                else:
                        self.tripleToot.play()
                        
                self.waitMsec((self.random.nextInt(3) + 2) * 1000)
                # Start moving
                self.throttle.setSpeedSetting(self.getSpeed(isForward))

        def leaveTipple(self):

                self.enterHoistCavern = False
                if (self.random.nextInt(100) < 70) :
                        #
                        #  backup sometimes

                        self.enterHoistCavern = self.random.nextInt(100) < 70

                        if (self.enterHoistCavern) :
                                self.hoistCavernTurnoutSwitchR.setState(ACTIVE)
                                self.waitMsec(4000)

                        self.startTrain(False)

                        if (self.enterHoistCavern) :
                                self.waitSensorActive(self.hoistCavernSensor)
                                self.throttle.setSpeedSetting(0.1) # Slow down so we don't overrun EOT
                                self.waitSensorActive(self.hoistCavernEOTSensor)
                        else :
                                self.waitSensorActive(self.leftTunnelSensor)
                                self.waitMsec(2500)

                        self.stopTrain()

                        self.waitMsec(10000)


                self.startTrain(True)

                return

        #
        #  Clean shutdown when switch is turned off.  Return train to the front of the layout (Hoist Cavern Entrance)
        #  and shut the train down.
        def shutdown(self):
                #
                #  Clean shutdown...move train to HCE and stop
                self.throttle.setSpeedSetting(0.4)
                self.waitSensorActive(self.hoistCavernEntranceSensor)
                self.throttle.setSpeedSetting(0)
                self.throttle.setF0(False)
                self.throttle.setF1(False)
                self.throttle.setF2(False)
                self.hoistCavernTurnoutSwitchN.setState(ACTIVE)                                        
		jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/VeryLongSingleTootA.wav")).play()
                self.indicator.setState(INACTIVE)


	def handle(self):
                self.indicator.setState(ACTIVE)
		# handle() is called repeatedly until it returns false.

                #
                #  Decide if we are going to stop at the tipple.  If so, we will keep the speed down.
		self.tippleProb = java.util.Random().nextInt(100)
		if (self.tippleProb < self.probTippleStop and self.shutdownSwitch.getState() == ACTIVE) :
			self.stoppingAtTipple = True
                else :
                        self.stoppingAtTipple = False

                        
		# set loco to forward
                if (self.throttle.getSpeedSetting() == 0) :
                        self.startTrain(True)

                #
                #  Pause train in back of left tunnel to make the mine seem bigger than it is.
		self.waitSensorActive(self.leftTunnelSensor)

                        
#                self.leftTunnelBlock.setValue("AoS #" + str(self.locoNumber))                                
                if (self.hoistCavernTurnout.getState() == THROWN) :
			self.waitMsec(4500)
		
			self.throttle.setSpeedSetting(0.0)
                        self.throttle.setF4(True)
			self.waitMsec(5000)

                        #self.hoistCavernTurnout.setState(CLOSED)
                        self.hoistCavernTurnoutSwitchN.setState(ACTIVE)                        
                        self.waitMsec(5000)
                        
			self.throttle.setF4(False)
			self.waitMsec(1500)

			# self.doubleToot.play()
			self.waitMsec(1500)
			self.throttle.setSpeedSetting(0.1)
                        if (not self.stoppingAtTipple) :
                                self.waitMsec(500)
                                self.throttle.setSpeedSetting(0.2)
                #
                #  Front Tunnel
                #
		self.waitSensorActive(self.frontTunnelSensor)
###                self.frontTunnelBlock.setValue("AoS #" + str(self.locoNumber))                                                
                if (self.stoppingAtTipple) :
			self.throttle.setSpeedSetting(0.1)
			self.tippleLights.setState(ACTIVE)
		else :
			self.stoppingAtTipple = False
			self.throttle.setSpeedSetting(0.3)

		# wait for tipple sensor to trigger, then stop
		self.waitSensorActive(self.tippleSensor)

#                self.tippleBlock.setValue("AoS #" + str(self.locoNumber))
                

		# Greet a train on the upper bridge
		if (self.l2RightBridgeSensor.getState() == ACTIVE) :
			self.longSingleToot.play()

		if (self.stoppingAtTipple) :
			self.waitMsec(2800)
                        self.stopTrain()
			self.waitMsec(2000)

			self.chainPulley.play();
			self.waitMsec(2000)
			self.rocks.play();
			self.waitMsec(7000) # was 18000						
			self.chainPulley.play();
			self.waitMsec(1000)
						
			# delay for a time (remember loco could still be moving
			# due to simulated or actual inertia). Time is in milliseconds
			self.waitMsec(15000)  # wait for 20 seconds

                        #
                        #  Leave Tipple
                        self.leaveTipple()
			self.waitMsec(500)  # wait 1 second for Xpressnet to catch up

		# wait for back cavern sensor  to trigger
		if (java.util.Random().nextInt(100) < self.probLakeStop and self.shutdownSwitch.getState() == ACTIVE) :
			self.stoppingAtLake = True
			self.waitSensorActive(self.rightTunnelSensor)
			self.bridgeLights.setState(ACTIVE)
		else :
			self.stoppingAtLake = False

		self.waitSensorActive(self.backCavernSensor)
                self.tippleLights.setState(INACTIVE)
#                self.backCavernBlock.setValue("AoS #" + str(self.locoNumber))                                

		if (self.stoppingAtLake) :
			self.waitMsec(1200)
			self.stopTrain()

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
								
			# delay for a time (remember loco could still be moving
			# due to simulated or actual inertia). Time is in milliseconds
			self.waitMsec(20000)  # wait for 20 seconds

			self.startTrain(True)

			self.waitMsec(3000)
			self.bridgeLights.setState(INACTIVE)

			# Scare the bats
			if (self.random.nextInt(100) < self.probBackTunnelBats) :						
				self.bats.play()

		# and continue around again
		print "End of Loop"
		if (self.shutdownSwitch.getState() != ACTIVE) :
                        self.shutdown()
                        
		return self.shutdownSwitch.getState() == ACTIVE
		# (requires JMRI to be terminated to stop - caution
		# doing so could leave loco running if not careful)

# end of class definition

# start one of these up
AoSL1().start()
