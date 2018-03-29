import jmri
from java.util import Random

#Sets all sensors to INACTIVE 
class L2TunnelLights(jmri.jmrit.automat.AbstractAutomaton) :
    def init(self):
        self.l2TrainActive = sensors.provideSensor ("L2 Auto")
        self.demoMode = sensors.provideSensor ("Building Light Demo")
        self.lightMode = sensors.provideSensor ("S3 Demo")        

        self.l2LeftTunnel = lights.provideLight("L2 Left Tunnel Lanterns")
        self.l2RightTunnel = lights.provideLight("L2 Right Tunnel Lanterns")        
        self.l2MidTunnel = lights.provideLight("L2 Middle Tunnel Lanterns")
        self.l2MidTunnelBlue = lights.provideLight("L2 Middle Tunnel Blue Flicker")        
        self.l2FrontLeftTunnel = lights.provideLight("L2 Front Left Tunnel Lanterns")
        self.l2TailingDump = lights.provideLight("L2 Tailing Dump Lanterns")
        self.l2UpperDeck = lights.provideLight("L2 Upper Deck Lanterns")
        self.l2LowerDeck = lights.provideLight("L2 Lower Deck Lanterns")        


        self.l2LeftTunnel.setState(OFF)
        self.l2RightTunnel.setState(OFF)        
        self.l2MidTunnel.setState(OFF)
        self.l2MidTunnelBlue.setState(OFF)
        self.l2FrontLeftTunnel.setState(OFF)
        self.l2TailingDump.setState(OFF)
        self.l2UpperDeck.setState(OFF)
        self.l2LowerDeck.setState(OFF)                

    def delayMinutes(self, minMinutes) :

        scale = 1.0
        if (self.demoMode.getState() == ACTIVE) :
            scale = .25

        varMins = java.util.Random().nextInt(int(float(minMinutes*60.0) / 4.0))

        myDelay = int(float(minMinutes*60.0 + varMins) * scale)
        if (myDelay <= 0) :
            myDelay = 1

        self.waitMsec(myDelay * 1000)

    def keepGoing(self):
        if (self.lightMode.getState() != ACTIVE) :
            self.stop();
            return False
        
            
    def handle(self):
        self.l2LeftTunnel.setState(ON)


        if (java.util.Random().nextInt(100) < 50) :
            self.waitMsec(1500)
            if (self.l2FrontLeftTunnel.getState() == ON) :
                self.l2FrontLeftTunnel.setState(OFF)
            else :
                self.l2FrontLeftTunnel.setState(ON)        

        self.keepGoing()
                
        self.delayMinutes(2)
        self.l2MidTunnel.setState(ON)


        
        if (java.util.Random().nextInt(100) > 35) :
            self.delayMinutes(.5)
            self.l2MidTunnelBlue.setState(ON)
            self.delayMinutes(1.5)
            self.l2MidTunnelBlue.setState(OFF)

        self.l2LeftTunnel.setState(OFF)

        self.keepGoing()        
        
        self.delayMinutes(2)
        self.l2RightTunnel.setState(ON)

        self.keepGoing()
        
        self.delayMinutes(1)
        if (java.util.Random().nextInt(100) < 70) :
            self.l2UpperDeck.setState(ON)
        else :
            self.l2UpperDeck.setState(OFF)

        self.keepGoing()
        
        self.delayMinutes(1)
        if (java.util.Random().nextInt(100) < 70) :
            self.l2LowerDeck.setState(ON)
        else :
            self.l2LowerDeck.setState(OFF)                    

        if (java.util.Random().nextInt(100) < 50) :
            self.waitMsec(1500)
            if (self.l2TailingDump.getState() == ON) :
                self.l2TailingDump.setState(OFF)
            else :
                self.l2TailingDump.setState(ON)
                
        self.keepGoing()

        self.delayMinutes(2)
        self.l2MidTunnel.setState(OFF)

        self.keepGoing()
        self.delayMinutes(3)
        self.l2RightTunnel.setState(OFF)                

        self.keepGoing()
        
        self.delayMinutes(5)

        
        return (self.l2TrainActive.getState() == INACTIVE) and (self.lightMode.getState() == ACTIVE)  # Loop until level 3 train is activated

L2TunnelLights().start()
