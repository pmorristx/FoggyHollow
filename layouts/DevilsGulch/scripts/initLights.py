class initLights(jmri.jmrit.automat.AbstractAutomaton) :
   def init(self):
      import sys
      sys.path.append(jmri.util.FileUtil.getExternalFilename("preference:scripts"))
      import ManagePanelIcons
      self.iconHandler =  ManagePanelIcons.ManagePanelIcons()
      return
   def handle(self):
      #
      fullname = jmri.util.FileUtil.getExternalFilename("preference:panels/Lights4.xml")
      jmri.InstanceManager.configureManagerInstance().load(java.io.File(fullname))
      self.waitMsec(2000)         # time is in milliseconds

      #
      #  Init the power switch to OFF
      sensors.getSensor("IS100:BO").setState(INACTIVE)
      sensors.getSensor("IS100:BT").setState(INACTIVE)
      sensors.getSensor("IS100:BF").setState(ACTIVE)

      self.iconHandler.init()
      self.iconHandler.getPanelHandle("Foggy Hollow Lights Editor")

     #
     #  Start the threads that monitor button presses on the panel
      execfile(jmri.util.FileUtil.getExternalFilename("preference:scripts/ButtonToggleMonitor.py"));
      execfile(jmri.util.FileUtil.getExternalFilename("preference:scripts/TripleToggleMonitor.py"));
      execfile(jmri.util.FileUtil.getExternalFilename("preference:scripts/LightMasterPower.py"));

      #
      # Play the steam whistle on the hour.
      execfile(jmri.util.FileUtil.getExternalFilename("preference:scripts/FactoryWhistle.py"));

      layoutLights = [101, 102, 103, 104, 105, 106, 107]
      for i in range(len(layoutLights)) :
         lightNumber = str(layoutLights[i])
         #
         #  Turn all lights off
         buttonName = "IS" + lightNumber + ":BF"
         button = sensors.getSensor(buttonName)
         if (button is not None) :
            button.setState(ACTIVE)
            #
            # Enable all buttons when we start to keep from being stuck 
            self.iconHandler.findSensorIcon(buttonName).setControlling(True)

         #
         #  Turn all lights off
         buttonName = "IS" + lightNumber + ":BO"
         button = sensors.getSensor(buttonName)

         if (button is None) :
            buttonName = "IS" + lightNumber + ":T"
            button = sensors.getSensor(buttonName)
         if (button is not None) :
            button.setState(INACTIVE)
            #
            # Enable all buttons when we start to keep from being stuck 
            self.iconHandler.findSensorIcon(buttonName).setControlling(True)

      return False              # all done, don't repeat again
initLights().start()          # create one of these, and start it running





 

