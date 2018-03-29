import jarray
import jmri
import java.util.Random
import time
from time import mktime
import threading
from threading import Timer
from datetime import datetime, timedelta, date
#import pytz


class BuildingLights(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):

        #print "Initializing building light scheduler"
        
        self.debug = True

        self.startTime = time.localtime()
        
        self.bldgLights = []
        self.onTime = []
        self.offTime = []
        self.isOn = []
        self.isSensor = []
        
        #
        # Init sensors to known state.
        sensors.provideSensor("TO East Green").setState(ACTIVE)
        sensors.provideSensor("TO West Green").setState(ACTIVE)        

        #
        #  Create the scheduler
        #self.scheduler = sched.scheduler(time.time, time.sleep)

#         self.bldgLights.append(lights.provideLight("NL78")) # Mine Bldg Roof Sign
#         self.onTime.append(15)
#         self.offTime.append(5)
#         self.isOn.append(True)

#         self.bldgLights.append(lights.provideLight("NL74")) # Mine Bldg Loading Dock
#         self.onTime.append(10)
#         self.offTime.append(10)
#         self.isOn.append(False)
# 
#         self.bldgLights.append(lights.provideLight("NL70")) # Mine Bldg Side Door
#         self.onTime.append(5)
#         self.offTime.append(5)
#         self.isOn.append(False)

        self.bldgLights.append(sensors.provideSensor("Winding House Side Door")) # Winding House Side Door
        self.onTime.append(10)
        self.offTime.append(5)
        self.isOn.append(False)
        self.isSensor.append(True)

        self.bldgLights.append(lights.provideLight("NL84")) # Turntable 1
        self.onTime.append(10)
        self.offTime.append(5)
        self.isOn.append(True)
        self.isSensor.append(False)        

#         self.bldgLights.append(lights.provideLight("NL72")) # Mine Bldg Level 2 - Locker Room
#         self.onTime.append(15)
#         self.offTime.append(8)
#         self.isOn.append(False)
        
        self.bldgLights.append(lights.provideLight("NL73")) # Mine Bldg Level 3 Bridge
        self.onTime.append(12)
        self.offTime.append(7)
        self.isOn.append(False)
        self.isSensor.append(False)                
   
        self.bldgLights.append(sensors.provideSensor("Winding House 2nd Floor Inside")) # Winding House 2nd Floor Inside
        self.onTime.append(11)
        self.offTime.append(8)
        self.isOn.append(True)
        self.isSensor.append(True)                

        self.bldgLights.append(sensors.provideSensor("Winding House Bridge")) # Winding House Bridge
        self.onTime.append(10)
        self.offTime.append(5)
        self.isOn.append(True)
        self.isSensor.append(True)                
               

        #
        #  Big lights in winding house 
        self.windingHouseEngineRoom = sensors.provideSensor("Winding House Engine Room")


        self.demoModeListener = self.DemoModeListener()
        self.demoModeListener.init(self.demoOff, 20)
        
        self.privateModeListener = self.DemoModeListener()
        self.privateModeListener.init(self.demoOff, 120)

        self.demoMode = sensors.provideSensor("Building Light Demo")
        self.demoMode.setState(jmri.Sensor.ACTIVE)
        self.demoMode.addPropertyChangeListener(self.demoModeListener)
        
        self.privateSwitch = sensors.provideSensor("Private")
        self.privateSwitch.setState(INACTIVE)        
        self.privateSwitch.addPropertyChangeListener(self.privateModeListener)
        #
        #  Schedule demo mode to end
        #self.scheduler.enter(60*15, 1, self.demoOff, argument=(self.demoMode,))
        threading.Timer(60*15, self.demoOff, [self.demoMode]).start()

        #
        #  Turn all lights off
        #for i in range(0, len(self.bldgLights)) :
        #    self.bldgLights[i].setState(jmri.jmrix.nce.NceLight.OFF)
        #    self.waitMsec(500)

        #self.waitMsec(1000)
        #
        #  Flash all lights on start up
        for i in range(0, len(self.bldgLights)) :            
            self.bldgLights[i].setState(jmri.jmrix.nce.NceLight.OFF)
            self.waitMsec(5000)

        self.sequenceTurntableLights(jmri.jmrix.nce.NceLight.OFF)
        #
        #  Schedule all lights to go on.
        for i in range(0, len(self.bldgLights)) :
            print "Scheduling init turnOn for " + self.bldgLights[i].getUserName()            
            #self.scheduler.enter(30*(i+1), 1, self.turnOn, argument=(self.bldgLights[i], self.onTime[i], self.offTime[i]))
            threading.Timer(30*(i+1), self.turnOn, [self.bldgLights[i], self.onTime[i], self.offTime[i], self.isSensor[i]]).start()


        #
        #  Schedule the big lights in the winding house
        #self.scheduler.enter(10,1, self.windingHouseOn, argument=(self.windingHouseLights, 10, 10))
        threading.Timer(10, self.windingHouseOn, [self.windingHouseEngineRoom, 10, 10]).start()        


        #self.scheduler.run()                                 


        #Initialize Turntable indicators
        #self.ttIndicators = [];
        #self.ttIndicators.append(sensors.provideSensor("TT Track 2 Indicator"));
        #self.ttIndicators.append(sensors.provideSensor("TT Track 3 Indicator"));
        #self.ttIndicators.append(sensors.provideSensor("TT Track 4 Indicator"));
        #self.ttIndicators.append(sensors.provideSensor("TT Track 5 Indicator"));
        #self.ttIndicators.append(sensors.provideSensor("TT Track 6 Indicator"));                
        #for i in range (len(self.ttIndicators)) :
        #    sen = self.ttIndicators[i]
        #    sen.requestUpdateFromLayout()
        #    knownState = sen.getKnownState()
        #    rawState = sen.getRawState()
        #    print "TT Known State = " + str(knownState)
        #    print "TT Raw State = " + str(rawState)            
        #    if (knownState == ACTIVE) :
        #        print "Setting turntable track " + str(i+2) + " ACTIVE"
        #    else :
        #        print "Setting turntable track " + str(i+2) + " INACTIVE"                
        #    sen.setState(knownState)

        
    class DemoModeListener(java.beans.PropertyChangeListener) :
        def init(self, callback, delayMinutes):
            self.demoOff = callback
            self.delayMinutes = delayMinutes

        def propertyChange(self, event):
            if (event.source.getState() == jmri.Sensor.ACTIVE) :
                #
                #  Schedule demo mode to end
                #self.scheduler.enter(60*self.delayMinutes, 1, self.demoOff, argument=(event.source,))
                threading.Timer(60*self.delayMinutes, self.demoOff, [event.source]).start()                                
            return  
        
    def demoOff(self, sensor) :
        import jmri
        sensor.setState(jmri.Sensor.INACTIVE)        
        return  

        
    def turnOn(self, light, onTime, offTime, isSensor):
        import jmri
        import math

        #
        #  Speed things up when first starting for demo

        print "Turning on " + light.getUserName() + " for " + str(onTime) + " minutes"
        if (isSensor) :
            light.setState(ACTIVE)
        else:
            light.setState(jmri.jmrix.nce.NceLight.ON)            
        #self.waitMsec(500)
        #light.setState(jmri.jmrix.nce.NceLight.ON)
        #self.waitMsec(500)
        #light.setState(jmri.jmrix.nce.NceLight.ON)        
#         delaySec = ((onTime / 2) + java.util.Random().nextInt(int(onTime/2)))  * 60
#         if (self.demoMode.getState() == jmri.Sensor.ACTIVE) :
#             delaySec = math.ceil (float(delaySec) / 2.0)
            
        print light.getUserName() + " on"
        #delay =  datetime.fromtimestamp(time.time(), pyzt.timezone('America/Chicago')) + timedelta(minutes=onTime)
        #print " Scheduling " + light.getUserName() + " to turn off in " + str(delay.total_seconds()) + " seconds"
        threading.Timer(onTime * 60, self.turnOff, [light, onTime, offTime, isSensor]).start()

        if (light.getUserName() == "Turntable 1") :
            self.sequenceTurntableLights(jmri.jmrix.nce.NceLight.ON)            
            
        ##print "Dimmer for " + light.getUserName() + " is " + dim
        #    if (java.util.Random().nextInt(5) > 3) :
        #        lights.provideLight(dim).setState(jmri.jmrix.nce.NceLight.ON)
        #    else :
        #        lights.provideLight(dim).setState(jmri.jmrix.nce.NceLight.OFF)

                
    def turnOff(self, light, onTime, offTime, isSensor):
        import jmri
        import math

        print "Turning off " + light.getUserName()
        if (isSensor) :
            light.setState(INACTIVE)
        else :
            light.setState(jmri.jmrix.nce.NceLight.OFF)        
        #self.waitMsec(500)
        #light.setState(jmri.jmrix.nce.NceLight.OFF)
        #self.waitMsec(500)
        #light.setState(jmri.jmrix.nce.NceLight.OFF)        
#         delaySec = ((offTime / 2) + java.util.Random().nextInt(int(offTime/2))) * 60
# 
#         if (self.demoMode.getState() == jmri.Sensor.ACTIVE) :            
#             delaySec = math.ceil (float(delaySec) / 2.0)        


        #self.scheduler.enter(delaySec, 1, self.turnOn, argument=(light, onTime, offTime))
        
        #delay =  datetime.fromtimestamp(time.time(), pyzt.timezone('America/Chicago')) + timedelta(minutes=int(offTime))
        #print "Scheduling turnOn for " + light.getUserName() + " after " + str(delay.total_seconds())        
        threading.Timer(offTime*60, self.turnOn, [light, onTime, offTime]).start()        

        if (light.getUserName() == "Turntable 1") :
            self.sequenceTurntableLights(jmri.jmrix.nce.NceLight.OFF)


    def sequenceTurntableLights(self, state) :
        delayMsec = 2000 + java.util.Random().nextInt(2000)            
        self.waitMsec(delayMsec)
        nextLight = lights.provideLight("NL82") # Turntable 2
        nextLight.setState(state)
        delayMsec = 2000 + java.util.Random().nextInt(2000)            
        self.waitMsec(delayMsec)
        nextLight = lights.provideLight("NL83") # Water Tower
        nextLight.setState(state)

            
    def windingHouseOn(self, throttle, onTime, offTime):
        import jmri
        import math
        
        self.windingHouseEngineRoom.setState(ACTIVE)
        delaySec = ((onTime / 2) + java.util.Random().nextInt(int(onTime/2)))  * 60

        if (self.demoMode.getState() == jmri.Sensor.ACTIVE) :                        
            delaySec = math.ceil (float(delaySec) / 2.0)        

        #self.scheduler.enter(delaySec, 1, self.windingHouseOff, argument=(throttle, onTime, offTime))
        threading.Timer(delaySec, self.windingHouseOff, [throttle, onTime, offTime]).start()        
        
    def windingHouseOff(self, throttle, onTime, offTime):
        import jmri
        import math
        
        self.windingHouseEngineRoom.setState(INACTIVE)        
        delaySec = ((offTime / 2) + java.util.Random().nextInt(int(offTime/2))) * 60

        if (self.demoMode.getState() == jmri.Sensor.ACTIVE) :                                    
            delaySec = math.ceil (float(delaySec) / 2.0)                

        #self.scheduler.enter(delaySec, 1, self.windingHouseOn,  argument=(throttle, onTime, offTime))                
        threading.Timer(delaySec, self.windingHouseOn, [throttle, onTime, offTime]).start()        

                              
    def handle (self):
        while (True) :
            #print "in Handle"
            self.waitMsec(5000)

#         for event in self.scheduler.queue :
#             print "Canceling scheduled event"
#             self.scheduler.cancel(event)
            
        return self.bldgLightSwitch.getState() == jmri.Sensor.ACTIVE
            
BuildingLights().start()
