import jmri
import java.util.Random
from foggyhollow.arduino import TriStateSensor

class MineSimulator(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):


        #
        #  Mine Building Lights
        self.roofSign = TriStateSensor(sensors.provideSensor("Mine Bldg Roof Sign Dim"),
                                          sensors.provideSensor("Mine Building Roof Sign On"),
                                          sensors.provideSensor("Mine Building Roof Sign Off"))
        
        self.loadingDock = TriStateSensor(sensors.provideSensor("Mine Building Loading Dock Dim"),
                                          sensors.provideSensor("Mine Building Loading Dock On"),
                                          sensors.provideSensor("Mine Building Loading Dock Off"))

        self.mineSideDoor = TriStateSensor(None, lights.provideLight("Mine Bldg Side Door Light"), None)
        self.mineS2Light = TriStateSensor(None, lights.provideLight("Mine Bldg S2 Light"), None)
        self.mineS3Light = TriStateSensor(None, lights.provideLight("Mine Bldg S3 Light"), None)

        #
        #  Hoist Call Buttons
        self.hoistS2 = TriStateSensor(None, sensors.provideSensor("IS Call Hoist To S2"), None)
        self.hoistS1 = TriStateSensor(None, sensors.provideSensor("IS Call Hoist To S1"), None)
        self.hoistL1 = TriStateSensor(None, sensors.provideSensor("IS Call Hoist To L1"), None)        

        
        #
        #  Tipple lights
        self.leftBridge = TriStateSensor(None, lights.provideLight("Tipple Bridge Left Light"), None)
        self.rightBridge = TriStateSensor(None, lights.provideLight("Tipple Bridge Right Light"), None)
        self.insideLights = TriStateSensor(None, lights.provideLight("Tipple Inside Lights"), None)        
        self.chuteLight = TriStateSensor(None, lights.provideLight("Tipple Chute Light"), None)
        self.gateLight = TriStateSensor(None, lights.provideLight("Tipple Gate Light"), None)
        self.lantern = TriStateSensor(lights.provideLight("Tipple EOT Lantern Red"), lights.provideLight("Tipple EOT Lantern White"), None)

        #
        # Tipple chutes
        self.rightChute = TriStateSensor(None, sensors.provideSensor("Tipple Chute Right"), None)
        self.leftChute = TriStateSensor(None, sensors.provideSensor("Tipple Chute Left"), None)                
        #
        #  Winding House Lights
        self.whSideDoor = TriStateSensor(None, lights.provideLight("Winding House Side Door Light"), None)
        self.whBridge = TriStateSensor(None, lights.provideLight("Winding House Bridge Light"), None)
        self.wh2ndFloor = TriStateSensor(None, lights.provideLight("Winding House 2nd Floor Light"), None)
        self.whEngineRoom = TriStateSensor(sensors.provideSensor("Winding House Engine Room Dim"),
                                          sensors.provideSensor("Winding House Engine Room On"),
                                          sensors.provideSensor("Winding House Engine Room Off"))
        
        self.boilerFire = TriStateSensor(sensors.provideSensor("Winding House Boiler Low"),
                                       sensors.provideSensor("Winding House Boiler High"),
                                       sensors.provideSensor("Winding House Boiler Off"))


        #
        #  Level 1 Lights
        self.l1BlueLight = TriStateSensor(sensors.provideSensor("L1 Blue Light Dim"),
                                          sensors.provideSensor("L1 Blue Light On"),
                                          sensors.provideSensor("L1 Blue Light Off"))

        self.l1YellowLight = TriStateSensor(sensors.provideSensor("L1 Yellow Light Dim"),
                                          sensors.provideSensor("L1 Yellow Light On"),
                                          sensors.provideSensor("L1 Yellow Light Off"))

        self.l1VioletLight = TriStateSensor(sensors.provideSensor("Level 1 Violet Light Dim"),
                                            sensors.provideSensor("Level 1 Violet Light On"),
                                            sensors.provideSensor("Level 1 Violet Light Off"))

        self.demoModeListener = self.DemoModeListener()
        self.demoModeListener.init(self.simulateActivity, self.shutdown)
        
        self.demoActive = sensors.provideSensor("S3 Demo")
        self.demoActive.addPropertyChangeListener(self.demoModeListener)        

    def getDelay(self, delay):
        if (sensors.provideSensor("Building Light Demo").getState() == ACTIVE) :
            delay = float(delay) / 3.0            
        return delay
        
    def simulateActivity(self):

        self.shutdown()
        self.waitMsec(5000)
        #
        self.l1BlueLight.scheduleStateChange(TriStateSensor.DIM, 0)
        self.l1VioletLight.setPeriodicStateChange(self.getDelay(3.0), self.getDelay(4.0), self.getDelay(5.0), 1)                                            
        self.callHoist("S1", 0.5)
        
        self.boilerFire.scheduleStateChange(TriStateSensor.DIM, 0)
        self.mineSideDoor.scheduleStateChange(TriStateSensor.ON, self.getDelay(0.5))
        self.whSideDoor.scheduleStateChange(TriStateSensor.ON, self.getDelay(.8))
        self.whEngineRoom.scheduleStateChange(TriStateSensor.ON, self.getDelay(1))

        self.whEngineRoom.setPeriodicStateChange(self.getDelay(2.0), self.getDelay(3.0), self.getDelay(1), 0)
        self.boilerFire.setPeriodicStateChange(self.getDelay(2.0), self.getDelay(2.0), self.getDelay(5.0), 1)
        self.wh2ndFloor.setPeriodicStateChange(self.getDelay(3.0), self.getDelay(3.0), self.getDelay(6.0), 0)
        self.whBridge.setPeriodicStateChange(self.getDelay(2.0), self.getDelay(2.0), self.getDelay(6.0), 0)                                

        self.loadingDock.scheduleStateChange(TriStateSensor.DIM, self.getDelay(1.5))
        self.roofSign.scheduleStateChange(TriStateSensor.ON, self.getDelay(2.2))
        self.roofSign.scheduleStateChange(TriStateSensor.DIM, self.getDelay(2.8))        

        self.callHoist("S2", 3)
        
        self.mineS2Light.scheduleStateChange(TriStateSensor.ON, self.getDelay(4))
        self.whEngineRoom.scheduleStateChange(TriStateSensor.OFF, self.getDelay(5))

        self.mineS2Light.scheduleStateChange(TriStateSensor.OFF, self.getDelay(6))
        self.mineS3Light.scheduleStateChange(TriStateSensor.ON, self.getDelay(7))

        self.roofSign.scheduleStateChange(TriStateSensor.ON, self.getDelay(7.5))
        self.loadingDock.scheduleStateChange(TriStateSensor.ON, self.getDelay(8))
        
        
        self.insideLights.scheduleStateChange(TriStateSensor.ON, self.getDelay(10))
        self.rightBridge.scheduleStateChange(TriStateSensor.ON, self.getDelay(11))
        self.lantern.scheduleStateChange(TriStateSensor.ON, self.getDelay(11.5))
        self.leftBridge.scheduleStateChange(TriStateSensor.ON, self.getDelay(12))

        self.lantern.scheduleStateChange(TriStateSensor.DIM, self.getDelay(13))
        
        self.chuteLight.scheduleStateChange(TriStateSensor.ON, self.getDelay(15))
        self.gateLight.scheduleStateChange(TriStateSensor.ON, self.getDelay(16))

        prob = java.util.Random().nextInt(10)
        if (prob < 3):
            self.rightChute.scheduleStateChange(TriStateSensor.ON, self.getDelay(17))
            self.rightChute.scheduleStateChange(TriStateSensor.OFF, self.getDelay(19))            
        elif (prob < 6):
            self.leftChute.scheduleStateChange(TriStateSensor.ON, self.getDelay(17))
            self.leftChute.scheduleStateChange(TriStateSensor.OFF, self.getDelay(19))                        
        else :
            self.leftChute.scheduleStateChange(TriStateSensor.ON, self.getDelay(17))
            self.rightChute.scheduleStateChange(TriStateSensor.ON, self.getDelay(17.5))
            self.leftChute.scheduleStateChange(TriStateSensor.OFF, self.getDelay(18.5))
            self.rightChute.scheduleStateChange(TriStateSensor.OFF, self.getDelay(19))                        
        
        self.gateLight.scheduleStateChange(TriStateSensor.OFF, self.getDelay(20))
        self.chuteLight.scheduleStateChange(TriStateSensor.OFF, self.getDelay(21))

        self.lantern.scheduleStateChange(TriStateSensor.OFF, self.getDelay(21.5))
        
        self.leftBridge.scheduleStateChange(TriStateSensor.OFF, self.getDelay(22))

        self.rightBridge.scheduleStateChange(TriStateSensor.OFF, self.getDelay(23))                
        self.insideLights.scheduleStateChange(TriStateSensor.OFF, self.getDelay(24))

        self.mineS3Light.scheduleStateChange(TriStateSensor.OFF, self.getDelay(25))
        self.mineS2Light.scheduleStateChange(TriStateSensor.ON, self.getDelay(26))
        self.callHoist("L1", 26.5)
        self.l1YellowLight.scheduleStateChange(TriStateSensor.ON, self.getDelay(28))
        self.callHoist("S2", 30)        
        self.l1YellowLight.scheduleStateChange(TriStateSensor.OFF, self.getDelay(30))                                          


        self.mineS2Light.scheduleStateChange(TriStateSensor.OFF, self.getDelay(35))
        self.loadingDock.scheduleStateChange(TriStateSensor.OFF, self.getDelay(36))
        self.mineSideDoor.scheduleStateChange(TriStateSensor.OFF, self.getDelay(36.5))
        self.whSideDoor.scheduleStateChange(TriStateSensor.OFF, self.getDelay(30.2))                
        self.roofSign.scheduleStateChange(TriStateSensor.DIM, self.getDelay(29))        



    def callHoist(self, level, delay):
        if (sensors.provideSensor("Hoist Motor Enabled").getState() == ACTIVE):
            if (level == "S2"):
                self.hoistS2.scheduleStateChange(TriStateSensor.ON, self.getDelay(delay))
            elif (level == "S1") :
                self.hoistL1.scheduleStateChange(TriStateSensor.ON, self.getDelay(delay))
            elif (level == "L1") :
                self.hoistL1.scheduleStateChange(TriStateSensor.ON, self.getDelay(delay))
                
    def turnAllLightsOff(self):

        self.leftChute.setState(TriStateSensor.OFF)
        self.rightChute.setState(TriStateSensor.OFF)        
        
        self.whSideDoor.setState(TriStateSensor.OFF)
        self.whBridge.setState(TriStateSensor.OFF)
        self.wh2ndFloor.setState(TriStateSensor.OFF)
        self.whEngineRoom.setState(TriStateSensor.OFF)        

        self.leftBridge.setState(TriStateSensor.OFF)
        self.rightBridge.setState(TriStateSensor.OFF)
        self.insideLights.setState(TriStateSensor.OFF)
        self.chuteLight.setState(TriStateSensor.OFF)
        self.gateLight.setState(TriStateSensor.OFF)
        self.lantern.setState(TriStateSensor.OFF)        

        self.roofSign.setState(TriStateSensor.OFF)
        self.loadingDock.setState(TriStateSensor.OFF)
        self.mineSideDoor.setState(TriStateSensor.OFF)
        self.mineS2Light.setState(TriStateSensor.OFF)
        self.mineS3Light.setState(TriStateSensor.OFF)
        
    def shutdown(self):
        
        self.turnAllLightsOff()
        self.whSideDoor.cancelScheduledTasks()
        self.whBridge.cancelScheduledTasks()
        self.wh2ndFloor.cancelScheduledTasks()
        self.whEngineRoom.cancelScheduledTasks()

        self.leftBridge.cancelScheduledTasks()
        self.rightBridge.cancelScheduledTasks()
        self.insideLights.cancelScheduledTasks()
        self.chuteLight.cancelScheduledTasks()
        self.gateLight.cancelScheduledTasks()
        self.lantern.cancelScheduledTasks()

        self.roofSign.cancelScheduledTasks()
        self.loadingDock.cancelScheduledTasks()
        self.mineSideDoor.cancelScheduledTasks()
        self.mineS2Light.cancelScheduledTasks()
        self.mineS3Light.cancelScheduledTasks

        
    def handle(self):
        
        if (self.demoActive.getState() == ACTIVE) :
            self.simulateActivity()
        else :
            self.shutdown()
            
        self.waitChange([self.demoActive], int(self.getDelay(40*60*1000)))

        if (self.demoActive.getState() == ACTIVE) :
            return True
        else:
            self.shutdown()
            return False

    class DemoModeListener(java.beans.PropertyChangeListener) :
        def init(self, simProc, shutdownProc):
            self.shutdownProc = shutdownProc
            self.simProc = simProc

        def propertyChange(self, event):
            if (event.source.getState() == jmri.Sensor.ACTIVE) :
                self.shutdownProc()
            else:
                self.simProc()
            return  
        
MineSimulator().start()
