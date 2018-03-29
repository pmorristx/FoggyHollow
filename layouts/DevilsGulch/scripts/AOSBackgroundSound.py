import jarray
import jmri
import java.util.Random
import time
from time import mktime
import threading
from threading import Timer
from datetime import datetime, timedelta, date
import foggyhollow.arduino.DimmableLight
import foggyhollow.arduino.DimmableSensor
from foggyhollow.arduino import TriStateSensor

class AceOfSpadesBackgroundSound(jmri.jmrit.automat.AbstractAutomaton) :

    
    def init(self) :
      	  arOn = lights.provideLight("NL101")
	  arDim = lights.provideLight("NL106")
	  jOn = sensors.provideSensor("Depot Platform On")
	  jOff = sensors.provideSensor("Depot Platform Off")
	  jDim = sensors.provideSensor("Depot Platform Dim")
      	  self.depotPlatform = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)

      	  arOn = lights.provideLight("NL102")
	  arDim = lights.provideLight("NL107")
	  jOn = sensors.provideSensor("Depot Waiting Room On")
	  jOff = sensors.provideSensor("Depot Waiting Room Off")
	  jDim = sensors.provideSensor("Depot Waiting Room Dim")
      	  self.depotWaitingRoom = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)          

      	  arOn = lights.provideLight("LL145")
	  arDim = lights.provideLight("LL149")
	  jOn = sensors.provideSensor("Mine Building Roof Sign On")
	  jOff = sensors.provideSensor("Mine Building Roof Sign Off")
	  jDim = sensors.provideSensor("Mine Building Roof Sign Dim")
      	  self.roofSign = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)

      	  arOn = lights.provideLight("LL143")
	  arDim = lights.provideLight("LL147")
	  jOn = sensors.provideSensor("Mine Building Level 2 On")
	  jOff = sensors.provideSensor("Mine Building Level 2 Off")
	  jDim = sensors.provideSensor("Mine Building Level 2 Dim")
      	  self.mineS2 = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)

      	  arOn = lights.provideLight("LL144")
	  arDim = lights.provideLight("LL148")
	  jOn = sensors.provideSensor("Mine Building Level 3 On")
	  jOff = sensors.provideSensor("Mine Building Level 3 Off")
	  jDim = sensors.provideSensor("Mine Building Level 3 Dim")
      	  self.mineS3 = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)                    

      	  arOn = lights.provideLight("LL140")
	  arDim = lights.provideLight("LL146")
	  jOn = sensors.provideSensor("Mine Building Loading Dock On")
	  jOff = sensors.provideSensor("Mine Building Loading Dock Off")
	  jDim = sensors.provideSensor("Mine Building Loading Dock Dim")
      	  self.loadingDock = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)

      	  arOn = lights.provideLight("Mine Bldg Side Door Light")
	  arDim = None
	  jOn = sensors.provideSensor("Mine Bldg Side Door")
	  jOff = None
	  jDim = None
      	  self.s2 = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)
          
      	  arOn = lights.provideLight("LL143")
	  arDim = None
	  jOn = sensors.provideSensor("Mine Bldg S2")
	  jOff = None
	  jDim = None
      	  self.s2 = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)

      	  arOn = lights.provideLight("LL144")
	  arDim = None
	  jOn = sensors.provideSensor("Mine Bldg S3")
	  jOff = None
	  jDim = None
      	  self.s3 = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)                    

          

      	  arOn = lights.provideLight("LL79")
	  arDim = lights.provideLight("LL80")
	  jOn = sensors.provideSensor("Winding House Boiler Low")
	  jOff = sensors.provideSensor("Winding House Boiler Off")
	  jDim = sensors.provideSensor("Winding House Boiler High")
      	  self.boilerFire = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)

      	  arOn = lights.provideLight("LL74")
	  arDim = lights.provideLight("LL75")
	  jOn = sensors.provideSensor("Winding House Engine Room On")
	  jOff = sensors.provideSensor("Winding House Engine Room Off")
	  jDim = sensors.provideSensor("Winding House Engine Room Dim")
      	  self.engineRoom = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)          

      	  arOn = lights.provideLight("NL123")
	  arDim = lights.provideLight("NL126")
	  jOn = sensors.provideSensor("Freight Dock On")
	  jOff = sensors.provideSensor("Freight Dock Off")
	  jDim = sensors.provideSensor("Freight Dock Dim")
      	  self.freightDock = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)

      	  arOn = lights.provideLight("NL121")
	  arDim = lights.provideLight("NL124")
	  jOn = sensors.provideSensor("Freight Platform On")
	  jOff = sensors.provideSensor("Freight Platform Off")
	  jDim = sensors.provideSensor("Freight Platform Dim")
      	  self.freightPlatform = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)                                        

      	  arOn = lights.provideLight("NL122")
	  arDim = lights.provideLight("NL125")
	  jOn = sensors.provideSensor("Freight Office On")
	  jOff = sensors.provideSensor("Freight Office Off")
	  jDim = sensors.provideSensor("Freight Office Dim")
      	  self.freightOffice = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)

      	  arOn = lights.provideLight("NL120")
	  jOn = sensors.provideSensor("Freight Stove")
      	  self.freightStove = foggyhollow.arduino.DimmableLight(None, arOn, None, jOn, None)          

      	  arOn = lights.provideLight("Level 1 Blue Light")
	  arDim = lights.provideLight("Level 1 Blue Dim")
	  jOn = sensors.provideSensor("L1 Blue Light On")
	  jOff = sensors.provideSensor("L1 Blue Light Off")
	  jDim = sensors.provideSensor("L1 Blue Light Dim")
      	  self.loadingDock = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)
          self.l1Blue = TriStateSensor(jDim,jOn, jOff)
          self.l1Blue.setState(TriStateSensor.ON)

      	  arOn = lights.provideLight("NL133")
	  arDim = lights.provideLight("Level 1 Violet Dim")
	  jOn = sensors.provideSensor("L1 Violet Light On")
	  jOff = sensors.provideSensor("L1 Violet Light Off")
	  jDim = sensors.provideSensor("L1 Violet Light Dim")
      	  self.loadingDock = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)          

      	  arOn = lights.provideLight("Level 1 Yellow Light")
	  arDim = lights.provideLight("Level 1 Yellow Dim")
	  jOn = sensors.provideSensor("L1 Yellow Light On")
	  jOff = sensors.provideSensor("L1 Yellow Light Off")
	  jDim = sensors.provideSensor("L1 Yellow Light Dim")
      	  self.loadingDock = foggyhollow.arduino.DimmableLight(arDim, arOn, jDim, jOn, jOff)

      	  arOn = sensors.provideSensor("Rock Wobble")
	  jOn = sensors.provideSensor("Rock Wobble")
	  jOff = sensors.provideSensor("Rock Off")
      	  self.dragonRock = foggyhollow.arduino.DimmableSensor(None, arOn, None, jOn, jOff)          


          self.demoModeListener = self.DemoModeListener()
          self.demoModeListener.init(self.demoOff, 20)
          
          self.demoMode = sensors.provideSensor("Building Light Demo")
          self.demoMode.setState(jmri.Sensor.ACTIVE)
          self.demoMode.addPropertyChangeListener(self.demoModeListener)          

          self.backgroundSound  = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/DangerousMineNoiseReduction16bit.wav"))
          self.waitMsec(5000)

          return;

    class DemoModeListener(java.beans.PropertyChangeListener) :
        def init(self, callback, delayMinutes):
            self.demoOff = callback
            self.delayMinutes = delayMinutes

        def propertyChange(self, event):
            if (event.source.getState() == jmri.Sensor.ACTIVE) :
                #
                #  Schedule demo mode to end
                #self.scheduler.enter(60*self.delayMinutes, 1, self.demoOff, argument=(event.source,))
                threading.Timer(60*self.delayMinutes, self.demoOff, [event.source]).start()                                
            return  
        
    def demoOff(self, sensor) :
        import jmri
        sensor.setState(jmri.Sensor.INACTIVE)        
        return  

    
    def handle(self):
        self.backgroundSound.play()

        self.waitMsec(60000) # Wait 1 minute

        return  (True)
    
AceOfSpadesBackgroundSound().start()
