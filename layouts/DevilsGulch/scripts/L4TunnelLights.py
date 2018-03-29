import jmri
from java.util import Random

#Sets all sensors to INACTIVE 
class L4TunnelLights(jmri.jmrit.automat.AbstractAutomaton) :
    def init(self):

        self.demoMode = sensors.provideSensor ("Building Light Demo")
        self.lightMode = sensors.provideSensor ("S3 Demo")        

        self.l4LakeTunnel = lights.provideLight("L4 Lake Tunnel Lanterns")
        self.l4LakeYellow = lights.provideLight("L4 Lake Yellow Flicker")
        self.l4Sump = lights.provideLight("L4 Sump Blue Flicker")
        self.l4LakeBlue = lights.provideLight("Lake Cavern Blue Flicker")
        self.l4LakeCavYellow= lights.provideLight("L2 Middle Tunnel - Lake Cavern Yellow Flicker")        

        self.l4LakeTunnel.setState(OFF)
        self.l4LakeYellow.setState(OFF)
        self.l4Sump.setState(OFF)
        self.l4LakeBlue.setState(OFF)
        self.l4LakeCavYellow.setState(OFF)


    def delayMinutes(self, minMinutes) :

        scale = 1.0
        if (self.demoMode.getState() == ACTIVE) :
            scale = .25

        varMins = java.util.Random().nextInt(int(float(minMinutes*60.0) / 4.0))

        myDelay = int(float(minMinutes*60 + varMins) * scale)
        self.waitMsec(myDelay * 1000)

    def switchLight(self, light, probOn) :
        if (java.util.Random().nextInt(100) < probOn) :
            light.setState(ON)
        else :
            light.setState(OFF)

    def handle(self) :
        self.switchLight(self.l4LakeBlue, 80)

        self.switchLight(self.l4LakeTunnel, 50)

        self.switchLight(self.l4LakeYellow, 75)

        self.switchLight(self.l4Sump, 70)

        self.switchLight(self.l4LakeCavYellow, 85)

        self.waitMsec(java.util.Random().nextInt(60) * 1000)

        
        return (self.lightMode.getState() == ACTIVE)

L4TunnelLights().start()
