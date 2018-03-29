import jmri
from java.util import Random

#Sets all sensors to INACTIVE 
class L3TunnelLights(jmri.jmrit.automat.AbstractAutomaton) :
    def init(self):
        self.l3TrainActive = sensors.provideSensor ("L1 Auto")
        self.demoMode = sensors.provideSensor ("Building Light Demo")
        self.lightMode = sensors.provideSensor ("S3 Demo")        

        self.l3LeftTunnel = lights.provideLight("L3 Left Tunnel Lanterns")
        self.l3MidTunnel = lights.provideLight("L3 Middle Tunnel Lanterns")
        self.l3RightTunnel = lights.provideLight("LL209")        
        self.l3Bridge = lights.provideLight("L3 Tipple Lake Bridge Lanterns")
        self.l3Tipple = lights.provideLight("L3 Tipple Lanterns")
        self.l3LakeBridge = lights.provideLight("L3 Lake Cavern Bridge")

        self.l3FarRightTunnel = lights.provideLight("L3 Far Right Tunnel Lanterns")
        self.l3LeftTunnelFlicker = lights.provideLight("L3 Far Left Tunnel Flicker")

        self.l3Hoist = lights.provideLight("L2 Hoist Frame & Cage")
        self.l3HoistCav = lights.provideLight("L3 Hoist Cavern Left Lanterns")

        self.l3LeftTunnelSignalEast = signals.getSignalHead("Left Tunnel Signal East")
        self.l3LeftTunnelSignalWest = signals.getSignalHead("Left Tunnel Signal West")
        self.l3RightTunnelSignalEast = signals.getSignalHead("Right Tunnel Signal East")

        self.turnout = turnouts.provideTurnout("Hoist Cavern Turnout")
        self.useHoistTurnout = sensors.provideSensor("Use Hoist Turnout")
        
        self.l3LeftTunnel.setState(OFF)
        self.l3MidTunnel.setState(OFF)
        self.l3Bridge.setState(OFF)
        self.l3Tipple.setState(OFF)
        self.l3FarRightTunnel.setState(OFF)
        self.l3LeftTunnelFlicker.setState(OFF)

        self.l3LeftTunnelSignalEast.setLit(True)
        self.l3LeftTunnelSignalWest.setLit(True)
        self.l3RightTunnelSignalEast.setLit(True)                

    def allOff(self):
        self.l3LeftTunnel.setState(OFF)
        self.l3MidTunnel.setState(OFF)
        self.l3RightTunnel.setState(OFF)
        self.l3Bridge.setState(OFF)
        self.l3LakeBridge.setState(OFF)                
        self.l3Tipple.setState(OFF)
        self.l3HoistCav.setState(OFF)
        self.l3Hoist.setState(OFF)        

        self.l3LeftTunnelSignalEast.setLit(False)
        self.l3LeftTunnelSignalWest.setLit(False)
        self.l3RightTunnelSignalEast.setLit(False)        

        
    def delayMinutes(self, minMinutes) :

        self.keepGoing()
        scale = 1.0
        if (self.demoMode.getState() == ACTIVE) :
            scale = .25

        varMins = java.util.Random().nextInt(int(float(minMinutes*60.0) / 4.0))

        myDelay = int(float(minMinutes*60 + varMins) * scale)
        self.waitMsec(myDelay * 1000)


    def keepGoing(self):
        if (self.lightMode.getState() != ACTIVE) :
            self.stop();
            return False        
            
    def handle(self):


        self.l3LeftTunnelFlicker.setState(ON)
        
        self.delayMinutes(2)
        self.l3LeftTunnelSignalWest.setAppearance(RED)
        self.delayMinutes(1)
        self.l3LeftTunnel.setState(ON)


        if (java.util.Random().nextInt(100) < 50 and self.useHoistTurnout.getState() == ACTIVE) :
            self.delayMinutes(1)
            self.l3HoistCav.setState(ON)
            self.delayMinutes(1)
            self.turnout.setState(THROWN)
            self.delayMinutes(1)            
            self.l3Hoist.setState(ON)

            self.delayMinutes(3)
            self.turnout.setState(CLOSED)
            self.delayMinutes(1)            
            self.l3Hoist.setState(OFF)
            self.delayMinutes(0.5)
            self.l3HoistCav.setState(OFF)
            
        self.delayMinutes(2)
        self.l3LeftTunnelSignalEast.setAppearance(RED)
        self.l3LeftTunnelSignalWest.setAppearance(GREEN)        
        self.l3MidTunnel.setState(ON)

        self.delayMinutes(2)
        self.l3Bridge.setState(ON)

        if (java.util.Random().nextInt(100) < 50) :
            self.waitMsec(1500)
            if (self.l3FarRightTunnel.getState() == ON) :
                self.l3FarRightTunnel.setState(OFF)
            else :
                self.l3FarRightTunnel.setState(ON)
                


        self.delayMinutes(2)
        self.l3LeftTunnel.setState(OFF)

        self.delayMinutes(1)
        self.l3Tipple.setState(ON)

        self.delayMinutes(2)
        self.l3MidTunnel.setState(OFF)

        self.delayMinutes(0.5)
        self.l3RightTunnel.setState(ON)
        
        self.delayMinutes(3)
        self.l3Tipple.setState(OFF)

        self.delayMinutes (.5)
        self.l3RightTunnelSignalEast.setAppearance(RED)
        self.l3LeftTunnelSignalEast.setAppearance(YELLOW)        

        self.delayMinutes(3)
        self.l3Bridge.setState(OFF)                

        if (java.util.Random().nextInt(100) < 50) :
            self.delayMinutes(1)
            self.l3LakeBridge.setState(ON)
            self.delayMinutes(2)
            self.l3LakeBridge.setState(OFF)

        self.l3RightTunnel.setState(OFF)

        self.delayMinutes (1)
        self.l3RightTunnelSignalEast.setAppearance(YELLOW)
        self.l3LeftTunnelSignalEast.setAppearance(GREEN)                
        
        self.l3LeftTunnelFlicker.setState(OFF)

        if (self.l3TrainActive.getState() == INACTIVE) and (self.lightMode.getState() == ACTIVE) : # Loop until level 3 train is activated
            self.l3LeftTunnelSignalEast.setLit(False)
            self.delayMinutes(0.4)
            self.l3LeftTunnelSignalWest.setLit(False)
            self.delayMinutes(0.4)            
            self.l3RightTunnelSignalEast.setLit(False)        

            self.delayMinutes(5)

            self.l3RightTunnelSignalEast.setAppearance(GREEN)
            self.l3LeftTunnelSignalEast.setAppearance(GREEN)
            self.l3LeftTunnelSignalWest.setAppearance(YELLOW)            
            
            
            self.l3LeftTunnelSignalEast.setLit(True)
            self.delayMinutes(0.4)            
            self.l3LeftTunnelSignalWest.setLit(True)
            self.delayMinutes(0.4)            
            self.l3RightTunnelSignalEast.setLit(True)
            self.delayMinutes(0.4)            
            
            return True
        else :
            return False 

L3TunnelLights().start()
