import jarray
import jmri
import java.util.Random
import sched, time

#Created on Jan 29, 2017

class Depot(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):
        #
        #  Create the scheduler
        self.scheduler = sched.scheduler(time.time, time.sleep)        
               
        self.trainPresentSensor = sensors.provideSensor("OS: Freight House")
        
        self.t1FHSensor = sensors.provideSensor("OS: T1 Freight House");
        self.t1DSensor = sensors.provideSensor("OS: T1 Depot");
        self.t1WTSensor = sensors.provideSensor("OS: T1 Water Tower");
        self.t1BSensor = sensors.provideSensor("OS: T1 Bridge");                        
        
        self.occupancySensors = [];
        self.occupancySensors.append(self.t1FHSensor);
        self.occupancySensors.append(self.t1DSensor);
        self.occupancySensors.append(self.t1WTSensor);
        self.occupancySensors.append(self.t1BSensor); 
        
        self.stove = lights.provideLight("NL100");
        self.platformLights = lights.provideLight("NL101");
        self.waitingRoomLights = lights.provideLight("NL102");
        self.officeLight = lights.provideLight("NL103");  
        self.signLights = lights.provideLight("NL104");
        self.indicatorLights = lights.provideLight("NL105");
                               
#        self.blockListener = self.BlockListener()
#        self.blockListener.init(self.scheduler, lights)   
#        self.trainPresentSensor.addPropertyChangeListener(self.blockListener)

        self.scheduler.run()                                         

#    class BlockListener(java.beans.PropertyChangeListener) :
#        def init(self, scheduler, lights):
#            self.scheduler = scheduler
#            self.lights = lights

#        def propertyChange(self, event):
#            print "freight house changed"
#            if (event.source.getState() == jmri.Sensor.ACTIVE) :
#                #  Train arrived (occupancy sensor active)
#                self.trainArrived()    
#            else :
#                self.trainDeparted()    
#            return
        
    #
    #  Train arriving soon
    #  -- Turn on office lights
    #  -- Light stoves
    #  -- Turn on platform lights dim
    #  -- Turn on waiting room lights dim
    def trainArriving(self):
        print "Train arriving at depot";
        self.scheduler = sched.scheduler(time.time, time.sleep)                
        self.turnOn (self.officeLight, None, False, None) # Turn on office lights 
        self.turnOn (self.stove, None, False, None) # Light stoves
        self.scheduler.enter(60*2, 1, self.turnOn, argument=(self.platformLights, lights.provideLight("NL106"), True, lights.provideLight("IL101")))          
        self.scheduler.enter(60*3, 1, self.turnOn, argument=(self.waitingRoomLights, lights.provideLight("NL107"), True, lights.provideLight("IL102"))) 
        self.scheduler.enter(60*4, 1, self.turnOn, argument=(self.indicatorLights, None, True, None))                                   

        self.scheduler.run();
    #
    #  Train arrived
    # -- Turn on sign lights
    # -- Turn platform lights on bright
    # -- Turn waiting room lights on bright                       
    def trainArrived(self):
        print "Train arrived at depot";        
        self.scheduler = sched.scheduler(time.time, time.sleep)        
        self.turnOn (self.signLights, None, False, None) # Turn on sign lights        
        
        self.turnOn (self.platformLights, lights.provideLight("NL106"), False, lights.provideLight("IL101")) # Turn on platform lights
        

        self.scheduler.enter(10, 1, self.turnOn, argument=(self.waitingRoomLights, lights.provideLight("NL107"), False, lights.provideLight("IL102")))
        self.scheduler.run();
    #
    #  Train departed
    #  -- Turn platform lights dim
    #  -- Turn waiting room lights dim
    #  -- Turn off sign lights.
    def trainDeparted(self):

        self.scheduler = sched.scheduler(time.time, time.sleep)        
        self.turnOff(self.indicatorLights, None);
        self.scheduler.enter(60*3, 1, self.turnOn, argument=(self.platformLights, lights.provideLight("NL106"), True, lights.provideLight("IL101"))) #Platform
        self.scheduler.enter(60*4, 1, self.turnOn, argument=(self.waitingRoomLights, lights.provideLight("NL107"), True,lights.provideLight("IL102"))) #Inside  
        #
        #  Schedule lights to go off
        self.scheduler.enter(60*5, 1, self.turnOff, argument=(self.signLights,None)) #Sign


        self.scheduler.enter(60*6, 1, self.turnOff, argument=(self.platformLights, lights.provideLight("IL101"))) #Platform
        self.scheduler.enter(60*7, 1, self.turnOff, argument=(self.waitingRoomLights, lights.provideLight("IL102"))) #Inside
        self.scheduler.enter(60*8, 1, self.turnOff, argument=(self.officeLight,None)) #Office                
        self.scheduler.run()
     
    #
    #  Depot is idle (20 minutes)   
    def depotIdle(self):
        print "Depot idle";
        self.scheduler = sched.scheduler(time.time, time.sleep)                
        delayMinutes = java.util.Random().nextInt(3) + 1;
        self.scheduler.enter(60*delayMinutes, 1, self.turnOff, argument=(self.stove,None)) #Stove 
        delayMinutes = java.util.Random().nextInt(6) + 2;
        self.scheduler.enter(60*delayMinutes, 1, self.turnOn, argument=(self.officeLight, None, False, None)) #Office         
        self.scheduler.enter(60*(delayMinutes+1), 1, self.turnOn, argument=(self.indicatorLights, None, False, None)) #Indicators                
        
        self.scheduler.enter(60*(delayMinutes+10), 1, self.turnOff, argument=(self.indicatorLights, None)) #Indicators                
        self.scheduler.enter(60*(delayMinutes+11), 1, self.turnOff, argument=(self.officeLight, None)) #Office                        
                
        self.scheduler.run();
    
    def turnOn(self, light, dim, isDim, indicator):
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
        if (indicator is not None) :
            indicator.setTargetIntensity(0.0)                     
            indicator.setState(jmri.jmrix.nce.NceLight.OFF)
        light.setState(jmri.jmrix.nce.NceLight.OFF)

            
    def handle (self):

        self.waitChange (self.occupancySensors)
        if (self.t1FHSensor.getState() == jmri.Sensor.ACTIVE) :
            self.trainArriving()
        if (self.t1DSensor.getState() == jmri.Sensor.ACTIVE) : 
            self.trainArrived()            
        if (self.t1WTSensor.getState() == jmri.Sensor.ACTIVE) :            
            self.trainDeparted()
        if (self.t1BSensor.getState() == jmri.Sensor.INACTIVE
            and self.t1FHSensor.getState() == jmri.Sensor.INACTIVE
            and self.t1DSensor.getState() == jmri.Sensor.INACTIVE
            and self.t1WTSensor.getState() == jmri.Sensor.INACTIVE) :
            self.depotIdle()
            

#        for event in self.scheduler.queue :
#            self.scheduler.cancel(event)
            
        return True
            
Depot().start()
