import jarray
import jmri
import foggyhollow.departureboard.DepartureBoard
import datetime
from datetime import datetime, timedelta, date
import java.util.Random
import java.awt.Frame
import time
from time import mktime
from java.lang.reflect import Array
from java.util import Vector
import threading
from threading import Timer
#import pytz
#from pytz import timezone
from TimeTableEntry import TimeTableEntry
from com.ziclix.python.sql import zxJDBC
import math

class DevilsGulchDepartureBoard(jmri.jmrit.automat.AbstractAutomaton) :

    departureBoard = None
    
    def init(self) :
        
        self.initTimeTable("Devil's Gulch")
        self.depotArrival = memories.provideMemory("Arrives Depot")
        self.depotDeparture = memories.provideMemory("Departs Depot")
        
        self.freightHouseArrival = memories.provideMemory("Arrives Freight House")
        self.freightHouseDeparture = memories.provideMemory("Departs Freight House")        


#        self.wobble = sensors.provideSensor("Rock Wobble")
        #
        # Provide for long & short delays for demo mode.
        
        self.demoSwitch = sensors.provideSensor("Building Light Demo")
        
        self.demoModeIdx = 0
        self.nonDemoModeIdx = 1
        self.stationDelayIdx =2
        self.freightHouseDelayIdx =1
        self.waterTowerDelayIdx =3
        self.bridgeDelayIdx =4
        self.goneDelayIdx =0
        
        self.delays = java.lang.reflect.Array.newInstance(java.lang.Integer,[2, 5])
        self.delays[self.demoModeIdx][self.goneDelayIdx] = 10
        self.delays[self.demoModeIdx][self.freightHouseDelayIdx] = 3
        self.delays[self.demoModeIdx][self.stationDelayIdx] = 10
        self.delays[self.demoModeIdx][self.waterTowerDelayIdx] = 4        
        self.delays[self.demoModeIdx][self.bridgeDelayIdx] = 4                
        
        self.delays[self.nonDemoModeIdx][self.goneDelayIdx] = 20
        self.delays[self.nonDemoModeIdx][self.freightHouseDelayIdx] = 5
        self.delays[self.nonDemoModeIdx][self.stationDelayIdx] = 10
        self.delays[self.nonDemoModeIdx][self.waterTowerDelayIdx] = 4        
        self.delays[self.nonDemoModeIdx][self.bridgeDelayIdx] = 4                        
                
        self.privateSwitch = sensors.provideSensor("Private")
        self.privateSwitch.setState(INACTIVE)

        DevilsGulchDepartureBoard.departureBoard = foggyhollow.departureboard.DepartureBoard("Ace of Spades Mine", "Departures", 325, 220, 4, 34)        
        DevilsGulchDepartureBoard.departureBoard.addField("GenericMsg", 0, 34, False)

        DevilsGulchDepartureBoard.departureBoard.addField("TrainNo", 0, 3, False)
        DevilsGulchDepartureBoard.departureBoard.addField("Direction", 3, 1, False)
        DevilsGulchDepartureBoard.departureBoard.addField("TrainName", 5, 20, False)
#        DevilsGulchDepartureBoard.departureBoard.addField("TrainName", 4, 15, False)        
#        DevilsGulchDepartureBoard.departureBoard.addField("Arrives", 19, 5, False)
        DevilsGulchDepartureBoard.departureBoard.addField("Departs", 26, 8, True)			                        
		
        self.showDeparture = True
        
        self.messages = java.lang.reflect.Array.newInstance(java.lang.String,[10, 4])
        self.messages[0][0] = ""
        self.messages[0][1] = "Welcome to the"
        self.messages[0][2] = "Ace of Spades Mine"
        self.messages[0][3] = " "
        
        self.messages[1][0] = ""
        self.messages[1][1] = "Ask the Station Master"
        self.messages[1][2] = "About Underground Tours"
        self.messages[1][3] = "Of The Mine"  
        
        self.messages[2][0] = "Easily Visitied Via"
        self.messages[2][1] = "Daily Excursions on the"
        self.messages[2][2] = "Foggy Hollow & Western"
        self.messages[2][3] = "Railroad"
        
        self.messages[3][0] = "Take the tour to see:"
        self.messages[3][1] = "- Huge Caverns"
        self.messages[3][2] = "- Dark Tunnels"
        self.messages[3][3] = "- An Underground Lake"        
        
        self.messages[4][0] = ""
        self.messages[4][1] = "Tickets Available at the"
        self.messages[4][2] = "Foggy Hollow & Western"
        self.messages[4][3] = "Ticket Counter"                      
        
        self.msgNum = 0
        self.numPublicMessages = 5
        
        self.messages[5][0] = ""
        self.messages[5][1] = "Tours Available to"
        self.messages[5][2] = "Men and Boys"
        self.messages[5][3] = "(Ages 14 and older)"
        
        self.messages[6][0] = ""
        self.messages[6][1] = "Secure Baskets Available"
        self.messages[6][2] = "For Clothing and Valuables"
        self.messages[6][3] = "During the Tour" 
        
        self.messages[7][0] = "Descend Deep Underground"
        self.messages[7][1] = "Into the hot and humid mine"
        self.messages[7][2] = "to see naked miners"
        self.messages[7][3] = "collecting the ore"   
        
        self.messages[8][0] = ""
        self.messages[8][1] = "Soak in an"
        self.messages[8][2] = "underground lake Before"
        self.messages[8][3] = "Returning to the Surface" 
        
        self.messages[9][0] = ""
        self.messages[9][1] = "Shower and towel Provided"
        self.messages[9][2] = "Before your return trip"
        self.messages[9][3] = ""                                             

        #
        #  Create the scheduler
        #self.scheduler = sched.scheduler(time.time, time.sleep)
        # Schedule train to arrive
        #self.scheduler.enter(10, 1, self.changeMessage, argument=("1",))
        #self.scheduler.enter(11, 1, self.trackEmpty, argument=("a",)) # Schedules a train to arrive
        threading.Timer(10, self.changeMessage, ["1"]).start()
        threading.Timer(11, self.trackEmpty, ["a"]).start()                                

        arriveDelay = self.getDelay(self.goneDelayIdx) + self.getDelay(self.freightHouseDelayIdx)
        departDelay1 = self.getDelay(self.goneDelayIdx) +  self.getDelay(self.freightHouseDelayIdx) + 3        
        departDelay2 = self.getDelay(self.goneDelayIdx) + self.getDelay(self.freightHouseDelayIdx) + self.getDelay(self.stationDelayIdx)

        self.arrivalTime =  datetime.fromtimestamp(time.time()) + timedelta(minutes=arriveDelay)

        self.departureTime1 =  datetime.fromtimestamp(time.time()) + timedelta(minutes=departDelay1)          
        self.departureTime2 =  datetime.fromtimestamp(time.time()) + timedelta(minutes=departDelay2)
        
#        self.depotArrival.setValue(self.arrivalTime.strftime("%Y-%m-%d %H:%M:%S.%f"))        
#        self.depotDeparture.setValue(self.departureTime2.strftime("%Y-%m-%d %H:%M:%S.%f"))
                          
        #self.scheduler.run()
        
        #self.waitMsec(5000)

#        self.wobble.setState(ACTIVE)
#        threading.Timer(15*60, self.stopWobble, ["1"]).start()
        
        threading.Timer(20, self.hidePanel, ["1"]).start()
        
        return;

#    def stopWobble(self, dummy) :
#        self.wobble.setState(INACTIVE)
        
    def hidePanel(self, dummy) :
        jmri.util.JmriJFrame.getFrame("PanelPro").setState(java.awt.Frame.ICONIFIED)

        
    def getDelay(self, location):
        if (self.demoSwitch.getState() == ACTIVE) :
            return self.delays[self.demoModeIdx][location]
        else :
            return self.delays[self.nonDemoModeIdx][location]
        

    def trainArriving(self, dummy):
        sensors.provideSensor("OS: T1 Bridge").setState (INACTIVE)         
        sensors.provideSensor("OS: T1 Freight House").setState (ACTIVE)
        #self.scheduler.enter(60*self.getDelay(self.freightHouseDelayIdx), 1, self.trainArrived, argument=("A",))
        threading.Timer(60*self.getDelay(self.freightHouseDelayIdx), self.trainArrived, ["a"]).start()        
        
    def trainArrived(self, dummy) :
        sensors.provideSensor("OS: T1 Freight House").setState (INACTIVE)
        sensors.provideSensor("OS: T1 Depot").setState (ACTIVE)        
        #self.scheduler.enter(60*self.getDelay(self.stationDelayIdx), 1, self.trainDepart, argument=("A",))
        threading.Timer(60*self.getDelay(self.stationDelayIdx), self.trainDepart, ["A"]).start()                                
        self.departureTime2 =  datetime.fromtimestamp(time.time()) + timedelta(minutes=10)
        self.departureTime1 =  datetime.fromtimestamp(time.time()) + timedelta(minutes=3)

    def trainDepart(self, dummy) :
        sensors.provideSensor("OS: Freight House").setState (INACTIVE)
        sensors.provideSensor("OS: T1 Depot").setState (INACTIVE) 
        sensors.provideSensor("OS: T1 Water Tower").setState (ACTIVE)        
        #self.scheduler.enter(60*self.getDelay(self.waterTowerDelayIdx), 1, self.depotIdle, argument=("A",))
        threading.Timer(60*self.getDelay(self.waterTowerDelayIdx), self.depotIdle, ["A"]).start()                
        
    def depotIdle(self, dummy):
        sensors.provideSensor("OS: T1 Water Tower").setState (jmri.Sensor.INACTIVE)               
        sensors.provideSensor("OS: T1 Bridge").setState (jmri.Sensor.ACTIVE) 
        #self.scheduler.enter(60*self.getDelay(self.bridgeDelayIdx), 1, self.trackEmpty, argument=("A",))
        threading.Timer(60*self.getDelay(self.bridgeDelayIdx), self.trackEmpty, ["A"]).start()                        
        
    def trackEmpty(self, dummy):
        sensors.provideSensor("OS: T1 Water Tower").setState (jmri.Sensor.INACTIVE)               
        sensors.provideSensor("OS: T1 Bridge").setState (jmri.Sensor.INACTIVE) 
        
        #
        #  schedule train to arrive at depot (set freight house occupancy sensor)
        #  update memory variable for arrival/departure at depot as an offset from the current time.
        arrivalOffset = self.getDelay(self.goneDelayIdx) + self.freightHouseDelayIdx
        #self.scheduler.enter(60*self.getDelay(self.goneDelayIdx), 1, self.trainArriving, argument=("A",))
        threading.Timer(60*self.getDelay(self.goneDelayIdx), self.trainArriving, ["A"]).start()                        
        self.departureTime1 =  datetime.fromtimestamp(time.time()) + timedelta(minutes=arrivalOffset + 3)
        self.departureTime2 =  datetime.fromtimestamp(time.time()) + timedelta(minutes=arrivalOffset+10)        
        self.arrivalTime =  datetime.fromtimestamp(time.time()) + timedelta(minutes=arrivalOffset)
        self.depotArrival.setValue(self.arrivalTime.strftime("%Y-%m-%d %H:%M:%S.%f"))        
        self.depotDeparture.setValue(self.departureTime2.strftime("%Y-%m-%d %H:%M:%S.%f"))
        
        #
        #  schedule train to arrive at freight house 
        arrivalOffset = self.getDelay(self.goneDelayIdx)
        departOffset = self.getDelay(self.freightHouseDelayIdx) + self.getDelay(self.stationDelayIdx)        
        self.freightHouseArrivalTime =  datetime.fromtimestamp(time.time()) + timedelta(minutes=arrivalOffset)        
        self.freightHouseDepartureTime =  datetime.fromtimestamp(time.time()) + timedelta(minutes=arrivalOffset+departOffset)        
        self.freightHouseArrival.setValue(self.freightHouseArrivalTime.strftime("%Y-%m-%d %H:%M:%S.%f"))        
        self.freightHouseDeparture.setValue(self.freightHouseDepartureTime.strftime("%Y-%m-%d %H:%M:%S.%f"))                       
       
    
    def initTimeTable(self, station):

        import datetime

        self.timeTable = Vector()
        dow = datetime.datetime.now().strftime("%a")

        connectionUrl = "jdbc:mysql://192.168.0.12:3306"
        try:
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
                            while row != None:
                                entry = TimeTableEntry()
                                entry.setTrainNumber(str(row[1]))
                                entry.setTrainName(str(row[2]))
                                entry.setArLv(str(row[3]))
                                entry.setScheduleTime(row[4].lstrip("0"))
                                entry.setDirection(row[5])
                                entry.setDestination(row[7])
                                self.timeTable.add(entry)
                                row = c.fetchone()
                        except StopIteration:
                            print ""
        except zx.JDBC.DatabaseError:
            print "Unable to connect to database"
            entry = TimeTableEntry()
            entry.setTrainNumber(-1)
            entry.setTrainName("Database Error")
            entry.setDestination("Connection Error")
            self.timeTable.add(entry)
            
        self.numDeparturePages = math.ceil(self.timeTable.size() / 4.0)
        self.currentPage = 0
        self.showDeparture = True
        self.showTrainName = True
    
    def changeMessage(self, messageNo):

        #print "***"
        #print "changeMessage - currentPage  = " + str(self.currentPage)
        #print "changeMessage - showDeparture = " + str(self.showDeparture)
        #print "changeMessage - self.currentPage = " + str(self.currentPage)
        
        if (self.showDeparture) :

            #print ""
            #print "num depart pages = " + str(self.numDeparturePages)

            if (self.numDeparturePages > 0):

                r = self.currentPage * 4
                c = 0
                if self.showTrainName:
                    DevilsGulchDepartureBoard.departureBoard.clearRow(0, True)            
                    DevilsGulchDepartureBoard.departureBoard.clearRow(1, True)            
                    DevilsGulchDepartureBoard.departureBoard.clearRow(2, True)            
                    DevilsGulchDepartureBoard.departureBoard.clearRow(3, True)   

                    while (c < min(4, self.timeTable.size() - (self.currentPage*4))):
                        entry = self.timeTable.get(r)
                        DevilsGulchDepartureBoard.departureBoard.setField("TrainNo", entry.getTrainNumber(), c, 0)
                        DevilsGulchDepartureBoard.departureBoard.setField("Direction", entry.getDirection()[0:1], c, 0)
                        DevilsGulchDepartureBoard.departureBoard.setField("TrainName", entry.getTrainName(), c, 0)
                        #DevilsGulchDepartureBoard.departureBoard.setField("Arrives", "", c, 0)                
                        DevilsGulchDepartureBoard.departureBoard.setField("Departs", entry.getScheduleTime(), c, 0)
                        r = r + 1
                        c = c + 1

                    self.showTrainName = False
                else:
                    self.showTrainName = True
                    while (c < min(4, self.timeTable.size() - (self.currentPage*4))):
                        entry = self.timeTable.get(r)
                        DevilsGulchDepartureBoard.departureBoard.setField("TrainName", entry.getDestination(), c, 0)
                        r = r + 1
                        c = c + 1
                    self.currentPage = self.currentPage + 1
                    #print "current page = "+ str(self.currentPage)
                    if (self.currentPage >= self.numDeparturePages):
                        #print "resetting timetable"
                        self.currentPage = 0
                        self.showDeparture = False
                    
            else:
                arrives = self.arrivalTime.strftime("%I:%M")
                departs1 = self.departureTime1.strftime("%I:%M")            
                departs2 = self.departureTime2.strftime("%I:%M")
          
                DevilsGulchDepartureBoard.departureBoard.setField("TrainNo", "3", 1, 0)
                DevilsGulchDepartureBoard.departureBoard.setField("TrainName", "Mountaineer", 1, 0)
                #DevilsGulchDepartureBoard.departureBoard.setField("Arrives", arrives, 1, 0)                
                DevilsGulchDepartureBoard.departureBoard.setField("Departs", departs1, 1, 0)
            
                DevilsGulchDepartureBoard.departureBoard.setField("TrainNo", "15", 2, 0)
                DevilsGulchDepartureBoard.departureBoard.setField("TrainName", "Mine Excursion", 2, 0)
                DevilsGulchDepartureBoard.departureBoard.setField("Departs", departs2, 2, 0)                 
        else :
            i = self.msgNum
            for j in range(len(self.messages[i])):
                if (len(self.messages[i][j]) == 0) :
                    DevilsGulchDepartureBoard.departureBoard.clearRow(j, True)
                else :                                    
                    DevilsGulchDepartureBoard.departureBoard.setField("GenericMsg", self.messages[i][j], j, 0)                        
            self.msgNum = self.msgNum + 1
            if ((self.privateSwitch.getState() == INACTIVE and self.msgNum >= self.numPublicMessages) or (self.privateSwitch.getState() == ACTIVE and self.msgNum >= len(self.messages))) :
                self.msgNum = 0            
            
            self.showDeparture = True       
        nextMsg = str(self.msgNum + 1)        

        #print "*** scheduling changeMessage, showDep = " + str(self.showDeparture) + " currentPage = " + str(self.currentPage)
        threading.Timer(30, self.changeMessage, [nextMsg]).start()
        #print "*** scheduled changeMessage, showDep = " + str(self.showDeparture) + " currentPage = " + str(self.currentPage)        
        return
    
    #  We never get here because we are always waiting in the scheduler
    def handle(self):
        self.waitMsec(100000)
        return  (True)
    
DevilsGulchDepartureBoard().start()
