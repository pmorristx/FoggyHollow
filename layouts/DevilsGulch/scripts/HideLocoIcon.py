from jmri.util import JmriJFrame
class HideLocoIcon(jmri.jmrit.automat.AbstractAutomaton) :
   from jmri.util import JmriJFrame
   #
   #  Initialize - Find panelEditor window.
   def init(self):
      windowsList = JmriJFrame.getFrameList()

      self.panelEditor = None
      self.windowsList = JmriJFrame.getFrameList()
      self.layoutEditor = None
      for i in range(windowsList.size()) :
         window = windowsList.get(i)
         windowClass = str(window.getClass())
         if (windowClass.endswith(".PanelEditor")) :
            self.panelEditor = window
            break
      return

   #
   #  Raise/lower loco icons depending on the state of the power switch
   def handle(self):
      if (self.panelEditor != None) :
         contents = self.panelEditor.getContents()
         for i in range(contents.size()) :
            object = contents.get(i)
            objectClass = str(object.getClass())
            if (objectClass.endswith(".LocoIcon")) :
               # Check if power is on....
               if (sensors.getSensor("IS7:TS").getState() == ACTIVE) :
                   object.setDisplayLevel(10)
               else :
                   object.setDisplayLevel(1)
      #      elif (objectClass.endswith("SensorIcon")) :
      #         src = object.getSensor()
      #         target = sensors.getSensor("IS:BLNK")
      #         if (src == target) :
      #            if (sensors.getSensor("IS7:TS").getState() == ACTIVE) :
      #               object.setDisplayLevel(1)
      #            else:
      #               object.setDisplayLevel(10)
      return False              # all done, don't repeat ag



HideLocoIcon().start()          # create one of these, and start it running





 

