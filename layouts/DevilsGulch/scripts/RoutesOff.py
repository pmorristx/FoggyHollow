class routesOff(jmri.jmrit.automat.AbstractAutomaton) :
   def init(self):
     return
   def handle(self):
     self.waitMsec(1000)         # time is in milliseconds

     sensors.getSensor("IS81:BK").setState(INACTIVE)
     sensors.getSensor("IS81:AK").setState(INACTIVE)

     sensors.getSensor("IS82:BK").setState(INACTIVE)
     sensors.getSensor("IS82:AK").setState(INACTIVE)

     sensors.getSensor("IS83:BK").setState(INACTIVE)
     sensors.getSensor("IS83:AK").setState(INACTIVE)

     sensors.getSensor("IS84:BK").setState(INACTIVE)
     sensors.getSensor("IS84:AK").setState(INACTIVE)

     sensors.getSensor("IS85:BK").setState(INACTIVE)
     sensors.getSensor("IS85:AK").setState(INACTIVE)

     sensors.getSensor("IS81:RTE").setState(INACTIVE)
     sensors.getSensor("IS82:RTE").setState(INACTIVE)
     sensors.getSensor("IS83:RTE").setState(INACTIVE)
     sensors.getSensor("IS84:RTE").setState(INACTIVE)
     sensors.getSensor("IS85:RTE").setState(INACTIVE)

     sensors.getSensor("IS10:TNW").setState(INACTIVE)
     sensors.getSensor("IS10:TNC").setState(INACTIVE)
     sensors.getSensor("IS10:TNE").setState(INACTIVE)
     sensors.getSensor("IS10:TCW").setState(INACTIVE)
     sensors.getSensor("IS10:TCC").setState(INACTIVE)
     sensors.getSensor("IS10:TCE").setState(INACTIVE)
     sensors.getSensor("IS10:TSW").setState(INACTIVE)
     sensors.getSensor("IS10:TSC").setState(INACTIVE)
     sensors.getSensor("IS10:TSE").setState(INACTIVE)

     return False              # all done, don't repeat again
routesOff().start()          # create one of these, and start it running





 

