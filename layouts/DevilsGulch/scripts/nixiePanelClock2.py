from jmri.util import JmriJFrame
from java.util import Arrays
from javax.swing import BoxLayout
from javax.swing import JLabel
from jmri.jmrit.display import PositionableJComponent
from jmri.jmrit.catalog import NamedIcon

class NixiePanelClock(jmri.jmrit.automat.AbstractAutomaton) :
   from jmri.util import JmriJFrame
   from jmri.jmrit.display import PositionableJComponent
   from jmri.jmrit.display import PositionableJPanel

   import java.awt
   import java.awt.event
   import javax.swing
   import java.util.Date

   frame = None
   panelEditor = None
   def init(self):
      return
   def handle(self):
      return              # all done, don't repeat ag

   windowsList = JmriJFrame.getFrameList()
   for i in range(windowsList.size()) :
      window = windowsList.get(i)
      windowClass = str(window.getClass())
      print "Frame class - " + windowClass
      print "Frame title = " + window.getTitle()
      if (window.getTitle() == "Foggy Hollow Control") :
         ctlPanel = window
      if (windowClass.endswith("Editor")) :
         editor = window

   comps = Arrays.asList(ctlPanel.getComponents())
   for j in range (comps.size()) :
      c = comps.get(j)
      print "Component class = " + str(c.getClass())
      if (str(c.getClass()).endswith("JRootPane")) :
         c2 = Arrays.asList(c.getComponents())
         for k in range(c2.size()) :
            d = c2.get(k)
            print "Next class = " + str(d.getClass())
            if (str(d.getClass()).endswith("LayeredPane")) :
               d2 = Arrays.asList(d.getComponents())
               for l in range (d2.size()) :
                 e = d2.get(l)
                 print "Layer class = " + str(e.getClass())

                 if (str(e.getClass()).endswith("JPanel")) :
                     e2 = Arrays.asList(e.getComponents())
                     for m in range (e2.size()) :
                       f = e2.get(m)
                       print "JPanel class = " + str(f.getClass())

                       if (str(f.getClass()).endswith("PositionableJPanel")) :
                           f2 = Arrays.asList(f.getComponents())
                           for n in range (f2.size()) :
                             g = f2.get(n)
                             print "PositionableJPanel class = " + str(g.getClass())
                             if (str(g.getClass()).endswith("JLabel")) :
                                print "Label = " +  g.getText()

                       if (str(f.getClass()).endswith("JScrollPane")) :
                           f2 = Arrays.asList(f.getComponents())
                           for n in range (f2.size()) :
                             g = f2.get(n)
                             print "ScrollPane class = " + str(g.getClass())

                             if (str(g.getClass()).endswith("Viewport")) :
                                 v = g.getView()
                                 print "View = " + str(v.getClass())
                                 if (str(v.getClass()).endswith("TargetPane")) :
                                    v1 = Arrays.asList(v.getComponents())
                                    for p in range(v1.size()) :
                                       v2 = v1.get(p)
                                     #  print "View component = " + v2.getNameString()
                                 
                                 #for o in range (f3.size()) :
                                 #  g2 = f3.get(o)
                                 #  print "viewport class = " + str(g2.getClass())


   newPanel = jmri.jmrit.display.PositionableJPanel(editor)
   newPanel.setLevel(10)
   newPanel.setDisplayLevel(10)
   tube = NamedIcon("resources/icons/misc/Nixie/M1B.gif", "resources/icons/misc/Nixie/M1B.gif")

#   for i in range(10) :
#      baseTubes[i] = NamedIcon("resources/icons/misc/Nixie/M" + i + "B.gif", "resources/icons/misc/Nixie/M" + i + "B.gif")
#      tubes[i] = NamedIcon("resources/icons/misc/Nixie/M" + i + "B.gif", "resources/icons/misc/Nixie/M" + i + "B.gif")
  
#   colonIcon =  NamedIcon("resources/icons/misc/Nixie/colonB.gif", "resources/icons/misc/Nixie/colonB.gif")
#   baseColon =  NamedIcon("resources/icons/misc/Nixie/colonB.gif", "resources/icons/misc/Nixie/colonB.gif")

   #set initial size the same as the original gifs
#   for i in range(10) :
#      scaledImage = baseTubes[i].getImage().getScaledInstance(23,32,Image.SCALE_SMOOTH)
#      tubes[i].setImage(scaledImage)
#  
#   scaledImage = baseColon.getImage().getScaledInstance(12,32,Image.SCALE_SMOOTH)
#   colonIcon.setImage(scaledImage)

   #determine aspect ratio of a single digit graphic
#   iconAspect = 24./32.

   #listen for changes to the timebase parameters
   #clock.addPropertyChangeListener(this);

   #init GUI
#   m1 = JLabel(tubes[0])
#   m2 = JLabel(tubes[0])
#   h1 = JLabel(tubes[0])
#   h2 = JLabel(tubes[0])
#   colon = JLabel(colonIcon)

   h1 = JLabel("TEST MY LABEL")
   newPanel.setLayout(BoxLayout(newPanel, BoxLayout.X_AXIS))
   newPanel.add(h1)
#   newpanel.add(h2)
#   newpanel.add(colon)
#   newpanel.add(m1)
#   newpanel.add(m2)



   v.add(newPanel)



NixiePanelClock().start()          # create one of these, and start it running





 

