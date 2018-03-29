# This is an example script for a JMRI "Automat" in Python

import jarray
import jmri
import java.util.Random

class AceOfSpadesLevel2(jmri.jmrit.automat.AbstractAutomaton) :

	def init(self):
		# init() is called exactly once at the beginning to do
		# any necessary configuration.
		print "Inside init(self)"

		# fwdSensor is reached when loco is running forward
		self.fwdSensor = sensors.provideSensor("OS:L2:BOT")
		self.revSensor = sensors.provideSensor("OS:L2:EOT")
                self.midSensor = sensors.provideSensor("OS:L2:Middle Tunnel")

		# get loco address. For long address change "False" to "True" 
		self.throttle = self.getThrottle(4, False)  # short address 4

                self.electricZap1 = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/ShortElectricClick.wav"))                
		return

        
        def getSpeed(self) :
                return 0.1 + 0.1 * java.util.Random().nextInt(3)
        
        def doBOT(self):
		# wait for sensor in forward direction to trigger, then stop
                print "Waiting for BOT Sensor"
                self.electricZap1.play()
		self.waitSensorActive(self.fwdSensor)
		self.throttle.setSpeedSetting(0)
		self.throttle.setF0(False)

		# delay for a time (remember loco could still be moving
		# due to simulated or actual inertia). Time is in milliseconds
		self.waitMsec(20000 + java.util.Random().nextInt(10000))          # wait for 20 seconds
		
		self.throttle.setIsForward(False)
		self.waitMsec(1000)                 # wait 1 second for Xpressnet to catch up
		self.throttle.setF0(True)
                self.waitMsec(2000)
		self.throttle.setSpeedSetting(self.getSpeed())

                if (sensors.getSensor("IS:L2AUTO").getState() != ACTIVE) :
                        self.throttle.setSpeedSetting(0)
                        self.throttle.setF0(False)                
                
        def doEOT(self):
                # wait for sensor in reverse direction to trigger
                print "Waiting for EOT sensor"
                self.waitSensorActive(self.revSensor)
                self.throttle.setSpeedSetting(0)
                self.throttle.setF0(False)
                        
                # delay for a time (remember loco could still be moving
                # due to simulated or actual inertia). Time is in milliseconds
                self.waitMsec(20000 + java.util.Random().nextInt(10000))          # wait for 20 seconds

                self.throttle.setIsForward(True)
                self.throttle.setF0(True)
                self.waitMsec(2000)
                self.throttle.setSpeedSetting(self.getSpeed())

                if (sensors.getSensor("IS:L2AUTO").getState() != ACTIVE) :
                        self.throttle.setSpeedSetting(0)
                        self.throttle.setF0(False)                
                
               
	def handle(self):
		# handle() is called repeatedly until it returns false.

		# set loco to forward
		self.throttle.setIsForward(True)
		self.throttle.setF0(True)
		
		# wait 1 second for layout to catch up, then set speed
		self.waitMsec(1000)                 
		self.throttle.setF0(True)
		self.throttle.setSpeedSetting(self.getSpeed())

                self.doBOT()

                #  Stop in the middle tunnel 25% of the time when going backward
                if (java.util.Random().nextInt(100) < 25) :
                        print "Waiting for Mid sensor reversing"
                        self.waitSensorActive(self.midSensor)
                        self.throttle.setSpeedSetting(0)
                        self.throttle.setF4(True)
                        self.waitMsec(5000 + java.util.Random().nextInt(10000))

                        if (java.util.Random().nextInt(100) < 40) :
                                #  40% of the time, change directions and go back forward
                                self.throttle.setIsForward(True)
                                
                                self.throttle.setF4(False)
                                self.waitMsec(3000)
                                self.throttle.setSpeedSetting(self.getSpeed())
                        else :
                                                               
                                self.throttle.setF4(False)
                                self.waitMsec(3000)
                                self.throttle.setSpeedSetting(self.getSpeed())
                                self.doEOT()

                        if (sensors.getSensor("IS:L2AUTO").getState() != ACTIVE) :
                                self.throttle.setSpeedSetting(0)
                                self.throttle.setF0(False)                                
                else :
                        self.doEOT()

                #  Stop in the middle tunnel 50% of the time when going forward
                if (java.util.Random().nextInt(100) < 50) :
                        print "Waiting for mid sensor forward"
                        self.waitSensorActive(self.midSensor)
                        self.throttle.setSpeedSetting(0)
                        self.throttle.setF4(True)
                        self.waitMsec(5000 + java.util.Random().nextInt(10000))

                        if (java.util.Random().nextInt(100) < 40) :
                                #  40% of the time, change directions and go back forward
                                self.throttle.setIsForward(False)
                                
                                self.throttle.setF4(False)
                                self.waitMsec(3000)
                                self.throttle.setSpeedSetting(self.getSpeed())
                                self.doEOT()
                        else :
                                                               
                                self.throttle.setF4(False)
                                self.waitMsec(3000)
                                self.throttle.setSpeedSetting(self.getSpeed())


                        if (sensors.getSensor("IS:L2AUTO").getState() != ACTIVE) :
                                self.throttle.setSpeedSetting(0)
                                self.throttle.setF0(False)                                 
                else :
                        self.doEOT()                        
                        
                # and continue around again
                #print "End of Loop"
                if (sensors.getSensor("IS:L2AUTO").getState() != ACTIVE) :
                        self.throttle.setSpeedSetting(0)
                        self.throttle.setF0(False)
                return sensors.getSensor("IS:L2AUTO").getState() == ACTIVE 

# end of class definition

# start one of these up
AceOfSpadesLevel2().start()

