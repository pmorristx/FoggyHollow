class powerTurntable(jmri.jmrit.automat.AbstractAutomaton) :
   def init(self):
      return
   def handle(self):
      self.waitMsec(1000)

      sensors.getSensor("IS22:TT1").setState(INACTIVE)
      sensors.getSensor("IS22:TT2").setState(INACTIVE)
      sensors.getSensor("IS22:TT3").setState(INACTIVE)
      sensors.getSensor("IS22:TT4").setState(INACTIVE)
      
      # If power is on
      if (sensors.getSensor("IS7:TS").getState() == ACTIVE) :
         signals.getSignalHead("IH22:TT1").setAppearance(RED)
         signals.getSignalHead("IH22:TT2").setAppearance(RED)
         signals.getSignalHead("IH22:TT3").setAppearance(RED)
         signals.getSignalHead("IH22:TT4").setAppearance(RED)

         value = str(memories.getMemory("IM21:TT").getValue())
         if (value == str(165)) :
            sensors.getSensor("IS22:TT1").setState(ACTIVE)
            signals.getSignalHead("IH22:TT1").setAppearance(GREEN)
         elif (value == str(30)) :
            sensors.getSensor("IS22:TT2").setState(ACTIVE)
            signals.getSignalHead("IH22:TT2").setAppearance(GREEN)
         elif (value == str(90)) :
            sensors.getSensor("IS22:TT3").setState(ACTIVE)
            signals.getSignalHead("IH22:TT3").setAppearance(GREEN)
         elif (value == str(135)) :
            sensors.getSensor("IS22:TT4").setState(ACTIVE)
            signals.getSignalHead("IH22:TT4").setAppearance(GREEN)
      else :
         signals.getSignalHead("IH22:TT1").setAppearance(DARK)
         signals.getSignalHead("IH22:TT2").setAppearance(DARK)
         signals.getSignalHead("IH22:TT3").setAppearance(DARK)
         signals.getSignalHead("IH22:TT4").setAppearance(DARK)
      return False              # all done, don't repeat again
powerTurntable().start()          # create one of these, and start it running





 

