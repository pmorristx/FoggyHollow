#
#  Script to turn Beaver Bend depot tower light on

import jarray
import jmri
import sys

class TowerLight(jmri.jmrit.automat.AbstractAutomaton) :
	
	# init() is called exactly once at the beginning to do
	# any necessary configuration.
	def init(self):
                try :
		        self.throttle = self.getThrottle(20, True) 
		        self.sensor = sensors.provideSensor("LS7")
                except :
                        print "***"
                        print "*** Error in TowerLight.py:init(): ", sys.exc_info()[0], sys.exc_info()[1]
                        print "***"	                
		return
	def handle(self):
                try :
		        self.throttle.setF3(self.sensor.getState() != ACTIVE)
                except :
                        print "*** Error in TowerLight.py:handle(): ", sys.exc_info()[0], sys.exc_info()[1]
                        print "***"	                
		return 0
# create one of these
a = TowerLight()

a.setName("Beaver Bend Tower Light [TowerLight.py]")

# and start it running
a.start()
