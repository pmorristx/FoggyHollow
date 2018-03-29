class SendReceiveRelay(jmri.jmrit.automat.AbstractAutomaton) :
	def init(self):
		self.relayClick = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/EnhancedCTCRelay.wav"))
		return
	def handle(self):

		# Turn sending light on for 8 seconds
		sensors.getSensor("Code Send Indicator").setState(ACTIVE)
		lights.getLight("Code Send Indicator").setState(jmri.Light.ON)
		self.relayClick.play()
		self.waitMsec(8000)
		sensors.getSensor("Code Send Indicator").setState(INACTIVE)
		lights.getLight("Code Send Indicator").setState(jmri.Light.OFF)	  
		
		
		self.waitMsec(3000) # Wait 3 seconds
		
		#  Turn indication light on for 5 seconds
		sensors.getSensor("Code Receive Indicator").setState(ACTIVE)
		lights.getLight("Code Receive Indicator").setState(jmri.Light.ON)	  
		self.relayClick.play()
		self.waitMsec(8000)
		sensors.getSensor("Code Receive Indicator").setState(INACTIVE)
		lights.getLight("Code Receive Indicator").setState(jmri.Light.OFF)	  
		
		return False              # all done, don't repeat again
SendReceiveRelay().start()          # create one of these, and start it running