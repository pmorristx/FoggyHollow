import jarray
import jmri
import java.util.Random
import threading
from threading import Timer
from Building import Building

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
          
        self.stove = lights.provideLight("NL120");
        self.platformLights = lights.provideLight("NL121");
        self.officeLight = lights.provideLight("NL122");
        self.dockLight = lights.provideLight("NL123");        
        
        self.platformIndicator = lights.provideLight("IL121");
        self.officeIndicator = lights.provideLight("IL122");
        self.dockIndicator = lights.provideLight("IL123"); 
        
        self.platformLightDimmer = lights.provideLight("NL124");               
        self.officeLightDimmer = lights.provideLight("NL125");               
        self.dockLightDimmer = lights.provideLight("NL126");                               
                
    def scheduleDeparture(self):
        memVal = memories.provideMemory(self.departsMemoryVariable).getValue()
        if (memVal != None) :
            departureTime = datetime.strptime( memVal, "%Y-%m-%d %H:%M:%S.%f" )
            self.freightHouse.dimLightsAfter(departureTime, 3, self.dockLight, self.dockLightDimmer, self.dockIndicator)
            self.freightHouse.dimLightsAfter(departureTime, 4, self.platformLights, self.platformLightDimmer, self.platformIndicator) 
            self.freightHouse.dimLightsAfter(departureTime, 6, self.officeLight, self.officeLightDimmer, self.officeIndicator)             
            
            self.freightHouse.turnOffLightsAfter(departureTime, 10, self.dockLight, self.dockIndicator)  
            self.freightHouse.turnOffLightsAfter(departureTime, 11, self.platformLights, self.platformIndicator)              
            self.freightHouse.turnOffLightsAfter(departureTime, 12, self.officeLight, self.officeIndicator)                      
            self.freightHouse.turnOffLightsAfter(departureTime, 14, self.stove, None) 
            
            if (java.util.Random().nextInt(10) > 5) :
                self.freightHouse.dimLightsAfter(departureTime, 18, self.officeLight, self.officeLightDimmer, self.officeIndicator) 
                self.freightHouse.dimLightsAfter(departureTime, 19, self.dockLight, self.dockLightDimmer, self.dockIndicator)                            
                self.freightHouse.turnOffLightsAfter(departureTime, 21, self.dockLight, self.dockIndicator)  
                self.freightHouse.turnOffLightsAfter(departureTime, 22, self.officeLight, self.officeIndicator)                      
            
                    
    def scheduleArrival(self):
        memVal = memories.provideMemory("Arrives Depot").getValue()
        if (memVal != None) :
            arrivalTime = datetime.strptime( memVal, "%Y-%m-%d %H:%M:%S.%f" )
            
            #  Station master arrives & turns on office light
            self.freightHouse.turnOnLightBefore(arrivalTime, 10, self.officeLight, self.officeLightDimmer, True, self.officeIndicator)
            self.freightHouse.turnOnLightBefore(arrivalTime, 8, self.stove, None, False, None)
            
            self.freightHouse.turnOnLightBefore(arrivalTime, 7, self.platformLights, self.platformLightDimmer, True, self.platformIndicator)
            self.freightHouse.turnOnLightBefore(arrivalTime, 6, self.dockLight, self.dockLightDimmer, True, self.dockIndicator)            
            self.freightHouse.turnOnLightBefore(arrivalTime, 3, self.platformLights, self.platformLightDimmer, False, self.platformIndicator) 
            self.freightHouse.turnOnLightBefore(arrivalTime, 2, self.dockLight, self.dockLightDimmer, False, self.dockIndicator)                                    
                                  
    def handle (self):
        
        self.waitChange(self.scheduleTimes)
        self.scheduleArrival()
        self.scheduleDeparture()
        
        return True
            
DevilsGulchFreightHouse().start()
