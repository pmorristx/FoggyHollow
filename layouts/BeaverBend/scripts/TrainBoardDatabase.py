import jarray
import jmri
import jmri.jmrit.roster
import sys
from java.awt import Font
import jmri.jmrit.operations.trains
from com.ziclix.python.sql import zxJDBC
import datetime
from datetime import timedelta
from TimeTableEvent import TimeTableEvent

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
		#self.setMemoryIconFont()

                self.lastUpdateDate = (datetime.datetime.now() + timedelta(days=-1)).date()
                
                self.orderBoardLightOn = sensors.provideSensor("Station Order Board Light On")
                self.orderBoardLightOff = sensors.provideSensor("Station Order Board Light Off")

                self.stationTowerLightOn = sensors.provideSensor("Station Tower Light On")
                self.stationTowerLightOff = sensors.provideSensor("Station Tower Light Off")

                self.stationMasterLightOn = sensors.provideSensor("Station Master Light On")
                self.stationMasterLightOff = sensors.provideSensor("Station Master Light Off")

                self.stationSignLightOn = sensors.provideSensor("Station Sign Light On")
                self.stationSignLightOff = sensors.provideSensor("Station Sign Light Off")

                self.events = []
                e = TimeTableEvent(self.stationMasterLightOn, self.stationMasterLightOff, ACTIVE, -15)
                self.events.append(e)
                self.events.append(TimeTableEvent(self.stationTowerLightOn, self.stationTowerLightOff, ACTIVE, -13))
                self.events.append(TimeTableEvent(self.stationSignLightOn, self.stationSignLightOff, ACTIVE, -10))
                self.events.append(TimeTableEvent(self.orderBoardLightOn, self.orderBoardLightOff, ACTIVE, -5))

                self.events.append(TimeTableEvent(self.orderBoardLightOn, self.orderBoardLightOff, INACTIVE, 5))
                self.events.append(TimeTableEvent(self.stationSignLightOn, self.stationSignLightOff, INACTIVE, 10))
                self.events.append(TimeTableEvent(self.stationTowerLightOn, self.stationTowerLightOff, INACTIVE, 13))
                self.events.append(TimeTableEvent(self.stationMasterLightOn, self.stationMasterLightOff, INACTIVE, 15))                


        def initDepartureTimes(self):

                self.lastUpdateDate = datetime.date.today()
                
                dow = datetime.datetime.now().strftime("%a")

                r = 1
                while r < 7 :
                    memories.getMemory("IM:" + str(r) + ":DIR").setValue("")
                    memories.getMemory("IM:" + str(r) + ":TNO").setValue("")
                    memories.getMemory("IM:" + str(r) + ":TNM").setValue("")			
                    memories.getMemory("IM:" + str(r) + ":DST").setValue("")
                    memories.getMemory("IM:" + str(r) + ":DPRT").setValue("")
                    memories.getMemory("IM:" + str(r) + ":RMK").setValue("")
                    memories.getMemory("IM:" + str(r) + ":DPRTTS").setValue("")                    
                    r = r + 1

                    
                connectionUrl = "jdbc:mysql://192.168.1.2:3306/foggyhollow"

                query = "select direction, trainNumber, trainName, arlv, destination, date_format(str_to_date(scheduleTime, '%h:%i %p'), '%l:%i %p'), scheduleTime from foggyhollow.station_schedules where station=? and arlv='Lv' and (trainDays like ? or trainDays like 'Daily') order by str_to_date(scheduleTime, '%h:%i %p') ;"                
                with zxJDBC.connect(
                        connectionUrl,
                        "foggyhollow",
                        "foggyhollow",
                        "com.mysql.jdbc.Driver") as conn:


                    with conn:
                        with conn.cursor() as c:
                            c.execute(query, ["Beaver Bend", "%" + dow + "%"])
                            try:
                                i = 1
                                row = c.fetchone()
                                while row != None and i < 7:

                                    trainNum = str(row[1])
                                    trainName = str(row[2])
                                    arlv = str(row[3])
                                    schedTime = str(row[5])
                                    schedTS = str(row[6])                                    
                                    direction = row[0]
                                    dest = row[4]

                                    memories.getMemory("IM:" + str(i) + ":DIR").setValue(direction)
                                    memories.getMemory("IM:" + str(i) + ":TNO").setValue(trainNum)
                                    memories.getMemory("IM:" + str(i) + ":TNM").setValue(trainName)			
                                    memories.getMemory("IM:" + str(i) + ":DST").setValue(dest)
                                    memories.getMemory("IM:" + str(i) + ":DPRT").setValue(schedTime)
                                    memories.getMemory("IM:" + str(i) + ":DPRTTS").setValue(schedTS)                                    
                                    memories.getMemory("IM:" + str(i) + ":RMK").setValue("")

                                    #print trainName + " " + schedTime + " " + dest

                                    i = i+ 1                                    
                                    row = c.fetchone()

                                #
                                #  Display 'no trains' message if there aren't any trains scheduled for this
                                #  station of this day-of-week.
                                if i == 1 :
                                        dayOfWeek = datetime.datetime.now().strftime("%A")                                        
                                        #memories.getMemory("IM:" + str(i) + ":TNO").setValue("No")
                                        memories.getMemory("IM:" + str(i) + ":TNM").setValue("No Trains")			
                                        memories.getMemory("IM:" + str(i) + ":DST").setValue(dayOfWeek)

                                        #  Look for next train
                                        tomorrow = datetime.datetime.now() + timedelta(days=1)
                                        nextTrainDay = tomorrow.strftime("%A")                                                               
                                        dow = tomorrow.strftime("%a")
                                        c.execute(query, ["Beaver Bend", "%" + dow + "%"])
                                        r = 1
                                        row = c.fetchone()
                                        #if row != None :
                                        #    memories.getMemory("IM:" + str(r+1) + ":TNM").setValue("Next Train")
                                        #    memories.getMemory("IM:" + str(r+1) + ":DST").setValue(nextTrainDay)

                                        departDayFull = tomorrow.strftime("%A")
                                        departDay = departDayFull
                                        if (len(departDayFull) > 7) :
                                                departDay = dow
                                        while row != None and r < 6:

                                            trainNum = str(row[1])
                                            trainName = str(row[2])
                                            arlv = str(row[3])
                                            schedTime = str(row[5])
                                            schedTS = str(row[6])                                            
                                            direction = row[0]
                                            dest = row[4]

                                            memories.getMemory("IM:" + str(r+1) + ":DIR").setValue(direction)
                                            memories.getMemory("IM:" + str(r+1) + ":TNO").setValue(trainNum)
                                            memories.getMemory("IM:" + str(r+1) + ":TNM").setValue(trainName)			
                                            memories.getMemory("IM:" + str(r+1) + ":DST").setValue(dest)
                                            memories.getMemory("IM:" + str(r+1) + ":DPRT").setValue(schedTime)
                                            memories.getMemory("IM:" + str(r+1) + ":DPRTTS").setValue(schedTS)                                            
                                            memories.getMemory("IM:" + str(r+1) + ":RMK").setValue(departDay)

                                            #print trainName + " " + schedTime + " " + dest

                                            r = r+ 1                                    
                                            row = c.fetchone()                                        
                                        
                            except StopIteration:
                                print ""

                                
        def handle (self) :
                timeDelay = 1
                r = 1
                currentDate = datetime.date.today()
                currentTime = datetime.datetime.now() # - timedelta(hours=5)
                #currentTime = currentTime - timedelta(minutes=30)
                
                today = datetime.datetime.strftime(currentTime, '%b %d %Y')                

                #
                #  If date has changed (past midnight), we refresh from the database with current data
                if (currentDate > self.lastUpdateDate) :
                        self.initDepartureTimes()
                        
                

                while r < 7 :
                        departStr = memories.getMemory("IM:" + str(r) + ":DPRT").getValue()                        
                        if (len(departStr) > 0) :

                                remarkStr = memories.getMemory("IM:" + str(r) + ":RMK").getValue()
                                departStr = today + " " + departStr
                                #print 'departStr = "', departStr, "'"
                                #datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
                                departTime = datetime.datetime.strptime(departStr, '%b %d %Y %I:%M %p')


                                #
                                #  If we have a departure time, and we don't have a remark (train doesn't leave today), then
                                #  check if we are past the departure time
                                if (len(remarkStr) == 0 or remarkStr == "Arriving") :
                                        if (departTime < currentTime) :
                                                memories.getMemory("IM:" + str(r) + ":RMK").setValue("Deprted")
                                        elif (departTime > currentTime and departTime < (currentTime + timedelta(minutes=5))) :
                                                memories.getMemory("IM:" + str(r) + ":RMK").setValue("Arriving")

                                for event in self.events:
                                        eventTime = departTime + timedelta(minutes = event.offset)
                                        if (eventTime > currentTime and eventTime < currentTime + timedelta(minutes=timeDelay) ) :
                                                print "Changing event state ", event.onSensor.getUserName(), " ", event.state, " ", datetime.datetime.strftime(eventTime, '%b %d %Y %I:%M %p')
                                                event.toggleSensor(event.state)
                                        
                        r = r + 1;
                self.waitMsec(1000 * 60 * timeDelay) # Wait 5 mintues to check again
                return True
        
# create one of these
main = TrainBoardDatabase()

# set the name, as a example of configuring it
main.setName("Beaver Bend Train Board")

# and start it running
main.start()	
