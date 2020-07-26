
#
#  Script to shuttle mine train back & forth, turning on various lights, etc. along the way.
from Locomotive import Locomotive
from StopTrainListener import StopTrainListener

import jmri
import jmri.jmrit.roster
import jmri.jmrit.display.panelEditor.configurexml.PanelEditorXml
import jmri.jmrix.AbstractThrottle
import jmri.jmrit.display

from random import randint
import random
import time
import datetime

import java
import sys
sys.path.append("/home/pi/MyJMRI/lib/foggyhollow.jar")

import foggyhollow
import foggyhollow.departureboard.DepartureBoard

#import MineTrackDepartureBoard

from org.apache.log4j import Logger
#import org.slf4j.Logger;

#import org.slf4j.LoggerFactory;

global mine_track_departure_board

class MineTrack(jmri.jmrit.automat.AbstractAutomaton) :

	def init(self) :

                

		import foggyhollow
		import foggyhollow.departureboard.DepartureBoard

		from Locomotive import Locomotive
                from StopTrainListener import StopTrainListener

                from org.apache.log4j import Logger
                
                import random
                import time

                #import MineTrackDepartureBoard
                #global mine_track_departure_board
                
                self.log = Logger.getLogger("jmri.jmrit.jython.exec.MineTrack")
                
		#global throttle

                self.throttle = None
                self.mineCar = None
                self.reseting = True
                self.departureBoardRow = 3
                self.trainName = "HIGH LINE GOPHER"
                departs = time.strftime("%I:%M", time.localtime(time.time()))		                
                self.mineTrain = {"trainNum": "16", "trainName" : "High Line Gopher", "destination" : "Ace of Spades #2", "departs" : departs, "remark": ""}
                
                #
                #  Beginning/End of track delays (in minutes) for demo and non-demo mode.
                self.eotDelayDemo = 3
                self.botDelayDemo = 2

                self.eotDelayLong = 15
                self.botDelayLong = 10

                # Delay between return-to-train signal and departue
                self.returnToTrainDelay = 4
                self.returnToTrainDelayDemo = 1


                self.rosterId = ""
                self.rosterDescription = ""
                
		self.locomotive = Locomotive()
		self.locoAddress = int(memories.getMemory("Mine Locomotive").getValue())		
		self.locomotive.init("Foggy Hollow & Western", self.locoAddress, memories)
		
		self.mineCar = Locomotive()
		self.mineCar.init("Ace of Spades", 6, memories)
		
                self.tripCounter = 0
		self.currentState = 999
		self.automationSwitch = sensors.provideSensor("IS:MTS")	
		#self.automationSwitch.setState(INACTIVE);
		sensors.provideSensor("Demo Switch").setState(INACTIVE)		
		
		#
		#
		self.fastSpeed = 37 	#18	
		self.mediumSpeed = 20 	#16			
		self.slowSpeed = 17      #14
		self.extraSlowSpeed = 12 #12
		self.creepSpeed = 9       #8
                self.stopSpeed = 0
		
		#
		#  Listen for user to turn off the animation switch
		stopTrainListener = StopTrainListener()
		stopTrainListener.init(self.automationSwitch, self)
		self.automationSwitch.addPropertyChangeListener(stopTrainListener)	

		#
		#  Show the ID of the selected loco on the panel
		self.setRosterIcon()

                self.maxDepartures = 3
                self.departureBoard = memories.getMemory("Departure Board").getValue()

                self.departures = []
                
                self.specialTrain = None
                self.specialTrain = self.scheduleSpecialTrain()
                
		self.needBoilerPurge = True

                self.reseting = True
                self.currentState = 999
                self.reset()

                self.setEOTLanternState('Off')

		return

        def setEOTLanternState(self, state) :
                #
                # valid states = 'Off', 'Blue Steady', 'Red Steady', 'Red Swing', 'White Steady, 'White Swing')
                
                sensors.provideSensor("Red EOT Lantern Swinging").setState(INACTIVE)
                sensors.provideSensor("Red EOT Lantern Steady").setState(INACTIVE)
                sensors.provideSensor("White EOT Lantern Swinging").setState(INACTIVE)
                sensors.provideSensor("White EOT Lantern Steady").setState(INACTIVE)
                sensors.provideSensor("Blue EOT Lantern Steady").setState(INACTIVE)
                if (state == 'Red Steady') :
                        sensors.provideSensor("Red EOT Lantern Steady").setState(ACTIVE)
                elif (state == 'Red Swing') :
                        sensors.provideSensor("Red EOT Lantern Swinging").setState(ACTIVE)
                elif (state == 'White Steady') :
                        sensors.provideSensor("White EOT Lantern Steady").setState(ACTIVE)
                elif (state == 'White Swing') :
                        sensors.provideSensor("White EOT Lantern Swinging").setState(ACTIVE)
                elif (state == 'Blue Steady') :
                        sensors.provideSensor("Blue EOT Lantern Steady").setState(ACTIVE)                        

                #
                #  Mimic the state on the 'real' lantern
                if (state.startswith('Red')) :
                        sensors.provideSensor('Red EOT Lantern').setState(ACTIVE)
                        sensors.provideSensor('White EOT Lantern').setState(INACTIVE)                        
                elif (state.startswith('White')) :
                        sensors.provideSensor('White EOT Lantern').setState(ACTIVE)
                        sensors.provideSensor('Red EOT Lantern').setState(INACTIVE)
                elif (state == 'Off') :
                        sensors.provideSensor('White EOT Lantern').setState(INACTIVE)
                        sensors.provideSensor('Red EOT Lantern').setState(INACTIVE)
                        
                return
        
	def setDepartureBoard(self, trainNo, direction, trainName, destination, departTime, status, row):

                if (len(direction) < 1) :
                        direction = " "
                self.departureBoard.setField("Direction", direction[0], row, 0)
                
		self.departureBoard.setField("Train", trainNo, row, 0)
		if (len(destination) > 0 and len(trainName) > 0) :	
			self.departureBoard.setField("Destination", [destination, trainName], row, 0)	
		elif (len(destination) > 0):
			self.departureBoard.setField("Destination", destination, row, 0)
		else :
			self.departureBoard.setField("Destination", trainName, row, 0)
                        
                if (len(departTime) > 0) :
		        self.departureBoard.setField("Departs", departTime, row, 0)

                if (len(status) > 0) :                        
		        self.departureBoard.setField("Status", status, row, 0)
		
		self.waitMsec(int(len(destination)/2 * 1000))
									
	#
	#  Count down the BOT or EOT delay on the GUI.  The delay time is randomized using a Gaussian distribution with
	#  the supplied delay as the mean and 1 sigma...  The delay parameter is in seconds.
	def nixieDelay(self, station, direction, delaySeconds):		
		self.departureBoard.clock("Departs", delaySeconds, self.departureBoardRow, False)
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
		timeStr24 = time.strftime("%H:%M", time.localtime(now + delaySeconds))	# Used to sort by time on departure board			

                #
                # Strip off leading '0' if before 10:00
                if (timeStr.startswith("0")) :
                        temp = list(timeStr)
                        temp[0] = " "
                        timeStr = "".join(temp)                        

		self.departureBoard.setField("Departs", timeStr, row, 0)
                
	        self.mineTrain['departs'] = timeStr
                self.mineTrain['departs_ts'] = timeStr24

		correctedTime = int(   round (((now + float(delaySeconds)) - now) / 60.0)  * 60.0)
		return correctedTime
		
		
	#
	# Check for a delayed departure.  10% of the time delay by 5 minutes + up to 5 more minutes.
	def checkForDelay(self):
                import random
		if ((not self.isDemoMode()) and self.isProbable(10) and (self.tripCounter > 1)) :
			delaySeconds = random.randint(5, 10) * 60
			adjustedDelay = self.postDepartureTime(delaySeconds, self.departureBoardRow)
			self.departureBoard.setField("Status", "DELAYED", self.departureBoardRow, 1)
			self.waitMsec(adjustedDelay*1000)
		return 0
	

        #
        # Returns true if a random mumber falls within the specified probability of occurrence; otherwise returns false
        def isProbable(self, percent) :
                import random
                if (random.randint(1,100) < percent) :
                        return True
                else :
                        return False
                
	#
	#  Get the train number to display on the departure board.  Southbound train uses the locomotive number;
	#  Northbound trains are locomotive number +1.
	def getTrainNumber(self, direction):
		locoids = self.rosterEntry.getId().split()
		if (direction == "NORTH") :
			trainNumber = str(int(locoids[1]) +1).lstrip("0")	# Strip leading zeros from loco number (used in roster for good sort)			
		else :
			trainNumber = locoids[1].lstrip("0")	# Strip leading zeros from loco number (used in roster for good sort)			
		return trainNumber
	
	#
	#  Clear the locomotive description from the departure board after the loco has completed service.
	def clearLocomotiveDescription(self):
		self.departureBoard.clearRow(self.departureBoardRow, True); # stops toggling "Service Loco"		
		return
	
	#
	#  Display the locomotive description on the departure board while the locomotive is being serviced.			
	def setLocomotiveDescription(self):
		locoids = self.rosterEntry.getId().split()
		locoid = locoids[0] + " " + locoids[1].lstrip("0")	# Strip leading zeros from loco number (used in roster for good sort)	
					
		description = locoid + " " + self.rosterEntry.getMfg() + " " + self.rosterEntry.getModel()
		description = description.replace("&", "+").upper()
		self.departureBoard.setField("LocoDescr", description[:44], self.departureBoardRow, 0)	
		
		#self.waitMsec(1500) # Wait for description to get set so track number doesn't get clobbered
		#self.departureBoard.setField("Track", str(self.departureBoardRow), 2, 0)
		return
		
	#
	# Change the locomotive picture on the GUI to use the picture from the Roster for the currently selected locomotive.
	def setRosterIcon(self):
		try :
			#
			#  Turn the animation switch off to stop any currently running locomotive.  Force reset to BOT next time animation is restarted.
                        #try:
			#        blockList = blocks.getNamedBeanList()
		        #except:
			#        print "Unexpected error in SetRosterIcon getting blockList: ", sys.exc_info()[0], sys.exc_info()[1]	                                
					
			rosterlist = jmri.jmrit.roster.Roster.getDefault().matchingList(None, None, memories.getMemory("Mine Locomotive").getValue(), None, None, None, None)		
			for entry in rosterlist.toArray() :
				#print "Roster ", entry.getDccAddress(), " entry.getMfg()= ", entry.getMfg()
				if ((entry.getDecoderFamily().startswith("Tsunami Steam")) or (entry.getDecoderFamily().startswith("WOW Sound")) or len(rosterlist) == 1):
					#memories.getMemory("Roster ID").setValue("FH&W #" + entry.getDccAddress() )
                                        self.rosterId = "FH&W #" + entry.getDccAddress()

					#memories.getMemory("Roster Description 1").setValue(entry.getMfg() + " " + entry.getModel())
                                        self.rosterDescription = entry.getMfg() + " " + entry.getModel()
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
		#
		#  If train is already at the beginning-of-track, just start the train moving forward
		#  Otherwise, we need to find the train.		
		try :		
			self.departureBoard.clearRow(0, False)
			self.departureBoard.clearRow(1, False)
			self.departureBoard.clearRow(2, False)                        
			self.departureBoard.clearRow(3, True)	# Wait for last row to clear											
			if (sensors.provideSensor("BOT").getState() != ACTIVE) :					
				self.reseting = True
				self.currentState = 999
                                self.tripCounter = 0

				self.departureBoard.clearRow(0, True)				
				self.setDepartureBoard(self.getTrainNumber("NORTH"), "N", "Beginning of Track", "RESET TRAIN LOCATION",  " ", " ", 0)

				self.resetLights(True)
				self.waitMsec(100)
				self.locomotive.setBrake(False)
				self.waitMsec(100)
				self.locomotive.reverseWhistle()
				self.waitMsec(200)
				
				self.setEOTLanternState('Off')
				self.locomotive.changeDirection("Reverse")

				slowForTunnel = False
                                if (self.sectionIsActive("Bridge-1") or self.sectionIsActive("Bridge-2") or self.sectionIsActive("Mine Building")) :
                                        slowForTunnel = True
                                        
                                if (self.sectionIsActive("Bridge-2") or self.sectionIsActive("Mine Building")) :
                                        speed = self.fastSpeed
                                else :
                                        speed = self.mediumSpeed-2

                                
				self.locomotive.setSpeed(speed)

                                if (slowForTunnel) :
		                        self.waitSensorActive(sensors.provideSensor("Bridge-1"))
                                        self.locomotive.changeSpeed(self.mediumSpeed-2, 5)
                                

                                

		except :
			print "Unexpected error in reset: ", sys.exc_info()[0], sys.exc_info()[1]
	                self.log.error("Unexpected error in MineTrack.reset")
		
		return 0

        def sectionIsActive(self, sectionName) :
                return (sensors.provideSensor(sectionName).getState() == ACTIVE)
        
	def stopAnimation(self):
		try :
			self.locomotive.setSpeed(self.stopSpeed)
			self.locomotive.changeDirection("Forward")				
			self.locomotive.setFunction("Light", True)  # Turn headlight on
			self.locomotive.setFunction("Bell", False) # Turn bell off
			self.locomotive.throttle.setF2(False) # Turn whistle off				
			self.locomotive.setFunction("SteamRelease", False) # Turn steam release off
			self.locomotive.setTenderMarkers(True)  # Turn tender lights on
			self.locomotive.setFunction("WaterFill", False) # Turn water fill off	
			self.locomotive.setCabLight(True) # Turn cab light on
			self.mineCar.setFunction("Light", True)

		except:
			print "Unexpected error in SetRosterIcon: ", sys.exc_info()[0], sys.exc_info()[1]	

                self.setEOTLanternState('Red Steady')
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
		#self.departureBoard.setField("Destination", "Dump Ashes", 3, 0)
                memories.getMemory("Service 2").setValue("Dump Ashes");
		self.waitMsec(2000)
		self.locomotive.dumpAshes(seconds)
		#self.departureBoard.clearField("Destination", 3, 0)
	
	#
	#  Play the sound of the fireman blowing out the boiler the specified number of seconds
	def steamRelease(self, seconds):
		#self.departureBoard.setField("Destination", "BLOWOUT BOILER", 3, 0)
                memories.getMemory("Service 1").setValue("Blowout Boiler");                
		self.waitMsec(2000)
		self.locomotive.steamRelease(seconds)
		#self.departureBoard.clearField("Destination", 3, 0)
		return 0

	#
	#  Randomly blow out the boiler
	def blowoutBoiler(self) :
                import random                
                if (self.isProbable(35)) :
			self.locomotive.steamRelease(random.randint(2, 6))
			self.needBoilerPurge = False
		
	#
	#  Play the sound of filling the tender with water for the specified number of seconds.
	def waterFill(self, seconds):
		#self.departureBoard.setField("Destination", "FILL TENDER", 3, 0)
                memories.getMemory("Service 3").setValue("Fill Tender");                
		self.waitMsec(2000)
		self.locomotive.waterFill(seconds)
		#self.departureBoard.clearField("Destination", 3, 0)		


        #
        #  After servicing locomotive, move to EOT
        def moveToEOT(self):

                #  Move train forward to EOT
                self.setEOTLanternState('White Swing')
                
		self.changeDirection("Forward")	
		self.waitMsec(300)
		self.locomotive.setBrake(False)
		self.waitMsec(500)
		self.locomotive.ringBell(True) # Start ringing bell
		self.waitMsec(500)
		self.locomotive.tootWhistle(2)                
		self.waitMsec(3000)			
		self.locomotive.setSpeed(self.extraSlowSpeed);


                # Wait for train to get to EOT
		self.waitSensorActive(sensors.provideSensor("EOT"))
                self.setEOTLanternState('Red Swing')                
		self.waitMsec(5000)
                
                # Stop the train at EOT
		self.locomotive.setSpeed(self.stopSpeed);
		self.waitMsec(100)
		self.locomotive.tapBrake(2)
                self.setEOTLanternState('Red Steady')                                

		self.waitMsec(100)
		self.locomotive.ringBell(False) # Quit ringing bell		
				
		self.waitMsec(1500)
		self.locomotive.tootWhistle(1)

		self.waitMsec(1500)
                self.setEOTLanternState('Off')

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
	
	#
	#  Set the locomotive/mine car lights to the specified state.  Called at block transitions to restore lights if lost due to dirty track.
	def resetLights(self, state):
		self.locomotive.setFunction("Light", state)  # Turn the light on (in case it went off)
		self.mineCar.setFunction("Light", state)  # Turn the light on (in case it went off)
		self.locomotive.setTenderMarkers(state)  # Turn the tender markers on (in case it went off)	
		return 0

        #
        #  Convenience to return true/false if demo switch is active
        def isDemoMode(self) :
                return (sensors.provideSensor("Demo Switch").getState() == ACTIVE)                

        #
        #  Handle Beginning of Track activity
	def BOTAction(self):
                import random	        
                self.waitMsec(750)


		if (self.currentState == -2 or self.currentState == 999) :
			# Don't delay 1st time
			if (self.currentState != 999) :
				self.currentState = 1 # do this here to get it done fast before a wagging sensor sends us back here						 					
				#self.locomotive.setMute(True) # Mute the sound while we wait

				#self.locomotive.tapBrake(3)
                                self.locomotive.setLight(False)
				self.locomotive.emergencyStop()

				self.locomotive.setSpeed(self.stopSpeed)
                                
				self.resetLights(False)
				self.locomotive.setCabLight(False)	# Turn cab light off
	
				# Hide the direction indicator
				sensors.provideSensor("IS:DIR").setState(UNKNOWN)		
				
				self.reseting = False
				
				#
				#  Delay at BOT
				botDelay = (random.randint(self.botDelayLong, self.botDelayLong*2))
				if (self.isDemoMode()) :	
					botDelay = self.botDelayDemo


					
				#self.departureBoard.clearRow(self.departureBoardRow, True)
				#self.setDepartureBoard(self.getTrainNumber("SOUTH"), "S", self.trainName, "ACE OF SPADES #2", "     ", "ON TIME", self.departureBoardRow)
				#secsToDepart = self.postDepartureTime(botDelay*60, self.departureBoardRow)

                                secsToDepart = self.initDepartures()
                                
				self.waitMsec(secsToDepart * 1000) #  Still have to wait here to prevent train from moving.
				
			else: # currentState = 999 -> Reset
				self.currentState = 1	

				#self.locomotive.tapBrake(4)
				self.locomotive.emergencyStop()

				self.locomotive.setSpeed(self.stopSpeed)
                                self.initDepartures()                                                                        

				self.setDepartureBoard(self.getTrainNumber("SOUTH"),  "S", self.trainName, "ACE OF SPADES #2", "     ", "ON TIME", self.departureBoardRow)
				secsToDepart = self.postDepartureTime(0, self.departureBoardRow)                                                                
			
			#
			#  Start moving toward the mine	
			if (self.automationSwitch.getState() != ACTIVE)	:
				self.stopAnimation()	
			else:
				#
				#  Possibly delay departure.
				self.checkForDelay()
				
				self.currentState = 1


                                self.tripCounter = self.tripCounter + 1
		                sensors.provideSensor("IS:SERVICENEEDED").setState(INACTIVE)
		                sensors.provideSensor("IS:SERVICELIGHT").setState(INACTIVE)                                                
			        if (self.isProbable(50) or self.tripCounter == 1) :
                                        sensors.provideSensor("IS:SERVICENEEDED").setState(ACTIVE)
                                        self.waitMsec(2000)
                                        memories.getMemory("Roster ID").setValue(self.rosterId)
                                        memories.getMemory("Roster Description 1").setValue(self.rosterDescription)                                                                                                                        

                                
				self.changeDirection("Forward")
		                sensors.provideSensor("IS:DIR").setState(ACTIVE)
                                
				self.locomotive.setTenderMarkers(True)  # Turn on tender markers
				self.locomotive.setFunction("Light", True)
				self.mineCar.setFunction("Light", True)  # Turn the light on (in case it went off)
				self.locomotive.setBrake(False)
				self.locomotive.changeSpeed(self.fastSpeed, 10) # Start moving forward

				#secsToDepart = self.postDepartureTime(0, self.departureBoardRow-1)                                
				self.departureBoard.setField("Status", "DEPARTED", self.departureBoardRow, 4)

				#
				#  Turn the sound back on...
				#self.locomotive.setMute(False)													
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

			if (self.isProbable(70)) :
				self.locomotive.longWhistle(1)
			else :
				self.locomotive.tootWhistle(1)                        
			
			#
			#  Wait to get into the tunnel, then slow the locomotive down before we hit the end.
			#  Hopefully, the loco will coast and be quiet before stopping(?)
			#self.waitMsec(2000)
			#self.locomotive.setSpeed(self.slowSpeed)			
		return 0		
	
	#
	#  Southbound train enters Bridge-1.  Speed the train to fast.
	def bridge1South(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if ((self.currentState == 2) and (not self.reseting)) :
			self.currentState = 3
			self.resetLights(True)		
			self.locomotive.setCabLight(False) # Turn cab light off
                        
			if (self.isProbable(15)) :
				self.locomotive.longWhistle(1)

                        
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

			self.locomotive.changeSpeed(self.mediumSpeed, 4)
	                self.locomotive.tapBrake(1)                        
		return 0

	def bridge2South(self):	
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if (self.currentState == 3 and (not self.reseting) and (self.automationSwitch.getState() == ACTIVE)) :
			self.currentState = 4		
			self.resetLights(True)
			
			if (self.isProbable(70)) :
				self.locomotive.longWhistle(1)
			else :
				self.locomotive.tootWhistle(1)

                        self.locomotive.changeSpeed(self.slowSpeed, 22)

		return 0
		
	def bridge2North(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if (self.currentState == -5  and (not self.reseting)) : 
			self.currentState = -4
                        self.locomotive.changeSpeed(self.fastSpeed-4, 5)
                        self.waitMsec(4000)
			self.locomotive.openCylinderCocks(False)
                                                

		return 0
		
	def buildingSouth(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if ((self.currentState == 4)) :		
			self.currentState = 5		
			self.locomotive.ringBell(True)  # Start the bell ringing
			self.resetLights(True)
			self.locomotive.dimLight(True)
			self.locomotive.changeSpeed(self.extraSlowSpeed, 2)
			self.departureBoard.setField("Status", "ARRIVED", self.departureBoardRow, 1)							
		return 0
		
	def buildingNorth(self):
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		if (self.currentState == 6 ) :
			self.currentState = -5		
			self.locomotive.ringBell(False) # Turn bell after after leaving building
			self.locomotive.changeSpeed(self.mediumSpeed, 3)
			self.locomotive.dimLight(False)
		return
	
	#
	#  Service locomotive after going through building
	def serviceLocomotive(self):
                import random                
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()	

		self.setDepartureBoard(self.getTrainNumber("NORTH"), "", "", "SERVICE LOCOMOTIVE", " ", " ", self.departureBoardRow)

		self.waitMsec(2000) # Try to wait to get Service Loco message to stabilize ?????
		#
		#  Delay at EOT before backing up to start servicing locomotive		
		delaySeconds = random.randint(90, 270)
		if (self.isDemoMode()) :
		        delaySeconds = random.randint(30, 120)
		secsToDepart = self.postDepartureTime(delaySeconds, self.departureBoardRow)
		
		self.waitMsec(secsToDepart * 1000) #  Still have to wait here to prevent train from moving.
					
		#
		#  Move the loco backward to service the locomotive
                self.setEOTLanternState('White Swing')
		self.changeDirection("Reverse")	
		self.waitMsec(1000)
		self.locomotive.setBrake(False)
		self.waitMsec(500)
		self.locomotive.ringBell(True) # Start ringing bell
		self.waitMsec(500)
		self.locomotive.reverseWhistle()
		self.waitMsec(3000)			
		self.locomotive.setSpeed(self.slowSpeed);

		self.waitMsec(17000)
                self.setEOTLanternState('Off')
                
		self.locomotive.tapBrake(2)

		self.locomotive.setSpeed(self.stopSpeed);
		
		self.waitMsec(1500)

		sensors.provideSensor("IS:DIR").setState(UNKNOWN)		
		self.locomotive.ringBell(False)  # Stop ringing bell

		self.waitMsec(4000)
		self.locomotive.stopWhistle()

		self.waitMsec(5000)
                
		sensors.provideSensor("IS:SERVICENEEDED").setState(INACTIVE)
		sensors.provideSensor("IS:SERVICELIGHT").setState(ACTIVE)                
		self.setEOTLanternState("Blue Steady")
                
		#self.setLocomotiveDescription()

		self.locomotive.setCabLight(True) # Turn the cab light on
		self.waitMsec(random.randint(30, 45) * 1000)
		
		#
		#  If we didn't blow out the boiler on the way here, do it now.
		if (self.needBoilerPurge) :
			self.steamRelease(random.randint(8, 20))
			self.waitMsec(random.randint(20,40) * 1000)
		else :
			self.needBoilerPurge = True
			
		self.dumpAshes(20)
		self.waitMsec(random.randint(30, 45) * 1000)
		
		
		#
		#  Pull loco forward for water fill
		self.changeDirection("Forward")
		self.locomotive.setBrake(False)
		self.locomotive.tootWhistle(2)
		self.waitMsec(2000)	
		self.locomotive.ringBell(True)
		self.waitMsec(1500)
		self.locomotive.setSpeed(self.slowSpeed)

		#
		#  Move forward and wait in building
		self.waitMsec(14500)	
		self.locomotive.setBrake(True)
		self.waitMsec(1000)
		self.locomotive.setSpeed(self.stopSpeed)	
		self.locomotive.ringBell(False)
		self.waitMsec(1000)
		self.locomotive.tootWhistle(1)

                self.waitMsec(random.randint(15, 45) * 1000)
		self.waterFill(30)
                self.waitMsec(random.randint(30, 90) * 1000)
		#
		#  Service complete
		#self.clearLocomotiveDescription()
		sensors.provideSensor("IS:SERVICELIGHT").setState(INACTIVE)
                self.setEOTLanternState('Off')
                
		memories.getMemory("Roster ID").setValue("")
		memories.getMemory("Roster Description 1").setValue("")                
                self.waitMsec(300)                
                memories.getMemory("Service 1").setValue("");
                self.waitMsec(300)                
                memories.getMemory("Service 2").setValue("");
                self.waitMsec(300)                
                memories.getMemory("Service 3").setValue("");                                
                self.moveToEOT()
                
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()
		return		
	#
	#  Return northbound to mine after delay at building.	
	def returnToMine(self):	
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()

                self.setEOTLanternState('White Swing')

                self.waitMsec(500)
                
	        self.locomotive.setLight(True)
                self.waitMsec(500)
		self.changeDirection("Reverse")
		sensors.provideSensor("IS:DIR").setState(INACTIVE)
	        
		self.locomotive.reverseWhistle()

		self.locomotive.setBrake(False)
		self.locomotive.ringBell(True) # Turn bell on
		self.locomotive.openCylinderCocks(True)
		self.locomotive.setSpeed(self.extraSlowSpeed) # Start going back	
		self.waitMsec(3000)
                
		self.departureBoard.setField("Status", "DEPARTED", self.departureBoardRow, 3)
                self.setEOTLanternState('Off')		
		if (self.automationSwitch.getState() != ACTIVE)	:
			self.stopAnimation()		
		return;
	#
	# EOTAction		
	def EOTAction(self):
                import random                
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
                        self.setEOTLanternState('Red Steady')
			sensors.provideSensor("IS:DIR").setState(UNKNOWN)			

			#
			#  Service Locomotive when indicated	
                        if (sensors.provideSensor("IS:SERVICENEEDED").getState() == ACTIVE):
				self.serviceLocomotive()
			else :
			        self.waitMsec(1000)                        
                                self.locomotive.setLight(False)
			        
                        #
                        #  Wait at EOT before returning...
                        returnToTrainMins = self.returnToTrainDelay
		        if (self.isDemoMode()) :
                                returnToTrainMins = self.returnToTrainDelayDemo

                        # Set the EOT delay (in seconds) based on the demo switch
                        minDelay = returnToTrainMins + 2
                        eotDelayMin = random.randint(minDelay, self.eotDelayLong)
			if (self.isDemoMode()) :
			        eotDelayMin = random.randint(minDelay, self.eotDelayDemo)

                        #
                        #  Sometimes the EOT delay is a coffee break....
                        if (self.isProbable(65) or self.tripCounter == 1) :
                                # Take a coffee break
                                breakString = "Back in " + str(eotDelayMin - returnToTrainMins) + " minutes"
                                memories.getMemory("Service 1").setValue("Taking a coffee break");
                                memories.getMemory("Service 2").setValue(breakString);
                                self.setEOTLanternState('Off')
                                
                        self.setDepartureBoard(self.getTrainNumber("NORTH"), "N", self.trainName,  "DEVIL'S GULCH", "", "ON TIME", self.departureBoardRow)                                
			secsToDepart = self.postDepartureTime(eotDelayMin*60, self.departureBoardRow)                                
			self.waitMsec((secsToDepart - returnToTrainMins*60) * 1000)

                        #
                        #  Clear coffee break message
                        memories.getMemory("Service 1").setValue("");
                        memories.getMemory("Service 2").setValue("");                                                                                
			self.waitMsec(random.randint(10,20) * 1000)	                

			#
			#  Signal train men to return 4 minutes prior to departure.
			self.locomotive.tootWhistle(4)

			self.waitMsec(60*returnToTrainMins*1000)
			
			#
			#  Possibly delay departure.
			self.checkForDelay()
			
			if (self.automationSwitch.getState() == ACTIVE)	:
				#
				#  Start going back....
				self.returnToMine()
		return



        #
        #  Convert a time in the form HH:MM AM to 24-hour time: HH:MM
        def convert24(self, str1):

            if str1[-2:] == "AM" and str1[:2] == "12": 
                return "00" + str1[2:-2] 

            elif str1[-2:] == "AM": 
                return str1[:-2] 

            elif str1[-2:] == "PM" and str1[:2] == "12": 
                return str1[:-2] 

            else: 
                return (str(int(str1[:2]) + 12) + str1[2:5]).strip()

        #
        #  Get today's trains from the (already initialized) JMRI memories that were retreived from the common timetable database.
        #  Build an array of 'dictionary' items so we can sort the array by departure time.  We keep both 12hr and 24hr departure
        #  times to make the sorting work.
        #
        #  We also create a dictionary entry for the mine train and add it to the array.  It will be sorted along with the other trains.
        #
        #  If any of today's trains have not departed yet, we keep the 2 closest to departure time; otherwise we keep the 2 most recently departed trains.
        #
        #  Since the mine train can move up & down in the list based on departure times, we set the self.departureBoardRow 
        #
        def initDepartures(self):

                from operator import itemgetter
                from foggyhollow.timetable import TimeTable
                from foggyhollow.timetable import TimetableEntry
                import datetime
                import time

                currentTime = datetime.datetime.now()
                today = datetime.datetime.strftime(currentTime, '%b %d %Y')
                dom = datetime.datetime.strftime(currentTime, '%A - %B %d')
                memories.getMemory("IM:DOM").setValue(dom)


                #
                #  Get all of today's trains from the timetable
                r = 1
                tempDepartures = []
                self.departures = []

                timetableIpAddress = memories.getMemory("Timetable IP Address").getValue()
                if (len(timetableIpAddress) < 18) :
                        timetableIpAddress = "192.168.1.2:3306" # Default to PlexRaspberry MySQL server
                        
                timeTable = TimeTable(str(timetableIpAddress))
                todaysDepartures = timeTable.getTodaysDepartures("Beaver Bend")
                for train in todaysDepartures :
                        trainNum = str(train.getTrainNumber())
                        trainName = str(train.getTrainName())
                        trainType = train.getTrainType()
                        if (trainType == "S" or trainType == "X") :
                                trainNum = "X" + trainNum
                        destination = str(train.getDestination())
                        direction = str(train.getDirection())
                        departs = str(train.getScheduleTime12())
                        departs_ts = str(train.getScheduleTime24())
                        remark = ""

                        #
                        #  Check if the current time is after the scheduled departure time.  If so,
                        #  set the remark field
                        if (len(departs) > 0) :
                                departStr = today + " " + departs                                
                                departTime = datetime.datetime.strptime(departStr, '%b %d %Y %I:%M %p')
                                minutesAgo = currentTime - datetime.timedelta(minutes=2)
                                if (departTime <= currentTime) :
                                        remark = "DEPARTED"
                                elif ((departTime > minutesAgo) and (departTime < currentTime)) :
                                        remark = "ARRIVED"
                        

                        #
                        #  Trim leading "0" off departure hours < "10"
                        if (departs.startswith("0")) :
                                temp = list(departs)
                                temp[0] = " "
                                departs = "".join(temp)


                        trainDict = {"trainNum": trainNum, "direction" : direction, "trainName" : trainName, "destination" : destination, "departs" : departs[0:-3], "departs_ts" : departs_ts, "remark": remark}
                        tempDepartures.append(trainDict)
                        

                #
                #  I only want to keep 'maxDepartures' trains....either the most recently departed
                try :
                        #if (len(tempDepartures) > self.maxDepartures) :
                        for t in tempDepartures:
                                if (len(t['remark']) < 2) : #  Train hasn't departed....keep it
                                        self.departures.append(t)
                                        if (len(self.departures) == self.maxDepartures):
                                                break
                except :
                        print " "
                        print "*** Unexpected error in initDepartures trimming departures: " , sys.exc_info()[0], sys.exc_info()[1]
                        for t in tempDepartures :
                                print t['trainNum'] + " ts: |" + t['departs_ts'] + "| departs: |" + t['departs'] + "|"
                        print " "
                #
                #  If we didn't find 'maxDepartures' trains that haven't departed yet, get trains from the end of the temp list...

                numFound = len(self.departures)
                if (numFound < self.maxDepartures):
                        for t in reversed(tempDepartures) :
                                if (len(t['remark']) > 0) :
                                        self.departures.append(t)                                        
                                if (len(self.departures) == self.maxDepartures):
                                        break                                



                #
                #  Add in the mine train

		now = time.time()

                delaySeconds = self.botDelayLong * 60                
                if (self.isDemoMode()) :
                        delaySeconds = self.botDelayDemo * 60
                if (self.currentState == 999) :
                        delaySeconds = 0
		departs = time.strftime("%I:%M", time.localtime(now + delaySeconds))
		departs_ts = time.strftime("%H:%M", time.localtime(now + delaySeconds)).strip()
                mineTrainDeparts = delaySeconds
                
                if (departs.startswith("0")) :
                        temp = list(departs)
                        temp[0] = " "
                        departs = "".join(temp)

                
                mineTrain = {"trainNum": "16", "direction" : "S", "trainName" : "High Line Gopher", "destination" : "Ace of Spades #2", "departs" : departs, "departs_ts" : departs_ts, "remark": ""}
                self.departures.append(mineTrain)

                #
                # If it's a slow day, add a special train
                if (len(self.departures) < 2) :
                        departs = self.specialTrain['departs_ts']
                        if (len(departs) > 0) :
                                departStr = today + " " + departs                                
                                departTime = datetime.datetime.strptime(departStr, '%b %d %Y %H:%M')
                                minutesAgo = currentTime - datetime.timedelta(minutes=2)
                                remark = ""
                                if (departTime <= currentTime) :
                                        remark = "DEPARTED"
                                elif ((departTime > minutesAgo) and (departTime < currentTime)) :
                                        remark = "ARRIVED"
                                self.specialTrain['remark'] = remark
                        
                        self.departures.append(self.specialTrain)

                #
                #  With the mine train added in, sort the departures again so the mine train get positioned correctly
                sortedTrains = sorted(self.departures, key=itemgetter('departs_ts'))

                #
                #  Determine which row the mine train is on after sorting
                r = 0
                for t in sortedTrains: 
                        if t['trainNum'] == "16": 
                                #mineTrain = t 
                                break
                        r = r + 1
                self.departureBoardRow = r

                row = 0;
                for train in sortedTrains:
                        self.departureBoard.clearRow(row, True)
                        self.setDepartureBoard (train['trainNum'], str(train['direction'])[0],  train['trainName'], train['destination'], train['departs'], train['remark'], row)
                        row = row + 1
                        if (row > self.maxDepartures):
                                break
                        
                return mineTrainDeparts
                

        #
        #  Schedule special train that may or may not appear.  Special trains happen on days when there are few trains from the timetable.  We
        #  create the special train during init so it remains on the schedule throughout the runs of the mine train.
        #
        def scheduleSpecialTrain (self):

                import random
                import time

                train = None

                randomDestinations = ['Faun Glen', 'Empire', 'Devil\'s Gulch', 'Mystic Springs', 'Satyr\'s Glade', 'Fall River']
                randomTrains = ['Fierce Sparrow', 'Track Maintenance', 'Water Service', 'Freight Extra', 'Private Excursion']

                now = time.time()

                direction = "East"
                remark = ""

                trainNum = 16
                while (trainNum == 16 or trainNum == 17) :
                        trainNum = random.randint(30,88)

                #
                #  We only want 10% of the special trains to be westbound.  If we randomly generated a westbound train,
                #  increment the train number to get an eastbound train
                if ((trainNum % 2) != 0) :
                        if (random.randint(0, 100) > 10) :
                                trainNum = trainNum + 1
                        
                if ((trainNum % 2) != 0) :
                        direction = "West"
                trainName = randomTrains[random.randint(0,4)]
                destination = "Mystic Springs"
                if (direction == "East") :
                        destination = randomDestinations[random.randint(0,5)]

                delaySeconds = random.randint(5, 180) * 60
                offset = now + delaySeconds

                departs = time.strftime("%I:%M", time.localtime(offset))
                departs_ts = time.strftime("%H:%M", time.localtime(offset))


                if (str(departs).startswith('0')) :
                        temp = list(departs)
                        temp[0] = " "
                        departs = "".join(temp)

                specialTrainNum = "X" + str(trainNum)
                train = {"trainNum": specialTrainNum, "direction" : direction, "trainName" : trainName, "destination" : destination, "departs" : departs, "departs_ts" : departs_ts, "remark": remark}                


                return train
                        
	#	
	# handle() is called repeatedly until it returns false.
	def handle(self):
                try :
                        self.waitSensorActive(self.automationSwitch)


                        self.waitSensorActive([self.automationSwitch, sensors.provideSensor("BOT")])
                        if (self.automationSwitch.getState() == ACTIVE and self.sectionIsActive("BOT")) :
                                self.BOTAction()

                        if (not self.reseting):
                                self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Tunnel")])
                                if (self.automationSwitch.getState() == ACTIVE and self.sectionIsActive("Tunnel")) :
                                        self.tunnelSouth()

                        if (not self.reseting):
                                self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-1")])
                                if (self.automationSwitch.getState() == ACTIVE and self.sectionIsActive("Bridge-1")) :
                                        #
                                        #  Only trigger when moving away from the mine
                                        self.bridge1South()                                

                        if (not self.reseting):
                                self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-2")])
                                if (self.automationSwitch.getState() == ACTIVE and self.sectionIsActive("Bridge-2")) :
                                        self.bridge2South()

                        if (not self.reseting):
                                self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Mine Building")])
                                if (self.automationSwitch.getState() == ACTIVE and self.sectionIsActive("Mine Building")) :
                                        self.buildingSouth()

                        if (not self.reseting):
                                self.waitSensorActive([self.automationSwitch, sensors.provideSensor("EOT")])
                                if (self.automationSwitch.getState() == ACTIVE and self.sectionIsActive("EOT")) :
                                        self.EOTAction()

                        if (not self.reseting):
                                self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Mine Building")])
                                if (self.automationSwitch.getState() == ACTIVE and not self.sectionIsActive("Mine Building")) :
                                        self.buildingNorth()		

                        if (not self.reseting):
                                self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-2")])
                                if (self.automationSwitch.getState() == ACTIVE and self.sectionIsActive("Bridge-2")) :
                                        self.bridge2North()	

                        if (not self.reseting):
                                self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Bridge-1")])
                                if (self.automationSwitch.getState() == ACTIVE and self.sectionIsActive("Bridge-1")) :
                                        self.bridge1North()

                        if (not self.reseting):
                                self.waitSensorActive([self.automationSwitch, sensors.provideSensor("Tunnel")])
                                if (self.automationSwitch.getState() == ACTIVE and self.sectionIsActive("Tunnel")) :
                                        self.tunnelNorth()		

                        self.waitMsec(500)

                        return 1
                except :
                        self.locomotive.emergencyStop()
			print "Unexpected error in MineTrack!handle: ", sys.exc_info()[0], sys.exc_info()[1]	                        
						

                return
        
	
# end of class definition
	
# create one of these
main = MineTrack()

# set the name, as a example of configuring it
main.setName("Automated Beaver Bend Mine Track")

# and start it running
main.start()
