from jmri.util import JmriJFrame
class HideNixieIcons(jmri.jmrit.automat.AbstractAutomaton) :
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
         windowClassName = window.__class__.__name__
         if (windowClassName.endswith("PanelEditor")) :
            self.panelEditor = window
            break
      return

   #
   #  Raise/lower loco icons depending on the state of the power switch
   def handle(self):
      if (sensors.getSensor("IS7:TS").getState() == ACTIVE) :
         self.waitMsec(30000)
      else :
         self.waitMsec(1000)
      if (self.panelEditor != None) :
         contents = self.panelEditor.getContents()
         for i in range(contents.size()) :
            object = contents.get(i)
            objectClass = str(object.getClass())
            if (object.__class__.__name__.endswith("MemoryIcon")) :
               # Check if power is on....
               name = object.getMemory().getSystemName()
               if (name.startswith("IM20")) :
                  if (sensors.getSensor("IS7:TS").getState() == ACTIVE) :
                      object.setDisplayLevel(5)
                  else :
                      object.setDisplayLevel(0)
      return False              # all done, don't repeat ag



HideNixieIcons().start()          # create one of these, and start it running





 

