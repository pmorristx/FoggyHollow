import jarray
import jmri
import jmri.jmrit.roster
import sys
from java.awt import Font
import jmri.jmrit.operations.trains


	
class TrainBoard(jmri.jmrit.automat.AbstractAutomaton) :
	
	
	
	def findPanelIcon(self, panelEditor, targetName) :
		if (panelEditor != None) :
			contents = panelEditor.getContents()
			for i in range(contents.size()) :
				object = contents.get(i)
				objectClass = str(object.getClass())
#				print "Object class = %s  Object name = %s" % (str(object.getClass()), object.getTooltip().getText())				
				if (objectClass.endswith("MemoryIcon'>")) :
					src = object.getTooltip().getText()
#					print "Memory Object name found = %s" % (src)
					if (src == targetName) :
						return object	
						
	def setMemoryIconFont(self):
		
		import jmri.jmrit.display
		import sys	
		
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
		
		try:
	#		handFont = Font("Comic Sans MS", Font.ITALIC, 12)
			handFont = Font("Tempus Sans ITC", Font.ITALIC , 12)			
			for editor in editorList:
				panel = editor.getFrame()
				for i in range(6) :
					icon = self.findPanelIcon(panel,"IM:" + str(i+1) + ":TNO")
					if (icon is not None) :
						icon.setFont(Font("Tempus Sans ITC", Font.ITALIC , 12))	
						
					icon = self.findPanelIcon(panel,"IM:" + str(i+1) + ":TNM")
					if (icon is not None) :
						icon.setFont(handFont)	
						
					icon = self.findPanelIcon(panel,"IM:" + str(i+1) + ":DST")
					if (icon is not None) :
						icon.setFont(handFont)	
						
					icon = self.findPanelIcon(panel,"IM:" + str(i+1) + ":RMK")
					if (icon is not None) :
						icon.setFont(handFont)	
						
					icon = self.findPanelIcon(panel,"IM:" + str(i+1) + ":DPRT")
					if (icon is not None) :
						icon.setFont(handFont)	
						
					icon = self.findPanelIcon(panel,"IM:" + str(i+1) + ":DIR")
					if (icon is not None) :
						icon.setFont(handFont)																																					
		except:
			print "Error setting MemoryIcon font: ", sys.exc_info()[0], sys.exc_info()[1]		
		return
		
	def init(self):
		self.setMemoryIconFont()
		trains = jmri.jmrit.operations.trains.TrainManager.instance().getTrainsByTimeList()
		i = 1
		for train in trains :
			train.addAfterBuildScript("preference:scripts/TrainBoard.py")			
			name = train.getName()
			nextLocation = train.getNextLocationName()
			engine = train.getLeadEngine()
			engine = train.getLeadEngine()			
			
			engineNumber = ""
			if (engine is not None):
				engineNumber = engine.getNumber()
				
			print "IM:" + str(i) + ":TNO"
			
			direction = train.getRoute().getDepartsRouteLocation().getTrainDirection()
			if (direction == jmri.jmrit.operations.routes.RouteLocation.WEST) :
				memories.getMemory("IM:" + str(i) + ":DIR").setValue("West")
			elif (direction == jmri.jmrit.operations.routes.RouteLocation.EAST) :
				memories.getMemory("IM:" + str(i) + ":DIR").setValue("East")												
			elif (direction == jmri.jmrit.operations.routes.RouteLocation.NORTH) :
				memories.getMemory("IM:" + str(i) + ":DIR").setValue("North")												
			elif (direction == jmri.jmrit.operations.routes.RouteLocation.SOUTH) :
				memories.getMemory("IM:" + str(i) + ":DIR").setValue("South")																				
				
			memories.getMemory("IM:" + str(i) + ":TNO").setValue(train.getLeadEngineNumber())
			memories.getMemory("IM:" + str(i) + ":TNM").setValue(train.getName())			
			memories.getMemory("IM:" + str(i) + ":DST").setValue(train.getTrainTerminatesName())						
			memories.getMemory("IM:" + str(i) + ":RMK").setValue(train.getComment())
			if (train.getFormatedDepartureTime() != "00:00") :									
				memories.getMemory("IM:" + str(i) + ":DPRT").setValue(train.getFormatedDepartureTime())	
			else :
				memories.getMemory("IM:" + str(i) + ":DPRT").setValue("")	

			i = i+ 1


# create one of these
main = TrainBoard()

# set the name, as a example of configuring it
main.setName("Beaver Bend Train Board")

# and start it running
main.start()	