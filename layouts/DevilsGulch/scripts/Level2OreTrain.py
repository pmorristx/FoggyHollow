# This is an example script for a JMRI "Automat" in Python

import jarray
import jmri
import java.util.Random
import sys
from MineTrain import MineTrain

class AceOfSpadesLevel2(jmri.jmrit.automat.AbstractAutomaton) :

	class rightCavernListener(java.beans.PropertyChangeListener) :	
		def init(self, mineTrain):
			self.mineTrain = mineTrain
			self.l1TippleSensor = sensors.provideSensor("OS:L1:Tipple")
#						self.bridgeCreakRight  = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/WoodCreakRightShort.wav"))

			self.bridgeCreaks = []						
			self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak1.wav")))
			self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak2.wav")))
			#self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak3.wav")))
			#self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak4.wav")))
			
			self.longSingleToot = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/LongSingleToot.wav"))
			self.mineTrain.random = java.util.Random()

			return		
		
		def propertyChange(self, event) :

			if (event.source.getState() == ACTIVE) :
				try:
					if (not self.mineTrain.throttle.getIsForward()):
						self.mineTrain.throttle.setSpeedSetting(0.1)                                        
					if (self.l1TippleSensor.getState() == ACTIVE) :
						self.longSingleToot.play()
                                                self.bridgeCreaks[self.mineTrain.random.nextInt(2)].play()
                                                print "In right cavern bridge creak"
				except :
					print "Error playing bridge creak in right cavern listener ", sys.exc_info()[0], sys.exc_info()[1]																


	class leftCavernListener(java.beans.PropertyChangeListener) :	
		def init(self, mineTrain):
			self.mineTrain = mineTrain
			self.bridgeCreaks = []						
			self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak5.wav")))
			self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak6.wav")))
			#self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak7.wav")))
			#self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak8.wav")))
			self.mineTrain.random = java.util.Random()						
			return		
		
		def propertyChange(self, event) :
			if (event.source.getState() == ACTIVE) :
				try :
					self.bridgeCreaks[self.mineTrain.random.nextInt(2)].play()
					if (self.mineTrain.throttle.getIsForward()):
						self.mineTrain.throttle.setSpeedSetting(0.1)
				except :
					print "Error playing bridge creak in left cavern listener ", sys.exc_info()[0], sys.exc_info()[1]						
										
				
	def init(self):
		# init() is called exactly once at the beginning to do
		# any necessary configuration.
		#print "Inside init(self)"

		locoNumber = memories.provideMemory("L2 Loco Number").getValue()
		self.mineTrain = MineTrain()
		self.mineTrain.init(locoNumber, 2)		
		self.middleTunnelLightOn = False

		# botSensor is reached when loco is running forward
		self.botSensor = sensors.provideSensor("OS:L2:BOT")
		self.eotSensor = sensors.provideSensor("OS:L2:EOT")
		self.midSensor = sensors.provideSensor("OS:L2:Middle Tunnel")
		self.l2RightBridgeSensor = sensors.provideSensor("OS:L2:Right Bridge")
		self.l2LeftBridgeSensor = sensors.provideSensor("OS:L2:Hoist Cavern")				
		self.indicator = sensors.provideSensor("L2 Auto Indicator")

		self.middleTunnelBlock = blocks.provideBlock("L2 Middle Tunnel")

		self.l2MidTunnelLight = lights.provideLight("L2 Middle Tunnel Blue Flicker")
		
		self.sounds = []
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/SteamWindingEngineConnectingRod.wav")) # 1.37

		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/WardrobeChainLoweringAndRaising.wav")) # 0.19
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/SignalBell.wav")) # 0.11
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/FactoryWhistle.wav")) # 0.2
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Creak-Metal.wav")) # .02
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/GearTurning.wav")) # 0.03
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/MineTelephone.wav")) #.21
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Hoist.wav")) # 1.16
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Compressor.wav")) # 2.05
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/CaveIn.wav")) #0.9
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/SteamEngine.wav")) # 0.59
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/PickAxe.wav")) # 19
		self.sounds.append(self.mineTrain.loadSoundFile("preference:resources/sounds/MineRockFall.wav")) # 19				

		self.soundDelays = [97, 19, 11, 2, 2, 3, 21, 76, 125, 9, 59, 19, 30]
						
		self.bats = self.mineTrain.loadSoundFile("preference:resources/sounds/BatsInCave.wav")

		self.mineTrain.singleToot = self.mineTrain.loadSoundFile("preference:resources/sounds/ShortSingleToot.wav")
		self.mineTrain.doubleToot = self.mineTrain.loadSoundFile("preference:resources/sounds/LongDoubleToot.wav")
		self.mineTrain.tripleToot = self.mineTrain.loadSoundFile("preference:resources/sounds/TripleToot.wav")												
		
		self.speed = 0
		self.firstTime = True
		self.mineTrain.random = java.util.Random()

		self.probMiddleTunnelStop = int(memories.provideMemory("Prob L2 Middle Tunnel Stop").getValue())
		self.probMiddleTunnelChangeDirection = int(memories.provideMemory("Prob L2 Middle Tunnel Change Direction").getValue())
		self.probLeftTunnelBats = int(memories.provideMemory("Prob L2 Left Tunnel Bats").getValue())
		
		# get loco address. For long address change "False" to "True"

		self.mineTrain.throttle = self.getThrottle(int(self.mineTrain.locoNumber), False)  # short address 14				

		rightCavernListener = self.rightCavernListener()
		rightCavernListener.init(self.mineTrain)
		self.l2RightBridgeSensor.addPropertyChangeListener(rightCavernListener)

		leftCavernListener = self.leftCavernListener()
		leftCavernListener.init(self.mineTrain)
		self.l2LeftBridgeSensor.addPropertyChangeListener(leftCavernListener)											  


		self.mineTrain.findTrain()
		return

	def playRandomSound(self) :
		idx = self.mineTrain.random.nextInt(len(self.sounds))
		print idx
		self.sounds[idx].play()
		self.waitMsec(self.soundDelays[idx]*1000 + self.mineTrain.random.nextInt(5000))								   
		
	def doBOT(self):
		# wait for sensor in forward direction to trigger, then stop
				#print "Waiting for BOT Sensor"
		self.waitSensorActive(self.botSensor)
		self.mineTrain.stopTrain()                
		blocks.provideBlock("L2 BOT").setValue("AoS #" + str(self.mineTrain.locoNumber))							   
		#print "BOT sensor active"


		# Scare the bats
		if (self.mineTrain.random.nextInt(100) < self.probLeftTunnelBats) :
				self.bats.play()

		# delay for a time (remember loco could still be moving
		# due to simulated or actual inertia). Time is in milliseconds
		if (not self.firstTime) :
				self.waitMsec(20000 + self.mineTrain.random.nextInt(10000))		  # wait
		else :
				self.firstTime = False

		#print "BOT moving back"
		self.mineTrain.startTrain(False)

		if (sensors.getSensor("IS:L2AUTO").getState() != ACTIVE) :
				self.shutdown()				

	#
	#  Wait for train to get to EOT, pause, then start back toward BOT
	def doEOT(self):
		# wait for sensor in reverse direction to trigger
	   # print "Waiting for EOT sensor"
		#self.waitSensorActive(self.eotSensor)
                self.waitSensorActive(self.l2RightBridgeSensor) # Temp for bad track in tunnel
                self.waitMsec(4700) # Temp for bad track in tunnel
		self.mineTrain.stopTrain()                
		blocks.provideBlock("L2 EOT").setValue("AoS #" + str(self.mineTrain.locoNumber))											  

				
		# delay for a time (remember loco could still be moving
		# due to simulated or actual inertia). Time is in milliseconds
		self.waitMsec(20000 + self.mineTrain.random.nextInt(10000))		  # wait for 20 seconds

		self.mineTrain.startTrain(True)

		self.waitSensorActive(self.l2RightBridgeSensor) 
		blocks.provideBlock("L2 Right Bridge").setValue("AoS #" + str(self.mineTrain.locoNumber))											  

	#
	#  Clean shutdown when switch is turned off.  Return train to the front of the layout (Hoist Cavern Entrance)
	#  and shut the train down.				
	def shutdown(self):
		#
		#  Clean shutdown...move train to right bridge and stop
		self.mineTrain.throttle.setSpeedSetting(0.0)

		if (self.eotSensor.getState() == ACTIVE):
			self.mineTrain.throttle.setSpeedSetting(0.0)
			self.mineTrain.throttle.setIsForward(True)
		else:
			self.mineTrain.throttle.setSpeedSetting(0.0)
			self.mineTrain.throttle.setIsForward(False)

		if (not (self.l2RightBridgeSensor.getState() == ACTIVE)):
			self.mineTrain.throttle.setSpeedSetting(0.4)
				
		self.waitSensorActive(self.l2RightBridgeSensor)
		self.waitMsec(2000)
		self.mineTrain.throttle.setSpeedSetting(0)
		self.mineTrain.throttle.setF0(False)
		self.mineTrain.throttle.setF1(False)
		self.mineTrain.throttle.setF2(False)
		jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/VeryLongSingleToot.wav")).play()
		self.indicator.setState(INACTIVE)
				
	def handle(self):
		# handle() is called repeatedly until it returns false.

		self.indicator.setState(ACTIVE)

		# set loco to forward
		self.mineTrain.startTrain(True)

		self.doBOT()

		while (sensors.getSensor("IS:L2AUTO").getState() == ACTIVE) :
				
			self.waitSensorActive(self.midSensor)
			try :
				self.middleTunnelBlock.setValue("AoS #" + str(self.mineTrain.locoNumber))
			except :
				print "Failed setting block value", sys.exc_info()[0], sys.exc_info()[1]

			# Remember speed so we don't change it if we don't stop in tunnel
			self.speed = self.mineTrain.throttle.getSpeedSetting()
			#  Stop in the middle tunnel 30% of the time 
			if (self.mineTrain.random.nextInt(100) < self.probMiddleTunnelStop) :
				if (self.mineTrain.random.nextInt(100) < 50) :
					self.middleTunnelLightOn = True
				#  Stop the loco and dim the headlight
				self.waitMsec(750) 
				self.mineTrain.throttle.setSpeedSetting(0)
				self.mineTrain.singleToot.play()
				self.waitMsec(1000)
				if (self.middleTunnelLightOn) :
						self.l2MidTunnelLight.setState(ON)								
				self.waitMsec(2000)
				self.mineTrain.throttle.setF0(False)

				self.playRandomSound()

				self.speed = self.mineTrain.getSpeed(True)
				if (self.mineTrain.random.nextInt(100) < self.probMiddleTunnelChangeDirection) :
					#  40% of the time, change direction, undim headlight and start moving
					if (self.mineTrain.throttle.getIsForward()) :
						self.mineTrain.throttle.setIsForward(False)
						self.mineTrain.tripleToot.play()
						self.waitMsec(1000)												
					else :
						self.mineTrain.throttle.setIsForward(True)
						self.mineTrain.doubleToot.play()
						self.waitMsec(1000)
			#
			#  Start moving
			if (self.middleTunnelLightOn) :
				self.l2MidTunnelLight.setState(OFF)
				self.middleTunnelLightOn = False
			#print "Starting moving from middle tunnel"
			self.mineTrain.throttle.setF0(True)
			self.waitMsec(3000)
			self.mineTrain.throttle.setSpeedSetting(self.speed)
			print "L2 Train - 1 - setting speed to " + str(self.speed)

					
			if (self.mineTrain.throttle.getIsForward()) :
				self.doBOT()
			else :
				self.doEOT()
			  
				
		#print "End of Loop"
		if (sensors.getSensor("IS:L2AUTO").getState() != ACTIVE) :
			self.shutdown()
		return sensors.getSensor("IS:L2AUTO").getState() == ACTIVE 

# end of class definition

# start one of these up
AceOfSpadesLevel2().start()
