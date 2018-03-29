#
#  Script to shuttle mine train back & forth, turning on various lights, etc. along the way.

import jmri
import jmri.jmrit.roster
import jmri.jmrix.AbstractThrottle
import sys
from java.awt import Font
import jmri.jmrit.display.panelEditor.configurexml.PanelEditorXml
import foggyhollow.departureboard.DepartureBoard

sys.modules.clear()

class MineTrack(jmri.jmrit.automat.AbstractAutomaton) :
	
	throttle = None
	mineCar = None
	speedScale = 1
	reseting = True
	trackNumber = 3
	trainName = "HIGH LINE GOPHER"

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
			if (event.source.getState() != ACTIVE) :
				#self.stopAnimation(self.parent)
				print "Stopping animation from StopTrainListener"
				self.parent.currentState = 999
				try :
					self.parent.throttle.setSpeedSetting(self.parent.stopSpeed)
					self.parent.throttle.setIsForward(True)				
					self.parent.throttle.setF0(True)  # Turn headlight on
					self.parent.throttle.setF1(False) # Turn bell off
					self.parent.throttle.setF2(False) # Turn whistle off				
					self.parent.throttle.setF4(False) # Turn steam release off
					self.parent.throttle.setF5(True)  # Turn tender lights on
					self.parent.throttle.setF6(False) # Turn water fill off	
					self.parent.throttle.setF11(True) # Turn cab light on
					self.parent.mineCar.setF0(True)
				except:
					print "Unexpected error in SetRosterIcon: ", sys.exc_info()[0], sys.exc_info()[1]	
									
				sensors.provideSensor("Red EOT Lantern").setState(ACTIVE)
				sensors.provideSensor("IS:DIR").setState(UNKNOWN)	
				
				self.parent.departureBoard.clearRow(1,True)
				self.parent.departureBoard.clearRow(2,True)
				self.parent.departureBoard.clearRow(0,True)
				self.parent.departureBoard.clearRow(3,True)
																								
				self.parent.departureBoard.setField("LocoDescr", "Welcome to the", 1, 0)
				self.parent.departureBoard.setField("LocoDescr", "Foggy Hollow & Western RailRoad", 2, 0)	
				self.parent.departureBoard.setField("LocoDescr", "Beaver Bend Division", 3, 0)							

#				self.parent.waitMsec(2000)
				self.parent.departureBoard.stop()

				#self.parent.stop()
				print "stopAnimation done in StopTrainListener"	
			else :
				print "Starting animation from StopTrainListener"
				self.parent.reseting = True
				self.parent.currentState = 999
				self.parent.reset()							
			return	
		
	class LocoChangeListener(java.beans.PropertyChangeListener) :
		def init(self, parent):
			self.parent = parent
			return		
		
		def propertyChange(self, event) :			
			self.parent.setRosterIcon()
			return						
	
	def setDepartureBoard(self, trainNo, trackNo, trainName, destination, departTime, status, row):
		self.departureBoard.setField("Track", trackNo, row, 0)
		self.departureBoard.setField("Train", trainNo, row, 0)
		if (len(destination) > 0 and len(trainName) > 0) :	
			self.departureBoard.setField("Destination", [destination, trainName], row, 0)	
		elif (len(destination) > 0):
			self.departureBoard.setField("Destination", destination, row, 0)
		else :
			self.departureBoard.setField("Destination", trainName, row, 0)
		self.departureBoard.setField("Departs", departTime, row, 0)
		self.departureBoard.setField("Status", status, row, 0)
		
		self.waitMsec(int(len(destination)/3 * 1000))
									
	#
	#  Count down the BOT or EOT delay on the GUI.  The delay time is randomized using a Gaussian distribution with
	#  the supplied delay as the mean and 1 sigma...  The delay parameter is in seconds.
	def nixieDelay(self, station, direction, delaySeconds):		
		self.departureBoard.clock("Departs", delaySeconds, self.trackNumber-1, False)
		self.waitMsec(int(delaySeconds * 1000)) #  Still have to wait here to prevent train from moving.
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		return							
		
	# init() is called exactly once at the beginning to do
	# any necessary configuration.
	def init(self) :
		
		print "Initializing MineTrack animation"
		global throttle

		self.currentState = 999
		self.automationSwitch = sensors.provideSensor("IS:MTS")	
		self.automationSwitch.setState(INACTIVE);
		sensors.provideSensor("Demo Switch").setState(INACTIVE)		
		
		self.mineCar = self.getThrottle(6,False) 	
		self.locoAddress = int(memories.getMemory("Mine Locomotive").getValue())
		self.throttle = self.getThrottle(self.locoAddress, False)						

#		self.splitFlapSound = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/typewriterClipped.wav"))		
		if (self.throttle == None) :
			print "Couldn't assign throttle!"		
		self.throttle.setSpeedStepMode(1)
		self.speedScale = 1

		#
		#  
		self.fastSpeed = 22 * self.throttle.getSpeedIncrement()		
		self.mediumSpeed = 16 * self.throttle.getSpeedIncrement()				
		self.slowSpeed = 14 * self.throttle.getSpeedIncrement()
		self.extraSlowSpeed = 9 * self.throttle.getSpeedIncrement()
		self.creepSpeed = 6 * self.throttle.getSpeedIncrement()
		
		#
		#  Listen for user to turn off the animation switch
		stopTrainListener = self.StopTrainListener()
		stopTrainListener.init(self.automationSwitch, self)
		self.automationSwitch.addPropertyChangeListener(stopTrainListener)	

		#
		#  Show the ID of the selected loco on the panel
		print "In MineTrack.init() - starting to init Roster Icon"		
		self.setRosterIcon()
#		self.setMemoryIconFont()		
		
		print "In MineTrack.init() - starting to create departure board"
		self.departureBoard = foggyhollow.departureboard.DepartureBoard("Ace of Spades Mine", "Departures", 30, 322, 4, 44)
#		self.departureBoard = jmri.jmrit.departureboard.DepartureBoard("Ace of Spades Mine", "Departures", 30, 322, 4, 44)
		self.departureBoard.addField("Track", 0, 2, True)
		self.departureBoard.addField("Train", 3, 7, False)		
		self.departureBoard.addField("Destination", 10, 20, False)		
		self.departureBoard.addField("Departs", 31, 5, True)
		self.departureBoard.addField("Status", 37, 7, True)			
		self.departureBoard.addField("LocoDescr", 0, 44, False)			
		
		self.departureBoard.setField("LocoDescr", "Welcome to the", 1, 0)
		self.departureBoard.setField("LocoDescr", "Foggy Hollow & Western RailRoad", 2, 0)	
		self.departureBoard.setField("LocoDescr", "Beaver Bend Division", 3, 0)			
		#
		#  Listen for changes in locomotive number to change picture & labels
		print "In MineTrack.init() - starting to loco Change Listener"
		listener = self.LocoChangeListener()
		listener.init(self)
		memories.getMemory("Mine Locomotive").addPropertyChangeListener(listener)
						
		return
	
	def getTrainNumber(self, direction):
		locoids = self.rosterEntry.getId().split()
		if (direction == "NORTH") :
			trainNumber = locoids[0] + " " + str(int(locoids[1]) +1).lstrip("0")	# Strip leading zeros from loco number (used in roster for good sort)			
		else :
			trainNumber = locoids[0] + " " + locoids[1].lstrip("0")	# Strip leading zeros from loco number (used in roster for good sort)			
		return trainNumber
	
	def clearLocomotiveDescription(self):
		self.departureBoard.clearRow(2, True); # stops toggling "Service Loco"		
		return
				
	def setLocomotiveDescription(self):
		locoids = self.rosterEntry.getId().split()
		locoid = locoids[0] + " " + locoids[1].lstrip("0")	# Strip leading zeros from loco number (used in roster for good sort)	
					
		description = locoid + " " + self.rosterEntry.getMfg() + " " + self.rosterEntry.getModel()
		description = description.replace("&", "+").upper()
		self.departureBoard.setField("LocoDescr", description[:44], 2, 0)	
		
		self.waitMsec(1500) # Wait for description to get set so track number doesn't get clobbered
		self.departureBoard.setField("Track", str(self.trackNumber), 2, 0)
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
					
					#
					#  Remember this for later....
					self.rosterEntry = entry
					
					# Break loco ID at 
					locoids = entry.getId().split()
					locoid = locoids[0] + " " + locoids[1].lstrip("0")
					
					for b in blockList:
						if (b.getState() == jmri.Block.OCCUPIED) :
							b.setValue(locoid)
						else :
							b.setValue("")						
							
		except:
			print "Unexpected error in SetRosterIcon: ", sys.exc_info()[0], sys.exc_info()[1]	
		return	
	
	def reset(self):
		print "in MineTrack.reset()"
		#
		#  If train is already at the beginning-of-track, just start the train moving forward
		#  Otherwise, we need to find the train.		
		try :		
			if (sensors.provideSensor("BOT").getState() != ACTIVE) :					
				self.reseting = True
				self.currentState = 999

				self.departureBoard.clearRow(2, True)				
				self.setDepartureBoard(self.getTrainNumber("NORTH"), str(self.trackNumber), "Beginning of Track", "RESET EXPRESS",  " ", " ", 2)

				self.departureBoard.clearRow(1, False)
#				self.departureBoard.clearRow(0, False)
				self.departureBoard.clearRow(3, False)												
					
				self.resetLights(True)
				self.setBrake(False)
				self.forwardWhistle()
				self.waitMsec(200)
				
				sensors.provideSensor("Red EOT Lantern").setState(INACTIVE)				
				self.changeDirection("Forward")
				self.throttle.setSpeedSetting(self.fastSpeed * self.speedScale)

		except :
			print "Unexpected error in reset: ", sys.exc_info()[0], sys.exc_info()[1]	
		
		return 0
	
	def stopAnimation(self):
		try :
			self.throttle.setSpeedSetting(self.stopSpeed)
			self.throttle.setIsForward(True)				
			self.throttle.setF0(True)  # Turn headlight on
			self.throttle.setF1(False) # Turn bell off
			self.throttle.setF2(False) # Turn whistle off				
			self.throttle.setF4(False) # Turn steam release off
			self.throttle.setF5(True)  # Turn tender lights on
			self.throttle.setF6(False) # Turn water fill off	
			self.throttle.setF11(True) # Turn cab light on
			self.mineCar.setF0(True)
		except:
			print "Unexpected error in SetRosterIcon: ", sys.exc_info()[0], sys.exc_info()[1]	
							
		sensors.provideSensor("Red EOT Lantern").setState(ACTIVE)
		sensors.provideSensor("IS:DIR").setState(UNKNOWN)	
		
		return					
	#
	# Change the direction of both the locomotive & leading mine car.  
	def changeDirection(self, direction):

		self.reseting = False
		if (direction == "Reverse"):
			self.throttle.setIsForward(False)
			self.mineCar.setIsForward(False)
			sensors.provideSensor("IS:DIR").setState(ACTIVE)
		else :
			self.throttle.setIsForward(True)
			self.mineCar.setIsForward(True)	
			sensors.provideSensor("IS:DIR").setState(INACTIVE)		
		return 0
			
	#
	#  Short toot of the whistle 
	def tootWhistle(self, numToots):
		for n in range(numToots) :
			self.throttle.setF3(not self.throttle.getF3())			
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
			self.throttle.setF2(True)
			self.waitMsec(int(duration))		
			self.throttle.setF2(False)
			randomGap = gap + java.util.Random().nextGaussian()*(gap *.2)			
			self.waitMsec(int(randomGap))

		return 0
	
	#
	#  Cab Light
	def setCabLight(self, state):
		self.throttle.setF11(state)
		return 0
	#
	#  Brake
	def setBrake(self, state):
		self.throttle.setF7(state)
		return 0
	
	#
	#
	def ringBell(self, state):
		self.throttle.setF1(state)
		return 0
	
	#
	#  Play the sound of the fireman blowing out the boiler the specified number of seconds
	def steamRelease(self, seconds):
		self.departureBoard.setField("Destination", "BLOWOUT BOILER", 3, 0)
		self.waitMsec(2000)
		self.throttle.setF4(True)
		self.waitMsec(seconds * 1000)
		self.throttle.setF4(False)	
		self.departureBoard.clearField("Destination", 3, 0)
		
		
	#
	#  Play the sound of filling the tender with water for the specified number of seconds.
	def waterFill(self, seconds):
		self.departureBoard.setField("Destination", "FILL TENDER", 3, 0)
		self.waitMsec(2000)
		self.throttle.setF6(True)
		self.waitMsec(seconds * 1000)
		self.throttle.setF6(False)		
		self.departureBoard.clearField("Destination", 3, 0)		
		
	#
	#  Dim the headlight
	def dimLight(self, state):
		self.throttle.setF9(state)
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
# 		for editor in editorList:
# 			try :
# 				panel = editor.getFrame()
# 				icon = self.findPanelIcon(panel,"Roster ID")
# 				if (icon is not None) :
# 					icon.setFont(Font("Tempus Sans ITC", Font.ITALIC , 20))	
# 					
# 				icon = self.findPanelIcon(panel,"Roster Description")
# 				if (icon is not None) :
# 					icon.setFont(Font("tempus sans itc", Font.ITALIC, 16))						
# 			except:
# 				print "Error setting MemoryIcon font: "	
		return 0
	
	#
	#  Set the locomotive/mine car lights to the specified state.  Called at block transitions to restore lights if lost due to dirty track.
	def resetLights(self, state):
		self.throttle.setF0(state)  # Turn the light on (in case it went off)
		if (int(memories.getMemory("Mine Locomotive").getValue() != 6)) :						
			self.mineCar.setF0(state)  # Turn the light on (in case it went off)						
		self.throttle.setF5(state)  # Turn the tender markers on (in case it went off)	
		return 0
	
	def BOTAction(self):					
		if (self.currentState == -2 or self.currentState == 999) :
#			print "BOTAction"
			
			# Don't delay 1st time
			if (self.currentState != 999) :
				self.currentState = 1 # do this here to get it done fast before a wagging sensor sends us back here						 					
				self.throttle.setF8(True) # Mute the sound while we wait
				
				#
				#  Unlock decoder to write CVs
				self.throttle.setSpeedSetting(self.stopSpeed)	
				self.resetLights(False)
				self.setCabLight(False)	# Turn cab light off
	
				sensors.provideSensor("IS:DIR").setState(UNKNOWN)		
				
				self.reseting = False
				
				#
				#  Delay at BOT
				botDelay = self.botDelayLong
				if (sensors.provideSensor("Demo Switch").getState() == ACTIVE) :	
					botDelay = self.botDelayDemo
					
				self.departureBoard.clearRow(2, True)
				self.setDepartureBoard(self.getTrainNumber("SOUTH"), str(self.trackNumber), self.trainName, "ACE OF SPADES MINE", "     ", "ON TIME", 2)
				self.nixieDelay("EOT", "SOUTH", botDelay)

			else:
				self.currentState = 1						 									
				self.throttle.setSpeedSetting(self.stopSpeed)
				self.departureBoard.clearRow(2, True)				
				self.setDepartureBoard(self.getTrainNumber("SOUTH"), str(self.trackNumber), self.trainName, "ACE OF SPADES MINE", "     ", "ON TIME", 2)				
				self.departureBoard.createRandomRow(0, 0);
				self.departureBoard.createRandomRow(1, 10);			
				
				
			if (self.automationSwitch.getState() != ACTIVE)	:
				self.stopAnimation()	
			else:			
				self.currentState = 1						 					
				self.changeDirection("Reverse")
				self.throttle.setF5(True)  # Turn on tender markers
				self.throttle.setF0(True)
				if (int(memories.getMemory("Mine Locomotive").getValue() != 6)) :						
					self.mineCar.setF0(True)  # Turn the light on (in case it went off)
				self.setBrake(False)
				self.throttle.setSpeedSetting(self.fastSpeed * self.speedScale) # Start moving forward
				self.departureBoard.setField("Status", "DEPARTD", self.trackNumber-1, 4)
			
				#
				#  Turn the sound back on...
				self.throttle.setF8(False)													
				#self.tootWhistle(1)	
		return		
	
	#
	# Tunnel is occupied with southbound train.  No commands to train, just change state.
	def tunnelSouth(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()			
		if (self.currentState == 1) :
			self.currentState = 2	
#			print "Tunnel South"			
		return 0
				
	#
	#  Northbound train enters tunnel.  Blow whistle & turn on cab light.
	def tunnelNorth(self):	
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if ((self.currentState == -3) and (not self.reseting)):
			self.currentState = -2
#			print "Tunnel North"
			self.setCabLight(True) # Turn the cab light on
			self.waitMsec(500)				
			self.longWhistle(1, 1)
		return 0		
	
	#
	#  Southbound train enters Bridge-1.  Speed the train to fast.
	def bridge1South(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if ((self.currentState == 2) and (not self.reseting)) :
			self.currentState = 3
#			print "Bridge 1 South"
			self.resetLights(True)		
			speed = self.fastSpeed * self.speedScale
			self.throttle.setSpeedSetting(speed)
			self.setCabLight(False) # Turn cab light off					
		return
	
	#
	#  Northbound train enters Bridge-1.  Turn off bell & cab light and speed up (twice)
	def bridge1North(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if (self.currentState == -4 and (not self.reseting)) :
			self.currentState = -3		
#			print "Bridge 1 North"
			self.setCabLight(False) # Turn cab light off		
			self.ringBell(False) # Turn bell off	
			self.resetLights(True)
			
			speed = self.mediumSpeed * self.speedScale
			self.throttle.setSpeedSetting(speed)	
#			print "Bridge2North Speed = ", speed, " speedScale = ", self.speedScale, " speedIncrement = ", self.throttle.getSpeedIncrement()			
					
			self.waitMsec(1500)
			speed = self.fastSpeed * self.speedScale
#			print "Bridge2North Speed = ", speed, " speedScale = ", self.speedScale, " speedIncrement = ", self.throttle.getSpeedIncrement()
						
			self.throttle.setSpeedSetting(speed)	
		return 0

	def bridge2South(self):		
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if (self.currentState == 3 and (not self.reseting) and (self.automationSwitch.getState() == ACTIVE)) :
			self.currentState = 4		
			print "Bridge 2 South"
			self.resetLights(True)
			
			self.longWhistle(1, 2.5)
	
			speed = self.slowSpeed * self.speedScale
			self.throttle.setSpeedSetting(speed)
#			print "Bridge2South Speed = ", speed, " speedScale = ", self.speedScale, " speedIncrement = ", self.throttle.getSpeedIncrement()	
			
			self.waitMsec(11000)
			speed = self.extraSlowSpeed * self.speedScale
			self.throttle.setSpeedSetting(speed)
#			print "Bridge2South Speed = ", speed, " speedScale = ", self.speedScale, " speedIncrement = ", self.throttle.getSpeedIncrement()				
		return 0
		
	def bridge2North(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if (self.currentState == -5  and (not self.reseting)) : 
			self.currentState = -4			
			print "Bridge 2 North"
			speed = self.slowSpeed * self.speedScale
			self.throttle.setSpeedSetting(speed)
#			print "Bridge2North speed = ", speed, " speedScale = ", self.speedScale, " speedIncrement = ", self.throttle.getSpeedIncrement()		
		return 0
		
	def buildingSouth(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if ((self.currentState == 4)) :		
			self.currentState = 5		
			print "Building South"
			self.ringBell(True)  # Start the bell ringing
			self.resetLights(True)
			self.dimLight(True)
			speed = self.creepSpeed * self.speedScale
			self.throttle.setSpeedSetting(speed)
			self.departureBoard.setField("Status", "ARRIVED", self.trackNumber-1, 1)							
#			print "BuildingSouth speed = ", speed, " speedScale = ", self.speedScale, " speedIncrement = ", self.throttle.getSpeedIncrement()	
		return 0
		
	def buildingNorth(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if (self.currentState == 6 ) :
			self.currentState = -5		
			print "Building North"
#			print "Building Listener ",  " self.currentState = ", self.currentState						
			self.ringBell(False) # Turn bell after after leaving building
			speed = self.slowSpeed * self.speedScale
			self.throttle.setSpeedSetting(speed)
			self.dimLight(False)
#			print "BuildingNorth speed = ", speed	
		return
	
	#
	#  Service locomotive after going through building
	def serviceLocomotive(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		self.setBrake(True)
		self.throttle.setSpeedSetting(self.stopSpeed);
		
		sensors.provideSensor("IS:DIR").setState(UNKNOWN)		
		self.ringBell(False)  # Stop ringing bell

		self.waitMsec(4000)
		self.stopWhistle()
		
		sensors.provideSensor("IS:SERVICELIGHT").setState(ACTIVE)
		
		self.setLocomotiveDescription()
#		self.departureBoard.clearRow(2, True); # stops toggling "Service Loco"


		self.setCabLight(True) # Turn the cab light on
		self.waitMsec(4000)
		self.waterFill(25)
		self.waitMsec(8000)
		self.steamRelease(15)
		self.waitMsec(8000)
		
		self.clearLocomotiveDescription()
		sensors.provideSensor("IS:SERVICELIGHT").setState(INACTIVE)	
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()
		return		
	#
	#  Return northbound to mine after delay at building.	
	def returnToMine(self):	
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		self.changeDirection("Forward")		
#		print "Return to Mine"
		self.forwardWhistle()

		self.setBrake(False)
		self.waitMsec(1000)
		self.throttle.setF1(True) # Turn bell on
		self.throttle.setSpeedSetting(self.creepSpeed * self.speedScale) # Start going back	
		self.waitMsec(3000)			
		self.throttle.setSpeedSetting(self.extraSlowSpeed * self.speedScale) # Start going back	
		
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		return;
			
	def EOTAction(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()
					
		if ((self.currentState == 5) and (self.automationSwitch.getState() == ACTIVE)) :		
			self.currentState = 6		
			self.resetLights(True)
	
			# Keep going 3 seconds until we are really at the end of track, then stop & toot the whistle	
			self.waitMsec(2000)

			print "At EOT, setting brake, current value = ", self.throttle.getF7()
			self.setBrake(True)
			self.waitMsec(500)
			print "At EOT, setting brake, new value = ", self.throttle.getF7()			
			self.throttle.setSpeedSetting(self.stopSpeed);
			
			self.waitMsec(1000)
			self.ringBell(False) # Quit ringing bell		
				
			self.waitMsec(1000)
			self.stopWhistle()			
	
			sensors.provideSensor("IS:DIR").setState(UNKNOWN)			
			
			#
			#  Wait 15 seconds at EOT
			self.setDepartureBoard(self.getTrainNumber("NORTH"), str(self.trackNumber), "", "SERVICE LOCO", " ", " ", 2)
#			self.setDepartureBoard(self.getTrainNumber("NORTH"), str(self.trackNumber), "MEN AT WORK", "SERVICE LOCO", " ", " ", 2)			
			self.nixieDelay("EOT", "NORTH", 15)		

						
			#
			#  Move the loco forward to service the locomotive
			self.changeDirection("Forward")		
			self.setBrake(False)
			self.waitMsec(1000)
			self.ringBell(True) # Start ringing bell
			self.tootWhistle(2)
			self.waitMsec(1500)			
			self.throttle.setSpeedSetting(self.extraSlowSpeed);
			
			#
			#  Service Locomotive		
			self.waitMsec(7000)						
			self.serviceLocomotive()
						
			eotDelay = self.eotDelayLong
			if (sensors.provideSensor("Demo Switch").getState() == ACTIVE) :
				eotDelay = self.eotDelayDemo
			
			self.setDepartureBoard(self.getTrainNumber("NORTH"), str(self.trackNumber), self.trainName,  "MYSTIC SPRINGS", "     ", "ON TIME", 2)
			self.nixieDelay("EOT", "NORTH", eotDelay)	
			if (self.automationSwitch.getState() == ACTIVE)	:
	#			self.departTimeBoard.flipWord("DEP'D", 5)	
				self.departureBoard.setField("Status", "DEPARTD", self.trackNumber-1, 3)				
				#
				#  Start going back....
	
				self.returnToMine()
		return	

	#	
	# handle() is called repeatedly until it returns false.
	def handle(self):
		self.waitSensorActive(self.automationSwitch)
		#
		#  Reset the locomotive to BOT so we know where we are	
		#if (self.currentState == 999 and not self.reseting == True) : 
		#	self.reset()
		
#		print "handle top", self.currentState, " resetting = ", self.reseting				

#		self.waitSensorActive(sensors.provideSensor("BOT"))
		self.waitSensorActive([self.automationSwitch, sensors.provideSensor("BOT")])
		if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("BOT").getState() == ACTIVE) :
			self.BOTAction()
		
#		print "Handle waiting tunnel", self.currentState, " resetting = ", self.reseting				
#		self.waitSensorActive(sensors.provideSensor("Tunnel"))	
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Tunnel")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Tunnel").getState() == ACTIVE) :
				self.tunnelSouth()

#		print "Handle waiting bridge 1", self.currentState, " resetting = ", self.reseting				
#		self.waitSensorActive(sensors.provideSensor("Bridge-1"))
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-1")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Bridge-1").getState() == ACTIVE) :
				#
				#  Only trigger when moving away from the mine
				self.bridge1South()
			
#		print "Handle waiting bridge 2", self.currentState, " resetting = ", self.reseting							
#		self.waitSensorActive(sensors.provideSensor("Bridge-2"))
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-2")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Bridge-2").getState() == ACTIVE) :
				self.bridge2South()
						
#		print "Handle waiting building", self.currentState, " resetting = ", self.reseting												
#		self.waitSensorActive(sensors.provideSensor("Mine Building"))	
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Mine Building")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Mine Building").getState() == ACTIVE) :
				self.buildingSouth()

#		print "Handle waiting eot", self.currentState, " resetting = ", self.reseting				
#		self.waitSensorActive(sensors.provideSensor("EOT"))	
#		print "EOT Sensor Active"	
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("EOT")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("EOT").getState() == ACTIVE) :
				self.EOTAction()

#		print "Handle waiting mine building", self.currentState, " resetting = ", self.reseting				
#		self.waitSensorInactive(sensors.provideSensor("Mine Building"))	
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Mine Building")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Mine Building").getState() != ACTIVE) :
				self.buildingNorth()		
		
#		print "Handle waiting bridge2", self.currentState, " resetting = ", self.reseting						
#		self.waitSensorActive(sensors.provideSensor("Bridge-2"))
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-2")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Bridge-2").getState() == ACTIVE) :
				self.bridge2North()	
		
#		print "Handle waiting Bridge1", self.currentState, " resetting = ", self.reseting						
#		self.waitSensorActive(sensors.provideSensor("Bridge-1"))	
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-1")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Bridge-1").getState() == ACTIVE) :
				self.bridge1North()
		
#		print "Handle waiting tunnel", self.currentState, " resetting = ", self.reseting						
#		self.waitSensorActive(sensors.provideSensor("Tunnel"))	
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Tunnel")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Tunnel").getState() == ACTIVE) :
				self.tunnelNorth()		
				
		self.waitMsec(500)
						
		return 1 # continue
	
# end of class definition
	
# create one of these
main = MineTrack()

# set the name, as a example of configuring it
main.setName("Automated Beaver Bend Mine Track")

# and start it running
main.start()
