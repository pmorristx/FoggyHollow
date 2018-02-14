#
#  Script to turn Beaver Bend depot tower light on

import jarray
import jmri

class TowerLight(jmri.jmrit.automat.AbstractAutomaton) :
	
	# init() is called exactly once at the beginning to do
	# any necessary configuration.
	def init(self):
		self.throttle = self.getThrottle(20, True) 
		self.sensor = sensors.provideSensor("LS7")
		return
	def handle(self):
		self.throttle.setF3(self.sensor.getState() != ACTIVE)
		return 0
# create one of these
a = TowerLight()

a.setName("Beaver Bend Tower Light")

# and start it running
a.start()