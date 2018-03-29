import jmri
import jmri.jmrit.roster
import jmri.jmrix.AbstractThrottle
import sys
from java.awt import Font
import jmri.jmrit.display.panelEditor.configurexml.PanelEditorXml

class ThrottleTest(jmri.jmrit.automat.AbstractAutomaton) :
	def init(self):
		self.throttle = self.getThrottle(6, False) 
		
	#
	#  Short toot of the whistle 
	def tootWhistle(self, numToots):
		for n in range(numToots) :
			self.throttle.setF3(not self.throttle.getF3())			
			self.waitMsec(500)
		return 0
	
	#
	#  Long whistle
	def forwardWhistle(self):
		self.longWhistle()
		self.waitMsec(1000)
		self.longWhistle()
		return 0
		
	#
	#  Signal reverse with 3 short toots
	def reverseWhistle(self):
		self.tootWhistle(3)
		return 0
	
	#
	#  Signal stop with one short toot
	def stopWhistle(self):
		self.tootWhistle(1)
		return 0
	
	#
	#  Long whistle
	def longWhistle(self):
		self.throttle.setF2(True)
		self.waitMsec(1000)
		self.throttle.setF2(False)
		return 0
	
	#
	#  Cab Light
	def setCabLight(self, state):
		self.throttle.setF11(state)
		return 0
	#
	#  Brake
	def setBrake(self, state):
		self.throttle.setF7(state)
		return 0
	
	#
	#
	def ringBell(self, state):
		self.throttle.setF1(state)
		return 0		
		
	def handle(self):
		
		print "Setting direction forward"
		self.throttle.setIsForward(True)
		self.waitMsec(2000)
						
		print "Starting loco at speed 0.2"
		self.throttle.setSpeedSetting(0.1)		
		self.waitMsec(3000)
		
		print "Setting Brake"
		self.setBrake(True)
		self.waitMsec(5000)
		
		print "Releasing Brake"
		self.setBrake(False)
		self.waitMsec(5000)
		
		print "Stopping Locomotive"
		self.throttle.setSpeedSetting(0.0)	
		
		print "Releasing Brake After Stop"
		self.setBrake(False)
		self.waitMsec(5000)
		
		
	
	
# create one of these
main = ThrottleTest()

# set the name, as a example of configuring it
main.setName("Throttle Test")

# and start it running
main.start()	