import jmri

class Lvl1Light1(jmri.jmrit.automat.AbstractAutomaton):

    def init(self) :

        LnConnection =  jmri.jmrix.loconet.LocoNetSystemConnectionMemo()
        slot = jmri.jmrix.loconet.LocoNetSlot(1)
        self.throttle = jmri.jmrix.loconet.LocoNetThrottle(LnConnection, slot);
        
        #self.throttle = self.getThrottle(136, False) # 136->Yellow; 138->Blue

    def handle(self):
        for i in range(0, 100)  :
            self.throttle.setSpeedSetting(i)
            self.waitMsec(1000)
            print " i = " + str(i)
        return False

Lvl1Light1().start()
            
