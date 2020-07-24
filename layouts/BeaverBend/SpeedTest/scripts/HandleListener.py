from java.beans import PropertyChangeListener

class HandleListener(PropertyChangeListener) :

    from java.beans import PropertyChangeListener
    from jmri.jmrit.automat import AutomatSummary

    def init(self, locomotive) :
        self.locomotive = locomotive
        return		

    def propertyChange(self, event) :

        from jmri import Sensor
        if (event.source.getState() == Sensor.INACTIVE) :
            self.locomotive.emergencyStop()
            self.locomotive.tootWhistle(1)
        return
