import jmri
import java.util.Random
import datetime
from datetime import datetime, timedelta, date
import time
from time import mktime
import threading
from threading import Timer
#import pytz
from foggyhollow.arduino import TriStateSensor
#Created on Jan 29, 2017

class Depot(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):

        self.debug = sensors.provideSensor("Private").getState() == ACTIVE               
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

        self.mineTourSwitch = sensors.provideSensor("Mine Tour")
        
        self.scheduleTimes = []
        self.scheduleTimes.append(memories.provideMemory("Arrives Depot"))
        
        self.stove = lights.provideLight("NL100");
        #self.platformLights = lights.provideLight("NL101");
        #self.waitingRoomLights = lights.provideLight("NL102");
        self.officeLight = lights.provideLight("NL103");  
        self.signLights = lights.provideLight("NL104");
        self.indicatorLights = lights.provideLight("NL105");


        self.platformLights = TriStateSensor(sensors.provideSensor("Depot Platform Dim"),
                                          sensors.provideSensor("Depot Platform On"),
                                          sensors.provideSensor("Depot Platform Off"))

        self.waitingRoomLights = TriStateSensor(sensors.provideSensor("Depot Waiting Room Dim"),
                                          sensors.provideSensor("Depot Waiting Room On"),
                                          sensors.provideSensor("Depot Waiting Room Off"))                

        #self.roofSign = sensors.provideSensor("Mine Bldg Roof")
        #self.roofDim = sensors.provideSensor("Mine Bldg Roof Dim")
        #self.roofIndicator = lights.provideLight("IL145")

        self.roofSignOn = sensors.provideSensor("Mine Building Roof Sign On") # Mine Bldg Roof Sign
        self.roofSignOff = sensors.provideSensor("Mine Building Roof Sign Off") # Mine Bldg Roof Sign
        self.roofSignDim = sensors.provideSensor("Mine Building Roof Sign Dim") # Mine Bldg Roof Sign        
        self.roofSign = TriStateSensor(self.roofSignDim, self.roofSignOn, self.roofSignOff)        

        self.loadingDock = TriStateSensor(sensors.provideSensor("Mine Building Loading Dock Dim"),
                                          sensors.provideSensor("Mine Building Loading Dock On"),
                                          sensors.provideSensor("Mine Building Loading Dock Off"))


        
#        self.waitingRoomLightDimmer = lights.provideLight("NL107")
#        self.waitingRoomIndicator = lights.provideLight("IL102")
        
#        self.platformLightDimmer = lights.provideLight("NL106")
#        self.platformIndicator = lights.provideLight("IL101")
        
        self.waterTower = lights.provideLight("NL83") # Water Tower
        self.waterSpout = sensors.provideSensor ("Water Spout")
        
        self.trainOrderEast = masts.getSignalMast("SM Depot East")
        self.trainOrderWest = masts.getSignalMast("SM Depot West")
        self.switchStand = lights.provideLight("LL130")

        self.trainOrderEast.setAspect("Stop")
        self.waitMsec(2000)        
        self.trainOrderWest.setAspect("Stop")
        self.waitMsec(2000)
        self.trainOrderEast.setAspect("Approach")
        self.waitMsec(1500)        
        self.trainOrderWest.setAspect("Approach")
        self.waitMsec(2000)        
        self.trainOrderEast.setAspect("Clear")
        self.waitMsec(2000)
        self.trainOrderWest.setAspect("Clear")        
        
        self.waterSpout.setState(INACTIVE);

        #
        #  Play with locomotive
        self.locomotive = self.getThrottle(32, False)
        self.locomotive.setF0(True)
        #self.locomotive.setF4(True)


        #
        #  Turn lights on idle locomotives
        self.locomotive41 = self.getThrottle(41, False)
        self.locomotive41.setF0(True)  # Headlight & Firebox
        self.locomotive41.setF11(True) # Marker Lights

        self.locomotive6 = self.getThrottle(6, False)
        self.locomotive6.setF0(True)  # Headlight & Firebox
        self.locomotive6.setF5(True) # Marker Lights
        self.locomotive6.setF11(True) # Cab Light        
        self.locomotive6.setIsForward(True)
        
        #
        #  Turn the lights in the Combine Car "Red Fox" #512 on
        self.combine512 = self.getThrottle(512, True) 
        self.combine512.setF0(True) #  Turn on marker lights

        self.eastBound = True

    def scheduleSignalMast(self, arrivalTime, offset, myMast, myAspect) :
        xtime = arrivalTime + timedelta(minutes=offset)
        delay = xtime - datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.setSignalMast, [myMast, myAspect]).start()

    def setSignalMast(self, myMast, myAspect):
        myMast.setAspect(myAspect)


    def scheduleTurntableLights(self, arrivalTime, offset, isOn) :
        xtime = arrivalTime + timedelta(minutes=offset)
        delay = xtime - datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.sequenceTurntableLights, [isOn]).start()
        
    def sequenceTurntableLights(self, isOn) :

        state = jmri.jmrix.nce.NceLight.OFF
        
        if (isOn) :
            state = jmri.jmrix.nce.NceLight.ON
                     
        nextLight = lights.provideLight("NL84") # Turntable 1
        nextLight.setState(state)                     
        delayMsec = 2000 + java.util.Random().nextInt(2000)            
        self.waitMsec(delayMsec)
                     
        nextLight = lights.provideLight("NL82") # Turntable 2
        nextLight.setState(state)
        delayMsec = 2000 + java.util.Random().nextInt(2000)            
        self.waitMsec(delayMsec)
                     
        nextLight = lights.provideLight("NL83") # Water Tower
        nextLight.setState(state)        
        
                               
    def turnOn(self, sensor, dim, isDim, indicator):
        if (self.debug) :
            print "Turning on " + sensor.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M");                       
        if (dim is not None and indicator is not None) :
            if (isDim) :
                dim.setState(jmri.jmrix.nce.NceLight.ON) 
                indicator.setTargetIntensity(0.5) 
            else:          
                dim.setState(jmri.jmrix.nce.NceLight.OFF)
                indicator.setTargetIntensity(1.0)             
                indicator.setState(jmri.jmrix.nce.NceLight.ON)
                
        try: 
            sensor.setState(ACTIVE)
            self.waitMsec(250)
            sensor.setState(ACTIVE)
            self.waitMsec(250)
            sensor.setState(ACTIVE)
        except:
            sensor.setState(jmri.jmrix.nce.NceLight.ON)
            self.waitMsec(250)
            sensor.setState(jmri.jmrix.nce.NceLight.ON)
            self.waitMsec(250)
            sensor.setState(jmri.jmrix.nce.NceLight.ON)        


    def turnOff(self, sensor, indicator):
        if (self.debug) :
            print "Turning off " + sensor.getUserName() + " at " + datetime.fromtimestamp(mktime(time.localtime())).strftime("%I:%M");                               
        if (indicator is not None) :
            indicator.setTargetIntensity(0.0)                     
            indicator.setState(jmri.jmrix.nce.NceLight.OFF)
        try :
            sensor.setState(jmri.jmrix.nce.NceLight.OFF)
            self.waitMsec(250)
            sensor.setState(jmri.jmrix.nce.NceLight.OFF)
            self.waitMsec(250)
            sensor.setState(jmri.jmrix.nce.NceLight.OFF)
        except:
            sensor.setState(INACTIVE)
            self.waitMsec(250)
            sensor.setState(INACTIVE)
            self.waitMsec(250)
            sensor.setState(INACTIVE)            
    
    #
    #  level = 0 -> off
    #  level = 50 -> dim
    #  level = 126 -> bright
    def setCombineLights(self, level):
        self.combine512.setSpeedSetting(level)  # Turn on interior lights
        self.combine512.setF0(level > 0)

    def scheduleCombineLights(self, baseTime, offset, level):
        if (self.debug) :
            print "Scheduling combine lights"
        if (offset < 0) :            
            xtime = baseTime - timedelta(minutes=abs(offset))
        else :
            xtime = baseTime + timedelta(minutes=abs(offset))

        delay = xtime -  datetime.fromtimestamp(time.time())                
        threading.Timer(delay.total_seconds(), self.setCombineLights, [level]).start()
        if (self.debug) :
            print "Combine lights scheduled for level " + str(level)


    def setLocomotiveFunction(self, function, state):
        if (self.debug) :
            print " Setting locomotive function " + str(function) + " to state = " + str(state)
        if (function == 2 ) :
            self.locomotive.setF2(True)
            self.waitMsec(2000)
            self.locomotive.setF2(False)

        elif (function == 1) : # bell
            self.locomotive.setF1(state)
        elif (function == 3) : # toot
            self.locomotive.setF3(not self.locomotive.getF3())
        elif (function == 4) : # Quill
            self.locomotive.setF4(not self.locomotive.getF4())
        elif (function == 0) : # Headlight
            self.locomotive.setF0(state)
        elif (function == 9) :
            self.locomotive.setF9(state)
        elif (function == 10) :
            self.locomotive.setF10(state)
        elif (function == 11) : #Firebox
            self.locomotive.setF11(state)
        elif (function == 12) : # Cab
            self.locomotive.setF12(state)
        elif (function == 16) : # Blowdown
            self.locomotive.setF16(state)                        
        elif (function == 21) : # Water Fill
            self.locomotive.setF21(state)
        if (self.debug) :            
            print " Done Setting locomotive function " + str(function) + " to state = " + str(state)            
            
    def scheduleLocomotive(self, baseTime, offset, function, state):
        if (self.debug) :
            print "Scheduling locomotive"
        if (offset < 0) :            
            xtime = baseTime - timedelta(minutes=abs(offset))
        else :
            xtime = baseTime + timedelta(minutes=abs(offset))

        delay = xtime -  datetime.fromtimestamp(time.time())                
        threading.Timer(delay.total_seconds(), self.setLocomotiveFunction, [function, state]).start()
        if (self.debug) :
            print "Locomotive function scheduled " + str(function)        

    def dimLightsAfter(self, departureTime, offset, light, dimmer, indicator):
        xtime = departureTime + timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.turnOn, [light, dimmer, True, indicator]).start()

    def turnOffLightsAfter(self, departureTime, offset, light, indicator):
        xtime = departureTime + timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.turnOff, [light, indicator]).start()
            
    def turnOffLightsBefore(self, departureTime, offset, light, indicator):
        xtime = departureTime - timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.turnOff, [light, indicator]).start()            

    def turnOnLightBefore(self, arrivalTime, offset, light, dimmer, isDim, indicator):
        xtime = arrivalTime - timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.turnOn, [light, dimmer, isDim, indicator]).start()
            
    def turnOnLightAfter(self, arrivalTime, offset, light, dimmer, isDim, indicator):
        xtime = arrivalTime + timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.turnOn, [light, dimmer, isDim, indicator]).start()            

    def waterTowerAnimation (self, state) :
        self.waterSpout.setState(state)
        #self.waitMsec(3000)
        #print "Activating locomotive fill-water sound"
        #self.locomotive.setF21(ACTIVE) # Water fill
        #self.waitMsec(10000)
        #self.locomotive.setF21(INACTIVE) # Water fill
        #print "Deactivating locomotive fill-water sound"        
        #self.waterSpout.setState(INACTIVE)
        #print "Animating water tower complete"        
            
    def animateWaterTower(self, arrivalTime, offset, state) :
        if (self.debug) :
            print " Scheduling water tower "
        xtime = arrivalTime + timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.waterTowerAnimation, [state]).start()                    
        
    def scheduleDeparture(self):
        memVal = memories.provideMemory("Departs Depot").getValue()
        if (memVal != None) :
            depStr = memVal[0:19]            
            departureTime = datetime.strptime( memVal, "%Y-%m-%d %H:%M:%S.%f" )

            if (self.eastBound) :
                self.scheduleSignalMast(departureTime, 2, self.trainOrderWest, "Clear")
                self.scheduleSignalMast(departureTime, 2.2, self.trainOrderEast, "Approach")
                self.scheduleSignalMast(departureTime, 5, self.trainOrderEast, "Clear")
                self.scheduleSignalMast(departureTime, 10, self.trainOrderWest, "Not Lit")
                self.scheduleSignalMast(departureTime, 10.2, self.trainOrderEast, "Not Lit")                                                
            else:
                self.scheduleSignalMast(departureTime, 2, self.trainOrderEast, "Clear")
                self.scheduleSignalMast(departureTime, 2.2, self.trainOrderWest, "Approach")
                self.scheduleSignalMast(departureTime, 5, self.trainOrderWest, "Clear")
                self.scheduleSignalMast(departureTime, 10, self.trainOrderWest, "Not Lit")
                self.scheduleSignalMast(departureTime, 10.2, self.trainOrderEast, "Not Lit")                                

            self.eastBound = not self.eastBound

            self.scheduleLocomotive(departureTime, -0.3, 2, False) # Whistle
            self.scheduleLocomotive(departureTime, -0.2, 2, False) # Whistle
            self.scheduleLocomotive(departureTime, 0.0, 1, True) # Bell
            self.scheduleLocomotive(departureTime, 1.0, 1, False) # Bell
            self.scheduleLocomotive(departureTime, 1.2, 12, False) # Cab            
            self.scheduleLocomotive(departureTime, 2.0, 10, False) # Class. Light
            self.scheduleLocomotive(departureTime, 2.2, 0, False) # HeadLight                                                            
            
            self.turnOffLightsAfter(departureTime, 3, self.signLights, None)
            self.platformLights.scheduleStateChangeAfter(TriStateSensor.DIM, depStr, 3)
            self.waitingRoomLights.scheduleStateChangeAfter(TriStateSensor.DIM, depStr, 5.5)            
#            self.dimLightsAfter(departureTime, 3, self.platformLights, self.platformLightDimmer, self.platformIndicator)
#            self.dimLightsAfter(departureTime, 5.5, self.waitingRoomLights, self.waitingRoomLightDimmer, self.waitingRoomIndicator)

            if (self.mineTourSwitch.getState() != ACTIVE) :
                self.scheduleTurntableLights(departureTime, 7.5, False)
            
            self.turnOffLightsAfter(departureTime, 7, self.indicatorLights, None)             
#            self.turnOffLightsAfter(departureTime, 8, self.platformLights, self.platformIndicator)
            self.platformLights.scheduleStateChangeAfter(TriStateSensor.OFF, depStr, 8)                        
            self.turnOffLightsAfter(departureTime, 9, self.stove, None) 
#            self.turnOffLightsAfter(departureTime, 10, self.waitingRoomLights, self.waitingRoomIndicator) 
            self.waitingRoomLights.scheduleStateChangeAfter(TriStateSensor.OFF, depStr, 10)            
            self.turnOffLightsAfter(departureTime, 11, self.officeLight, None)
            self.turnOffLightsAfter(departureTime, 12, self.switchStand, None)

#            self.turnOnLightAfter(departureTime, 6, self.roofSign, self.roofDim, True, self.roofIndicator)
            self.roofSign.scheduleStateChangeAfter(TriStateSensor.DIM, depStr, 6.0)
            self.loadingDock.scheduleStateChangeAfter(TriStateSensor.DIM, depStr, 6.6)            
#            self.turnOnLightAfter(departureTime, 6.6, self.loadingDock, self.loadingDockDim, True, self.loadingDockIndicator)

            #self.turnOffLightsAfter(departureTime, 9.5, self.roofSign, self.roofIndicator)
            #self.turnOffLightsAfter(departureTime, 10.5, self.loadingDock, self.loadingDockIndicator)                                    
            self.roofSign.scheduleStateChangeAfter(TriStateSensor.OFF, depStr, 9.5)
            self.loadingDock.scheduleStateChangeAfter(TriStateSensor.OFF, depStr, 10.5)
            
            self.turnOffLightsBefore(departureTime, 3, self.waterTower, None)                  
            
                    
    def scheduleArrival(self):
        memVal = memories.provideMemory("Arrives Depot").getValue()
        if (memVal != None) :
            arrStr = memVal[0:19]
            arrivalTime = datetime.strptime( memVal, "%Y-%m-%d %H:%M:%S.%f" )
            

            self.scheduleCombineLights(arrivalTime, -5, 50)
            self.scheduleCombineLights(arrivalTime, -1, 127) 
            self.scheduleCombineLights(arrivalTime, 10, 50) 
            self.scheduleCombineLights(arrivalTime, 11, 0)


            self.scheduleLocomotive(arrivalTime, -4.4, 10, True) # Class. Light
            self.scheduleLocomotive(arrivalTime, -4.3, 0, True) # HeadLight                                                                        
            self.scheduleLocomotive(arrivalTime, -4.2, 4, True) #Quill
            self.scheduleLocomotive(arrivalTime, -2.5, 2, False) # Whistle            
            self.scheduleLocomotive(arrivalTime, -1, 1, True) # Bell on
            self.scheduleLocomotive(arrivalTime, 0, 1, False) # Bell off
            self.scheduleLocomotive(arrivalTime, 0.2, 3, False) # Brake set.
            self.scheduleLocomotive(arrivalTime, 0.3, 12, True) # Cab light

            if (self.mineTourSwitch.getState() != ACTIVE) :
                self.scheduleTurntableLights(arrivalTime, -7, True)
            
            #  Station master arrives & turns on office light
            #self.turnOnLightBefore(arrivalTime, 15.5, self.roofSign, self.roofDim, True, self.roofIndicator)
            #self.turnOnLightBefore(arrivalTime, 16, self.loadingDock, self.loadingDockDim, True, self.loadingDockIndicator)            
            self.roofSign.scheduleStateChangeBefore(TriStateSensor.DIM, arrStr, 15.5)
            self.loadingDock.scheduleStateChangeBefore(TriStateSensor.DIM, arrStr, 16)
            
            self.turnOnLightBefore(arrivalTime, 15, self.officeLight, None, False, None)
            self.waitingRoomLights.scheduleStateChangeBefore(TriStateSensor.DIM, arrStr, 14)
#            self.turnOnLightBefore(arrivalTime, 14, self.waitingRoomLights, self.waitingRoomLightDimmer, True, self.waitingRoomIndicator)
            self.turnOnLightBefore(arrivalTime, 13, self.stove, None, False, None)
            
            if (self.eastBound) :
                self.scheduleSignalMast(arrivalTime, -4, self.trainOrderEast, "Stop")
                self.scheduleSignalMast(arrivalTime, -4.1, self.trainOrderWest, "Approach")                       
            else:
                self.scheduleSignalMast(arrivalTime, -4, self.trainOrderWest, "Stop")
                self.scheduleSignalMast(arrivalTime, -4.1, self.trainOrderEast, "Approach")                                       

            self.turnOnLightBefore(arrivalTime, 11, self.switchStand, None, False, None)
            
 #           self.turnOnLightBefore(arrivalTime, 10, self.platformLights, self.platformLightDimmer, True, self.platformIndicator)
            self.platformLights.scheduleStateChangeBefore(TriStateSensor.DIM, arrStr, 10)
            if (self.debug) :
                self.turnOnLightBefore(arrivalTime, 9, self.indicatorLights, None, False, None)                        
#            self.turnOnLightBefore(arrivalTime, 5, self.waitingRoomLights, self.waitingRoomLightDimmer, False, self.waitingRoomIndicator)            
            self.waitingRoomLights.scheduleStateChangeBefore(TriStateSensor.ON, arrStr, 5)
            self.platformLights.scheduleStateChangeBefore(TriStateSensor.ON, arrStr, 4)            
#self.turnOnLightBefore(arrivalTime, 4, self.platformLights, self.platformLightDimmer, False, self.platformIndicator) 
            self.turnOnLightBefore(arrivalTime, 3, self.signLights, None, False, None)            
            #self.turnOnLightBefore(arrivalTime, 2, self.roofSign, self.roofDim, False, self.roofIndicator)
            #self.turnOnLightBefore(arrivalTime, 1.8, self.loadingDock, self.loadingDockDim, False, self.loadingDockIndicator)            
            self.roofSign.scheduleStateChangeBefore(TriStateSensor.ON, arrStr, 2.0)
            self.loadingDock.scheduleStateChangeBefore(TriStateSensor.ON, arrStr, 1.8)
            
            self.turnOnLightAfter(arrivalTime, 1.5, self.waterTower, None, False, None)
            self.animateWaterTower(arrivalTime, 1.6, ACTIVE)
            self.scheduleLocomotive(arrivalTime, 1.7, 21, True) # Water fill  on
            self.scheduleLocomotive(arrivalTime, 2.9, 21, False) # Water fill off
            self.animateWaterTower(arrivalTime, 2.3, INACTIVE)
            if (java.util.Random().nextInt(100) > 50) :
                self.scheduleLocomotive(arrivalTime, 3.4, 16, True) # Blow Down  on
                self.scheduleLocomotive(arrivalTime, 3.6, 16, False) # Blow Down off            
            self.turnOffLightsAfter(arrivalTime, 4.2, self.waterTower, None)            
          
                                       
    def handle (self):
        self.debug = sensors.provideSensor("Private").getState() == ACTIVE  
        
        self.waitChange(self.scheduleTimes)
        self.waitMsec(2000)
        self.scheduleArrival()
        self.scheduleDeparture()
                     
        return True
            
Depot().start()
