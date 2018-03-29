import jmri

class SensorInitTest(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):

        #Initialize Turntable indicators
        self.ttIndicators = [];
        self.ttIndicators.append(sensors.provideSensor("TT Track 2 Indicator"));
        self.ttIndicators.append(sensors.provideSensor("TT Track 3 Indicator"));
        self.ttIndicators.append(sensors.provideSensor("TT Track 4 Indicator"));
        self.ttIndicators.append(sensors.provideSensor("TT Track 5 Indicator"));
        self.ttIndicators.append(sensors.provideSensor("TT Track 6 Indicator"));                
        for i in range (len(self.ttIndicators)) :
            sen = self.ttIndicators[i]
            sen.requestUpdateFromLayout()
            knownState = sen.getKnownState()
            rawState = sen.getRawState()
            state = sen.getState()
            #print "TT Known State = " + str(knownState)
            #print "TT Raw State = " + str(rawState)
            #print "TT State = " + str(state)                        
            #if (knownState == ACTIVE) :
            #    print "Setting turntable track " + str(i+2) + " ACTIVE"
            #else :
            #    print "Setting turntable track " + str(i+2) + " INACTIVE"                
            sen.setState(knownState)


SensorInitTest().start()            
