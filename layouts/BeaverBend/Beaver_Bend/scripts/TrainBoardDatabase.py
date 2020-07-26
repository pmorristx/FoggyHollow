import jarray
import jmri
import jmri.jmrit.roster
import sys
from java.awt import Font
import jmri.jmrit.operations.trains

import datetime
from datetime import timedelta
from TimeTableEvent import TimeTableEvent
from foggyhollow.timetable import TimeTable
from foggyhollow.timetable import TimetableEntry

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

                timetableIpAddress = memories.getMemory("Timetable IP Address").getValue()
                if (len(timetableIpAddress) < 18) :
                        timetableIpAddress = "192.168.1.2:3306" # Default to PlexRaspberry MySQL server
                        
                timeTable = TimeTable(str(timetableIpAddress))
                todaysDepartures = timeTable.getTodaysDepartures("Beaver Bend")

                if (len(todaysDepartures) > 0) :
                        self.populateDepartureBoard (todaysDepartures, 1, 7)
                else:
                        memories.getMemory("IM:1:DST").setValue("No Trains Today")

        def populateDepartureBoard(self, todaysDepartures, startRow, maxRow) :
                i = startRow
                for train in todaysDepartures :

                        trainNum = train.getTrainNumber()
                        trainType = train.getTrainType()
                        if (trainType == "S" or trainType == "X") :
                                trainNum = "X" + trainNum
                        departs = str(train.getScheduleTime12())
                        remark = ""

                        #
                        #  Check if the current time is after the scheduled departure time.  If so,
                        #  set the remark field
                        if (len(departs) > 0) :
                                currentTime = datetime.datetime.now()
                                today = datetime.datetime.strftime(currentTime, '%b %d %Y')                                
                                departStr = today + " " + departs                                
                                departTime = datetime.datetime.strptime(departStr, '%b %d %Y %I:%M %p')
                                if (departTime < currentTime) :
                                        remark = "DPARTED"

                        #
                        #  Trim leading "0" off departure hours < "10"
                        if (departs.startswith("0")) :
                                temp = list(departs)
                                temp[0] = " "
                                departs = "".join(temp)

                        memories.getMemory("IM:" + str(i) + ":DIR").setValue(train.getDirection())
                        memories.getMemory("IM:" + str(i) + ":TNO").setValue(trainNum)
                        memories.getMemory("IM:" + str(i) + ":TNM").setValue(train.getTrainName())
                        memories.getMemory("IM:" + str(i) + ":DST").setValue(train.getDestination())
                        memories.getMemory("IM:" + str(i) + ":DPRT").setValue(departs)
                        memories.getMemory("IM:" + str(i) + ":RMK").setValue(remark)

                        i = i + 1
                        if (i > maxRow) :
                                break

                                
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
