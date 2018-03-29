#
#  Operates a Solari-style split-flap destination board.  Each instance of FlipBoard operates one word (destination, train number, departure time, etc).
#  Each column of the word is represented by a MemoryIcon (created on the JMRI PANEL).  The MemoryIcon displays different letter images based on its
#  single character value.  The memories should be created (via JMRI Panel/Layout Editor) and named IM:xxxxnn with nn being a sequential number
#  (no leading zeros) starting at 1.

import jmri
import sys

sys.modules.clear()

class FlipBoardColumn(jmri.jmrit.automat.AbstractAutomaton) :

	numeric = " 0123456789" 
	alphaNumeric =  " :+-#'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	keyClick = None
	
	def __init__(self, memoryName, isNumeric):	
		
		self.memory = memoryName
		self.isNumeric = isNumeric
		self.letters = []
		self.moreLetters = []
		self.newValue = " "
		self.thisIndex = 0
		self.currentLetter = " "
		
		sysName = "IS:" + self.memory
		userName = "US:" + self.memory		
		
		self.trigger = sensors.newSensor(sysName, userName)	
		self.trigger.setState(INACTIVE)		
		
# 		if (FlipBoardColumn.keyClick is None) :	
# 			try:	
# 				FlipBoardColumn.keyClick = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/keyclick.wav"))		
# 			except:
# 				a = 1
	
	def init(self):		
		self.letters = []
		self.moreLetters = []
		self.newValue = " "
		self.thisIndex = 0
		self.currentLetter = " "

		sysName = "IS:" + self.memory
		userName = "US:" + self.memory 	

# 		if (FlipBoardColumn.keyClick is None) :
# 			try:
# 				FlipBoardColumn.keyClick = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/keyclick.wav"))		
# 			except:
# 				a = 1
		self.trigger = sensors.newSensor(sysName, userName)
		self.trigger.setState(INACTIVE)	
		return
	
	def handle(self):
		self.waitSensorActive(self.trigger)
		self.trigger.setState(INACTIVE)	
		
		self.currentLetter = " "	
		
		try :
			#
			#  Get the current letter from the memory.  We use this to sort the list of letters so the flipping
			#  will start from this letter.
			currentLetter = self.jmriMemory.getValue()[:1]		
		except:		
			self.currentLetter = " "					
			print "Unexpected error in FlipBoardColumn.handle: error getting currentLetter ", sys.exc_info()[0], sys.exc_info()[1], " currentLetter = '",self.currentLetter,"' new letter = '",self.newValue,"'"			
			
		try:			
			if (self.isNumeric):			
				sortedLetters = FlipBoardColumn.numeric		# Default
				numLetters = len(FlipBoardColumn.numeric)
				try:				
					thisIndex = FlipBoardColumn.numeric.index(currentLetter)	
				except:
					thisIndex = 0
					currentLetter = " "
					print "*** Error getting current letter index in FlipBoardColumn.handle currentLetter = ", currentLetter, " size of allNumbers = ", len(FlipBoardColumn.numeric)
				#
				#  The first part of the list should be from the previous letter to the end of the list.  If the previous letter
				#  was "4", then this list will be "4-9"
				tail = FlipBoardColumn.numeric[thisIndex:numLetters]
				#
				#  Now get the front of the list: "0-3".
				head = FlipBoardColumn.numeric[0:thisIndex]				
			else:
				numLetters = len(FlipBoardColumn.alphaNumeric)
				try:
					thisIndex = FlipBoardColumn.alphaNumeric.index(currentLetter)	
				except:
					thisIndex = 0
					currentLetter = " "
					print "*** Error getting current letter index in FlipBoardColumn.handle currentLetter = ", currentLetter, " size of allLetters = ", len(FlipBoardColumn.alphaNumeric)					
				tail = FlipBoardColumn.alphaNumeric[thisIndex:numLetters]
				head = FlipBoardColumn.alphaNumeric[0:thisIndex]

			#
			#  Combine the tail with the head lists
			sortedLetters = tail + head
		except:			
			print "Unexpected error in FlipBoardColumn.handle: error getting sortedLetters ", sys.exc_info()[0], sys.exc_info()[1], " currentLetter = '",currentLetter,"' new letter = '",self.newValue,"'"						

		try:
#			print "in FlipColumn.handle numLetters = ", len(self.sortedLetters), " seeking '",self.newValue,"'"
			#
			#  Loop through all the letters.  These are sorted so the previous (old, before we came here) letter is 
			#  first in the list.
			for ltr in sortedLetters :
# 				try:	
# 					FlipBoardColumn.keyClick.play()
# 				except:
# 					fail = 1
				self.jmriMemory.setValue(ltr) # Set the memory variable to display the letter on the GUI
				if (ltr == self.newValue) :  #  Bail out when the displayed letter is the requested letter
					self.trigger.setState(INACTIVE)	# Make sure the trigger is inactive to be ready for the next loop through handle						
					return True #  Keep the handle alive
				self.waitMsec(80) #  If we didn't bail out, slight delay to show the currently displayed letter
							

		except:			
			print "Unexpected error in FlipBoardColumn.handle: ", sys.exc_info()[0], sys.exc_info()[1], " currentLetter = '",self.currentLetter,"' new letter = '",self.newValue,"'"
		return True

	
	def setIsNumeric(self, isNumeric):
		self.isNumeric = isNumeric
		return	
	
	def initColumn(self, memoryName):
		self.jmriMemory = memories.getBySystemName(memoryName)
		if (self.jmriMemory is not None):
			self.jmriMemory.setValue(" ")
		else :
			print "FlipBoardColumn.initColumn failed to find memory, name = ", memoryName
		self.memory = memoryName	
		return
			
	def flipColumn(self, value):	
		try:
			self.newValue = value
			self.trigger.setState(ACTIVE)
		except:
			print "Unexpected error in FlipBoardColumn.flipColumn: value='", value,"' ", sys.exc_info()[0], sys.exc_info()[1]					
		return	

class FlipBoard(jmri.jmrit.automat.AbstractAutomaton) :
	def init(self):
		self.board = []
		del self.board[:]
		
		self.newWord = " "
		
#		print "in short init memory = ", self.boardMemory, " columns = ", self.numBoardColumns	
		
		for c in range(self.numBoardColumns):
			memName = "IM:" + self.boardMemory + str(c+1)
			threadName = self.boardMemory + str(c+1) + "Handler"
			flipCol = FlipBoardColumn(memName, self.boardIsNumeric)
			self.board.append(flipCol)			
			flipCol.initColumn(memName)
			flipCol.setName(threadName)	

			
		for c in range(self.numBoardColumns):			
			self.board[c].start()
			
		sysName = "IS:BRD:" + self.boardMemory
		usrName = "US:BRD:" + self.boardMemory		
		self.boardTrigger = sensors.newSensor(sysName, usrName)
 		self.boardTrigger.setState(INACTIVE)			
		
#		print "In short init, size of board = ",self.numBoardColumns
		return 
		
	def stopColumns(self):
#		self.flipWord(" ", 0)
		for c in range (self.numBoardColumns):	
			self.board[c].stop()	
		self.stop()
		
	def setColumns(self, columns):
		self.numBoardColumns = columns
		return
	
	def setMemory(self, memory):
		self.boardMemory = memory
		return
	
	def setIsNumeric(self, isNumeric):
		self.boardIsNumeric = isNumeric
		return
	
	def __init__(self, memory, columns, isNumeric, animationSensor):
#		print "in long init"		
		self.boardMemory = memory
		self.numBoardColumns = columns
		self.boardIsNumeric = isNumeric	
		self.animationSensor = animationSensor
			
						
	def reset(self):
		
		try:
			board = self.board
		except:
			print "Unexpected error in FlipBoard.reset ", sys.exc_info()[0], sys.exc_info()[1]	
			
		if (self.numBoardColumns is not None and self.numBoardColumns > 0):				
			for c in range (self.numBoardColumns):
				try:
					col = board[c]
				except:
					print "Unexpected error in FlipBoard.reset getting column at index ", c, " board size = ", len(board), " numBoardColumns = ", self.numBoardColumns, " ", sys.exc_info()[0], " ", sys.exc_info()[1]
				try:			
					col.flipColumn(" ")	
				except:
					print "Unexpected error in FlipBoard.reset blanking column at index ", c,  " ",  sys.exc_info()[0], " ", sys.exc_info()[1]
		return
	
	def flipWord(self, newWord, delaySecs):
		try:
			if (delaySecs > 0) :
				self.waitMsec(delaySecs * 1000)
#			self.newWord = newWord[:self.numBoardColumns].ljust(self.numBoardColumns)
			self.newWord = newWord[:self.numBoardColumns]
			sensorName = "IS:BRD:" + self.boardMemory
			sensor = sensors.getSensor(sensorName)
			if (sensor is not None):							
				sensor.setState(ACTIVE)			
			else:
				print " In FlipWord, sensor is none, ", sensorName
		except:
			print "Unexpected error in FlipBoard.flipWord ", sys.exc_info()[0], sys.exc_info()[1]	
		return
			
	def handle(self):
		self.waitSensorActive(self.boardTrigger)
		self.boardTrigger.setState(INACTIVE)
		
		try:
			word = self.newWord
			if (self.boardIsNumeric):
				word = word.rjust(self.numBoardColumns) 
			else:
				word = word.center(self.numBoardColumns)				
		except:
				print "Unexpected error in FlipBoard.handle ", sys.exc_info()[0], sys.exc_info()[1], " word = '",word					
			
			
		try:
# 			if (self.numBoardColumns > 2):
# 				self.splitFlapSound.loop()		
			for c in range (self.numBoardColumns):
				self.board[c].flipColumn(word[c])	
				self.waitMsec(5)
# 			if (self.numBoardColumns > 2):				
# 				self.splitFlapSound.stop()						
		except:		
			print "Unexpected error in FlipBoard.handle ", sys.exc_info()[0], sys.exc_info()[1], " word = '",word,"' memory = ", self.boardMemory, " columns = ", self.numBoardColumns, " board size = ", len(self.board)		
		self.boardTrigger.setState(INACTIVE)	
		
		state = True
		if (self.animationSensor is not None):	
			state = self.animationSensor.getState() == ACTIVE
			
		return state
	
# 	def createBoard(self, panelName, boardName, numColumns, x, y, isNumeric):
# 		import jmri.jmrit.display
# 		
# 		# initialize loop to find all panel editors
# 		i = 0
# 		editorList = []
# 		editor = jmri.InstanceManager.configureManagerInstance().findInstance(java.lang.Class.forName("jmri.jmrit.display.panelEditor.PanelEditor"),i)
# 		
# 		# loop, adding each editor found to the list
# 		while (editor != None) : 
# 			editorList.append(editor)
# 			# loop again
# 			i = i + 1
# 			editor = jmri.InstanceManager.configureManagerInstance().findInstance(java.lang.Class.forName("jmri.jmrit.display.panelEditor.PanelEditor"),i)
# 		    
# 		# Now we have a list of editors.
# 		# For each editor, get the related panel and walk down 
# 		# its object hierarchy until the widgets themselves are reached    
# 		for editor in editorList:
# 			try :
# 				if (editor.getName == panelName):
# 					panelEditor = editor.getFrame()	
# 					if	(panelEditor.getName() == "Ace of Spades Mine")):
# 						contents = panelEditor.getContents()					
# 						for c in range(numColumns)):
# 							memName = "IM:" + boardName + str(c)
# 							memIcon = jmri.jmrit.display.layoutEditor.MemoryIcon(memName, panel)
							
# 							
					
					
		