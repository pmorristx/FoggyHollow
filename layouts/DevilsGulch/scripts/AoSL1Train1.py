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
from jmri import InstanceManager
from jmri import TransitManager
from jmri import Section

class AoSL1Train1(jmri.jmrit.automat.AbstractAutomaton) :

	def init(self):
		# init() is called exactly once at the beginning to do
		# any necessary configuration.
		print "Inside init(self)"

		# set up sensor numbers
		# fwdSensor is reached when loco is running forward


		
		
		self.tippleSensor = sensors.provideSensor("OS:L1:Tipple")
		self.leftTunnelSensor = sensors.provideSensor("OS:L1:Left Tunnel")
		self.frontTunnelSensor = sensors.provideSensor("OS:L1:Front Tunnel")
		self.rightTunnelSensor = sensors.provideSensor("OS:L1:Right Tunnel")
		self.backTunnelSensor = sensors.provideSensor("OS:L1:Back Tunnel")
		self.backCavernSensor = sensors.provideSensor("OS:L1:Back Cavern")
		self.hoistCavernSensor = sensors.provideSensor("OS:L1:Hoist Cavern Entrance")
		
		self.blockSensors = []
		self.blockSensors.append(self.tippleSensor)
		self.blockSensors.append(self.rightTunnelSensor)
		self.blockSensors.append(self.backCavernSensor)
		self.blockSensors.append(self.backTunnelSensor)	
		self.blockSensors.append(self.leftTunnelSensor)	
		self.blockSensors.append(self.hoistCavernSensor)
		self.blockSensors.append(self.frontTunnelSensor)
		
		self.automateSensor = sensors.provideSensor("L1 Auto")

		self.tippleLights = sensors.provideSensor("Tipple Lights")
		self.bridgeLights = sensors.provideSensor("Lake Cavern Bridge")

		# get loco address. For long address change "False" to "True" 
		self.throttle = self.getThrottle(4, False)  # short address 14
		
		self.currentBlockNum = 0
		
		self.moveTrainToStartSection()


		self.currentSequence = 1
		self.transitManager = InstanceManager.transitManagerInstance()
		self.transit = self.transitManager.getBySystemName("IZ1")		
		self.tsections = self.transit.getTransitSectionList()
		for tsection in self.tsections :
		#	print tsection.getSectionName()
			sequenceNumber = tsection.getSequenceNumber()
			print "Occupancy: " + str(tsection.getSection().getOccupancy())
			print "State: " + str(tsection.getSection().getState())	# FREE or OCCUPIED		                        
			if (tsection.getSection().getOccupancy() == jmri.Section.OCCUPIED):
				self.currentSection = tsection.getSection()
                                print "Train found in sequence: " + str(sequenceNumber) + " Section: " + str(tsection.getSection().getUserName())
		#	print "Direction: " + str(tsection.getDirection())

			nextSequence = (tsection.getSequenceNumber() +1) % self.transit.getMaxSequence()
                        print "Section: Username: " + str(tsection.getSection().getUserName()) + " SystemName: " + str(tsection.getSection().getSystemName())                        
			if (nextSequence == 0):
				nextSequence = 1
		#	print "Next Sequence: " + str(nextSequence)
			self.nextSection = self.transit.getSectionListBySeq(nextSequence)[0]
		#	print "NextSection: " + self.nextSection.getUserName()
					
			masts = self.nextSection.getUserName().split(":")
			thisMastName = masts[0];
			nextMastName = masts[1]
		#	print "Next mast: " + nextMastName
			nextMast = InstanceManager.signalMastManagerInstance().getByUserName(masts[1])
		#	print "Next signal aspect"  + str(nextMast.getAspect())                

		print "Current aspect: " + str(self.getCurrentAspect())                                
		return
	
	def getCurrentAspect(self):
			masts = self.currentSection.getUserName().split(":")
			thisMastName = masts[0];
			nextMastName = masts[1]
			thisMast = InstanceManager.signalMastManagerInstance().getByUserName(masts[0])
		#	print "Next signal aspect "  + str(thisMast.getAspect()) + " Mast: " + masts[0]		
			return thisMast.getAspect()
	# Move train to the tipple
	def moveTrainToStartSection(self):
		self.throttle.setIsForward(True)
		self.moveTrain()
		self.waitSensorActive(self.tippleSensor);
		self.stopTrain()
                print "Train initial stopped at tipple"

		
	def getNextBlockSensor(self):
                print "Current Section: " + self.currentSection.getUserName()
                print "Entry Block: " + self.currentSection.getExitBlock().getUserName()
                print "Next Sensor: " + self.currentSection.getExitBlock().getSensor().getUserName()
		nextBlockSensor = self.currentSection.getEntryBlock().getSensor()
                return nextBlockSensor
		
	def moveTrain(self):
		self.throttle.setSpeedSetting(0.4)
		self.throttle.setF0(True)
		
	def stopTrain(self):
		self.throttle.setSpeedSetting(0.0)
		self.throttle.setF0(False)		

	def handle(self):
		# handle() is called repeatedly until it returns false.
#		print "Inside handle(self)"
		
		#
		#  If next block is vacant, move train forward
		aspect = self.getCurrentAspect()
		if (aspect == "Clear" or aspect == "Approach"):
			print "moving train"
			self.moveTrain()
			#  Wait for train to get to next block
			sensor = self.getNextBlockSensor()
			print "Waiting for sensor: " + sensor.getUserName()
			self.waitSensorActive(sensor)
			
			nextSequence = (self.currentSequence +1) % self.transit.getMaxSequence()
			if (nextSequence == 0):
				nextSequence = 1			
			self.currentSection = self.transit.getSectionListBySeq(nextSequence)[0]	
			print "Current Section: " + self.currentSection.getUserName()		
		else :
			#print "Stopping train"
			self.stopTrain()
			
		self.waitMsec(1000)
			
# 		# and continue around again
		#print "End of Loop"
		if (sensors.getSensor("L1 Auto").getState() != ACTIVE) :
		    self.throttle.setSpeedSetting(0)
		    self.throttle.setF0(False)
 		#return sensors.getSensor("L1 Auto").getState() == ACTIVE	
 		return True
		# (requires JMRI to be terminated to stop - caution
		# doing so could leave loco running if not careful)

# end of class definition

# start one of these up
AoSL1Train1().start()

