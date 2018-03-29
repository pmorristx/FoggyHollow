#
#  Script to shuttle mine train back & forth, turning on various lights, etc. along the way.

import jarray
import jmri

class MineSignals(jmri.jmrit.automat.AbstractAutomaton) :
	
	# init() is called exactly once at the beginning to do
	# any necessary configuration.
	def init(self):
		
		# get the sensor and throttle objects
		
		self.block3 = sensors.provideSensor("High Bridge")
		self.block4 = sensors.provideSensor("Mine Approach Bridge")
		self.block5 = sensors.provideSensor("Mine Building")
		self.block6 = sensors.provideSensor("EOT")
		self.block1 = sensors.provideSensor("BOT")
		self.block2 = sensors.provideSensor("Mine Tunnel")		
		self.automationOn = sensors.provideSensor("IS:MTS")
		


		self.direction = sensors.provideSensor("IS:DIR")

		return


	# handle() is called repeatedly until it returns false.
	#
	def handle(self):
		
		
		if (self.waitChange(self.direction.knownState, self.direction) == ACTIVE) :
			
		self.waitChange([self.block1, self.block2, self.block3, self.block4. self.block5, self.block6])
		
		if self.block6.knownState == ACTIVE :
		return 1  # to continue
	
# end of class definition

# create one of these
a = MineSignals()

# set the name, as a example of configuring it
a.setName("Automated Beaver Bend Mine Signals")

# and start it running
a.start()
