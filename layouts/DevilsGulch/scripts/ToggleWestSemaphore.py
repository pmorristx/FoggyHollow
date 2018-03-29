class toggleWestSemaphore(jmri.jmrit.automat.AbstractAutomaton) :
   def init(self):
      return
   def handle(self):
      if sensors.getSensor("IS8:WLC").getState() == ACTIVE :
         sensors.getSensor("IS8:WLL").setState(INACTIVE)
         sensors.getSensor("IS8:WLC").setState(INACTIVE)
         sensors.getSensor("IS8:WLR").setState(ACTIVE)

      elif sensors.getSensor("IS8:WLR").getState() == ACTIVE :
         sensors.getSensor("IS8:WLL").setState(INACTIVE)
         sensors.getSensor("IS8:WLR").setState(INACTIVE)
         sensors.getSensor("IS8:WLC").setState(ACTIVE)

      sensors.getSensor("IS8:CB").setState(ACTIVE)
      sensors.getSensor("IS8:CB").setState(INACTIVE)

      return False;

toggleWestSemaphore().start()          # create one of these, and start it running





 

