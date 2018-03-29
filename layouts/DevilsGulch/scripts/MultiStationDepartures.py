import datetime
import jmri
from com.ziclix.python.sql import zxJDBC
from java.awt import Font

class MultiStationDepartures(jmri.jmrit.automat.AbstractAutomaton) :

    def clearBoard(self) :
        r = 1

        while r < 11 :
            memories.getMemory("Direction:" + str(r) ).setValue("")
            memories.getMemory("Destination:" + str(r)).setValue("")
            memories.getMemory("Time:" + str(r)).setValue("")
            memories.getMemory("Train Name:" + str(r)).setValue("")
            memories.getMemory("Train Number:" + str(r)).setValue("")
            r = r + 1
            
    def findPanelIcon(self, panelEditor, targetName) :
		if (panelEditor != None) :
			contents = panelEditor.getContents()
			for i in range(contents.size()) :
				object = contents.get(i)
				objectClass = str(object.getClass())
# 				print "Object class = %s  Object name = %s" % (str(object.getClass()), object.getToolTip().getText())
				if (objectClass.endswith("MemoryIcon'>")) :
					src = object.getToolTip().getText()
# 					print "Memory Object name found = %s" % (src)
					if (src == targetName) :
						return object
        
    def setMemoryIconFont(self):

		import jmri.jmrit.display
		import sys

		# initialize loop to find all panel editors
		i = 0
		editorList = []
		editor = jmri.InstanceManager.configureManagerInstance().findInstance(java.lang.Class.forName("jmri.jmrit.display.panelEditor.PanelEditor"), i)

		# loop, adding each editor found to the list
		while (editor != None) :
			editorList.append(editor)
			# loop again
			i = i + 1
			editor = jmri.InstanceManager.configureManagerInstance().findInstance(java.lang.Class.forName("jmri.jmrit.display.panelEditor.PanelEditor"), i)

		# Now we have a list of editors.
		# For each editor, get the related panel and walk down
		# its object hierarchy until the widgets themselves are reached

		try:
	# 		handFont = Font("Comic Sans MS", Font.ITALIC, 12)
			handFont = Font("Tempus Sans ITC", Font.ITALIC , 12)
			for editor in editorList:
				panel = editor.getFrame()
				for i in range(6) :
					icon = self.findPanelIcon(panel, "IM:" + str(i + 1) + ":TNO")
					if (icon is not None) :
						icon.setFont(Font("Tempus Sans ITC", Font.ITALIC , 12))

					icon = self.findPanelIcon(panel, "IM:" + str(i + 1) + ":TNM")
					if (icon is not None) :
						icon.setFont(handFont)

					icon = self.findPanelIcon(panel, "IM:" + str(i + 1) + ":DST")
					if (icon is not None) :
						icon.setFont(handFont)

					icon = self.findPanelIcon(panel, "IM:" + str(i + 1) + ":RMK")
					if (icon is not None) :
						icon.setFont(handFont)

					icon = self.findPanelIcon(panel, "IM:" + str(i + 1) + ":DPRT")
					if (icon is not None) :
						icon.setFont(handFont)

					icon = self.findPanelIcon(panel, "IM:" + str(i + 1) + ":DIR")
					if (icon is not None) :
						icon.setFont(handFont)
		except:
			print "Error setting MemoryIcon font: ", sys.exc_info()[0], sys.exc_info()[1]
		return

    def readDatabase(self, station):

        import datetime

        self.clearBoard()
        dow = datetime.datetime.now().strftime("%a")

        connectionUrl = "jdbc:mysql://192.168.0.12:3306"
        with zxJDBC.connect(
                connectionUrl,
                "foggyhollow",
                "foggyhollow",
                "com.mysql.jdbc.Driver") as conn:
            query = "select * from foggyhollow.station_schedules where station=? and arlv='Lv' and (trainDays like ? or trainDays like 'Daily') order by str_to_date(scheduleTime, '%l:%i %p') ;"
            with conn:
                with conn.cursor() as c:
                    c.execute(query, [station, "%" + dow + "%"])
                    try:
                        i = 1
                        row = c.fetchone()
                        while row != None and i < 11:
                            memories.getMemory("Train Number:" + str(i)).setValue(str(row[1]))
                            memories.getMemory("Direction:" + str(i)).setValue(str(row[5]))
                            memories.getMemory("Train Name:" + str(i)).setValue(str(row[2]))
                            memories.getMemory("Time:" + str(i)).setValue(str(row[4]))
                            memories.getMemory("Destination:" + str(i)).setValue(str(row[7]))
                            row = c.fetchone()
                            i = i + 1
                    except StopIteration:
                        print ""
    def init(self):
        #  Memory we will watch for a station change
        self.station = memories.getMemory("Current Station")

        #self.setMemoryIconFont()

        self.clearBoard()
        self.station.setValue("Beaver Bend")
        self.readDatabase("Beaver Bend")

    def handle(self):
        self.waitChange([self.station])
        self.readDatabase(self.station.getValue())
        return True
MultiStationDepartures().start()
