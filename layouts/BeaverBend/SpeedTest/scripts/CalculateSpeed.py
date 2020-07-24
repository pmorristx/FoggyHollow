import sys
sys.path.insert(1, '../../scripts')

import jmri

class CalculateSpeed(jmri.jmrit.automat.AbstractAutomaton) :

	def init(self) :
		scaleLength = float(memories.getMemory("Track Length (Scale)").getValue())
		duration = float(memories.getMemory("Elapsed Time-0").getValue())		

		feetPerSecond = scaleLength / duration
		milesPerHour = float(feetPerSecond) * float('0.6818')		

		print "mph = " + str(milesPerHour)
		
		memories.getMemory("Feet Per Second-0").setValue(feetPerSecond)
		memories.getMemory("Miles Per Hour-0").setValue(str(milesPerHour))		
		
		
# .6818 x Scale Factor x Distance (in decimal feet) / Time (in seconds)		
me = CalculateSpeed()
me.start()		
