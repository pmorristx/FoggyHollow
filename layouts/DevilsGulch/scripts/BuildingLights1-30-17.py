import jarray
import jmri
import java.util.Random
import sched, time

class BuildingLights(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):

        print "Initializing building light scheduler"
        
        self.debug = True

        self.startTime = time.time()
        
        self.bldgLights = []
        self.onTime = []
        self.offTime = []
        self.isOn = []

        #
        #  Create the scheduler
        self.scheduler = sched.scheduler(time.time, time.sleep)

        self.bldgLights.append(lights.provideLight("NL78")) # Mine Bldg Roof Sign
        self.onTime.append(15)
        self.offTime.append(5)
        self.isOn.append(True)

        self.bldgLights.append(lights.provideLight("NL74")) # Mine Bldg Loading Dock
        self.onTime.append(10)
        self.offTime.append(10)
        self.isOn.append(False)

        self.bldgLights.append(lights.provideLight("NL70")) # Mine Bldg Side Door
        self.onTime.append(5)
        self.offTime.append(5)
        self.isOn.append(False)

        self.bldgLights.append(lights.provideLight("NL76")) # Winding House Side Door
        self.onTime.append(10)
        self.offTime.append(5)
        self.isOn.append(False)

        self.bldgLights.append(lights.provideLight("NL84")) # Turntable 1
        self.onTime.append(10)
        self.offTime.append(5)
        self.isOn.append(True)                

        self.bldgLights.append(lights.provideLight("NL72")) # Mine Bldg Level 2 - Locker Room
        self.onTime.append(15)
        self.offTime.append(8)
        self.isOn.append(False)
        
        self.bldgLights.append(lights.provideLight("NL73")) # Mine Bldg Level 3 Bridge
        self.onTime.append(12)
        self.offTime.append(7)
        self.isOn.append(False)                
   
        self.bldgLights.append(lights.provideLight("NL75")) # Winding House 2nd Floor Inside
        self.onTime.append(11)
        self.offTime.append(8)
        self.isOn.append(True)

        self.bldgLights.append(lights.provideLight("NL77")) # Winding House Bridge
        self.onTime.append(10)
        self.offTime.append(5)
        self.isOn.append(True)

        self.bldgLights.append(lights.provideLight("NL121")) # Freight House Platform
        self.onTime.append(15)
        self.offTime.append(5)
        self.isOn.append(True)

        self.bldgLights.append(lights.provideLight("NL122")) # Freight House Inside
        self.onTime.append(15)
        self.offTime.append(5)
        self.isOn.append(True)

        self.bldgLights.append(lights.provideLight("NL123")) # Freight House Dock
        self.onTime.append(15)
        self.offTime.append(5)
        self.isOn.append(True)                

        lights.provideLight("NL120").setState(jmri.jmrix.nce.NceLight.ON) # Freight House Stove


        #
        #  Big lights in winding house are controlled by the motor decoder
        self.windingHouseLights = self.getThrottle(99, False)
        self.windingHouseEngineRoom = lights.provideLight("NL99")


        self.demoModeListener = self.DemoModeListener()
        self.demoModeListener.init(self.scheduler, self.demoOff)


        self.demoMode = sensors.provideSensor("Building Light Demo")
        self.demoMode.setState(jmri.Sensor.ACTIVE)
        self.demoMode.addPropertyChangeListener(self.demoModeListener)

        #
        #  Schedule demo mode to end
        self.scheduler.enter(60*15, 1, self.demoOff, argument=(self.demoMode,))        

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
            self.scheduler.enter(30*(i+1), 1, self.turnOn, argument=(self.bldgLights[i], self.onTime[i], self.offTime[i]))


        #
        #  Schedule the big lights in the winding house
        self.scheduler.enter(10,1, self.windingHouseOn, argument=(self.windingHouseLights, 10, 10))

        self.scheduler.run()                                 

    class DemoModeListener(java.beans.PropertyChangeListener) :
        def init(self, scheduler, callback):
            self.scheduler = scheduler
            self.demoOff = callback

        def propertyChange(self, event):
            if (event.source.getState() == jmri.Sensor.ACTIVE) :
                #
                #  Schedule demo mode to end
                self.scheduler.enter(60*15, 1, self.demoOff, argument=(event.source,))        
            return


        
    def demoOff(self, sensor) :
        import jmri
        sensor.setState(jmri.Sensor.INACTIVE)        
        return
    
    def turnOn(self, light, onTime, offTime):
        import jmri
        import math

        #
        #  Speed things up when first starting for demo

        print "Turning on " + light.getUserName()                    
        light.setState(jmri.jmrix.nce.NceLight.ON)
        self.waitMsec(500)
        light.setState(jmri.jmrix.nce.NceLight.ON)
        self.waitMsec(500)
        light.setState(jmri.jmrix.nce.NceLight.ON)        
        delaySec = ((onTime / 2) + java.util.Random().nextInt(int(onTime/2)))  * 60
        if (self.demoMode.getState() == jmri.Sensor.ACTIVE) :
            delaySec = math.ceil (float(delaySec) / 2.0)
            
        print "Scheduling turnOff for " + light.getUserName()
        self.scheduler.enter(delaySec, 1, self.turnOff, argument=(light, onTime, offTime))

        if (light.getUserName() == "Turntable 1") :
            self.sequenceTurntableLights(jmri.jmrix.nce.NceLight.ON)

        if (light.getUserName().startswith("Freight")) :
            dim = "NL12" + str(int(light.getSystemName()[4:5]) + 3);
            print "Dimmer for " + light.getUserName() + " is " + dim
            if (java.util.Random().nextInt(5) > 3) :
                lights.provideLight(dim).setState(jmri.jmrix.nce.NceLight.ON)
            else :
                lights.provideLight(dim).setState(jmri.jmrix.nce.NceLight.OFF)

                
    def turnOff(self, light, onTime, offTime):
        import jmri
        import math

        print "Turning off " + light.getUserName()        
        light.setState(jmri.jmrix.nce.NceLight.OFF)
        self.waitMsec(500)
        light.setState(jmri.jmrix.nce.NceLight.OFF)
        self.waitMsec(500)
        light.setState(jmri.jmrix.nce.NceLight.OFF)        
        delaySec = ((offTime / 2) + java.util.Random().nextInt(int(offTime/2))) * 60

        if (self.demoMode.getState() == jmri.Sensor.ACTIVE) :            
            delaySec = math.ceil (float(delaySec) / 2.0)        

        print "Scheduling turnOn for " + light.getUserName()
        self.scheduler.enter(delaySec, 1, self.turnOn, argument=(light, onTime, offTime))

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
        
        throttle.setF0(True)
        self.windingHouseEngineRoom.setState(jmri.jmrix.nce.NceLight.ON)
        delaySec = ((onTime / 2) + java.util.Random().nextInt(int(onTime/2)))  * 60

        if (self.demoMode.getState() == jmri.Sensor.ACTIVE) :                        
            delaySec = math.ceil (float(delaySec) / 2.0)        

        self.scheduler.enter(delaySec, 1, self.windingHouseOff, argument=(throttle, onTime, offTime))
        
    def windingHouseOff(self, throttle, onTime, offTime):
        import jmri
        import math
        
        throttle.setF0(False)
        self.windingHouseEngineRoom.setState(jmri.jmrix.nce.NceLight.OFF)        
        delaySec = ((offTime / 2) + java.util.Random().nextInt(int(offTime/2))) * 60

        if (self.demoMode.getState() == jmri.Sensor.ACTIVE) :                                    
            delaySec = math.ceil (float(delaySec) / 2.0)                

        self.scheduler.enter(delaySec, 1, self.windingHouseOn,  argument=(throttle, onTime, offTime))                
                  
    def handle (self):
        while (True) :
            print "in Handle"
            self.waitMsec(5000)

        for event in self.scheduler.queue :
            print "Canceling scheduled event"
            self.scheduler.cancel(event)
            
        return self.bldgLightSwitch.getState() == jmri.Sensor.ACTIVE
            
BuildingLights().start()
