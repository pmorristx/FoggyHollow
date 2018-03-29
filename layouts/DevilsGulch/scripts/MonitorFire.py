import jmri

class MonitorFire(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):

        self.debug = sensors.provideSensor("Private").getState() == ACTIVE               
        self.boilerIntensity = sensors.provideSensor("Winding House Boiler Intensity")
        self.boilerFire = sensors.provideSensor("Winding House Boiler Fire")
        self.boilerIndicator = sensors.provideSensor("Boiler Indicator")
        self.windingHouseBoiler = []
        self.windingHouseBoiler.append(self.boilerIntensity)
        self.windingHouseBoiler.append(self.boilerFire)
        
    def handle(self):

        self.waitChange(self.windingHouseBoiler)
        if (self.boilerFire.getState() == ACTIVE and self.boilerIntensity.getState() == ACTIVE) :
            self.boilerIndicator.setState(ACTIVE)
        elif (self.boilerFire.getState() == ACTIVE and self.boilerIntensity.getState() == INACTIVE) :
            self.boilerIndicator.setState(INCONSISTENT)
        else :
            self.boilerIndicator.setState(INACTIVE)

        return True
MonitorFire().start()
