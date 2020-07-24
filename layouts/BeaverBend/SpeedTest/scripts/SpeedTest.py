
import os
import sys
sys.path.insert(1, os.path.expanduser('~') + "/MyJMRI/SpeedTest/scripts")

import jmri
import jmri.jmrix.AbstractThrottle

from Locomotive import Locomotive

import datetime

class SpeedTest(jmri.jmrit.automat.AbstractAutomaton) :
        
	def init(self) :

                from EmergencyStopListener import EmergencyStopListener
                from HandleListener import HandleListener                
                from LocomotiveChangeListener import LocomotiveChangeListener                
                from SpeedChangeListener import SpeedChangeListener                
		from Locomotive import Locomotive		

		sensors.getSensor("Start Button").setState(INACTIVE)
		
		memories.getMemory("Bridge 2 Timer").setValue(str(0))
		memories.getMemory("Mine Building Timer").setValue(str(0))

                locoNumber = memories.getMemory("Locomotive Number").getValue()
                
                self.locomotive = Locomotive()
		self.locomotive.init("Foggy Hollow & Western", int(locoNumber), memories)
                memories.getMemory("IM:Loco MFG").setValue(self.locomotive.rosterEntry.getMfg())
                memories.getMemory("IM:Loco Model").setValue(self.locomotive.rosterEntry.getModel())
                memories.getMemory("IM:Loco Decoder").setValue(self.locomotive.rosterEntry.getDecoderFamily())
                memories.getMemory("IM:Loco Decoder Model").setValue(self.locomotive.rosterEntry.getDecoderModel())
                memories.getMemory("IM:Loco ID").setValue("FH&W " + self.locomotive.rosterEntry.getDccAddress())

		locomotiveChangeListener = LocomotiveChangeListener()
		locomotiveChangeListener.init(self, memories, sensors.getSensor("Emergency Stop") )
		memories.getMemory("Locomotive Number").addPropertyChangeListener(locomotiveChangeListener)	                        
                
		self.tunnelSensor = sensors.getSensor("Tunnel")
		self.bridge2Sensor = sensors.getSensor("Bridge-2")

		emergencyStopListener = EmergencyStopListener()
		emergencyStopListener.init(self.locomotive)                
                sensors.getSensor("Emergency Stop").addPropertyChangeListener(emergencyStopListener)	                        

                handleListener = HandleListener()
                handleListener.init(self.locomotive)
                sensors.getSensor("Start Button").addPropertyChangeListener(handleListener)
                
                for i in range(8) :
		        speedChangeListener = SpeedChangeListener()
		        speedChangeListener.init(memories)
                        thisMemory = "Elapsed Time-" + str(i)
		        memories.getMemory(thisMemory).addPropertyChangeListener(speedChangeListener)	                        


        
	def handle(self) :

		self.waitSensorActive(sensors.getSensor("Start Button"))


		memories.getMemory("Bridge 2 Timer").setValue(str(0))
		memories.getMemory("Mine Building Timer").setValue(str(0))
                
                for i in range (8) :
		        memories.getMemory("Feet Per Second-" + str(i)).setValue("0")
		        memories.getMemory("Miles Per Hour-" + str(i)).setValue("0")
		        memories.getMemory("Elapsed Time-" + str(i)).setValue("0")
                        
                        sensors.getSensor("State" + str(i) + "-Grn").setState(INACTIVE)
                        sensors.getSensor("State" + str(i) + "-Yel").setState(INACTIVE)                        
                        sensors.getSensor("State" + str(i) + "-Red").setState(ACTIVE)                                                

                        
                for i in range (8) :
                        if (sensors.getSensor("Start Button").getState() == INACTIVE) :
                                break
                        
                        speedStep =int(memories.getMemory("Speed Step-" + str(i)).getValue())
                        print "Speed step = " + str(speedStep)

                        if (self.stillGoing()) :
                                if (self.tunnelSensor.getState() != ACTIVE) :

                                        self.locomotive.changeDirection("Reverse")
                                        self.locomotive.setSpeed(32)
                                        self.waitSensorInactive(sensors.getSensor("Bridge-2"))
                                        self.waitMsec(3500)
                                        self.locomotive.setSpeed(0)

                        if (self.stillGoing()) :                                        
                                self.locomotive.changeDirection("Forward")
                                self.locomotive.setSpeed(speedStep)			

                                self.waitSensorActive(sensors.getSensor("Bridge-2"))
                                start = datetime.datetime.now()
                                startStr = start.strftime('%I:%M:%S')		
                                memories.getMemory("Bridge 2 Timer").setValue(startStr)
                                sensors.getSensor("IS:state-red-" + str(i)).setState(INACTIVE)
                                sensors.getSensor("IS:state-yel-" + str(i)).setState(ACTIVE)

                        if (self.stillGoing()) :                                                                        
                                self.waitSensorActive(sensors.getSensor("Mine Building"))
                                end = datetime.datetime.now()
                                endStr = end.strftime('%I:%M:%S')				
                                memories.getMemory("Mine Building Timer").setValue(endStr)

                                self.locomotive.setSpeed(0)

                                duration = (end - start).total_seconds()
                                memories.getMemory("Elapsed Time-" + str(i)).setValue(str(format(duration, '.2f')))
                                sensors.getSensor("IS:state-yel-" + str(i)).setState(INACTIVE)
                                sensors.getSensor("IS:state-grn-" + str(i)).setState(ACTIVE)                        

                sensors.getSensor("Start Button").setState(INACTIVE)                        

		return True

        def stillGoing(self) :
                return sensors.getSensor("Start Button").getState() == ACTIVE
        
	def calculateTrackLength(self) :
		actualLength = memories.getMemory("Track Length (Actual)").getValue()						
		scaleLength = (int(actualLength) * 48) / 12
		memories.getMemory("Track Length (Scale)").setValue(scaleLength)
		

		
me = SpeedTest()
me.start()
