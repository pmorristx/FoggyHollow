import jmri

class soundtest(jmri.jmrit.automat.AbstractAutomaton):
	def init(self):
		self.splitFlapSound = audio.provideAudio("IAS1")
		self.buffer = audio.provideAudio("IAB1")	
		#print "Audio buffer url = ", self.buffer.getUrl()	
	def handle(self):
		self.splitFlapSound.play()
		self.waitMsec(2000)
		self.splitFlapSound.fadeOut()
		self.waitMsec(2000)
		self.splitFlapSound.stop()				
		return 0
tst = soundtest()
tst.start()