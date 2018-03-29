class randomArc(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        self.electricZap1 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ShortElectricClick.wav"))
        self.electricZap2 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ShortTesla.wav"))
        self.electricZap3 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ElectricSizzle.wav"))
        self.electricZap4 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ElectricSizzle2.wav"))       
        return

    def handle(self) :
        #
        # Play random arcing sound...for long sounds delay before turning light on.
        try :
            delay = 50
            prob =  java.util.Random().nextInt(10) # Switch arcing delay
            if (prob > 9):
                self.electricZap4.play()
                delay = 950
            elif (prob > 8) :
                self.electricZap3.play()
                delay = 800
            elif (prob > 6) :
                self.electricZap2.play()
                delay = 350
            elif (prob > 2) :
                self.electricZap1.play()
                delay = 250

            self.waitMsec(delay)
        except :
            print "*** Failure in randomArc.py"
        return 0

randomArc().start()          # create one of these, and start it running	
