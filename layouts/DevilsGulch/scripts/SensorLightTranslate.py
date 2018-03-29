import jmri
import foggyhollow.arduino.DimmableLight
import foggyhollow.arduino.DimmableSensor


class SensorLightTranslate(jmri.jmrit.automat.AbstractAutomaton) :
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

      	  arOn = sensors.provideSensor("Mine Bldg Roof")
	  arDim = sensors.provideSensor("Mine Bldg Roof Dim")
	  jOn = sensors.provideSensor("Mine Building Roof Sign On")
	  jOff = sensors.provideSensor("Mine Building Roof Sign Off")
	  jDim = sensors.provideSensor("Mine Building Roof Sign Dim")
      	  self.roofSign = foggyhollow.arduino.DimmableSensor(arDim, arOn, jDim, jOn, jOff)

      	  arOn = sensors.provideSensor("Mine Bldg Loading Dock")
	  arDim = sensors.provideSensor("Mine Bldg Loading Dock Dim")
	  jOn = sensors.provideSensor("Mine Building Loading Dock On")
	  jOff = sensors.provideSensor("Mine Building Loading Dock Off")
	  jDim = sensors.provideSensor("Mine Building Loading Dock Dim")
      	  self.loadingDock = foggyhollow.arduino.DimmableSensor(arDim, arOn, jDim, jOn, jOff)

      	  arOn = sensors.provideSensor("Winding House Boiler Fire")
	  arDim = sensors.provideSensor("Winding House Boiler Intensity")
	  jOn = sensors.provideSensor("Winding House Boiler Low")
	  jOff = sensors.provideSensor("Winding House Boiler Off")
	  jDim = sensors.provideSensor("Winding House Boiler High")
      	  self.boilerFire = foggyhollow.arduino.DimmableSensor(arDim, arOn, jDim, jOn, jOff)

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

      	  arOn = sensors.provideSensor("Level 1 Blue Light")
	  arDim = sensors.provideSensor("Level 1 Blue Light Dim")
	  jOn = sensors.provideSensor("L1 Blue Light On")
	  jOff = sensors.provideSensor("L1 Blue Light Off")
	  jDim = sensors.provideSensor("L1 Blue Light Dim")
      	  self.loadingDock = foggyhollow.arduino.DimmableSensor(arDim, arOn, jDim, jOn, jOff)

      	  arOn = sensors.provideSensor("Level 1 Violet Light On")
	  arDim = sensors.provideSensor("Level 1 Violet Light Dim")
	  jOn = sensors.provideSensor("L1 Violet Light On")
	  jOff = sensors.provideSensor("L1 Violet Light Off")
	  jDim = sensors.provideSensor("L1 Violet Light Dim")
      	  self.loadingDock = foggyhollow.arduino.DimmableSensor(arDim, arOn, jDim, jOn, jOff)          

      	  arOn = sensors.provideSensor("Level 1 Yellow Light")
	  arDim = sensors.provideSensor("Level 1 Yellow Light Dim")
	  jOn = sensors.provideSensor("L1 Yellow Light On")
	  jOff = sensors.provideSensor("L1 Yellow Light Off")
	  jDim = sensors.provideSensor("L1 Yellow Light Dim")
      	  self.loadingDock = foggyhollow.arduino.DimmableSensor(arDim, arOn, jDim, jOn, jOff)          
          
      def handle(self):
            self.waitMsec(10000)
            return True

SensorLightTranslate().start()
      	  
