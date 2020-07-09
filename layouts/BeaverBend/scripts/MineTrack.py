import java
#
#  Script to shuttle mine train back & forth, turning on various lights, etc. along the way.

import sys
sys.path.append("/home/pi/MyJMRI/lib/foggyhollow.jar")

import jmri
import jmri.jmrit.roster
import jmri.jmrix.AbstractThrottle

from java.awt import Font
import jmri.jmrit.display.panelEditor.configurexml.PanelEditorXml
import foggyhollow
import foggyhollow.departureboard.DepartureBoard
from Locomotive import Locomotive

class MineTrack(jmri.jmrit.automat.AbstractAutomaton) :
	
	import sys
	throttle = None
	mineCar = None
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
	
	eotDelayLong = 7 * 60
	botDelayLong = 8 * 60

        # Delay for coffee break
        coffeeDelayLong = 10 * 60
        coffeeDelayDemo = 2 * 60        
	
	#
	#  Listen for user to turn the GUI automation switch off.  Stop the locomotive and turn lights on.			
	import java
	class StopTrainListener(java.beans.PropertyChangeListener) :	
		def init(self, sensor, parent):
			self.sensor = sensor
			self.parent = parent
			return		
		
		def propertyChange(self, event) :
			if (event.source.getState() != ACTIVE) :
                                print "\n\n ### Stopping mine train animation ###\n\n"
				self.parent.currentState = 999
				try :
					self.parent.locomotive.setSpeed(self.parent.stopSpeed)
					self.parent.changeDirection("Forward")				
					self.parent.locomotive.setFunction("Light", True)  # Turn headlight on
					self.parent.locomotive.ringBell(False) # Turn bell off
					self.parent.locomotive.setFunction("Whistle", False) # Turn whistle off				
					#self.parent.steamRelease(0.1) # Turn steam release off
					self.parent.locomotive.setTenderMarkers(True)
					#self.parent.waterFill(0.1) # Turn water fill off	
					self.parent.locomotive.setCabLight(True)
					self.parent.mineCar.setFunction("Light", True)
				except:
					print "Unexpected error in SetRosterIcon: ", sys.exc_info()[0], sys.exc_info()[1]	
									
				sensors.provideSensor("Red EOT Lantern").setState(ACTIVE)
				sensors.provideSensor("IS:DIR").setState(UNKNOWN)	

				self.parent.departureBoard.stop()
                                
				self.parent.departureBoard.clearRow(1,True)
				self.parent.departureBoard.clearRow(2,True)
				self.parent.departureBoard.clearRow(0,True)
				self.parent.departureBoard.clearRow(3,True)
																								
				self.parent.departureBoard.setField("LocoDescr", "Welcome to the", 1, 0)
				self.parent.departureBoard.setField("LocoDescr", "Foggy Hollow & Western RailRoad", 2, 0)	
				self.parent.departureBoard.setField("LocoDescr", "Beaver Bend Division", 3, 0)							


			else :
				self.parent.reseting = True
				self.parent.currentState = 999
				self.parent.reset()							
			return	
	
	import java
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
	
	#
	#  Post the departure time on the departure board.  Use the current time plus the number of 
	#  seconds to calculate when the train will depart in local time (HH:MM)
	def postDepartureTime(self, delaySeconds, row):
		import time

		now = time.time()
		timeStr = time.strftime("%I:%M", time.localtime(now + delaySeconds))		
		self.departureBoard.setField("Departs", timeStr, row, 0)	
		
		correctedTime = int(   round (((now + float(delaySeconds)) - now) / 60.0)  * 60.0)
		return correctedTime
		
		
	#
	# Check for a delayed departure.  10% of the time delay by 5 minutes + up to 5 more minutes.
	def checkForDelay(self):
		import java

		if (sensors.provideSensor("Demo Switch").getState == INACTIVE and java.util.Random().nextInt(100) <= 10) :
			delaySeconds = 5*60 + java.util.Random().nextInt(5*60)
			adjustedDelay = self.postDepartureTime(delaySeconds, self.trackNumber-1)
			self.departureBoard.setField("Status", "DELAYED", self.trackNumber-1, 1)
			self.waitMsec(adjustedDelay*1000)
		return 0
			
		
	# init() is called exactly once at the beginning to do
	# any necessary configuration.
	def init(self) :
		
		import foggyhollow
		import foggyhollow.departureboard.DepartureBoard
		from Locomotive import Locomotive

		#global throttle
		
		self.locomotive = Locomotive()
		self.locoAddress = int(memories.getMemory("Mine Locomotive").getValue())		
		self.locomotive.init("Foggy Hollow & Western", self.locoAddress)
		
		self.mineCar = Locomotive()
		self.mineCar.init("Ace of Spades", 6)
		
                self.tripCounter = 0
		self.currentState = 999
		self.automationSwitch = sensors.provideSensor("IS:MTS")	
		self.automationSwitch.setState(INACTIVE);
		sensors.provideSensor("Demo Switch").setState(INACTIVE)		
		
		#
		#  
		self.fastSpeed = 19 * self.locomotive.throttle.getSpeedIncrement()		
		self.mediumSpeed = 16 * self.locomotive.throttle.getSpeedIncrement()				
		self.slowSpeed = 14 * self.locomotive.throttle.getSpeedIncrement()
		self.extraSlowSpeed = 12 * self.locomotive.throttle.getSpeedIncrement()
		self.creepSpeed = 8 * self.locomotive.throttle.getSpeedIncrement()
		
		#
		#  Listen for user to turn off the animation switch
		stopTrainListener = self.StopTrainListener()
		stopTrainListener.init(self.automationSwitch, self)
		self.automationSwitch.addPropertyChangeListener(stopTrainListener)	

		#
		#  Show the ID of the selected loco on the panel
		self.setRosterIcon()
		
		self.departureBoard = foggyhollow.departureboard.DepartureBoard("Ace of Spades Mine", "Departures", 30, 322, 4, 44)
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
		listener = self.LocoChangeListener()
		listener.init(self)
		memories.getMemory("Mine Locomotive").addPropertyChangeListener(listener)
		
		self.needBoilerPurge = True
						
		return
	
	#
	#  Get the train number to display on the departure board.  Southbound train uses the locomotive number;
	#  Northbound trains are locomotive number +1.
	def getTrainNumber(self, direction):
		locoids = self.rosterEntry.getId().split()
		if (direction == "NORTH") :
			trainNumber = locoids[0] + " " + str(int(locoids[1]) +1).lstrip("0")	# Strip leading zeros from loco number (used in roster for good sort)			
		else :
			trainNumber = locoids[0] + " " + locoids[1].lstrip("0")	# Strip leading zeros from loco number (used in roster for good sort)			
		return trainNumber
	
	#
	#  Clear the locomotive description from the departure board after the loco has completed service.
	def clearLocomotiveDescription(self):
		self.departureBoard.clearRow(2, True); # stops toggling "Service Loco"		
		return
	
	#
	#  Display the locomotive description on the departure board while the locomotive is being serviced.			
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
		import sys
		try :
			#
			#  Turn the animation switch off to stop any currently running locomotive.  Force reset to BOT next time animation is restarted.
                        #try:
			#        blockList = blocks.getNamedBeanList()
		        #except:
			#        print "Unexpected error in SetRosterIcon getting blockList: ", sys.exc_info()[0], sys.exc_info()[1]	                                
					
			rosterlist = jmri.jmrit.roster.Roster.getDefault().matchingList(None, None, memories.getMemory("Mine Locomotive").getValue(), None, None, None, None)		
			for entry in rosterlist.toArray() :
				print "Roster ", entry.getDccAddress(), " entry.getMfg()= ", entry.getMfg()
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


					#for b in blockList:
					#	if (b.getState() == jmri.Block.OCCUPIED) :
					#		b.setValue(locoid)
					#	else :
					#		b.setValue("")						
							
		except:
			print "Unexpected error in SetRosterIcon: ", sys.exc_info()[0], sys.exc_info()[1]	
		return	
	
	def reset(self):
		import sys
		#
		#  If train is already at the beginning-of-track, just start the train moving forward
		#  Otherwise, we need to find the train.		
		try :		
			if (sensors.provideSensor("BOT").getState() != ACTIVE) :					
				self.reseting = True
				self.currentState = 999
                                self.tripCounter = 0

				self.departureBoard.clearRow(2, True)				
				self.setDepartureBoard(self.getTrainNumber("NORTH"), str(self.trackNumber), "Beginning of Track", "RESET TRAIN LOCATION",  " ", " ", 2)

				self.departureBoard.clearRow(1, False)
				self.departureBoard.clearRow(3, True)	# Wait for last row to clear											
					
				self.resetLights(True)
				self.waitMsec(100)
				self.locomotive.setBrake(False)
				self.waitMsec(100)
				self.locomotive.reverseWhistle()
				self.waitMsec(200)
				
				sensors.provideSensor("Red EOT Lantern").setState(INACTIVE)				
				self.locomotive.changeDirection("Reverse")
				self.locomotive.setSpeed(self.fastSpeed)

		except :
			print "Unexpected error in reset: ", sys.exc_info()[0], sys.exc_info()[1]	
		
		return 0
	
	def stopAnimation(self):
		import sys
		try :
			self.locomotive.setSpeed(self.stopSpeed)
			self.locomotive.changeDirection("Forward")				
			self.locomotive.setFunction("Light", True)  # Turn headlight on
			self.locomotive.setFunction("Bell", False) # Turn bell off
			self.locomotive.throttle.setF2(False) # Turn whistle off				
			#self.steamRelease(0.1) # Turn steam release off
			self.locomotive.setTenderMarkers(True)  # Turn tender lights on
			#self.waterFill(0.1) # Turn water fill off	
			self.locomotive.setCabLight(True) # Turn cab light on
			self.mineCar.setFunction("Light", True)

		except:
			print "Unexpected error in SetRosterIcon: ", sys.exc_info()[0], sys.exc_info()[1]	
							
		sensors.provideSensor("Red EOT Lantern").setState(ACTIVE)
		sensors.provideSensor("IS:DIR").setState(UNKNOWN)	
		
		return					
	#
	# Change the direction of both the locomotive & leading mine car.  
	def changeDirection(self, direction):

		self.reseting = False
		self.locomotive.changeDirection(direction)
		self.mineCar.changeDirection(direction)
	#	if (direction == "Reverse"):
	#		sensors.provideSensor("IS:DIR").setState(INACTIVE)
	#	else :
	#		sensors.provideSensor("IS:DIR").setState(ACTIVE)	
		return 0

	#
	#  Play the sound of the fireman dumping the ashes
	def dumpAshes(self, seconds):
		self.departureBoard.setField("Destination", "Dump Ashes", 3, 0)
		self.waitMsec(2000)
		self.locomotive.dumpAshes(seconds)
		self.departureBoard.clearField("Destination", 3, 0)
	
	#
	#  Play the sound of the fireman blowing out the boiler the specified number of seconds
	def steamRelease(self, seconds):
		self.departureBoard.setField("Destination", "BLOWOUT BOILER", 3, 0)
		self.waitMsec(2000)
		self.locomotive.steamRelease(seconds)
		self.departureBoard.clearField("Destination", 3, 0)
		return 0
	
	#
	#  Randomly blow out the boiler
	def blowoutBoiler(self) :
		import java
		if (java.util.Random().nextInt(100) < 35) :
			self.locomotive.steamRelease(2 + java.util.Random().nextInt(3))
			self.needBoilerPurge = False
		
	#
	#  Play the sound of filling the tender with water for the specified number of seconds.
	def waterFill(self, seconds):
		self.departureBoard.setField("Destination", "FILL TENDER", 3, 0)
		self.waitMsec(2000)
		self.locomotive.waterFill(seconds)
		self.departureBoard.clearField("Destination", 3, 0)		

        #
        #  Let the crew take a coffee break before heading back to the mine
        def coffeeBreak(self, seconds):

                #  Move train forward to EOT
		self.changeDirection("Forward")	
		self.waitMsec(300)
		self.locomotive.setBrake(False)
		self.waitMsec(500)
		self.locomotive.ringBell(True) # Start ringing bell
		self.waitMsec(500)
		self.locomotive.tootWhistle(2)                
		self.waitMsec(3000)			
		self.locomotive.setSpeed(self.creepSpeed);


                # Wait for train to get to EOT
		self.waitSensorActive(sensors.provideSensor("EOT"))
		self.waitMsec(5000)
                
                # Stop the train at EOT
		self.locomotive.setSpeed(self.stopSpeed);
		self.waitMsec(100)
		self.locomotive.tapBrake(2)

		self.waitMsec(100)
		self.locomotive.ringBell(False) # Quit ringing bell		
				
		self.waitMsec(1500)
		self.locomotive.tootWhistle(1)

		self.waitMsec(1500)
		sensors.provideSensor("Red EOT Lantern").setState(INACTIVE)                                        

                # Take a coffee break
                breakString = str(int(round(seconds / 60))) + " MIN COFFEE BREAK"
		self.departureBoard.setField("Destination", breakString, 3, 0)
		secsToDepart = self.postDepartureTime(seconds, 3)

		self.waitMsec(secsToDepart * 1000 )
		self.departureBoard.clearField("Destination", 3, 0)
		self.departureBoard.clearField("Departs", 3, 0)		                                
                

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
		import java
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
		self.locomotive.setFunction("Light", state)  # Turn the light on (in case it went off)
		self.mineCar.setFunction("Light", state)  # Turn the light on (in case it went off)
		self.locomotive.setTenderMarkers(state)  # Turn the tender markers on (in case it went off)	
		return 0
	
	def BOTAction(self):	
		import java

                self.waitMsec(1500)
                
		if (self.currentState == -2 or self.currentState == 999) :
#			print "BOTAction"
			
			# Don't delay 1st time
			if (self.currentState != 999) :
				self.currentState = 1 # do this here to get it done fast before a wagging sensor sends us back here						 					
				#self.throttle.setF8(True) # Mute the sound while we wait

				#self.locomotive.tapBrake(3)
				self.locomotive.emergencyStop()

				self.locomotive.setSpeed(self.stopSpeed)	
				self.resetLights(False)
				self.locomotive.setCabLight(False)	# Turn cab light off
	
				# Hide the direction indicator
				sensors.provideSensor("IS:DIR").setState(UNKNOWN)		
				
				self.reseting = False
				
				#
				#  Delay at BOT
				botDelay = (self.botDelayLong + java.util.Random().nextInt(self.botDelayLong))
				if (sensors.provideSensor("Demo Switch").getState() == ACTIVE) :	
					botDelay = self.botDelayDemo
					
				self.departureBoard.clearRow(2, True)
				self.setDepartureBoard(self.getTrainNumber("SOUTH"), str(self.trackNumber), self.trainName, "ACE OF SPADES #2", "     ", "ON TIME", 2)
				secsToDepart = self.postDepartureTime(botDelay, self.trackNumber-1)
				self.waitMsec(secsToDepart * 1000) #  Still have to wait here to prevent train from moving.
				
			else:
				self.currentState = 1	

				#self.locomotive.tapBrake(4)
				self.locomotive.emergencyStop()

				self.locomotive.setSpeed(self.stopSpeed)
				self.departureBoard.clearRow(2, True)				
				self.setDepartureBoard(self.getTrainNumber("SOUTH"), str(self.trackNumber), self.trainName, "ACE OF SPADES #2", "     ", "ON TIME", 2)				
				self.departureBoard.createRandomRow(0, 0);
				self.departureBoard.createRandomRow(1, 10);			
				
			
			#
			#  Start moving toward the mine	
			if (self.automationSwitch.getState() != ACTIVE)	:
				self.stopAnimation()	
			else:
				#
				#  Possibly delay departure.
				self.checkForDelay()
				
				self.currentState = 1						 					
				self.changeDirection("Forward")
		                sensors.provideSensor("IS:DIR").setState(ACTIVE)
                                
				self.locomotive.setTenderMarkers(True)  # Turn on tender markers
				self.locomotive.setFunction("Light", True)
				self.mineCar.setFunction("Light", True)  # Turn the light on (in case it went off)
				self.locomotive.setBrake(False)
				self.locomotive.setSpeed(self.fastSpeed) # Start moving forward
				self.departureBoard.setField("Status", "DEPARTD", self.trackNumber-1, 4)

                                self.tripCounter = self.tripCounter + 1
		                sensors.provideSensor("IS:SERVICENEEDED").setState(INACTIVE)
		                sensors.provideSensor("IS:SERVICELIGHT").setState(INACTIVE)                                                
			        if (java.util.Random().nextInt(100) < 50 or self.tripCounter == 1) :
                                        sensors.provideSensor("IS:SERVICENEEDED").setState(ACTIVE)
				#
				#  Turn the sound back on...
				#self.throttle.setF8(False)													
				#self.tootWhistle(1)	
		return		
	
	#
	# Tunnel is occupied with southbound train.  No commands to train, just change state.
	def tunnelSouth(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()			
		if (self.currentState == 1) :
			self.currentState = 2	
		return 0
				
	#
	#  Northbound train enters tunnel.  Blow whistle & turn on cab light.
	def tunnelNorth(self):	
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if ((self.currentState == -3) and (not self.reseting)):
			self.currentState = -2
			self.locomotive.setCabLight(True) # Turn the cab light on
			self.waitMsec(500)				
			self.locomotive.longWhistle(1)
			
			#
			#  Wait to get into the tunnel, then slow the locomotive down before we hit the end.
			#  Hopefully, the loco will coast and be quiet before stopping(?)
			self.waitMsec(2000)
			self.locomotive.setSpeed(self.mediumSpeed)			
		return 0		
	
	#
	#  Southbound train enters Bridge-1.  Speed the train to fast.
	def bridge1South(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if ((self.currentState == 2) and (not self.reseting)) :
			self.currentState = 3
			self.resetLights(True)		
			self.locomotive.setSpeed(self.fastSpeed)
			self.locomotive.setCabLight(False) # Turn cab light off
                        
			if (java.util.Random().nextInt(100) < 15) :
				self.locomotive.quillWhistle()

                        
			self.waitMsec(4000)
			self.blowoutBoiler()
		return
	
	#
	#  Northbound train enters Bridge-1.  Turn off bell & cab light and speed up (twice)
	def bridge1North(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if (self.currentState == -4 and (not self.reseting)) :
			self.currentState = -3		
			self.locomotive.setCabLight(False) # Turn cab light off		
			self.locomotive.ringBell(False) # Turn bell off	
			self.resetLights(True)
			
			self.locomotive.setSpeed(self.mediumSpeed)	
					
			self.waitMsec(1500)
			self.locomotive.setSpeed(self.fastSpeed)	
		return 0

	def bridge2South(self):	
		import java
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if (self.currentState == 3 and (not self.reseting) and (self.automationSwitch.getState() == ACTIVE)) :
			self.currentState = 4		
			self.resetLights(True)
			
			if (java.util.Random().nextInt(100) < 70) :
				self.locomotive.longWhistle(1)
			else :
				self.locomotive.tootWhistle(1)
	
			self.locomotive.setSpeed(self.slowSpeed)
			
			self.waitMsec(11000)
			self.locomotive.setSpeed(self.extraSlowSpeed)
		return 0
		
	def bridge2North(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if (self.currentState == -5  and (not self.reseting)) : 
			self.currentState = -4			
			self.locomotive.openCylinderCocks(False)
			self.locomotive.setSpeed(self.slowSpeed)
		return 0
		
	def buildingSouth(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if ((self.currentState == 4)) :		
			self.currentState = 5		
			self.locomotive.ringBell(True)  # Start the bell ringing
			self.resetLights(True)
			self.locomotive.dimLight(True)
			self.locomotive.setSpeed(self.creepSpeed)
			self.departureBoard.setField("Status", "ARRIVED", self.trackNumber-1, 1)							
		return 0
		
	def buildingNorth(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if (self.currentState == 6 ) :
			self.currentState = -5		
			self.locomotive.ringBell(False) # Turn bell after after leaving building
			self.locomotive.setSpeed(self.slowSpeed)
			self.locomotive.dimLight(False)
		return
	
	#
	#  Service locomotive after going through building
	def serviceLocomotive(self):
		import java
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()	

		self.setDepartureBoard(self.getTrainNumber("NORTH"), str(self.trackNumber), "", "SERVICE LOCO", " ", " ", 2)

			
		#
		#  Delay at EOT before backing up to start servicing locomotive		
		delaySeconds = 90 + java.util.Random().nextInt(180)		
		secsToDepart = self.postDepartureTime(delaySeconds, self.trackNumber-1)
		
		self.waitMsec(secsToDepart * 1000) #  Still have to wait here to prevent train from moving.
					
		#
		#  Move the loco backward to service the locomotive
		self.changeDirection("Reverse")	
		self.waitMsec(1000)
		self.locomotive.setBrake(False)
		self.waitMsec(500)
		self.locomotive.ringBell(True) # Start ringing bell
		self.waitMsec(500)
		self.locomotive.reverseWhistle()
		self.waitMsec(3000)			
		self.locomotive.setSpeed(self.extraSlowSpeed);
		self.waitMsec(18000)			
				
		self.locomotive.tapBrake(2)

		self.locomotive.setSpeed(self.stopSpeed);
		
		self.waitMsec(1500)

		sensors.provideSensor("IS:DIR").setState(UNKNOWN)		
		self.locomotive.ringBell(False)  # Stop ringing bell

		self.waitMsec(4000)
		self.locomotive.stopWhistle()
		
		sensors.provideSensor("IS:SERVICENEEDED").setState(INACTIVE)
		sensors.provideSensor("IS:SERVICELIGHT").setState(ACTIVE)                
		
		self.setLocomotiveDescription()

		self.locomotive.setCabLight(True) # Turn the cab light on
		self.waitMsec(30 + java.util.Random().nextInt(5) * 1000)
		
		#
		#  If we didn't blow out the boiler on the way here, do it now.
		if (self.needBoilerPurge) :
			self.steamRelease(8 + java.util.Random().nextInt(10))
			self.waitMsec((30 + java.util.Random().nextInt(5)) * 1000)
		else :
			self.needBoilerPurge = True
			
		self.dumpAshes(20)
		self.waitMsec((30 + java.util.Random().nextInt(5)) * 1000)
		
		
		#
		#  Pull loco forward for water fill
		self.changeDirection("Forward")
		self.locomotive.setBrake(False)
		self.locomotive.tootWhistle(2)
		self.waitMsec(2000)	
		self.locomotive.ringBell(True)
		self.waitMsec(1500)
		self.locomotive.setSpeed(self.extraSlowSpeed)
		#
		#  Move forward and wait in building
		self.waitMsec(14500)	
		self.locomotive.setBrake(True)
		self.waitMsec(1000)
		self.locomotive.setSpeed(self.stopSpeed)	
		self.locomotive.ringBell(False)
		self.waitMsec(1000)
		self.locomotive.tootWhistle(1)

		self.waitMsec(15 + java.util.Random().nextInt(30) * 1000)
		self.waterFill(30)
		self.waitMsec(30 + java.util.Random().nextInt(30) * 1000)
		#
		#  Service complete
		self.clearLocomotiveDescription()
		sensors.provideSensor("IS:SERVICELIGHT").setState(INACTIVE)

		if (self.automationSwitch.getState() == ACTIVE)	:
		        coffeeDelay = (self.coffeeDelayLong + java.util.Random().nextInt(self.coffeeDelayLong))
		        if (sensors.provideSensor("Demo Switch").getState() == ACTIVE) :
		                #coffeeDelay = self.coffeeDelayDemo
                                coffeeDelay = java.util.Random().nextInt(self.coffeeDelayDemo)
                        self.coffeeBreak(coffeeDelay)
                        
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()
		return		
	#
	#  Return northbound to mine after delay at building.	
	def returnToMine(self):	
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()

		sensors.provideSensor("White EOT Lantern").setState(ACTIVE)
                self.waitMsec(500)
                
	        self.locomotive.setLight(True)
                self.waitMsec(500)
		self.changeDirection("Reverse")
		sensors.provideSensor("IS:DIR").setState(INACTIVE)
	        
		self.locomotive.reverseWhistle()

		self.locomotive.setBrake(False)
		self.locomotive.ringBell(True) # Turn bell on
		self.locomotive.openCylinderCocks(True)
		self.locomotive.setSpeed(self.creepSpeed) # Start going back	
		self.waitMsec(3000)			
		self.locomotive.setSpeed(self.extraSlowSpeed) # Start going back
		
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		return;
	#
	# EOTAction		
	def EOTAction(self):
		import java
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()
					
		if ((self.currentState == 5) and (self.automationSwitch.getState() == ACTIVE)) :		
			self.currentState = 6		
			self.resetLights(True)
	
			# Keep going 3 seconds until we are really at the end of track, then stop & toot the whistle	
			self.waitMsec(4000)

			self.locomotive.setSpeed(self.stopSpeed);
			self.waitMsec(100)
			self.locomotive.tapBrake(2)

			self.waitMsec(1000)
			self.locomotive.ringBell(False) # Quit ringing bell		
				
			self.waitMsec(4000)
			self.locomotive.stopWhistle()

                        self.waitMsec(1500)
		        sensors.provideSensor("Red EOT Lantern").setState(INACTIVE)                        



                        
                        
			sensors.provideSensor("IS:DIR").setState(UNKNOWN)			

			#
			#  Service Locomotive when indicated	
                        if (sensors.provideSensor("IS:SERVICENEEDED").getState() == ACTIVE):
				self.serviceLocomotive()
			else :
			        self.waitMsec(1000)                        
                                self.locomotive.setLight(False)
			        
			eotDelay = (self.eotDelayLong + java.util.Random().nextInt(self.eotDelayLong))
			if (sensors.provideSensor("Demo Switch").getState() == ACTIVE) :
				eotDelay = self.eotDelayDemo
			
			self.setDepartureBoard(self.getTrainNumber("NORTH"), str(self.trackNumber), self.trainName,  "DEVIL'S GULCH", "     ", "ON TIME", 2)
			secsToDepart = self.postDepartureTime(eotDelay, self.trackNumber-1)
			# Hide the direction indicator
			sensors.provideSensor("IS:DIR").setState(UNKNOWN)		
			
			#
			#  If departure time is greater than ten minutes, signal train men to return 4 minutes prior
			#  to departure.
			if (secsToDepart > 60*10) :
				self.waitMsec((secsToDepart - 60*4 - 2) * 1000)
				self.locomotive.tootWhistle(4)
				self.waitMsec(60*4*1000)
			else :
				self.waitMsec(secsToDepart*1000)
			
			#
			#  Possibly delay departure.
			self.checkForDelay()
			
			if (self.automationSwitch.getState() == ACTIVE)	:
				self.departureBoard.setField("Status", "DEPARTD", self.trackNumber-1, 3)				
				#
				#  Start going back....
	
				self.returnToMine()
		return	

	#	
	# handle() is called repeatedly until it returns false.
	def handle(self):
		self.waitSensorActive(self.automationSwitch)
		self.waitSensorActive([self.automationSwitch, sensors.provideSensor("BOT")])
		if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("BOT").getState() == ACTIVE) :
			self.BOTAction()
		
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Tunnel")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Tunnel").getState() == ACTIVE) :
				self.tunnelSouth()

		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-1")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Bridge-1").getState() == ACTIVE) :
				#
				#  Only trigger when moving away from the mine
				self.bridge1South()
			
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-2")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Bridge-2").getState() == ACTIVE) :
				self.bridge2South()
						
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Mine Building")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Mine Building").getState() == ACTIVE) :
				self.buildingSouth()

		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("EOT")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("EOT").getState() == ACTIVE) :
				self.EOTAction()

		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Mine Building")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Mine Building").getState() != ACTIVE) :
				self.buildingNorth()		
		
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-2")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Bridge-2").getState() == ACTIVE) :
				self.bridge2North()	
		
		if (not self.reseting):
			self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-1")])
			if (self.automationSwitch.getState() == ACTIVE and sensors.provideSensor("Bridge-1").getState() == ACTIVE) :
				self.bridge1North()
		
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
