import jarray
import jmri

#Sets all sensors to INACTIVE 
class InitializeAllSensorsInactive(jmri.jmrit.automat.AbstractAutomaton) :
    def init(self):
        self.sen = sensors.getSystemNameList()
        self.lit = lights.getSystemNameList()

        self.lightDelay = 2500
     
    def handle(self):
        print "Setting sensors INACTIVE"
        for s in self.sen:
            # print s
            thisSensor = sensors.provideSensor(s)
            if (thisSensor.getSystemName() != "ISCLOCKRUNNING") and (thisSensor.getUserName() != None) and not (thisSensor.getUserName().startswith("OS:")) : 
                sensors.provideSensor(s).setState(INACTIVE)

        print "Setting lights OFF"
        for l in self.lit:
            lights.provideLight(l).setState(OFF)

        self.waitMsec(5000)

        turnouts.provideTurnout("Tipple Chute Left").setState(THROWN)
        turnouts.provideTurnout("Tipple Chute Right").setState(THROWN)

        lights.provideLight("LL200").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL201").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL202").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL203").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL205").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL207").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL212").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL213").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL214").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL215").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL216").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL217").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL218").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL219").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL220").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL221").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL222").setState(ON)
        self.waitMsec(self.lightDelay)

        lights.provideLight("LL223").setState(ON)
        self.waitMsec(self.lightDelay)                        
        return 0 # one shot, do not loop
 
InitializeAllSensorsInactive().start()
