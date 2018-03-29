
import jarray
import jmri

class MonitorMinePower(jmri.jmrit.automat.AbstractAutomaton) :
	
	# init() is called exactly once at the beginning to do
	# any necessary configuration.
	def init(self):
		self.automationOn = sensors.provideSensor("IS:MTS")
		self.throttle = self.getThrottle(int(memories.getMemory("Mine Locomotive").getValue()), True)  
		 		
		return
		
	# handle() is called repeatedly until it returns false.
	#
	# Modify this to do your calculation.
	def handle(self):
	    
		self.waitSensorInactive(self.automationOn)
		if (self.throttle.getSpeedSetting() > 0) :
			self.throttle.setSpeedSetting(0.0)
			self.waitSensorActive(self.automationOn)
		return 1	# to continue
	
# end of class definition

# create one of these
a = MonitorMinePower()

# set the name, as a example of configuring it
a.setName("Monitor Mine Power")

# and start it running
a.start()
