import jarray
import jmri
import java.util.Random
import threading
from threading import Timer

#Created on Jan 29, 2017

class FreightHouse(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):
        #
        self.t1FHSensor = sensors.provideSensor("OS: T1 Freight House");
        self.t1DSensor = sensors.provideSensor("OS: T1 Depot");
        self.t1WTSensor = sensors.provideSensor("OS: T1 Water Tower");
        self.t1BSensor = sensors.provideSensor("OS: T1 Bridge");             
               
        self.occupancySensors = [];
        self.occupancySensors.append(self.t1FHSensor);
        self.occupancySensors.append(self.t1DSensor);
        self.occupancySensors.append(self.t1WTSensor);
        self.occupancySensors.append(self.t1BSensor);      
        
        self.stove = lights.provideLight("NL120");
        self.platform = lights.provideLight("NL121");
        self.office = lights.provideLight("NL122");
        self.dock = lights.provideLight("NL123");        
        
        self.platformIndicator = lights.provideLight("IL121");
        self.officeIndicator = lights.provideLight("IL122");
        self.dockIndicator = lights.provideLight("IL123"); 
        
        self.platformDim = lights.provideLight("NL124");               
        self.officeDim = lights.provideLight("NL125");               
        self.dockDim = lights.provideLight("NL126");                               
                

    #
    #  Building idle - go home
    #    - Turn off platform lights.
    #    - Turn off dock light
    #    - Turn off stove
    #    - Turn off office light
    def idle(self):
        
        #
        #  Schedule lights to go off
        threading.Timer(60*8, self.turnOff, [self.dock, self.dockIndicator]).start()
        threading.Timer(60*9, self.turnOff, [self.platform, self.platformIndicator]).start()
        threading.Timer(60*10, self.turnOff, [self.stove, None]).start()
        threading.Timer(60*1,self.turnOff, [self.office, self.officeIndicator]).start()

    #
    #  Train arriving soon.
    #    - Turn on office light dim
    #    - Light stove
    #    - Turn on platform light dim
    def trainArriving(self):
        self.turnOn (self.office, self.officeDim, True, self.officeIndicator) 
        threading.Timer(30, self.turnOn, [self.stove, None, False, None]).start()
        threading.Timer(60, self.turnOn, [self.platform, self.platformDim, True, self.platformIndicator]).start()                  

    #
    #  Train has arrived
    #    - Turn office light on bright
    #    - Turn platform light on bright
    #    - Turn dock light on bright
    def trainArrived(self):
        self.turnOn (self.office, self.officeDim, False, self.officeIndicator)
        threading.Timer(30, self.turnOn, [self.platform, self.platformDim, False, self.platformIndicator]).start()
        threading.Timer(60, self.turnOn, [self.dock, self.dockDim, False, self.dockIndicator]).start()      

    #
    #  Train has left
    #    - Dim dock light
    #    - Dim platform light
    #    - Dim office light
    def trainDeparted(self):
        threading.Timer(60*4, self.turnOn, [self.dock, self.dockDim, True, self.dockIndicator]).start() #Dock
        threading.Timer(60*6, self.turnOn, [self.platform, self.platformDim, True, self.platformIndicator]).start() #Platform
        threading.Timer(60*10, self.turnOn, [self.office, self.officeDim, True, self.officeIndicator]).start() #Inside  

        if (java.util.Random().nextInt(10) > 5) :
            on = java.util.Random().nextInt(3) + 7
            threading.Timer(60*on, self.turnOn, [self.dock, self.dockDim, False, self.dockIndicator]).start() #Dock
            threading.Timer(60*(on+1), self.turnOn, [self.dock, self.dockDim, True, self.dockIndicator]).start() #Dock

#     def turnOn(self, light, dim, isDim, indicator):
#         print "Turnon "
#         if(isDim) :
#             dim.setState(jmri.jmrix.nce.NceLight.ON) 
#             indicator.setTargetIntensity(0.5) 
#         else:          
#             dim.setState(jmri.jmrix.nce.NceLight.OFF)
#             indicator.setTargetIntensity(1.0)             
#             indicator.setState(jmri.jmrix.nce.NceLight.ON)                  
#         light.setState(jmri.jmrix.nce.NceLight.ON)
        
    def turnOn(self, light, dim, isDim, indicator):
        if (self.debug) :
            print "Turning on " + light.getUserName() + " at " + datetime.fromtimestamp(time.time()).strftime("%I:%M");                               
        if (dim is not None) :
            if (isDim) :
                dim.setState(jmri.jmrix.nce.NceLight.ON) 
                indicator.setTargetIntensity(0.5) 
            else:          
                dim.setState(jmri.jmrix.nce.NceLight.OFF)
                indicator.setTargetIntensity(1.0)             
                indicator.setState(jmri.jmrix.nce.NceLight.ON)
                
        light.setState(jmri.jmrix.nce.NceLight.ON) 
        
    def turnOff(self, light, indicator):
        if (self.debug) :
            print "Turning off " + light.getUserName() + " at " + datetime.fromtimestamp(time.time()).strftime("%I:%M");                                       
        if (indicator is not None) :
            indicator.setTargetIntensity(0.0)                     
            indicator.setState(jmri.jmrix.nce.NceLight.OFF)
        light.setState(jmri.jmrix.nce.NceLight.OFF)               

            
    def handle (self):
        
        self.debug = sensors.provideSensor("Private").getState() == ACTIVE               
                
        self.waitChange (self.occupancySensors)
        if (self.t1FHSensor.getState() == jmri.Sensor.ACTIVE) :
            self.trainArrived()
        if (self.t1DSensor.getState() == jmri.Sensor.ACTIVE) : 
            self.trainDeparted()            
        if (self.t1WTSensor.getState() == jmri.Sensor.ACTIVE) :            
            self.idle()
        if (self.t1BSensor.getState() == jmri.Sensor.ACTIVE) :
            self.trainArriving()        
            
        return True
            
FreightHouse().start()
