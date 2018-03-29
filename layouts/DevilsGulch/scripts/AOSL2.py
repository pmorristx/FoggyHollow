# This is an example script for a JMRI "Automat" in Python

import jarray
import jmri
import java.util.Random
import sys

class AceOfSpadesLevel2(jmri.jmrit.automat.AbstractAutomaton) :

	class rightCavernListener(java.beans.PropertyChangeListener) :	
		def init(self):

                        self.l1TippleSensor = sensors.provideSensor("OS:L1:Tipple")
#                        self.bridgeCreakRight  = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/WoodCreakRightShort.wav"))

                        self.bridgeCreaks = []                        
                        self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak1.wav")))
                        self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak2.wav")))
                        self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak3.wav")))
                        self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak4.wav")))
                        
                        self.longSingleToot = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/LongSingleToot.wav"))
                        self.random = java.util.Random()

                        return		
		
		def propertyChange(self, event) :

			if (event.source.getState() == ACTIVE) :
                                if (self.l1TippleSensor.getState() == ACTIVE) :
                                        self.longSingleToot.play()
                                try:
                                        self.bridgeCreaks[self.random.nextInt(4)].play()
                                except :
                                        print "Error playing bridge creak in right cavern listener ", sys.exc_info()[0], sys.exc_info()[1]                                                                


	class leftCavernListener(java.beans.PropertyChangeListener) :	
		def init(self):
                        # self.bridgeCreakLeft  = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/WoodCreakLeft.wav"))
                        self.bridgeCreaks = []                        
                        self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak5.wav")))
                        self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak6.wav")))
                        self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak7.wav")))
                        self.bridgeCreaks.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/bridgecreak8.wav")))
                        self.random = java.util.Random()                        
			return		
		
		def propertyChange(self, event) :
			if (event.source.getState() == ACTIVE) :
                                try :
                                        self.bridgeCreaks[self.random.nextInt(4)].play()
                                except :
                                        print "Error playing bridge creak in left cavern listener ", sys.exc_info()[0], sys.exc_info()[1]                        



        def loadSoundFile(self, path) :
                try :
                        print "Loading sound file " + path
                        return jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename(path)) # 1.37
                except :
                        print "Error creating sound file ", path, sys.exc_info()[0], sys.exc_info()[1]                                        
                
	def init(self):
		# init() is called exactly once at the beginning to do
		# any necessary configuration.
		#print "Inside init(self)"

                self.middleTunnelLightOn = False

		# botSensor is reached when loco is running forward
		self.botSensor = sensors.provideSensor("OS:L2:BOT")
		self.eotSensor = sensors.provideSensor("OS:L2:EOT")
                self.midSensor = sensors.provideSensor("OS:L2:Middle Tunnel")
                self.l2RightBridgeSensor = sensors.provideSensor("OS:L2:Right Bridge")
                self.l2LeftBridgeSensor = sensors.provideSensor("OS:L2:Hoist Cavern")                
                self.indicator = sensors.provideSensor("L2 Auto Indicator")

                self.middleTunnelBlock = blocks.provideBlock("L2 Middle Tunnel")

                self.l2MidTunnelLight = turnouts.provideTurnout("L2 Middle Tunnel Flicker")
                
                self.sounds = []
                self.sounds.append(self.loadSoundFile("preference:resources/sounds/SteamWindingEngineConnectingRod.wav")) # 1.37
        
                try :
                        self.sounds.append(jmri.jmrit.Sound( jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/WardrobeChainLoweringAndRaising.wav"))) # 0.19
                except:
                        print "Error creating sound file WardrobeChainLoweringAndRaising", sys.exc_info()[0], sys.exc_info()[1]

                try:
                        self.sounds.append(jmri.jmrit.Sound( jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/SignalBell.wav"))) # 0.11
                except :
                        print "Error creating sound file SignalBell", sys.exc_info()[0], sys.exc_info()[1]

                try:
                        self.sounds.append(jmri.jmrit.Sound( jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/FactoryWhistle.wav"))) # 0.2
                except :
                        print "Error creating sound file FactoryWhistle", sys.exc_info()[0], sys.exc_info()[1]
                        
                self.sounds.append(self.loadSoundFile("preference:resources/sounds/Creak-Metal.wav")) # .02
                self.sounds.append(self.loadSoundFile("preference:resources/sounds/GearTurning.wav")) # 0.03
                self.sounds.append(self.loadSoundFile("preference:resources/sounds/MineTelephone.wav")) #.21
                self.sounds.append(self.loadSoundFile("preference:resources/sounds/Hoist.wav")) # 1.16
                self.sounds.append(self.loadSoundFile("preference:resources/sounds/Compressor.wav")) # 2.05
                self.sounds.append(self.loadSoundFile("preference:resources/sounds/CaveIn.wav")) #0.9
                self.sounds.append(self.loadSoundFile("preference:resources/sounds/SteamEngine.wav")) # 0.59
                self.sounds.append(self.loadSoundFile("preference:resources/sounds/PickAxe.wav")) # 19
                self.sounds.append(self.loadSoundFile("preference:resources/sounds/MineRockFall.wav")) # 19                

                self.soundDelays = [97, 19, 11, 2, 2, 3, 21, 76, 125, 9, 59, 19, 30]
                                
                self.bats = self.loadSoundFile("preference:resources/sounds/BatsInCave.wav")

                self.singleToot = self.loadSoundFile("preference:resources/sounds/ShortSingleToot.wav")
                self.doubleToot = self.loadSoundFile("preference:resources/sounds/LongDoubleToot.wav")
                self.tripleToot = self.loadSoundFile("preference:resources/sounds/TripleToot.wav")                                                
                
                self.speed = 0
                self.firstTime = True
                self.random = java.util.Random()

                self.probMiddleTunnelStop = int(memories.provideMemory("Prob L2 Middle Tunnel Stop").getValue())
                self.probMiddleTunnelChangeDirection = int(memories.provideMemory("Prob L2 Middle Tunnel Change Direction").getValue())
                self.probLeftTunnelBats = int(memories.provideMemory("Prob L2 Left Tunnel Bats").getValue())
                
		# get loco address. For long address change "False" to "True"
                self.locoNumber = memories.provideMemory("L2 Loco Number").getValue()
		self.throttle = self.getThrottle(int(self.locoNumber), False)  # short address 14                

		rightCavernListener = self.rightCavernListener()
		rightCavernListener.init()
		self.l2RightBridgeSensor.addPropertyChangeListener(rightCavernListener)

		leftCavernListener = self.leftCavernListener()
		leftCavernListener.init()
		self.l2LeftBridgeSensor.addPropertyChangeListener(leftCavernListener)                                              


                self.findTrain()
		return

        def findTrain(self) :
                trainName = "No. " + str(self.locoNumber)
                print "initializing loco " + trainName
                
                block = blocks.provideBlock("L2 BOT")
                if (block.getSensor().getState() == ACTIVE) :
                        block.setValue (trainName)

                block = blocks.provideBlock("L2 Hoist Cavern")
                if (block.getSensor().getState() == ACTIVE) :
                        block.setValue (trainName)

                block = blocks.provideBlock("L2 Middle Tunnel")
                if (block.getSensor().getState() == ACTIVE) :
                        block.setValue (trainName)

                block = blocks.provideBlock("L2 Right Bridge")
                if (block.getSensor().getState() == ACTIVE) :
                        block.setValue (trainName)

                block = blocks.provideBlock("L2 Right Tunnel")
                if (block.getSensor().getState() == ACTIVE) :
                        block.setValue (trainName)
                        
                block = blocks.provideBlock("L2 EOT")
                if (block.getSensor().getState() == ACTIVE) :
                        block.setValue (trainName)                        

        
        def getSpeed(self) :
                return 0.1 + 0.1 * self.random.nextInt(3)

        def playRandomSound(self) :
                idx = self.random.nextInt(len(self.sounds))
                print idx
                self.sounds[idx].play()
                self.waitMsec(self.soundDelays[idx]*1000 + self.random.nextInt(5000))                                   
        
        def doBOT(self):
		# wait for sensor in forward direction to trigger, then stop
                #print "Waiting for BOT Sensor"
		self.waitSensorActive(self.botSensor) 
                self.stopTrain()
                blocks.provideBlock("L2 BOT").setValue("AoS #" + str(self.locoNumber))                               
                #print "BOT sensor active"


                # Scare the bats
                if (self.random.nextInt(100) < self.probLeftTunnelBats) :
                        self.bats.play()

		# delay for a time (remember loco could still be moving
		# due to simulated or actual inertia). Time is in milliseconds
                if (not self.firstTime) :
                        self.waitMsec(20000 + self.random.nextInt(10000))          # wait
                else :
                        self.firstTime = False

                #print "BOT moving back"
                self.startTrain(False)

                if (sensors.getSensor("IS:L2AUTO").getState() != ACTIVE) :
                        self.shutdown()                

        #
        #  Wait for train to get to EOT, pause, then start back toward BOT
        def doEOT(self):
                # wait for sensor in reverse direction to trigger
               # print "Waiting for EOT sensor"
                self.waitSensorActive(self.eotSensor)
                self.stopTrain()                
                blocks.provideBlock("L2 EOT").setValue("AoS #" + str(self.locoNumber))                                              

                        
                # delay for a time (remember loco could still be moving
                # due to simulated or actual inertia). Time is in milliseconds
                self.waitMsec(20000 + self.random.nextInt(10000))          # wait for 20 seconds

                self.startTrain(True)

                self.waitSensorActive(self.l2RightBridgeSensor) 
                blocks.provideBlock("L2 Right Bridge").setValue("AoS #" + str(self.locoNumber))                                              
        #
        #  Stop the train.  Put headlight to dim, then turn it off.
        def stopTrain(self) :
                print "In AOSL2 stopping train"
                self.throttle.setSpeedSetting(0)
                self.waitMsec((self.random.nextInt(3)+2) * 1000)                                
                self.throttle.setF4(True)
                self.waitMsec((self.random.nextInt(2)+1) * 1000)                                
                self.throttle.setF0(False)

        #
        #  Start the train moving in the requested direction.  Turn the headlight on first, then undim it, then get
        #  a random speed to start moving.
        def startTrain(self, isForward):
                self.throttle.setF1(True)
                self.throttle.setF2(True)
                self.throttle.setIsForward(isForward)                
                self.throttle.setF0(True)                
                self.waitMsec((self.random.nextInt(2)+1) * 1000)                
                self.throttle.setF4(False)
                self.waitMsec((self.random.nextInt(3)+2) * 1000)
                self.throttle.setSpeedSetting(self.getSpeed())


        #
        #  Clean shutdown when switch is turned off.  Return train to the front of the layout (Hoist Cavern Entrance)
        #  and shut the train down.                
        def shutdown(self):
                #
                #  Clean shutdown...move train to right bridge and stop
                self.throttle.setSpeedSetting(0.0)

                if (self.eotSensor.getState() == ACTIVE):
                        self.throttle.setSpeedSetting(0.0)
                        self.throttle.setIsForward(True)
                else:
                        self.throttle.setSpeedSetting(0.0)
                        self.throttle.setIsForward(False)

                if (not (self.l2RightBridgeSensor.getState() == ACTIVE)):
                        self.throttle.setSpeedSetting(0.4)
                        
                self.waitSensorActive(self.l2RightBridgeSensor)
                self.throttle.setSpeedSetting(0)
                self.throttle.setF0(False)
                self.throttle.setF1(False)
                self.throttle.setF2(False)
                jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/VeryLongSingleToot.wav")).play()
                self.indicator.setState(INACTIVE)
                
	def handle(self):
		# handle() is called repeatedly until it returns false.

                self.indicator.setState(ACTIVE)

		# set loco to forward
                self.startTrain(True)


                self.doBOT()

                while (sensors.getSensor("IS:L2AUTO").getState() == ACTIVE) :
                        
                        self.waitSensorActive(self.midSensor)
                        try :
                                self.middleTunnelBlock.setValue("AoS #" + str(self.locoNumber))
                        except :
                                print "Failed setting block value", sys.exc_info()[0], sys.exc_info()[1]

                        # Remember speed so we don't change it if we don't stop in tunnel
                        self.speed = self.throttle.getSpeedSetting()
                        #  Stop in the middle tunnel 30% of the time 
                        if (self.random.nextInt(100) < self.probMiddleTunnelStop) :
                                if (self.random.nextInt(100) < 50) :
                                        self.middleTunnelLightOn = True
                                #  Stop the loco and dim the headlight
                                self.waitMsec(750) 
                                self.throttle.setSpeedSetting(0)
                                self.singleToot.play()
                                self.waitMsec(1000)
                                if (self.middleTunnelLightOn) :
                                        self.l2MidTunnelLight.setState(CLOSED)                                
                                self.waitMsec(2000)
                                self.throttle.setF0(False)

                                self.playRandomSound()

                                self.speed = self.getSpeed()
                                if (self.random.nextInt(100) < self.probMiddleTunnelChangeDirection) :
                                        #  40% of the time, change direction, undim headlight and start moving
                                        if (self.throttle.getIsForward()) :
                                                self.throttle.setIsForward(False)
                                                self.tripleToot.play()
                                                self.waitMsec(1000)                                                
                                        else :
                                                self.throttle.setIsForward(True)
                                                self.doubleToot.play()
                                                self.waitMsec(1000)
                        #
                        #  Start moving
                        if (self.middleTunnelLightOn) :
                                self.l2MidTunnelLight.setState(THROWN)
                                self.middleTunnelLightOn = False
                        #print "Starting moving from middle tunnel"
                        self.throttle.setF0(True)
                        self.waitMsec(3000)
                        self.throttle.setSpeedSetting(self.speed)

                                
                        if (self.throttle.getIsForward()) :
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

