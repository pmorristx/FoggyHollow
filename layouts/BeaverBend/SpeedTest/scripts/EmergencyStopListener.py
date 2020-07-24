
import os
import sys
sys.path.insert(1, os.path.expanduser('~') + "/MyJMRI/SpeedTest/scripts")

import jmri

from java.beans import PropertyChangeListener
from jmri.jmrit.automat import AutomatSummary


class EmergencyStopListener(PropertyChangeListener) :
	
        def init(self, locomotive) :
                self.locomotive = locomotive
                return		

        def propertyChange(self, event) :

                self.locomotive.emergencyStop()
                self.locomotive.tootWhistle(1)
                

                return
	
        def getName(self) :
                return "EmergencyStopListener" + self.locomotive.getName()
