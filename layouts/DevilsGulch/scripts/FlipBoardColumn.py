#
#  Script to shuttle mine train back & forth, turning on various lights, etc. along the way.

import jmri

class FlipBoardColumn(jmri.jmrit.automat.AbstractAutomaton) :
	
	allLetters = []
	allNumbers = []
	
	def init(self):		
#		print "In Flip Board Column Init"
		return
	
	def handle(self):
#		print "FlipBoardColumn waiting for ", self.trigger.getUserName()
		self.waitSensorActive(self.trigger)
		self.trigger.setState(INACTIVE)		
		try :
			currentLetter = memories.getMemory(self.memory).getValue()		
			
			if (self.isNumeric):
				numLetters = len(FlipBoardColumn.allNumbers)			
				thisIndex = FlipBoardColumn.allNumbers.index(currentLetter)	
				letters = FlipBoardColumn.allNumbers[thisIndex:numLetters]
				moreLetters = FlipBoardColumn.allNumbers[0:thisIndex]				
			else:
				numLetters = len(FlipBoardColumn.allLetters)
				thisIndex = FlipBoardColumn.allLetters.index(currentLetter)	
				letters = FlipBoardColumn.allLetters[thisIndex:numLetters]
				moreLetters = FlipBoardColumn.allLetters[0:thisIndex]

			letters = letters + moreLetters

			for ltr in letters :				
				memories.getMemory(self.memory).setValue(ltr)
				if (ltr == self.newValue) :
					return True
				self.waitMsec(50)

		except:			
			print "Unexpected error in FlipBoardColumn.handle: ", sys.exc_info()[0], sys.exc_info()[1]		
			print "FlipBoardColumn.handle currentLetter = '", currentLetter, "' new letter = '", self.newValue, "'"
		return True

	
	def setIsNumeric(self, isNumeric):
#		print "FlipBoardColumn setIsNumeric"		
		self.isNumeric = isNumeric
		return	
	
	def initColumn(self, memory):
#		print "FlipBoardColumn - initColumn, memory = ", memory
		memories.getMemory(memory).setValue(" ")
		self.memory = memory
		self.trigger = sensors.newSensor("IS:" + memory, "US:" + memory)
		self.trigger.setState(INACTIVE)		
		return
		
	def initLetters(self):
#		print "FlipBoardColumn initLetters"
		for c in range(26) :
			FlipBoardColumn.allLetters.append(chr(c + ord('A')))
		for c in range(9):
			FlipBoardColumn.allLetters.append(chr(c + ord('0')))
			FlipBoardColumn.allNumbers.append(chr(c + ord('0')))
			
		FlipBoardColumn.allLetters.append(" ")
		FlipBoardColumn.allLetters.append(":")
		
		FlipBoardColumn.allNumbers.append(" ")
		FlipBoardColumn.allNumbers.append(":")
		
	def flipColumn(self, value):	
		self.newValue = value
		#print "FLipBoardColumn value = ", value, " self.newValue = ", self.newValue, " memory = ", self.memory	
		self.trigger.setState(ACTIVE)
	
		return					