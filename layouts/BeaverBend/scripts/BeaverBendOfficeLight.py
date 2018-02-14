class officeLight(jmri.jmrit.automat.AbstractAutomaton) :
    import java
    import javax.swing
    def init(self):
        self.buttonClick = jmri.jmrit.Sound("resources/sounds/Signal-normal.wav")
        self.electricZap1 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ShortElectricClick.wav"))
        self.electricZap2 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ShortTesla.wav"))
        self.electricZap3 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ElectricSizzle.wav"))
        self.electricZap4 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ElectricSizzle2.wav"))       
        return

    def randomArc(self) :
        #
        # Play random arcing sound...for long sounds delay before turning light on.
        delay = 50
        prob =  java.util.Random().nextInt(10) # Switch arcing delay
        if (prob > 9) :
            self.electricZap4.play()
            delay = 900
        elif (prob > 8) :
            self.electricZap3.play()
            delay = 750
        elif (prob > 6) :
            self.electricZap2.play()
            delay = 300
        elif (prob > 2) :
            self.electricZap1.play()
            delay = 200

 #       self.parent.waitMsec(delay)
        return

    def handle(self):
        
        self.buttonClick.play()
        self.randomArc()          
        throt = self.getThrottle(3, False)
        button = sensors.getSensor("IS:200")
        if (button.getKnownState() == ACTIVE) :
            throt.setF1(False)
        else :
            throt.setF1(True)
        
        
        return False              # all done, don't repeat again
officeLight().start()          # create one of these, and start it running	