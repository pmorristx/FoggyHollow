#
#  Script to shuttle mine train back & forth, turning on various lights, etc. along the way.

import jmri
import jmri.jmrit.roster
import jmri.jmrix.AbstractThrottle
import sys
from java.awt import Font
import jmri.jmrit.display.panelEditor.configurexml.PanelEditorXml

class MineTrack(jmri.jmrit.automat.AbstractAutomaton) :
	
	throttle = None
	mineCar = None
	speedScale = 1
	reseting = True

	#
	#  Various speeds at different places along the track.  Initialized later.
	fastSpeed = 22
	mediumSpeed = 16
	slowSpeed = 14
	extraSlowSpeed = 9
	creepSpeed = 6	
	stopSpeed = 0.0
	
	currentState = 999
	
	automationSwitch = None
	
	locoAddress = -1	
	
	#
	#  Beginning/End of track delays (in seconds) for demo and non-demo mode.
	eotDelayDemo = 30
	botDelayDemo = 20
	
	eotDelayLong = 8 * 60
	botDelayLong = 5 * 60			
			
	#
	#  Listen for user to turn the GUI automation switch off.  Stop the locomotive and turn lights on.			
	class StopTrainListener(java.beans.PropertyChangeListener) :	
		def init(self, sensor, parent):
			self.sensor = sensor
			self.parent = parent
			return		
		
		def propertyChange(self, event) :
			if (event.source.getState() == INACTIVE) :
				#MineTrack.stopAnimation(self.parent)
				print "Stopping animation"
				MineTrack.throttle.setSpeedSetting(MineTrack.stopSpeed)
				MineTrack.throttle.setIsForward(True)				
				MineTrack.throttle.setF0(True)  # Turn headlight on
				MineTrack.throttle.setF1(False) # Turn bell off
				MineTrack.throttle.setF4(False) # Turn steam release off
				MineTrack.throttle.setF5(True)  # Turn tender lights on
				MineTrack.throttle.setF6(False) # Turn water fill off	
				MineTrack.throttle.setF11(True) # Turn cab light on
				MineTrack.mineCar.setF0(True)
				sensors.provideSensor("Red EOT Lantern").setState(ACTIVE)
				sensors.provideSensor("IS:DIR").setState(UNKNOWN)	
				self.parent.stop()
				print "stopAnimation done"					
			return	
		
	class LocoChangeListener(java.beans.PropertyChangeListener) :
		def init(self, parent):
			self.parent = parent
			return		
		
		def propertyChange(self, event) :			
			self.parent.setRosterIcon()
			return						
			
	#
	#  Count down the BOT or EOT delay on the GUI.  The delay time is randomized using a Gaussian distribution with
	#  the supplied delay as the mean and 1 sigma...  The delay parameter is in seconds.
	def nixieDelay(self, station, delay):
		m1 = memories.getMemory(station + " DELAY M-MSB")		
		m2 = memories.getMemory(station + " DELAY M-LSB")				
		
		s1 = memories.getMemory(station + " DELAY S-MSB")
		s2 = memories.getMemory(station + " DELAY S-LSB")

		randomDelay = delay + java.util.Random().nextGaussian()*(delay *.2)
		for s in range(int(randomDelay), -1, -1):
			s1.setValue(int((s % 60) / 10))	
			s2.setValue(s % 10)			

			m1.setValue(int( (s/60) / 10 ))
			m2.setValue(int((s / 60) % 10))			
			if (s > 0) : self.waitMsec(1000)
		return			
	
		
	# init() is called exactly once at the beginning to do
	# any necessary configuration.
	def init(self) :
		
		global throttle

		MineTrack.currentState = 999
		MineTrack.automationSwitch = sensors.provideSensor("IS:MTS")	
		
		MineTrack.mineCar = self.getThrottle(6,False) 	
		MineTrack.locoAddress = int(memories.getMemory("Mine Locomotive").getValue())
		MineTrack.throttle = self.getThrottle(MineTrack.locoAddress, False) 
		
		#
		#  Unlock decoder so we can ramp down sound at BOT.
#		self.writeOpsModeCV(15, 2, False, MineTrack.throttle.getLocoAddress().getNumber())							
		

		if (MineTrack.throttle == None) :
			print "Couldn't assign throttle!"		
		MineTrack.throttle.setSpeedStepMode(1)
		self.speedScale = 1

		#
		#  
		MineTrack.fastSpeed = 22 * MineTrack.throttle.getSpeedIncrement()		
		MineTrack.mediumSpeed = 16 * MineTrack.throttle.getSpeedIncrement()				
		MineTrack.slowSpeed = 14 * MineTrack.throttle.getSpeedIncrement()
		MineTrack.extraSlowSpeed = 9 * MineTrack.throttle.getSpeedIncrement()
		MineTrack.creepSpeed = 6 * MineTrack.throttle.getSpeedIncrement()
		
		#
		#  Listen for user to turn off the animation switch
		stopTrainListener = self.StopTrainListener()
		stopTrainListener.init(MineTrack.automationSwitch, self)
		MineTrack.automationSwitch.addPropertyChangeListener(stopTrainListener)
		
		#
		#  Listen for change the nixie delay readout
#		sensors.provideSensor("Demo Switch").addPropertyChangeListener(self.DemoSwitchListener())	
 		memories.getMemory("EOT DELAY S-MSB").setValue(0)			
		memories.getMemory("EOT DELAY S-LSB").setValue(0)	
		memories.getMemory("EOT DELAY M-MSB").setValue(0)	
		memories.getMemory("EOT DELAY M-LSB").setValue(0)			
		
		memories.getMemory("BOT DELAY S-MSB").setValue(0)			
		memories.getMemory("BOT DELAY S-LSB").setValue(0)	
		memories.getMemory("BOT DELAY M-MSB").setValue(0)	
		memories.getMemory("BOT DELAY M-LSB").setValue(0)			

		#
		#  Listen for changes in locomotive number to change picture & labels		
		listener = self.LocoChangeListener()
		listener.init(self)
		memories.getMemory("Mine Locomotive").addPropertyChangeListener(listener)

		#
		#  Show the ID of the selected loco on the panel
		self.setRosterIcon()
		self.setMemoryIconFont()		
							
		return
	
	#
	# Change the locomotive picture on the GUI to use the picture from the Roster for the currently selected locomotive.
	def setRosterIcon(self):
		try :
			#
			#  Turn the animation switch off to stop any currently running locomotive.  Force reset to BOT next time animation is restarted.

			blockList = blocks.getNamedBeanList()
					
			rosterlist = jmri.jmrit.roster.Roster.instance().matchingList(None, None, memories.getMemory("Mine Locomotive").getValue(), None, None, None, None)		
			for entry in rosterlist.toArray() :
				if ((entry.getDecoderFamily().startswith("Tsunami Steam")) or (entry.getDecoderFamily().startswith("WOW Sound")) or len(rosterlist) == 1):
					memories.getMemory("Roster ID").setValue(entry.getRoadName() + " #" + entry.getDccAddress() )
					memories.getMemory("Roster Description").setValue(entry.getMfg() + " - " + entry.getModel() )	
					namedIcon = jmri.jmrit.catalog.NamedIcon(entry.getIconPath(), "RosterIcon")
					memories.getMemory("Roster Icon").setValue(namedIcon)	
					
					# Break loco ID at 
					locoids = entry.getId().split()
					locoid = locoids[0] + " " + locoids[1].lstrip("0")
					
					for b in blockList:
						if (b.getState() == jmri.Block.OCCUPIED) :
							b.setValue(locoid)
						else :
							b.setValue("")
					
					if ( entry.getDccAddress() > 10 ) :
						memories.getMemory("IM:MINE:LOCOMSB").setValue(int(entry.getDccAddress()) // 10)
						memories.getMemory("IM:MINE:LOCOLSB").setValue(int(entry.getDccAddress()) % 10)
					else :
						memories.getMemory("IM:MINE:LOCOMSB").setValue(0)
						memories.getMemory("IM:MINE:LOCOLSB").setValue(int(entry.getDccAddress()))						
							
		except:
			print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]	
		return	
	
	def reset(self):
		#
		#  If train is already at the beginning-of-track, just start the train moving forward
		#  Otherwise, we need to find the train.		
		try :		
			if (sensors.provideSensor("BOT").getState() == INACTIVE) :
				print "In Reset"
				MineTrack.reseting = True
				self.resetLights(True)
				self.setBrake(False)
				self.forwardWhistle()
				self.waitMsec(1000)
				sensors.provideSensor("Red EOT Lantern").setState(INACTIVE)				
				self.changeDirection("Forward")
				MineTrack.throttle.setSpeedSetting(self.fastSpeed * self.speedScale)

		except :
			print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]	
		
		return 0
	
			
	def stopAnimation(self):
		self.setBrake(True)
		self.waitMsec(2000)
		MineTrack.throttle.setSpeedSetting(self.stopSpeed)
		self.waitMsec(2000)
		self.ringBell(False) # Turn bell off
		self.waitMsec(1000)
		self.stopWhistle()
		self.waitMsec(1000)		
		self.setCabLight(True) # Turn cab light on
		self.changeDirection("Forward")
		
		MineTrack.throttle.setF5(True)  # Turn tender lights on
		MineTrack.throttle.setF4(False)  # Turn steam release off
		MineTrack.throttle.setF6(False)  # Turn water fill off			
		MineTrack.throttle.setF0(True)  # Turn headlight on
		MineTrack.mineCar.setF0(True)
		sensors.provideSensor("Red EOT Lantern").setState(ACTIVE)
		sensors.provideSensor("IS:DIR").setState(UNKNOWN)	
		self.setBrake(False)
		
		#
		#  Relock decoder
#		self.writeOpsModeCV(15, 0, False, MineTrack.throttle.getLocoAddress().getNumber())									
		
		return 0
				
	#
	# Change the direction of both the locomotive & leading mine car.  
	def changeDirection(self, direction):

		MineTrack.reseting = False
		if (direction == "Reverse"):
			MineTrack.throttle.setIsForward(False)
			MineTrack.mineCar.setIsForward(False)
			sensors.provideSensor("IS:DIR").setState(ACTIVE)			
		else :
			MineTrack.throttle.setIsForward(True)
			MineTrack.mineCar.setIsForward(True)	
			sensors.provideSensor("IS:DIR").setState(INACTIVE)							
		return 0
			
	#
	#  Short toot of the whistle 
	def tootWhistle(self, numToots):
		for n in range(numToots) :
			MineTrack.throttle.setF3(not MineTrack.throttle.getF3())			
			self.waitMsec(500)
		return 0
	
	#
	#  Long whistle
	def forwardWhistle(self):
		self.longWhistle(2, 1.5)
		return 0
		
	#
	#  Signal reverse with 3 short toots
	def reverseWhistle(self):
		self.tootWhistle(3)
		return 0
	
	#
	#  Signal stop with one short toot
	def stopWhistle(self):
		self.tootWhistle(1)
		return 0
	
	#
	#  Long whistle
	def longWhistle(self, numBlows, seconds):
		gap = 500
		duration = seconds*1000 + java.util.Random().nextGaussian()*(seconds*1000 *.1)
		for n in range(numBlows) :
			MineTrack.throttle.setF2(True)
			self.waitMsec(int(duration))		
			MineTrack.throttle.setF2(False)
			randomGap = gap + java.util.Random().nextGaussian()*(gap *.2)			
			self.waitMsec(int(randomGap))

		return 0
	
	#
	#  Cab Light
	def setCabLight(self, state):
		MineTrack.throttle.setF11(state)
		return 0
	#
	#  Brake
	def setBrake(self, state):
		MineTrack.throttle.setF7(state)
		return 0
	
	#
	#
	def ringBell(self, state):
		MineTrack.throttle.setF1(state)
		return 0
	
	#
	#  Play the sound of the fireman blowing out the boiler the specified number of seconds
	def steamRelease(self, seconds):
		MineTrack.throttle.setF4(True)
		self.waitMsec(seconds * 1000)
		MineTrack.throttle.setF4(False)		
		
	#
	#  Play the sound of filling the tender with water for the specified number of seconds.
	def waterFill(self, seconds):
		MineTrack.throttle.setF6(True)
		self.waitMsec(seconds * 1000)
		MineTrack.throttle.setF6(False)		
		
	#
	#  Dim the headlight
	def dimLight(self, state):
		MineTrack.throttle.setF9(state)
		return	

	def findPanelIcon(self, panelEditor, targetName) :
		if (panelEditor != None) :
			contents = panelEditor.getContents()
			for i in range(contents.size()) :
				object = contents.get(i)
				objectClass = str(object.getClass())
				if (objectClass.endswith("MemoryIcon'>")) :
					src = object.getTooltip().getText()
#					print "Memory Object name found = %s" % (src)
					if (src == targetName) :
						return object	
	
	def setMemoryIconFont(self):
		
		import jmri.jmrit.display
		
		# initialize loop to find all panel editors
		i = 0
		editorList = []
		editor = jmri.InstanceManager.configureManagerInstance().findInstance(java.lang.Class.forName("jmri.jmrit.display.panelEditor.PanelEditor"),i)
		
		# loop, adding each editor found to the list
		while (editor != None) : 
			editorList.append(editor)
			# loop again
			i = i + 1
			editor = jmri.InstanceManager.configureManagerInstance().findInstance(java.lang.Class.forName("jmri.jmrit.display.panelEditor.PanelEditor"),i)
		    
		# Now we have a list of editors.
		# For each editor, get the related panel and walk down 
		# its object hierarchy until the widgets themselves are reached    
		for editor in editorList:
			try :
				panel = editor.getFrame()
				icon = self.findPanelIcon(panel,"Roster ID")
				if (icon is not None) :
					icon.setFont(Font("Tempus Sans ITC", Font.ITALIC , 20))	
					
				icon = self.findPanelIcon(panel,"Roster Description")
				if (icon is not None) :
					icon.setFont(Font("tempus sans itc", Font.ITALIC, 16))						
			except:
				print "Error setting MemoryIcon font: ", sys.exc_info()[0], sys.exc_info()[1]		
		return 0
	
	#
	#  Set the locomotive/mine car lights to the specified state.  Called at block transitions to restore lights if lost due to dirty track.
	def resetLights(self, state):
		MineTrack.throttle.setF0(state)  # Turn the light on (in case it went off)
		if (int(memories.getMemory("Mine Locomotive").getValue() != 6)) :						
			MineTrack.mineCar.setF0(state)  # Turn the light on (in case it went off)						
		MineTrack.throttle.setF5(state)  # Turn the tender markers on (in case it went off)	
		return 0
	
	def BOTAction(self):
		if (MineTrack.automationSwitch.getState() == INACTIVE) :
			self.stopAnimation()
			return 0
					
		if (MineTrack.currentState == -2 or MineTrack.currentState == 999) :
			
			# Don't delay 1st time
			if (MineTrack.currentState != 999) :
				MineTrack.currentState = 1 # do this here to get it done fast before a wagging sensor sends us back here						 					
				MineTrack.throttle.setF8(True) # Mute the sound while we wait
				
				#
				#  Unlock decoder to write CVs
				MineTrack.throttle.setSpeedSetting(MineTrack.stopSpeed)
	#			self.writeOpsModeCV(128, 0, False, MineTrack.throttle.getLocoAddress().getNumber())							
	
				self.resetLights(False)
				self.setCabLight(False)	# Turn cab light off
	
				sensors.provideSensor("IS:DIR").setState(UNKNOWN)		
				
				MineTrack.reseting = False
				
				#
				#  Delay at BOT
				botDelay = self.botDelayLong
				if (sensors.provideSensor("Demo Switch").getState() == ACTIVE) :	
					botDelay = self.botDelayDemo
				self.nixieDelay("BOT", botDelay)
				
			MineTrack.currentState = 1						 					
			self.changeDirection("Reverse")
			MineTrack.throttle.setF5(True)  # Turn on tender markers
			MineTrack.throttle.setF0(True)
			if (int(memories.getMemory("Mine Locomotive").getValue() != 6)) :						
				MineTrack.mineCar.setF0(True)  # Turn the light on (in case it went off)
			self.setBrake(False)
			MineTrack.throttle.setSpeedSetting(MineTrack.fastSpeed * MineTrack.speedScale) # Start moving forward
			#
			#  Turn the sound back on...	
			#self.waitMsec(2000) # Wait until after whistle blows
#			self.writeOpsModeCV(128, 25, False, MineTrack.throttle.getLocoAddress().getNumber())
			self.tootWhistle(1)	

			MineTrack.throttle.setF8(False)									

		return		
	
	#
	# Tunnel is occupied with southbound train.  No commands to train, just change state.
	def tunnelSouth(self):
		if (MineTrack.currentState == 1) :
			MineTrack.currentState = 2	
			print "Tunnel South"
# 			self.waitMsec(1500)							
# 			self.writeOpsModeCV(128, 45, False, MineTrack.throttle.getLocoAddress().getNumber())	
# 			self.waitMsec(1500)				
# 			self.writeOpsModeCV(128, 90, False, MineTrack.throttle.getLocoAddress().getNumber())	
# 			self.waitMsec(1500)		
# 			self.writeOpsModeCV(128, 135, False, MineTrack.throttle.getLocoAddress().getNumber())	
# 			self.waitMsec(1500)								
# 			self.writeOpsModeCV(128, 180, False, MineTrack.throttle.getLocoAddress().getNumber())			
		return 0
				
	#
	#  Northbound train enters tunnel.  Blow whistle & turn on cab light.
	def tunnelNorth(self):
		if (MineTrack.automationSwitch.getState() == INACTIVE) :
			self.stopAnimation()
			return 0
				
		if ((MineTrack.currentState == -3) and (not MineTrack.reseting)):
			MineTrack.currentState = -2
			print "Tunnel North"
			self.setCabLight(True) # Turn the cab light on
			self.waitMsec(500)				
			self.longWhistle(1, 1)
# 			self.waitMsec(2000)							
# 			self.writeOpsModeCV(128, 135, False, MineTrack.throttle.getLocoAddress().getNumber())	
# 			self.waitMsec(2000)		
# 			self.writeOpsModeCV(128, 90, False, MineTrack.throttle.getLocoAddress().getNumber())	
# 			self.waitMsec(2000)		
# 			self.writeOpsModeCV(128, 45, False, MineTrack.throttle.getLocoAddress().getNumber())		
# 			self.waitMsec(2000)		
# 			self.writeOpsModeCV(128, 25, False, MineTrack.throttle.getLocoAddress().getNumber())									

		return 0		
	
	#
	#  Southbound train enters Bridge-1.  Speed the train to fast.
	def bridge1South(self):
		if (MineTrack.automationSwitch.getState() == INACTIVE) :
			self.stopAnimation()
			return
		
		if ((MineTrack.currentState == 2) and (not MineTrack.reseting)) :
			MineTrack.currentState = 3
			self.resetLights(True)		
			speed = MineTrack.fastSpeed * MineTrack.speedScale
			MineTrack.throttle.setSpeedSetting(speed)
			self.setCabLight(False) # Turn cab light off					
		return
	
	#
	#  Northbound train enters Bridge-1.  Turn off bell & cab light and speed up (twice)
	def bridge1North(self):
		if (MineTrack.automationSwitch.getState() == INACTIVE) :
			self.stopAnimation()
			return
		
		if (MineTrack.currentState == -4 and (not MineTrack.reseting)) :
			MineTrack.currentState = -3		
			self.setCabLight(False) # Turn cab light off		
			self.ringBell(False) # Turn bell off	
			self.resetLights(True)
			
			speed = MineTrack.mediumSpeed * MineTrack.speedScale
			MineTrack.throttle.setSpeedSetting(speed)	
#			print "Bridge2North Speed = ", speed, " speedScale = ", MineTrack.speedScale, " speedIncrement = ", MineTrack.throttle.getSpeedIncrement()			
					
			self.waitMsec(1500)
			speed = MineTrack.fastSpeed * MineTrack.speedScale
#			print "Bridge2North Speed = ", speed, " speedScale = ", MineTrack.speedScale, " speedIncrement = ", MineTrack.throttle.getSpeedIncrement()
						
			MineTrack.throttle.setSpeedSetting(speed)	
		return 0

	def bridge2South(self):
		if (MineTrack.automationSwitch.getState() == INACTIVE) :
			self.stopAnimation()
			return 0
		
		if (MineTrack.currentState == 3 and (not MineTrack.reseting) and (MineTrack.automationSwitch.getState() == ACTIVE)) :
			MineTrack.currentState = 4		
			self.resetLights(True)
			
			self.longWhistle(1, 2.5)
	
			speed = MineTrack.slowSpeed * MineTrack.speedScale
			MineTrack.throttle.setSpeedSetting(speed)
#			print "Bridge2South Speed = ", speed, " speedScale = ", MineTrack.speedScale, " speedIncrement = ", MineTrack.throttle.getSpeedIncrement()	
			
			self.waitMsec(11000)
			speed = MineTrack.extraSlowSpeed * MineTrack.speedScale
			MineTrack.throttle.setSpeedSetting(speed)
#			print "Bridge2South Speed = ", speed, " speedScale = ", MineTrack.speedScale, " speedIncrement = ", MineTrack.throttle.getSpeedIncrement()				
		return 0
		
	def bridge2North(self):
		if (MineTrack.automationSwitch.getState() == INACTIVE) :
			self.stopAnimation()	
			return 0
				
		if (MineTrack.currentState == -5  and (not MineTrack.reseting)) : 
			MineTrack.currentState = -4			
			speed = MineTrack.slowSpeed * MineTrack.speedScale
			MineTrack.throttle.setSpeedSetting(speed)
#			print "Bridge2North speed = ", speed, " speedScale = ", MineTrack.speedScale, " speedIncrement = ", MineTrack.throttle.getSpeedIncrement()		
		return 0
		
	def buildingSouth(self):
		if (MineTrack.automationSwitch.getState() == INACTIVE) :
			self.stopAnimation()
			return 0
		
		if ((MineTrack.currentState == 4)) :		
			MineTrack.currentState = 5		

			self.ringBell(True)  # Start the bell ringing
			self.resetLights(True)
			self.dimLight(True)
			speed = MineTrack.creepSpeed * MineTrack.speedScale
			MineTrack.throttle.setSpeedSetting(speed)
#			print "BuildingSouth speed = ", speed, " speedScale = ", MineTrack.speedScale, " speedIncrement = ", MineTrack.throttle.getSpeedIncrement()	
		return 0
		
	def buildingNorth(self):
		if (MineTrack.automationSwitch.getState() == INACTIVE) :
			self.stopAnimation()
			return 0
		
		if (MineTrack.currentState == 6 ) :
			MineTrack.currentState = -5		
#			print "Building Listener ",  " MineTrack.currentState = ", MineTrack.currentState						
			self.ringBell(False) # Turn bell after after leaving building
			speed = MineTrack.slowSpeed * MineTrack.speedScale
			MineTrack.throttle.setSpeedSetting(speed)
			self.dimLight(False)
#			print "BuildingNorth speed = ", speed	
		return
	
	#
	#  Coffee break after going through building
	def coffeeBreak(self):
		self.setBrake(True)
		MineTrack.throttle.setSpeedSetting(MineTrack.stopSpeed);
		sensors.provideSensor("IS:DIR").setState(UNKNOWN)		
		self.ringBell(False)  # Stop ringing bell

		self.waitMsec(4000)
		self.stopWhistle()
		self.waitMsec(2000)
		self.setCabLight(True) # Turn the cab light on
		self.waitMsec(2000)
		self.waterFill(25)
		self.waitMsec(8000)
		self.steamRelease(6)

		return		
	#
	#  Return northbound to mine after delay at building.	
	def returnToMine(self):
		self.changeDirection("Forward")		
		print "Return to Mine"
		self.forwardWhistle()

		self.setBrake(False)
		self.waitMsec(1000)
		MineTrack.throttle.setF1(True) # Turn bell on
		MineTrack.throttle.setSpeedSetting(MineTrack.creepSpeed * MineTrack.speedScale) # Start going back	
		self.waitMsec(3000)			
		MineTrack.throttle.setSpeedSetting(MineTrack.extraSlowSpeed * MineTrack.speedScale) # Start going back	
		return;
			
	def EOTAction(self):
		if ((MineTrack.currentState == 5) and (MineTrack.automationSwitch.getState() == ACTIVE)) :		
			MineTrack.currentState = 6		
			self.resetLights(True)
	
			# Keep going 3 seconds until we are really at the end of track, then stop & toot the whistle	
			self.waitMsec(2500)

			print "At EOT, setting brake, current value = ", MineTrack.throttle.getF7()
			self.setBrake(True)
			self.waitMsec(1000)
			print "At EOT, setting brake, new value = ", MineTrack.throttle.getF7()			
			MineTrack.throttle.setSpeedSetting(MineTrack.stopSpeed);
			
			self.waitMsec(1000)
			self.ringBell(False) # Quit ringing bell		
				
			self.waitMsec(1000)
			self.stopWhistle()			
	
			sensors.provideSensor("IS:DIR").setState(UNKNOWN)			
			
			#
			#  Wait 15 seconds at EOT
			self.nixieDelay("EOT", 15)					
						
			#
			#  Move the loco forward to clear building for crew coffee break
			self.changeDirection("Forward")		
			self.setBrake(False)
			self.waitMsec(1000)
			self.ringBell(True) # Start ringing bell
			self.tootWhistle(2)
			self.waitMsec(1500)			
			MineTrack.throttle.setSpeedSetting(MineTrack.extraSlowSpeed);
			
			#
			#  Coffee break		
			self.waitMsec(7000)						
			self.coffeeBreak()
						
			eotDelay = self.eotDelayLong
			if (sensors.provideSensor("Demo Switch").getState() == ACTIVE) :
				eotDelay = self.eotDelayDemo
			self.nixieDelay("EOT", eotDelay)					
			#
			#  Start going back....

			self.returnToMine()
		elif (MineTrack.automationSwitch.getState() == INACTIVE) :
			self.stopAnimation()
		return	

	#	
	# handle() is called repeatedly until it returns false.
	def handle(self):
		self.waitSensorActive(MineTrack.automationSwitch)
		#
		#  Reset the locomotive to BOT so we know where we are	
		if (MineTrack.currentState == 999) : 
			self.reset()
		
		self.waitSensorActive(sensors.provideSensor("BOT"))
		self.BOTAction()
		
		self.waitSensorActive(sensors.provideSensor("Tunnel"))		
		self.tunnelSouth()

		self.waitSensorActive(sensors.provideSensor("Bridge-1"))		
		#
		#  Only trigger when moving away from the mine
		self.bridge1South()
			
		self.waitSensorActive(sensors.provideSensor("Bridge-2"))
		self.bridge2South()
								
		self.waitSensorActive(sensors.provideSensor("Mine Building"))	
		self.buildingSouth()

		self.waitSensorActive(sensors.provideSensor("EOT"))	
#		print "EOT Sensor Active"	
		self.EOTAction()

		self.waitSensorInactive(sensors.provideSensor("Mine Building"))	
		self.buildingNorth()		
		
		self.waitSensorActive(sensors.provideSensor("Bridge-2"))
		self.bridge2North()	
		
		self.waitSensorActive(sensors.provideSensor("Bridge-1"))	
		self.bridge1North()
		
		self.waitSensorActive(sensors.provideSensor("Tunnel"))	
		self.tunnelNorth()		
				
		#  Stop the train if the switch is turned off...
		if (MineTrack.automationSwitch.getState() != ACTIVE) :
			print "Handle: stopping animation"
			self.stopAnimation()
			return 0 # exit
		self.waitMsec(1000)
						
		return 1 # continue
	
# end of class definition
	
# create one of these
main = MineTrack()

# set the name, as a example of configuring it
main.setName("Automated Beaver Bend Mine Track")

# and start it running
main.start()
