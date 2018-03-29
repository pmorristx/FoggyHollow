import jmri
from datetime import datetime, timedelta, date
import time
from time import mktime
import threading
from threading import Timer
#import pytz

#Created on Jan 29, 2017

class Building(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self, arrivesMemoryVariable, departsMemoryVariable):
        sensors = jmri.InstanceManager.sensorManagerInstance()
        memories = jmri.InstanceManager.memoryManagerInstance()
        
        self.debug = sensors.provideSensor("Private").getState() == jmri.Sensor.ACTIVE               
        self.trainPresentSensor = sensors.provideSensor("OS: Freight House")                       
        
        self.scheduleTimes = []
        self.scheduleTimes.append(memories.provideMemory(arrivesMemoryVariable))        
        self.scheduleTimes.append(memories.provideMemory(departsMemoryVariable))                
        
#     def handle (self):
#         self.debug = sensors.provideSensor("Private").getState() == ACTIVE  
#         
#         self.waitChange(self.scheduleTimes)
#         self.scheduleArrival()
#         self.scheduleDeparture()        

    def turnOn(self, light, dim, isDim, indicator):
        if (self.debug) :
            print "Turning on " + light.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M");                       
        if (dim is not None) :
            if (isDim) :
                dim.setState(jmri.jmrix.nce.NceLight.ON)
                self.waitMsec(250)
                dim.setState(jmri.jmrix.nce.NceLight.ON)
                self.waitMsec(250)
                dim.setState(jmri.jmrix.nce.NceLight.ON)

                indicator.setTargetIntensity(0.5) 
            else:          
                dim.setState(jmri.jmrix.nce.NceLight.OFF)
                self.waitMsec(250)
                dim.setState(jmri.jmrix.nce.NceLight.OFF)
                self.waitMsec(250)
                dim.setState(jmri.jmrix.nce.NceLight.OFF)

                indicator.setTargetIntensity(1.0)             
                indicator.setState(jmri.jmrix.nce.NceLight.ON)
                
        light.setState(jmri.jmrix.nce.NceLight.ON)
        self.waitMsec(250)
        light.setState(jmri.jmrix.nce.NceLight.ON)
        self.waitMsec(250)
        light.setState(jmri.jmrix.nce.NceLight.ON)


    def turnOnSensor(self, sensor, dim, isDim, indicator):
        if (self.debug) :
            print "Turning on " + sensor.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M");                       
        if (dim is not None) :
            if (isDim) :
                dim.setState(ACTIVE)
                self.waitMsec(250)
                dim.setState(ACTIVE)
                self.waitMsec(250)
                dim.setState(ACTOVE)

            else:          
                dim.setState(INACTIVE)
                self.waitMsec(250)
                dim.setState(INACTIVE)
                self.waitMsec(250)
                dim.setState(INACTIVE)

                indicator.setState(ACTIVE)
                
        sensor.setState(ACTIVE)
        self.waitMsec(250)
        sensor.setState(ACTIVE)
        self.waitMsec(250)
        sensor.setState(ACTIVE)
        
        
    def turnOff(self, light, indicator):
        if (self.debug) :
            print "Turning off " + light.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M");                               
        if (indicator is not None) :
            indicator.setTargetIntensity(0.0)                     
            indicator.setState(jmri.jmrix.nce.NceLight.OFF)
        light.setState(jmri.jmrix.nce.NceLight.OFF)
        self.waitMsec(250)
        light.setState(jmri.jmrix.nce.NceLight.OFF)
        self.waitMsec(250)
        light.setState(jmri.jmrix.nce.NceLight.OFF)


        
    def turnOffSensor(self, sensor, indicator):
        if (self.debug) :
            print "Turning off " + sensor.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M");                               
        if (indicator is not None) :
            indicator.setState(INACTIVE)
        sensor.setState(INACTIVE)
        self.waitMsec(250)
        sensor.setState(INACTIVE)
        self.waitMsec(250)
        sensor.setState(INACTIVE)        

        
    def dimLightsAfter(self, departureTime, offset, light, dimmer, indicator):
            xtime = departureTime + timedelta(minutes=offset)
#            delay = xtime -  datetime.fromtimestamp(time.time(), pytz.timezone('America/Chicago'))
            delay = xtime -  datetime.fromtimestamp(time.time())            
            threading.Timer(delay.total_seconds(), self.turnOn, [light, dimmer, True, indicator]).start()

    def turnOffLightsAfter(self, departureTime, offset, light, indicator):
            print "ScheduleDeparture current time = " +  datetime.fromtimestamp(time.time()).strftime("%I:%M")
            xtime = departureTime + timedelta(minutes=offset)
            print "ScheduleDeparture " + str(offset) + "  minute delay =  " + xtime.strftime("%I:%M")        
            delay = xtime -  datetime.fromtimestamp(time.time())
            threading.Timer(delay.total_seconds(), self.turnOff, [light, indicator]).start() 
                  
    def turnOnLightsAfter(self, arrivalTime, offset, light, dimmer, isDim, indicator):
            xtime = arrivalTime + timedelta(minutes=offset)
            delay = xtime -  datetime.fromtimestamp(time.time())
            threading.Timer(delay.total_seconds(), self.turnOn, [light, dimmer, isDim, indicator]).start()            
                                
    def turnOnLightBefore(self, arrivalTime, offset, light, dimmer, isDim, indicator):
            xtime = arrivalTime - timedelta(minutes=offset)
            delay = xtime -  datetime.fromtimestamp(time.time())
            threading.Timer(delay.total_seconds(), self.turnOn, [light, dimmer, isDim, indicator]).start()


    def turnOffSensorAfter(self, departureTime, offset, light, indicator):
            print "ScheduleDeparture current time = " +  datetime.fromtimestamp(time.time()).strftime("%I:%M")
            xtime = departureTime + timedelta(minutes=offset)
            print "ScheduleDeparture " + str(offset) + "  minute delay =  " + xtime.strftime("%I:%M")        
            delay = xtime -  datetime.fromtimestamp(time.time())
            threading.Timer(delay.total_seconds(), self.turnOffSensor, [light, indicator]).start() 
                  
    def turnOnSensorAfter(self, arrivalTime, offset, light, dimmer, isDim, indicator):
            xtime = arrivalTime + timedelta(minutes=offset)
            delay = xtime -  datetime.fromtimestamp(time.time())
            threading.Timer(delay.total_seconds(), self.turnOnSensor, [light, dimmer, isDim, indicator]).start()            
                                
    def turnOnSensorBefore(self, arrivalTime, offset, light, dimmer, isDim, indicator):
            xtime = arrivalTime - timedelta(minutes=offset)
            delay = xtime -  datetime.fromtimestamp(time.time())
            threading.Timer(delay.total_seconds(), self.turnOnSensor, [light, dimmer, isDim, indicator]).start()            
