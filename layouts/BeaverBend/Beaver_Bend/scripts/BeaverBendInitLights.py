class BeaverBendInitLights(jmri.jmrit.automat.AbstractAutomaton) :
   def init(self):
      import sys
      import ManagePanelIcons

      try :
         sys.path.append(jmri.util.FileUtil.getExternalFilename("preference:scripts"))
         self.iconHandler =  ManagePanelIcons.ManagePanelIcons()
      except:
         print "***"
         print "*** Error in BeaverBendInitLights.py:init(): ", sys.exc_info()[0], sys.exc_info()[1]
         print "***"	                
      return
   
   def handle(self):
      #
      #
      #  Init the power switch to OFF
      sensors.getSensor("IS24:BO").setState(INACTIVE)
      sensors.getSensor("IS24:BF").setState(ACTIVE)

      try :
         self.iconHandler.init()
         self.iconHandler.getPanelHandle("Beaver Bend Editor")
      except:
         print "***"
         print "*** Error getting iconHandler BeaverBendInitLights.py:handle(): ", sys.exc_info()[0], sys.exc_info()[1]
         print "***"	                
      #
      #  Start the threads that monitor button presses on the panel
      try:
         execfile(jmri.util.FileUtil.getExternalFilename("preference:Beaver_Bend/scripts/BeaverBendButtonToggleMonitor.py"))
         execfile(jmri.util.FileUtil.getExternalFilename("preference:Beaver_Bend/scripts/BeaverBendLightMonitor.py"))
      except:
         print "***"
         print "*** Error executing monitor files in BeaverBendInitLights.py:handle(): ", sys.exc_info()[0], sys.exc_info()[1]
         print "***"	                

      #
      # Play the steam whistle on the hour.
#      execfile(jmri.util.FileUtil.getExternalFilename("preference:scripts/FactoryWhistle.py"));

      # Only change water tower ... make sure spout is up.  Don't do order board because it throws the turnouts on power up
      try:
         layoutLights = [24] 
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
               #            self.iconHandler.findSensorIcon(buttonName).setControlling(True)

            #
            #  Turn all lights off
            buttonName = "IS" + lightNumber + ":BO"
            button = sensors.getSensor(buttonName)
   
      except:
         print "***"
         print "*** Error raising water tower spout in BeaverBendInitLights.py:handle(): ", sys.exc_info()[0], sys.exc_info()[1]
         print "***"	                   


      return False              # all done, don't repeat again
BeaverBendInitLights().start()          # create one of these, and start it running





 

