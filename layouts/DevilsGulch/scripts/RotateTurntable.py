class rotateTurntable(jmri.jmrit.automat.AbstractAutomaton) :
   def init(self):
      return
   def handle(self):
      sensors.getSensor("IS22:TT1").setState(INACTIVE)
      sensors.getSensor("IS22:TT2").setState(INACTIVE)
      sensors.getSensor("IS22:TT3").setState(INACTIVE)
      sensors.getSensor("IS22:TT4").setState(INACTIVE)

      signals.getSignalHead("IH22:TT1").setAppearance(RED)
      signals.getSignalHead("IH22:TT2").setAppearance(RED)
      signals.getSignalHead("IH22:TT3").setAppearance(RED)
      signals.getSignalHead("IH22:TT4").setAppearance(RED)


      oldvalue = memories.getMemory("IM21:TT").getValue()
      newvalue = (int(oldvalue) + 15) % 180
      memories.getMemory("IM21:TT").setValue(newvalue)

      if (newvalue == 165) :
         sensors.getSensor("IS22:TT1").setState(ACTIVE)
         signals.getSignalHead("IH22:TT1").setAppearance(GREEN)
      elif (newvalue == 30) :
         sensors.getSensor("IS22:TT2").setState(ACTIVE)
         signals.getSignalHead("IH22:TT2").setAppearance(GREEN)
      elif (newvalue == 90) :
         sensors.getSensor("IS22:TT3").setState(ACTIVE)
         signals.getSignalHead("IH22:TT3").setAppearance(GREEN)
      elif (newvalue == 135) :
         sensors.getSensor("IS22:TT4").setState(ACTIVE)
         signals.getSignalHead("IH22:TT4").setAppearance(GREEN)
      return False              # all done, don't repeat again
rotateTurntable().start()          # create one of these, and start it running





 

