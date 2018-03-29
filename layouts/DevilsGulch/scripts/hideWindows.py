import jmri
import java.awt.Frame


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
        w.setExtendedState(java.awt.Frame.MAXIMIZED_BOTH)


#f = jmri.util.JmriJFrame.getFrame("PanelPro")
#f.setState(java.awt.Frame.ICONIFIED)


