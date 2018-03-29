class toggleEastSemaphore(jmri.jmrit.automat.AbstractAutomaton) :
   def init(self):
      return
   def handle(self):
      if sensors.getSensor("IS6:WLC").getState() == ACTIVE :
         sensors.getSensor("IS6:WLL").setState(INACTIVE)
         sensors.getSensor("IS6:WLC").setState(INACTIVE)
         sensors.getSensor("IS6:WLR").setState(ACTIVE)

      elif sensors.getSensor("IS6:WLR").getState() == ACTIVE :
         sensors.getSensor("IS6:WLL").setState(INACTIVE)
         sensors.getSensor("IS6:WLR").setState(INACTIVE)
         sensors.getSensor("IS6:WLC").setState(ACTIVE)

      sensors.getSensor("IS6:CB").setState(ACTIVE)
      sensors.getSensor("IS6:CB").setState(INACTIVE)

      return False;

toggleEastSemaphore().start()          # create one of these, and start it running





 

