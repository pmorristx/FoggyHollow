import os
import sys
sys.path.insert(1, os.path.expanduser('~') + "/MyJMRI/SpeedTest/scripts")

import jmri

from java.beans import PropertyChangeListener
from jmri.jmrit.automat import AutomatSummary

class SpeedChangeListener(PropertyChangeListener) :	
        def init(self, memories):
                self.memories = memories
                return		

        def propertyChange(self, event) :
                
                row = event.source.getUserName()[-1]

		scaleLength = float(self.memories.getMemory("Track Length (Scale)").getValue())
		duration = float(self.memories.getMemory("Elapsed Time-" + row).getValue())
		if (duration > 0) :

                        feetPerSecond = scaleLength / duration
                        milesPerHour = float(feetPerSecond) * float('0.6818')		

                        self.memories.getMemory("Feet Per Second-" + row).setValue(format(feetPerSecond, '.2f'))
                        self.memories.getMemory("Miles Per Hour-" + row).setValue(format(milesPerHour, '.2f'))

                return	
