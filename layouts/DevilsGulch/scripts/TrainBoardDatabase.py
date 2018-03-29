import jarray
import jmri
import jmri.jmrit.roster
import sys
from java.awt import Font
import jmri.jmrit.operations.trains
from com.ziclix.python.sql import zxJDBC
import datetime

	
class TrainBoardDatabase(jmri.jmrit.automat.AbstractAutomaton) :
	
	
	
	def findPanelIcon(self, panelEditor, targetName) :
		if (panelEditor != None) :
			contents = panelEditor.getContents()
			for i in range(contents.size()) :
				object = contents.get(i)
				objectClass = str(object.getClass())
#				print "Object class = %s  Object name = %s" % (str(object.getClass()), object.getToolTip().getText())				
				if (objectClass.endswith("MemoryIcon'>")) :
					src = object.getToolTip().getText()
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

                dow = datetime.datetime.now().strftime("%a")

                r = 1
                while r < 6 :
                    memories.getMemory("IM:" + str(r) + ":DIR").setValue("")
                    memories.getMemory("IM:" + str(r) + ":TNO").setValue("")
                    memories.getMemory("IM:" + str(r) + ":TNM").setValue("")			
                    memories.getMemory("IM:" + str(r) + ":DST").setValue("")
                    memories.getMemory("IM:" + str(r) + ":DPRT").setValue("")
                    memories.getMemory("IM:" + str(r) + ":RMK").setValue("")
                    r = r + 1

                    
                connectionUrl = "jdbc:mysql://192.168.0.12:3306"
                with zxJDBC.connect(
                        connectionUrl,
                        "foggyhollow",
                        "foggyhollow",
                        "com.mysql.jdbc.Driver") as conn:
                    query = "select * from foggyhollow.station_schedules where station=? and (trainDays like ? or trainDays like 'Daily') ;"
                    with conn:
                        with conn.cursor() as c:
                            c.execute(query, ["Empire", "%" + dow + "%"])
                #            c.execute(query, ["Devil's Gulch", "%" + dow + "%"])            
                            try:
                                i = 1
                                while c.next():
                                    row = c.fetchone()
                                    trainNum = str(row[1])
                                    trainName = str(row[2])
                                    arlv = str(row[3])
                                    schedTime = str(row[4])
                                    direction = row[5]
                                    dest = row[7]

                                    memories.getMemory("IM:" + str(i) + ":DIR").setValue(direction)
                                    memories.getMemory("IM:" + str(i) + ":TNO").setValue(trainNum)
                                    memories.getMemory("IM:" + str(i) + ":TNM").setValue(trainName)			
                                    memories.getMemory("IM:" + str(i) + ":DST").setValue(dest)
                                    memories.getMemory("IM:" + str(i) + ":DPRT").setValue(schedTime)
                                    memories.getMemory("IM:" + str(i) + ":RMK").setValue("")	                                    

                                    i = i+ 1                                    


                            except StopIteration:
                                print ""

                



# create one of these
main = TrainBoardDatabase()

# set the name, as a example of configuring it
main.setName("Beaver Bend Train Board")

# and start it running
main.start()	
