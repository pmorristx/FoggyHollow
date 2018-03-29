import jmri
import java.util.Random
import sys
from foggyhollow.arduino import TriStateSensor

class TippleTrain(jmri.jmrit.automat.AbstractAutomaton) :
    def init(self) :

        self.shuttingDown = False
        
        self.throttle = self.getThrottle(int(memories.provideMemory("L4 Locomotive").getValue()), False)

        self.activity = memories.provideMemory("S4 Action")
        
        self.BOT = sensors.provideSensor ("OS:L4:BOT")
        self.EOT = sensors.provideSensor ("OS:L4:Tipple-EOT")
        self.MineBldg = sensors.provideSensor("OS:L4:Mine Building")
        self.switch = sensors.provideSensor("S3 Auto")
        self.l3switch = sensors.provideSensor("L1 Auto")
        self.l2switch = sensors.provideSensor("L2 Auto")        
        self.mineBldgLoadingDockLight = sensors.provideSensor("Mine Bldg Loading Dock")
        self.mineBldgS2Light = sensors.provideSensor("Mine Bldg S2")
        self.mineBldgS3Light = sensors.provideSensor("Mine Bldg S3")        
        self.windingHouseBridgeLight = sensors.provideSensor("Winding House Bridge")
        self.gateLight = lights.provideLight("Tipple Gate Light")
        self.chuteLight = lights.provideLight("Tipple Chute Light")

        self.chuteLeft =  sensors.provideSensor("Tipple Chute Left")
        self.chuteRight =  sensors.provideSensor("Tipple Chute Right")        

        self.redLantern = lights.provideLight("LL97")
        self.whiteLantern = lights.provideLight("LL96")
        self.leftBridgeLight = lights.provideLight("LL92")
        self.rightBridgeLight = lights.provideLight("LL93")
        self.tippleLights = lights.provideLight("LL94")        


        self.roofSign = TriStateSensor(sensors.provideSensor("Mine Building Roof Sign Dim"),
                                          sensors.provideSensor("Mine Building Roof Sign On"),
                                          sensors.provideSensor("Mine Building Roof Sign Off"))

        self.roofSign.setState(TriStateSensor.DIM)
        
        self.whEngineRoom = TriStateSensor(sensors.provideSensor("Winding House Engine Room Dim"),
                                          sensors.provideSensor("Winding House Engine Room On"),
                                          sensors.provideSensor("Winding House Engine Room Off"))
        
        self.boilerFire = TriStateSensor(sensors.provideSensor("Winding House Boiler Low"),
                                       sensors.provideSensor("Winding House Boiler High"),
                                       sensors.provideSensor("Winding House Boiler Off"))
        
        self.level1Light = sensors.provideSensor("Level 1 Light");
        self.level1LightDim = sensors.provideSensor("Level 1 Light Dim");
        
        self.s1Button = sensors.provideSensor("IS Call Hoist To S1")
        self.s2Button = sensors.provideSensor("IS Call Hoist To S2")
        self.l3Button = sensors.provideSensor("IS Call Hoist To L3")                
        self.s1Indicator = sensors.provideSensor("Hoist S1 Indicator")
        self.s2Indicator = sensors.provideSensor("Hoist S2 Indicator")
        self.l3Indicator = sensors.provideSensor("Hoist L3 Indicator")        
        self.useHoist = sensors.provideSensor("Hoist Motor Enabled")
        
        self.loopCount = 0
        self.buildingLightDemo = sensors.provideSensor("Building Light Demo")
        self.random = java.util.Random()
        self.firstTime = True
        self.trainMoving = False

        masts.getSignalMast("Auto Train Indicator Mast").setAspect("Steady")        

        self.whEngineRoom.setPeriodicStateChange(.25, 3.0, 1.0, 0)
        self.boilerFire.setPeriodicStateChange(.25, 2.0, 5.0, 1)

        
        print "S3 Train Init Complete"


    def releaseSteam(self) :
        self.setActivityMsg("Blow out Boiler")        
        self.throttle.setF4(True)
        self.waitMsec(java.util.Random().nextInt(1000) + 1200)
        self.throttle.setF4(False)
        self.setActivityMsg("")                
        
    def forwardWhistle(self) :
        self.throttle.setF2(True)
        self.waitMsec(1600)
        self.throttle.setF2(False)
        self.waitMsec(750)
        self.throttle.setF2(True)
        self.waitMsec(1600)
        self.throttle.setF2(False)

    def reverseWhistle(self) :
        self.throttle.setF3(not self.throttle.getF3())
        self.waitMsec(600)
        self.throttle.setF3(not self.throttle.getF3())
        self.waitMsec(600)
        self.throttle.setF3(not self.throttle.getF3())


    def moveTrainForward(self) :
        if (not self.trainMoving) :
            self.throttle.setF5(False);
            self.throttle.setF7(False)
            self.throttle.setF8(False)            
            self.waitMsec(1000)                
            self.forwardWhistle()
            self.waitMsec(500)
            self.throttle.setF1(True)
            self.waitMsec(1000)
            self.throttle.setIsForward(True)
            self.throttle.setSpeedSetting(0.04)
            self.waitMsec(2000)
            self.throttle.setSpeedSetting(0.1)
            self.trainMoving = True

    def moveTrainReverse(self) :
        if (not self.trainMoving) :
            self.throttle.setF5(False);
            self.throttle.setF7(False)
            self.throttle.setF8(False)                        
            self.waitMsec(1000)        
            self.reverseWhistle()
            self.waitMsec(500)
            self.throttle.setF1(True)
            self.waitMsec(1000)
            self.throttle.setIsForward(False)
            self.throttle.setSpeedSetting(0.04)
            self.waitMsec(1500)        
            self.throttle.setSpeedSetting(0.1)
            self.trainMoving = True            
        
    def stopTrain (self) :
        if (self.trainMoving) :
            self.throttle.setF7(True)
            self.waitMsec(750)
            self.throttle.setSpeedSetting(0)
            self.waitMsec(1000)
            self.throttle.setF1(False)
            self.waitMsec(1200)
            self.throttle.setF3(not self.throttle.getF3())
            self.waitMsec(1000)
            self.throttle.setF5(True);
            self.trainMoving = False

    def turnOutTippleLights(self) :
        #if (self.redLantern.getState() == ON or self.whiteLantern.getState() == ON) :
            #self.waitSensorInactive(self.EOT)
        now = datetime.fromtimestamp(time.time())            
        self.turnOffLightAfter(now, 0, self.redLantern)
        self.turnOffLightAfter(now, 0, self.whiteLantern)
        self.turnOffLightAfter(now, .3, self.tippleLights)
        self.turnOffLightAfter(now, .5, self.leftBridgeLight)            

    def turnOnTippleLights(self) :
        now = datetime.fromtimestamp(time.time())            
        self.turnOnLightAfter(now, .1, self.rightBridgeLight)
        self.turnOnLightAfter(now, .25, self.whiteLantern)
        self.turnOffLightAfter(now, .4, self.rightBridgeLight)
        self.turnOnLightAfter(now, .5, self.tippleLights)
        self.turnOnLightAfter(now, .7, self.leftBridgeLight)                     

    def stopAtTipple(self) :
        self.waitSensorActive(self.EOT)
        self.redLantern.setState(ACTIVE)
        self.waitMsec(1000)
        self.stopTrain()
        self.setActivityMsg("Dumping Ore")

        if self.random.nextInt(100) < 50 :
            self.animateChutes()
        #
        #  Wait 2-4 minutes inside tipple before returning to winding house
        self.waitMsec(self.getDelay(self.random.nextInt(120) + 60) * 1000)
        self.setActivityMsg("")            
        self.moveTrainForward()
        
    def animateChutes(self) :
        self.shuttingDown = self.switch.getState() == INACTIVE
        if (not self.shuttingDown) :        
            self.setActivityMsg("Operating Chutes")
            self.chuteLight.setState(ON)
            self.waitMsec(3000)
            self.gateLight.setState(ON)
            self.waitMsec(10000)
            activeChute = self.chuteRight
            if (self.random.nextInt(100) < 50) :
                activeChute = self.chuteLeft

            activeChute.setState(ACTIVE)
            self.waitMsec(30000)
            activeChute.setState(INACTIVE)
            self.waitMsec(6000)
        
            self.gateLight.setState(OFF)
            self.waitMsec(3000)
            self.chuteLight.setState(OFF)
            self.setActivityMsg("")
        
    def runHoist(self) :
        
        self.roofSign.setState(TriStateSensor.ON)
        self.whEngineRoom.setState(TriStateSensor.ON)
        self.waitMsec(1000)
        self.boilerFire.setState(TriStateSensor.ON)

        if (self.random.nextInt(100) < 20) :
            self.setActivityMsg("Calling Hoist to L3")
            self.l3Button.setState(ACTIVE)
            self.level1Light.setState(ACTIVE)
            self.level1LightDim.setState(ACTIVE)
            self.waitSensorActive(self.l3Indicator)
        else :
            self.setActivityMsg("Calling Hoist to Surface")            
            self.s1Button.setState(ACTIVE)
            self.mineBldgLoadingDockLight.setState(ACTIVE)
            self.waitSensorActive(self.s1Indicator)
            self.mineBldgLoadingDockLight.setState(INACTIVE)            
            
        self.level1Light.setState(INACTIVE)
        
        self.waitMsec(10000)
        self.setActivityMsg("Sending Ore to S2")                    
        self.s2Button.setState(ACTIVE)
        self.mineBldgS2Light.setState(ACTIVE)
        self.waitSensorActive(self.s2Indicator)

        self.waitMsec(10000)
        self.mineBldgS2Light.setState(INACTIVE)
        self.setActivityMsg("")            
        
        self.boilerFire.setState(TriStateSensor.DIM)        
        self.roofSign.setState(TriStateSensor.ON)
        self.waitMsec(2000)
        self.whEngineRoom.setState(TriStateSensor.OFF)        
        self.waitMsec(2000)
        
    #
    #  Stop at the hoist to get a load of ore.
    #  If we are returning to the tipple, don't turn the tipple lights off
    def stopAtHoist(self, returnToTipple) :
        self.waitSensorActive(self.MineBldg)
        if (returnToTipple) :
            self.waitMsec(2000)
        else :
            self.waitMsec(500)

        self.shuttingDown = self.switch.getState() == INACTIVE
        if (self.shuttingDown) :
            masts.getSignalMast("Auto Train Indicator Mast").setAspect("Flashing")
            
        self.stopTrain()

        if (not returnToTipple and self.random.nextInt(100) < 20 and not self.shuttingDown and self.useHoist.getState() == ACTIVE) :
            self.runHoist()

        #  Wait 1-3 minutes inside hoist building
        if (not returnToTipple):
            self.turnOnTippleLights()

        self.setActivityMsg("Loading Ore")            
        self.waitMsec(self.getDelay(self.random.nextInt(120) + 60) * 1000)
        self.setActivityMsg("")            
        self.moveTrainReverse()
        self.mineBldgS3Light.setState(INACTIVE)

    #
    #  Let engineer take a coffee break at the winding house
    def coffeeBreak(self) :
        

        self.shuttingDown = self.switch.getState() == INACTIVE
        if (self.shuttingDown) :
            masts.getSignalMast("Auto Train Indicator Mast").setAspect("Flashing")
            
        self.stopTrain()
        self.waitMsec(1000)
        self.throttle.setF0(False)
        self.waitMsec(1000)
        self.throttle.setF8(True)

        delaySecs = self.getDelay(5*60)
        delayMins = delaySecs / float(60.0)
        delayStr = "%0.1f" % delayMins
        delayStr = delayStr + " minute Coffee Break"
        self.setActivityMsg(delayStr)        
        self.waitMsec(delaySecs * 1000)
        

    def getDelay(self, seconds) :
        if self.switch.getState() == INACTIVE :
            duration = 0
        else :
            duration = seconds + self.random.nextGaussian()*(seconds)

            if (self.buildingLightDemo.getState() != ACTIVE or self.loopCount < 5) :
                duration = duration * .25
            
        #if (self.debug) :
        #print "Returning delay = " + str(int(duration)) + " seconds (" + str(duration/60.0) + " minutes)" 

        return int(duration)
    
    def handle (self) :

        self.loopCount = self.loopCount + 1
        print "Tipple Train Loop Count = " + str(self.loopCount)
        
        if (self.firstTime) :
            self.setActivityMsg("Starting Shift")
        else :    
            self.setActivityMsg("")
        
        if (self.BOT.getState() != ACTIVE) :
            self.throttle.setF0(True);
            self.moveTrainForward()
            self.windingHouseBridgeLight.setState(ACTIVE)        

            stopForWater = self.random.nextInt(100) < 15
            returnToTipple = self.random.nextInt(100) < 65

            if self.switch.getState() == INACTIVE :
                stopForWater = False
                returnToTipple = False
                
            if (not returnToTipple) :
                self.turnOutTippleLights()
            
            #
            # Rarely stop when returning to winding house to take on water inside mime bldg.
            if (not self.firstTime) :
                if (stopForWater) :
                    self.waitSensorActive(self.MineBldg)
                    self.setActivityMsg("Filling Water")
                    self.stopTrain()
                    self.waitMsec(4000)
                    self.throttle.setF6(True)
                    self.waitMsec(self.getDelay(2*60) * 1000)
                    self.setActivityMsg("")                    
                    self.throttle.setF6(False)
                    self.waitMsec(5000)
                    self.moveTrainForward()
                elif (returnToTipple) :
                    self.stopAtHoist(True)
                    self.stopAtTipple()

            self.shuttingDown = self.switch.getState() == INACTIVE
            if (self.shuttingDown) :
                masts.getSignalMast("Auto Train Indicator Mast").setAspect("Flashing")
                    
            self.waitSensorActive(self.BOT)
            self.setActivityMsg("")

            
        #
        #  Wait at BOT, except 1st time through
        if (not self.firstTime) :
            self.coffeeBreak()
            if (self.random.nextInt(100) < 10) :
                self.releaseSteam()
            
            self.setActivityMsg("")
        else :
            self.stopTrain()                        
            self.firstTime = False

        self.throttle.setF8(False)
        self.waitMsec(self.getDelay(2) * 1000)
        self.throttle.setF0(True)
        self.moveTrainReverse()

        self.mineBldgS3Light.setState(ACTIVE)        
        self.windingHouseBridgeLight.setState(INACTIVE)


        #
        #  Stop in Mine Building going toward Tipple
        self.stopAtHoist(False)

        #
        #  Stop at tipple
        self.stopAtTipple()

        if (self.switch.getState() != ACTIVE) :
            self.stopTrain()

        self.activity.setValue("")                                    

        self.shuttingDown = self.switch.getState() == INACTIVE
        if (self.shuttingDown and self.l3switch.getState() == INACTIVE and self.l2switch.getState() == INACTIVE) :
            self.whEngineRoom.cancelScheduledTasks()
            self.boilerFire.cancelScheduledTasks()
            masts.getSignalMast("Auto Train Indicator Mast").setAspect("Not Lit")
            self.firstTime = True
            
            
        return (not self.shuttingDown) 

    def setActivityMsg (self, msg) :
        self.shuttingDown = self.switch.getState() == INACTIVE        
        if self.shuttingDown :
            self.activity.setValue("Ending Shift")
        else :
            self.activity.setValue(msg)

    def turnOn(self, sensor):
        try :
            sensor.setState(ACTIVE)
        except:
            sensor.setState(ON)

    def turnOff(self, sensor):
        try :
            sensor.setState(INACTIVE)
        except :
            sensor.setState(OFF)

    def turnOffLightAfter(self, departureTime, offset, sensor):
        xtime = departureTime + timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.turnOff, [sensor]).start()
            
            
    def turnOnLightAfter(self, arrivalTime, offset, sensor):
        xtime = arrivalTime + timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.turnOn, [sensor]).start()

        
TippleTrain().start()
