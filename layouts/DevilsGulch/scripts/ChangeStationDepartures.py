import datetime
import jmri
from com.ziclix.python.sql import zxJDBC
from java.awt import Font
from java.awt import Dimension

class ChangeStationDepartures(jmri.jmrit.automat.AbstractAutomaton) :

    def clearBoard(self) :
        r = 1

        while r < 11 :
            memories.getMemory("Direction:" + str(r) ).setValue('    ')
            memories.getMemory("Destination:" + str(r)).setValue('     ')
            memories.getMemory("Time:" + str(r)).setValue("        ")
            memories.getMemory("Train Name:" + str(r)).setValue("                  ")
            memories.getMemory("Train Number:" + str(r)).setValue("  ")
            r = r + 1
            
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
        #self.station.setValue("Beaver Bend")
        self.readDatabase(self.station.getValue())

    def handle(self):
        #self.waitChange([self.station])
        #self.readDatabase(self.station.getValue())
        return False
ChangeStationDepartures().start()
