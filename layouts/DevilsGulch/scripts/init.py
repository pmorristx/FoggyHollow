class setStartup(jmri.jmrit.automat.AbstractAutomaton) :
   def init(self):
     return
   def handle(self):

      #
      #  Read the state of the turnouts and set the panel lights to match.

      fullname = jmri.util.FileUtil.getExternalFilename("preference:panels/FoggyHollowControlRaspberry.xml")
      jmri.InstanceManager.configureManagerInstance().load(java.io.File(fullname))
      self.waitMsec(10000)         # time is in milliseconds


      #
      #  Start the NIXIE clock on the panel once.
      clockScript = jmri.util.FileUtil.getExternalFilename("preference:scripts/NixiePanelClock.py")
      execfile(clockScript);

      script = jmri.util.FileUtil.getExternalFilename("preference:scripts/TurnoutMonitor.py")
      execfile(script);

      script = jmri.util.FileUtil.getExternalFilename("preference:scripts/TurnoutStatePersistence.py")
      execfile(script);

      script = jmri.util.FileUtil.getExternalFilename("preference:scripts/SignalMonitor.py")
      execfile(script);

      #
      #  Turn maintenance call toggle off
      #sensors.getSensor("IS8:MCT").setState(INACTIVE)

      return False              # all done, don't repeat again
setStartup().start()          # create one of these, and start it running





 

