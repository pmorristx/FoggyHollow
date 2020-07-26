import java
import jmri
import java.util.Random

class BeaverBendLightMonitor(jmri.jmrit.automat.AbstractAutomaton) :
    def init(self):
        return
    def handle(self):
        # For the sensors that exist, attach a sensor listener
        ButtonList = ["IS:STA1:ON", "IS:STA1:OFF", "IS:STA2:ON", "IS:STA2:OFF", "IS:STA3:ON", "IS:STA3:OFF", "IS:STA4:ON", "IS:STA4:OFF"]
        throttle = self.getThrottle(20, False)        
        listener = self.SensorListener()
        listener.init(throttle)      
        for i in range(len(ButtonList)) :
            sensors.getSensor(ButtonList[i]).addPropertyChangeListener(listener)        
        return;
    

    # Define the sensor listener: Print some
    # information on the status change.
    import java
    import java.util.Random
    class SensorListener(java.beans.PropertyChangeListener) :
        
        def init(self, throttle) :
            self.throttle = throttle
            self.buttonClick = jmri.jmrit.Sound("resources/sounds/Signal-normal.wav")
            self.electricZap1 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ShortElectricClick.wav"))
            self.electricZap2 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ShortTesla.wav"))
            self.electricZap3 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ElectricSizzle.wav"))
            self.electricZap4 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ElectricSizzle2.wav"))       
            return
    
        import java
        def randomArc(self) :
            import java.util.Random
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
        
        
        def propertyChange(self, event):
            
            if (event.propertyName == "KnownState") :
                mesg = "Sensor "+event.source.systemName
            if (event.source.userName != None) :
                mesg += " ("+event.source.userName+")"
            print mesg
                
            self.buttonClick.play()
            
            self.randomArc()      
            
            buttonName = event.source.systemName
            button = sensors.getSensor(buttonName)
            buttonNumber = buttonName[6:7]
            prefix = buttonName[0:8]
            buttonOn = prefix + "ON"
            buttonOff = prefix + "OFF"
            buttonIndicator = prefix + "K"
            

            if (buttonNumber == "1") :
                print "Button = " + buttonName + " Number = " + buttonNumber + " On Button = " + buttonOn          
                if (button.getKnownState() == ACTIVE and buttonName.endswith("ON")) :
                    self.throttle.setF1(True)
                    sensors.getSensor(buttonOff).setState(INACTIVE)
                    sensors.getSensor(buttonIndicator).setState(ACTIVE)
                elif (button.getKnownState() == ACTIVE and buttonName.endswith("OFF")) :
                    self.throttle.setF1(False)    
                    sensors.getSensor(buttonOn).setState(INACTIVE)
                    sensors.getSensor(buttonIndicator).setState(INACTIVE)                    
            elif (buttonNumber == "2") :      
                if (button.getKnownState() == ACTIVE and buttonName.endswith("ON")) :
                    self.throttle.setF4(True)
                    sensors.getSensor(buttonOff).setState(INACTIVE)
                    sensors.getSensor(buttonIndicator).setState(ACTIVE)
                elif (button.getKnownState() == ACTIVE and buttonName.endswith("OFF")) :
                    self.throttle.setF4(False)    
                    sensors.getSensor(buttonOn).setState(INACTIVE)
                    sensors.getSensor(buttonIndicator).setState(INACTIVE)                
            elif (buttonNumber == "3") :      
                if (button.getKnownState() == ACTIVE and buttonName.endswith("ON")) :
                    self.throttle.setF3(True)
                    sensors.getSensor(buttonOff).setState(INACTIVE)
                    sensors.getSensor(buttonIndicator).setState(ACTIVE)
                elif (button.getKnownState() == ACTIVE and buttonName.endswith("OFF")) :
                    self.throttle.setF3(False)    
                    sensors.getSensor(buttonOn).setState(INACTIVE)
                    sensors.getSensor(buttonIndicator).setState(INACTIVE)  
            elif (buttonNumber == "4") :      
                if (button.getKnownState() == ACTIVE and buttonName.endswith("ON")) :
                    self.throttle.setF2(True)
                    sensors.getSensor(buttonOff).setState(INACTIVE)
                    sensors.getSensor(buttonIndicator).setState(ACTIVE)
                elif (button.getKnownState() == ACTIVE and buttonName.endswith("OFF")) :
                    self.throttle.setF2(False)    
                    sensors.getSensor(buttonOn).setState(INACTIVE)
                    sensors.getSensor(buttonIndicator).setState(INACTIVE)                                              
            # You can also speak the message by un-commenting the next line
            #java.lang.Runtime.getRuntime().exec(["speak", mesg])
            # For more info on the speak command, see http://espeak.sf.net/
            return
    


# Define a Manager listener.  When invoked, a new
# item has been added, so go through the list of items removing the 
# old listener and adding a new one (works for both already registered
# and new sensors)
#class ManagerListener(java.beans.PropertyChangeListener):
#  def propertyChange(self, event):
      
#    listener = SensorListener()      
#    ButtonList = ["IS:200"]
#    for i in range(len(ButtonList)) :
#        event.source.getSensor(ButtonList[i]).removePropertyChangeListener(listener)
#        event.source.getSensor(ButtonList[i]).addPropertyChangeListener(listener)

# Attach the sensor manager listener
#sensors.addPropertyChangeListener(ManagerListener())

BeaverBendLightMonitor().start()          # create one of these, and start it running


 
