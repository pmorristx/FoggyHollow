import jmri
from java.util import Random

#Sets all sensors to INACTIVE 
class SequenceTunnelLights(jmri.jmrit.automat.AbstractAutomaton) :
    def init(self):
        self.l3TrainActive = sensors.provideSensor ("L1 Auto")
        self.demoMode = sensors.provideSensor ("Building Light Demo")
        self.lightMode = sensors.provideSensor ("S3 Demo")        

        self.l3LeftTunnel = lights.provideLight("L3 Left Tunnel Lanterns")
        self.l3MidTunnel = lights.provideLight("L3 Middle Tunnel Lanterns")
        self.l3Bridge = lights.provideLight("L3 Tipple Lake Bridge Lanterns")
        self.l3Tipple = lights.provideLight("L3 Tipple Lanterns")

        self.l3FarRightTunnel = lights.provideLight("L3 Far Right Tunnel Lanterns")
        self.l3LeftTunnelFlicker = lights.provideLight("L3 Far Left Tunnel Flicker")

        self.l3LeftTunnel.setState(OFF)
        self.l3MidTunnel.setState(OFF)
        self.l3Bridge.setState(OFF)
        self.l3Tipple.setState(OFF)
        self.l3FarRightTunnel.setState(OFF)
        self.l3LeftTunnelFlicker.setState(OFF)        

    def delayMinutes(self, minMinutes) :

        scale = 1.0
        if (self.demoMode.getState() == ACTIVE) :
            scale = .25

        varMins = java.util.Random().nextInt(int(float(minMinutes*60.0) / 4.0))

        myDelay = int(float(minMinutes*60 + varMins) * scale)
        self.waitMsec((minMinutes + varMins) * 1000)

            
    def handle(self):



        self.l3LeftTunnelFlicker.setState(ON)
        
        self.delayMinutes(2)
        self.l3LeftTunnel.setState(ON)

        self.delayMinutes(2)
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

        self.delayMinutes(2)
        self.l3Tipple.setState(ON)

        self.delayMinutes(2)
        self.l3MidTunnel.setState(OFF)

        self.delayMinutes(3)
        self.l3Tipple.setState(OFF)

        self.delayMinutes(3)
        self.l3Bridge.setState(OFF)                

        self.l3LeftTunnelFlicker.setState(OFF)
        
        self.delayMinutes(5)
        
        return (self.l3TrainActive.getState() == INACTIVE) and (self.lightMode.getState() == ACTIVE)  # Loop until level 3 train is activated

SequenceTunnelLights().start()
