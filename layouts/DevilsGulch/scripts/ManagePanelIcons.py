import jmri.jmrit.automat.AbstractAutomaton
class ManagePanelIcons(jmri.jmrit.automat.AbstractAutomaton) :
    def init(self) :
        print "$$$ In ManagePanelIcons.init"
        self.panelEditor = None

    def getPanelHandle(self, panelTitle) :
        print "$$$ In ManagePanelIcons.getPanelHandle"
        #
        #  Get a handle to the panel
        windowsList = jmri.util.JmriJFrame.getFrameList()

        self.windowsList = jmri.util.JmriJFrame.getFrameList()
        self.layoutEditor = None
        for i in range(windowsList.size()) :
            window = windowsList.get(i)
            windowClass = str(window.getClass())
            if (windowClass.endswith(".PanelEditor")) :
                if (window.getTitle().endswith(panelTitle)) :
                    self.panelEditor = window
                    print "$$$ In ManagePanelIcons.getPanelHandle...found panel " + panelTitle
                    break

    def findSensorIcon(self, targetName) :
        print "$$$ In ManagePanelIcons.findSensorIcon ... looking for " + targetName
        if (self.panelEditor != None) :
            contents = self.panelEditor.getContents()
            for i in range(contents.size()) :
                object = contents.get(i)
                objectClass = str(object.getClass())
                if (objectClass.endswith("SensorIcon")) :
                    src = object.getTooltip().getText()
                    if (src == targetName) :
                        return object
#ManagePanelIcons().start()
