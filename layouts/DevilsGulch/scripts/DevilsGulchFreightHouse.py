import jarray
import jmri
import java.util.Random
import threading
from threading import Timer
from Building import Building
from foggyhollow.arduino import TriStateSensor

#Created on Jan 29, 2017

class DevilsGulchFreightHouse(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):
        #

        self.arrivesMemoryVariable = "Arrives Freight House"
        self.departsMemoryVariable = "Departs Freight House"
        self.freightHouse = Building()
        self.freightHouse.init(self.arrivesMemoryVariable, self.departsMemoryVariable) 
        
        self.scheduleTimes = []
        self.scheduleTimes.append(memories.provideMemory(self.arrivesMemoryVariable))                       
          
        #self.stove = lights.provideLight("NL120");
        #self.platformLights = lights.provideLight("NL121");
        #self.officeLight = lights.provideLight("NL122");
        #self.dockLight = lights.provideLight("NL123");        
        
        #self.platformIndicator = lights.provideLight("IL121");
        #self.officeIndicator = lights.provideLight("IL122");
        #self.dockIndicator = lights.provideLight("IL123"); 
        
        #self.platformLightDimmer = lights.provideLight("NL124");               
        #self.officeLightDimmer = lights.provideLight("NL125");               
        #self.dockLightDimmer = lights.provideLight("NL126");                               

        self.freightDock = TriStateSensor(sensors.provideSensor("Freight Dock Dim"),
                                          sensors.provideSensor("Freight Dock On"),
                                          sensors.provideSensor("Freight Dock Off"))

        self.freightOffice = TriStateSensor(sensors.provideSensor("Freight Office Dim"),
                                          sensors.provideSensor("Freight Office On"),
                                          sensors.provideSensor("Freight Office Off"))

        self.freightPlatform = TriStateSensor(sensors.provideSensor("Freight Platform Dim"),
                                          sensors.provideSensor("Freight Platform On"),
                                          sensors.provideSensor("Freight Platform Off"))

        self.freightStove = TriStateSensor(None,
                                          sensors.provideSensor("Freight Stove"),
                                           None)                        

        
        self.sideDoor = sensors.provideSensor("Mine Bldg Side Soor") # Mine Bldg Side Door
        self.lockerRoom = sensors.provideSensor("Mine Bldg S2") # Mine Bldg Level 2 - Locker Room
        self.tipple = sensors.provideSensor("Mine Bldg S3") # Mine Bldg Tipple        

        
    def scheduleDeparture(self):
        memVal = memories.provideMemory(self.departsMemoryVariable).getValue()
        if (memVal != None) :

            depStr = memVal[0:19]
            departureTime = datetime.strptime( memVal, "%Y-%m-%d %H:%M:%S.%f" )
            self.freightOffice.scheduleStateChangeAfter(TriStateSensor.DIM, depStr, 3)
            self.freightDock.scheduleStateChangeAfter(TriStateSensor.DIM, depStr, 6)
            self.freightPlatform.scheduleStateChangeAfter(TriStateSensor.DIM, depStr, 4)            
            
            self.freightDock.scheduleStateChangeAfter(TriStateSensor.OFF, depStr, 10)
            self.freightPlatform.scheduleStateChangeAfter(TriStateSensor.OFF, depStr, 11)                                    
            self.freightOffice.scheduleStateChangeAfter(TriStateSensor.OFF, depStr, 12)            
            self.freightStove.scheduleStateChangeAfter(TriStateSensor.OFF, depStr, 14)            
            
            if (java.util.Random().nextInt(10) > 5) :
                self.freightOffice.scheduleStateChangeAfter(TriStateSensor.DIM, depStr, 18)
                self.freightOffice.scheduleStateChangeAfter(TriStateSensor.OFF, depStr, 22)

                self.freightDock.scheduleStateChangeAfter(TriStateSensor.DIM, depStr, 19)
                self.freightDock.scheduleStateChangeAfter(TriStateSensor.OFF, depStr, 22)
                
    def scheduleArrival(self):
        memVal = memories.provideMemory("Arrives Depot").getValue()
        if (memVal != None) :
            arrStr = memVal[0:19]
            arrivalTime = datetime.strptime( memVal, "%Y-%m-%d %H:%M:%S.%f" )
            
            #  Station master arrives & turns on office light
            self.freightOffice.scheduleStateChangeBefore(TriStateSensor.ON, arrStr, 10)
            self.freightStove.scheduleStateChangeBefore(TriStateSensor.ON, arrStr, 9)                       
            

            self.freightPlatform.scheduleStateChangeBefore(TriStateSensor.DIM, arrStr, 7)
            self.freightPlatform.scheduleStateChangeBefore(TriStateSensor.ON, arrStr, 3)
            
            self.freightDock.scheduleStateChangeBefore(TriStateSensor.DIM, arrStr, 6)
            self.freightDock.scheduleStateChangeBefore(TriStateSensor.ON, arrStr, 2)            
                                  
    def handle (self):
        
        self.waitChange(self.scheduleTimes)
        self.scheduleArrival()
        self.scheduleDeparture()
        
        return True
            
DevilsGulchFreightHouse().start()
