import jmri
import java.awt.Frame
import threading
from threading import Timer

def hidePanel(dummy) :
        jmri.util.JmriJFrame.getFrame("PanelPro").setState(java.awt.Frame.ICONIFIED)

frs = jmri.util.JmriJFrame.getFrameList()
print "Number of frames = " + str(len(frs))

for w in jmri.util.JmriJFrame.getFrameList() :
    print " window = " + w.getTitle()
    if (w.getTitle() == "PanelPro" or w.getTitle() == "JMRI"):
        w.setState(java.awt.Frame.ICONIFIED)
        w.setExtendedState(java.awt.Frame.ICONIFIED)         
    if (w.getTitle() == "WiThrottle") :
        w.setExtendedState(java.awt.Frame.ICONIFIED)
    if (w.getTitle() == "Ace of Spades Mine") :
        w.setExtendedState(java.awt.Frame.NORMAL)
    if (w.getTitle() == "Beaver Bend") :
        w.setExtendedState(java.awt.Frame.NORMAL)
    threading.Timer(20, hidePanel, ["1"]).start()



#f = jmri.util.JmriJFrame.getFrame("PanelPro")
#f.setState(java.awt.Frame.ICONIFIED)


