import jmri
import java.util.Random
import datetime
from datetime import datetime, timedelta, date
import time
from time import mktime
import threading
from threading import Timer
from MineTrain import MineTrain
from foggyhollow.arduino import TriStateSensor

class WindingHouse(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):

        self.debug = sensors.provideSensor("Private").getState() == ACTIVE               
        self.trainPresentSensor = sensors.provideSensor("OS: Freight House")

        locoNumber = memories.provideMemory("L1 Loco Number").getValue()
        self.mineTrain = MineTrain()
        self.mineTrain.init(locoNumber, 1)
        self.tippleLights = sensors.provideSensor("Tipple Lights")
        self.bridgeLights = sensors.provideSensor("Lake Cavern Bridge")
        self.stoppingAtTipple = sensors.provideSensor("Stopping at Tipple")
        self.stoppingAtLake = sensors.provideSensor("Stopping at Lake")
        self.tippleSensor = sensors.provideSensor("OS:L1:Tipple")
        self.leftTunnelSensor = sensors.provideSensor("OS:L1:Left Tunnel")
        self.frontTunnelSensor = sensors.provideSensor("OS:L1:Front Tunnel")
        self.rightTunnelSensor = sensors.provideSensor("OS:L1:Right Tunnel")
        self.backTunnelSensor = sensors.provideSensor("OS:L1:Back Tunnel")
        self.backCavernSensor = sensors.provideSensor("OS:L1:Back Cavern")
        self.hoistCavernEntranceSensor = sensors.provideSensor("OS:L1:Hoist Cavern Entrance")
        self.hoistCavernEOTSensor = sensors.provideSensor("OS:L1:Hoist EOT")
        self.hoistCavernSensor = sensors.provideSensor("OS:L1:Hoist Cavern")

    
        self.splash = []
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/singleSwimmer.wav"))        
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash.wav"))
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash2.wav"))
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash3.wav"))
        self.splash.append(self.mineTrain.loadSoundFile("preference:resources/sounds/Splash4.wav"))         

        self.rightTunnelSignal = masts.getSignalMast("SM-L1-RT-E")
        self.hoistCavernEntranceSignal = masts.getSignalMast("SM-L1-HCE-E")
        self.backTunnelSignal = masts.getSignalMast("SM-L1-E-Back Tunnel")
        
        self.raiseHoistSound = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Short-Short-Long-Signal.wav"))
        self.lowerHoistSound = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Short-Long-Signal.wav"))        
        
        
        self.t1FHSensor = sensors.provideSensor("OS: T1 Freight House");
        self.t1DSensor = sensors.provideSensor("OS: T1 Depot");
        self.t1WTSensor = sensors.provideSensor("OS: T1 Water Tower");
        self.t1BSensor = sensors.provideSensor("OS: T1 Bridge");
        
        self.roofSignOn = sensors.provideSensor("Mine Building Roof Sign On") # Mine Bldg Roof Sign
        self.roofSignOff = sensors.provideSensor("Mine Building Roof Sign Off") # Mine Bldg Roof Sign
        self.roofSignDim = sensors.provideSensor("Mine Building Roof Sign Dim") # Mine Bldg Roof Sign        
        self.roofSign = TriStateSensor(self.roofSignDim, self.roofSignOn, self.roofSignOff)

        self.boilerFire = TriStateSensor(sensors.provideSensor("Winding House Boiler Low"),
                                       sensors.provideSensor("Winding House Boiler High"),
                                       sensors.provideSensor("Winding House Boiler Off"))
        self.boilerFire.setState(TriStateSensor.DIM)
        self.boilerFire.setPeriodicStateChange(0.0, 5.0, 1.0, 1)
        
        self.loadingDock = TriStateSensor(sensors.provideSensor("Mine Building Loading Dock Dim"),
                                          sensors.provideSensor("Mine Building Loading Dock On"),
                                          sensors.provideSensor("Mine Building Loading Dock Off"))
        self.sideDoor = sensors.provideSensor("Mine Bldg Side Soor") # Mine Bldg Side Door
        self.lockerRoom = sensors.provideSensor("Mine Bldg S2") # Mine Bldg Level 2 - Locker Room
        self.tipple = sensors.provideSensor("Mine Bldg S3") # Mine Bldg Tipple        

        self.roofSign.setState(TriStateSensor.OFF)
        
        
        self.occupancySensors = [];
        self.occupancySensors.append(self.t1FHSensor);
        self.occupancySensors.append(self.t1DSensor);
        self.occupancySensors.append(self.t1WTSensor);
        self.occupancySensors.append(self.t1BSensor);
        
        self.hoistLevelIndicators = [];
        self.hoistLevelIndicators.append(sensors.provideSensor("Hoist L4 Indicator"));
        self.hoistLevelIndicators.append(sensors.provideSensor("Hoist L3 Indicator"));
        self.hoistLevelIndicators.append(sensors.provideSensor("Hoist L2 Indicator"));
        self.hoistLevelIndicators.append(sensors.provideSensor("Hoist L1 Indicator"));
        self.hoistLevelIndicators.append(sensors.provideSensor("Hoist S1 Indicator"));
        self.hoistLevelIndicators.append(sensors.provideSensor("Hoist S2 Indicator"));
        self.hoistLevelIndicators.append(sensors.provideSensor("Hoist S3 Indicator"));
        
        for i in range (len(self.hoistLevelIndicators)) :
            sen = self.hoistLevelIndicators[i]
            sen.requestUpdateFromLayout()
            knownState = sen.getKnownState()
            print "Known state [" + str(i) + "] is " + str(knownState)
            rawState = sen.getRawState()
            print "Raw state [" + str(i) + "] is " + str(rawState)            


        self.hoistCallButtons = [];
        self.hoistCallButtons.append(sensors.provideSensor("IS Call Hoist To L4"));
        self.hoistCallButtons.append(sensors.provideSensor("IS Call Hoist To L3"));
        self.hoistCallButtons.append(sensors.provideSensor("IS Call Hoist To L2"));
        self.hoistCallButtons.append(sensors.provideSensor("IS Call Hoist To L1"));
        self.hoistCallButtons.append(sensors.provideSensor("IS Call Hoist To S1"));
        self.hoistCallButtons.append(sensors.provideSensor("IS Call Hoist To S2"));
        self.hoistCallButtons.append(sensors.provideSensor("IS Call Hoist To S3"));

        self.hoistBottomSensor = sensors.provideSensor("Hoist L3 Indicator")                  
        
        self.scheduleTimes = []
        self.scheduleTimes.append(memories.provideMemory("Arrives Depot"))
        
        self.bridgeLight = sensors.provideSensor("Winding House Bridge");
        self.sideDoorLight = sensors.provideSensor("Winding House Side Door");
        self.engineRoomLights = sensors.provideSensor("Winding House Engine Room");
        self.engineRoomDim = sensors.provideSensor("Winding House Engine Room Dim");
        self.secondFloorLight = sensors.provideSensor("Winding House 2nd Floor Inside");

#        self.boilerIntensity = sensors.provideSensor("Winding House Boiler Intensity")
#        self.boilerFire = sensors.provideSensor("Winding House Boiler Fire")        
        
        self.level1Light = sensors.provideSensor("Level 1 Light");
        self.level1LightDim = sensors.provideSensor("Level 1 Light Dim");
        
        self.engineRoomLightDimmer = sensors.provideSensor("Winding House Engine Room Dim")
        self.currentHoistIdx = -1 
        self.mineTour = sensors.provideSensor("Mine Tour");
        
#        self.boilerIntensity.setState(INACTIVE)
#        self.boilerFire.setState(ACTIVE)
        
    def findHoist(self) :
        i = 0
        while (self.currentHoistIdx < 0 and i < len(self.hoistLevelIndicators)) :
            if (self.hoistLevelIndicators[i].getState() == ACTIVE) :
                self.currentHoistIdx = i
            i = i + 1
                               
    def turnOn(self, sensor, dim, isDim, indicator):
        if (self.debug) :
            print "Turning on " + sensor.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M");                       
        if (dim is not None) :
            if (isDim) :
                dim.setState(ACTIVE) 
            else:          
                dim.setState(INACTIVE)
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
        if (self.debug) :
            print "Turned on " + sensor.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M");            
            
    def turnOffDimmable(self, onSensor, offSensor, dimSensor):
        if (self.debug) :
            print "Turning off " +sensor.getUserName() + " at " + datetime.fromtimestamp(mktime(time.localtime())).strftime("%I:%M");                               
        try:
            onSensor.setState(INACTIVE)
            offSensor
            self.waitMsec(250)
            onSensor.setState(INACTIVE)        
            self.waitMsec(250)
            onSensor.setState(INACTIVE) 
        except:
            sensor.setState(jmri.jmrix.nce.NceLight.OFF)
            self.waitMsec(250)
            sensor.setState(jmri.jmrix.nce.NceLight.OFF)        
            self.waitMsec(250)
            sensor.setState(jmri.jmrix.nce.NceLight.OFF)
        if (self.debug) :
            print "Turned off " +sensor.getUserName() + " at " + datetime.fromtimestamp(mktime(time.localtime())).strftime("%I:%M");
            
    def turnOff(self, sensor, indicator):
        if (self.debug) :
            print "Turning off " +sensor.getUserName() + " at " + datetime.fromtimestamp(mktime(time.localtime())).strftime("%I:%M");                               
        try:
            sensor.setState(INACTIVE)
            self.waitMsec(250)
            sensor.setState(INACTIVE)        
            self.waitMsec(250)
            sensor.setState(INACTIVE) 
        except:
            sensor.setState(jmri.jmrix.nce.NceLight.OFF)
            self.waitMsec(250)
            sensor.setState(jmri.jmrix.nce.NceLight.OFF)        
            self.waitMsec(250)
            sensor.setState(jmri.jmrix.nce.NceLight.OFF)
        if (self.debug) :
            print "Turned off " +sensor.getUserName() + " at " + datetime.fromtimestamp(mktime(time.localtime())).strftime("%I:%M");                               
                               

    def dimLightAfter(self, departureTime, offset, sensor, dimmer, indicator):
        xtime = departureTime + timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.turnOn, [sensor, dimmer, True, indicator]).start()

    def turnOffLightAfter(self, departureTime, offset, light, indicator):
        xtime = departureTime + timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.turnOff, [light, indicator]).start()
        if (self.debug) :
            print "Scheduled turning off " + light.getUserName()
            
    def turnOffLightBefore(self, departureTime, offset, light, indicator):
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

        
        
    def scheduleDeparture(self):
        memVal = memories.provideMemory("Departs Depot").getValue()
        if (memVal != None) :
            departureTime = datetime.strptime( memVal, "%Y-%m-%d %H:%M:%S.%f" )

            if (self.mineTour.getState() != ACTIVE) :
                self.turnOffLightAfter(departureTime, 5, self.engineRoomDim, None)
                self.turnOffLightAfter(departureTime, 9, self.bridgeLight, None) 
                self.turnOffLightAfter(departureTime, 11, self.sideDoorLight, None)    
                
                self.turnOffLightAfter(departureTime, 8, self.engineRoomLights, None)
                self.turnOnLightAfter(departureTime, 8, self.secondFloorLight, None, False, None)
            

    def scheduleArrival(self):
        memVal = memories.provideMemory("Arrives Depot").getValue()
        if (memVal != None) :
            arrivalTime = datetime.strptime( memVal, "%Y-%m-%d %H:%M:%S.%f" )

            if (self.mineTour.getState() == ACTIVE) :
                if (self.roofSign.getState() == TriStateSensor.ON) :                
                    arrivalTime = datetime.fromtimestamp(time.time())                
                    #  Schedule a mine tour to begin 1 minute after train arrives ... there are delays in the mine tour function
                    print "Scheduling mine tour"

                    threading.Timer(10, self.mineTourB, [arrivalTime]).start()
            else :
                #  Turn on winding house lights
                self.turnOnLightBefore(arrivalTime, 15, self.engineRoomLights, None, False, None)
                if (java.util.Random().nextInt(100) < 50) :
                    self.turnOnLightBefore(arrivalTime, 15, self.engineRoomDim, None, False, None)
                else :
                    self.turnOffLightBefore(arrivalTime, 15, self.engineRoomDim, None)
                self.turnOnLightBefore(arrivalTime, 14, self.sideDoorLight, None, False, None)
                self.turnOnLightBefore(arrivalTime, 13, self.bridgeLight, None, False, None)
 
    def setHoistLevel (self, gotoIdx):
        if (self.mineTour.getState() == ACTIVE) :
            i = 0
            self.currentHoistIdx = -1
            while (self.currentHoistIdx < 0 and i < len(self.hoistLevelIndicators)) :
                if (self.hoistLevelIndicators[i].getState() == ACTIVE) :
                    self.currentHoistIdx = i
                i = i + 1        
            print "In setHoistLevel, currentHoistIdx = " + str(self.currentHoistIdx)
            if (self.currentHoistIdx > 0) :
                if (gotoIdx > self.currentHoistIdx) :  # Going up
                    self.raiseHoistSound.play()
                    self.waitMsec(8000)
                elif (gotoIdx < self.currentHoistIdx) :  # Going down
                    self.lowerHoistSound.play()
                    self.waitMsec(8000)
                if (self.mineTour.getState() == ACTIVE) :
                    self.hoistCallButtons[gotoIdx].setState(ACTIVE)

        
    
    def moveHoist(self, arrivalTime, offset, gotoIdx): 
        delta = timedelta(minutes=(abs(offset)))
        if (offset > 0) :
            xtime = arrivalTime + delta
        else :
            xtime = arrivalTime - delta        
        delay = xtime - datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.setHoistLevel, [gotoIdx]).start()
        print "Hoist scheduled to goto level " + str(gotoIdx) + " after " + str(delay.total_seconds()) + " seconds"



    def waitBlockOccupied(self, sensor):
        self.ostate = sensor.getState()
        self.waitingFor.setValue(sensor.getUserName())
        self.waitChange([sensor], 30000)
        if (self.ostate == sensor.getState()) :
            print "Sensor timed out " + sensor.getUserName()
        self.waitingFor.setValue("")
        return
        
    def undergroundTour(self) :
        #
        #  Find train  by running until it gets to tipple.
        self.stoppingAtTipple.setState(ACTIVE)
        self.mineTrain.startTrain(True)
        
        self.waitBlockOccupied(self.tippleSensor)
        if (self.rightTunnelSignal.getAspect() == "Stop"):
            self.waitMsec(2100)
            self.mineTrain.stopTrain()
            self.waitMsec(2000)
            self.mineTrain.startTrainSlow(False)

            # Stop at cavern entrance
            self.waitBlockOccupied(self.hoistCavernEntranceSensor)
            #
            #  Wait for cage to reach L3
            self.stoppingAtTipple.setState(INACTIVE)                
            self.waitSensorActive(self.hoistBottomSensor)

            #
            #  Wait for tourists to board train
            self.waitMsec(20000)

            #  Go back to tipple
            self.stoppingAtTipple.setState(ACTIVE)                                
            self.mineTrain.startTrainSlow(True)
            self.waitBlockOccupied(self.tippleSensor)
            self.mineTrain.stopTrain()
            self.waitMsec(10000)

            #
            #  Go to Lake Cavern
            self.stoppingAtTipple.setState(INACTIVE)
            self.stoppingAtLake.setState(ACTIVE)
            self.mineTrain.startTrainSlow(True)

            #  Turn on bridge lights when we enter tunnel
            self.waitBlockOccupied(self.rightTunnelSensor)
            self.bridgeLights.setState(ACTIVE)

            self.waitBlockOccupied(self.backCavernSensor)
            if (self.backTunnelSignal.getAspect() == "Stop") :

                self.waitMsec(1200)
                self.mineTrain.stopTrain()
                for i in range(0,5) :
                    splashProb = java.util.Random().nextInt(100)
                    delay = java.util.Random().nextInt(3)
                    if (splashProb > 20):
                        self.splash[i].play();
                        self.waitMsec(2000 * delay)                
                
                self.mineTrain.startTrainSlow(True)

                self.waitMsec(3000)
                self.bridgeLights.setState(INACTIVE)

            #
            #  wait for tourists to get off train
            self.waitBlockOccupied(self.hoistCavernEntranceSensor)
            self.mineTrain.stopTrain()
            self.waitMsec(20000)

            #
            #  Move train away from turnout
            self.mineTrain.startTrainSlow()
            self.waitBlockOccupied(self.tippleSensor)
            self.mineTrain.stopTrain()
                
        
    #
    #  Mine tour B takes visitors on a top-down tour of the mine.  First going up to the tipple & winding house, 
    #  then down to the locker room before going down into the mine.
    def mineTourB(self, arrivalTime):
        if (self.roofSign.getState() == TriStateSensor.ON) :
            self.findHoist()
            self.boilerFire.setState(TriStateSensor.ON)
#            self.boilerIntensity.setState(ACTIVE)
            self.roofSign.setState(TriStateSensor.ON)

            #  Roof sign indicates a tour in progress.  We don't start another tour (triggered by train arrival) if a tour is 
            #  already in progress.
            #self.mineBuilding.turnOnLightBefore(arrivalTime, 5, self.roofSign, None, False, None)
            
            #
            #  Begin tour.  Turn on side light and move cage to surface level.  Don't keep the side door light on while
            #  the tour is going.
            self.turnOnLightAfter(arrivalTime, 1, self.sideDoor, None, False, None)
            self.moveHoist(arrivalTime, 1, 4) # Move hoist to surface to pick up tourists
            self.turnOffLightAfter(arrivalTime, 4, self.sideDoor, None)
            
            #
            #  Go up to tipple level
            self.turnOnLightAfter(arrivalTime, 5, self.tipple, None, False, None)
            #self.moveHoist(arrivalTime, 8, 6) # Move hoist to tipple - Go up to tipple to see ore dump
            self.turnOnLightAfter(arrivalTime, 10, self.bridgeLight, None, False, None)
            self.turnOffLightAfter(arrivalTime, 12, self.bridgeLight, None)
            self.turnOffLightAfter(arrivalTime, 12, self.tipple, None)
            
            #
            #  Go down to locker level
            self.turnOnLightAfter(arrivalTime, 14, self.lockerRoom, None, False, None)                                    
            self.moveHoist(arrivalTime, 15, 5) # Move hoist to locker
            self.turnOffLightAfter(arrivalTime, 23, self.lockerRoom, None)

            
            self.moveHoist(arrivalTime, 25, 1) # Move hoist to mine level 3 - Tour mine
            self.undergroundTour()
              
                       
            #self.moveHoist(arrivalTime, 40, 0) # Move hoist to sump - Return down to thermal spring
            #self.moveHoist(arrivalTime, 50, 1) # Move hoist to mine level 3 - Back to main level - tram to Lake Cavern            
            self.turnOnLighAfter(arrivalTime, 60, self.level1Light, self.level1LightDim, False, None) 
            self.moveHoist(arrivalTime, 70, 3) # Move hoist to Level 1 - Shower level 
            
            self.turnOnLightAfter(arrivalTime, 75, self.lockerRoom, None, False, None)
            self.turnOnLighAfter(arrivalTime, 76, self.level1Light, self.level1LightDim, True, None)             
            self.moveHoist(arrivalTime, 80, 5) # Move hoist to locker 
            self.turnOffLightAfter(arrivalTime, 100, self.lockerRoom, None)                          

            self.turnOnLightAfter(arrivalTime, 93, self.sideDoor, None, False, None)
            self.moveHoist(arrivalTime, 95, 4) # Move hoist to surface
            self.turnOffLightAfter(arrivalTime, 105, self.sideDoor, None)                          

            self.turnOffLightAfter(arrivalTime, 109, self.level1Light, None)

            self.roofSign.scheduleStateChange(TriStateSensor.OFF, 2)
            
    def handle (self):
        self.debug = sensors.provideSensor("Private").getState() == ACTIVE  
        
        self.waitSensorChange(self.mineTour.getState(), self.mineTour)
        if (self.mineTour.getState() == ACTIVE) :
            self.waitMsec(2000)
            self.scheduleArrival()
            self.scheduleDeparture()
        else :
            self.roofSign.setState(TriStateSensor.OFF)
            self.scheduleArrival()
                     
        return True
            
WindingHouse().start()
