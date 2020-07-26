import jmri

class SendReceiveRelay(jmri.jmrit.automat.AbstractAutomaton) :
   def init(self):
      try:
         self.relayClick = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/EnhancedCTCRelay.wav"))
      except:
         print "SendReceiveRelay.py unable to init sound file"
      return
   def handle(self):

      # Turn sending light on for 8 seconds
      sensors.getSensor("IS16:CCK").setState(ACTIVE)
      try:
         self.relayClick.play()
      except:
         print "SendReceiveRelay.py - no sound file!"
      self.waitMsec(8000)
      sensors.getSensor("IS16:CCK").setState(INACTIVE)

      self.waitMsec(3000) # Wait 3 seconds

      #  Turn indication light on for 5 seconds
      sensors.getSensor("IS17:ICK").setState(ACTIVE)
      try:
         self.relayClick.play()
      except:
         print "SendReceiveRelay.py - no sound file!"      
      self.waitMsec(8000)
      sensors.getSensor("IS17:ICK").setState(INACTIVE)
  
      return False              # all done, don't repeat again
SendReceiveRelay().start()          # create one of these, and start it running





 

