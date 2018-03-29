import jmri
from datetime import datetime
import threading
import time
from threading import Timer
import java.util.Random

#Created on Jan 29, 2017

class MineBuilding(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):

        self.lights = []
        self.lights.append(sensors.provideSensor("Mine Bldg Loading Dock")) # Mine Bldg Loading Dock
        self.lights.append(sensors.provideSensor("Mine Bldg Side Door")) # Mine Bldg Side Door
        self.lights.append(sensors.provideSensor("Mine Bldg S2")) # Mine Bldg Level 2 - Locker Room
        self.lights.append(sensors.provideSensor("Mine Bldg S3")) # Mine Bldg Tipple        
        
        self.onTimes = [5, 10, 15, 4]
        self.offTimes = [5, 10, 15, 4]
        
        self.firstTime = True
        self.debug = sensors.provideSensor("Private").getState() == ACTIVE
        
    def turnOn(self, light, onTime, offTime):
        if (self.debug) :
            print "MineBuilding.py >>> Turning on " + light.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M")

        try: 
            light.setState(ACTIVE)
            self.waitMsec(250)
            light.setState(ACTIVE)
            self.waitMsec(250)
            light.setState(ACTIVE)
        except:
            light.setState(jmri.jmrix.nce.NceLight.ON)
            self.waitMsec(250)
            light.setState(jmri.jmrix.nce.NceLight.ON)
            self.waitMsec(250)
            light.setState(jmri.jmrix.nce.NceLight.ON)
            
        #delay = java.util.Random().nextInt(self.onTimes[idx])

        xtime = datetime.fromtimestamp(time.time()) + timedelta(minutes=onTime)
        delay = xtime -  datetime.fromtimestamp(time.time())                            
        threading.Timer(delay.total_seconds(), self.turnOff, [light, onTime, offTime]).start()
                    
        if (self.debug) :
            print "MineBuilding.py >>> Turned on " + light.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M")

    def turnOff(self, light, onTime, offTime):
        if (self.debug) :
            print "MineBuilding.py >>> Turning off " + light.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M")

        try: 
            light.setState(INACTIVE)
            self.waitMsec(250)
            light.setState(INACTIVE)
            self.waitMsec(250)
            light.setState(INACTIVE)
        except:
            light.setState(jmri.jmrix.nce.NceLight.OFF)
            self.waitMsec(250)
            light.setState(jmri.jmrix.nce.NceLight.OFF)
            self.waitMsec(250)
            light.setState(jmri.jmrix.nce.NceLight.OFF)
            
        #delay = java.util.Random().nextInt(self.offTimes[idx])

        xtime = datetime.fromtimestamp(time.time()) + timedelta(minutes=offTime)
        delay = xtime -  datetime.fromtimestamp(time.time())                      
        threading.Timer(delay.total_seconds(), self.turnOn, [light, onTime, offTime]).start()
                    
        if (self.debug) :
            print "MineBuilding.py >>> Turned off " + light.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M")
        
    def handle (self):
        if (self.firstTime) :
            self.firstTime = False
            print " Len(self.lights) = " + str(len(self.lights))
            for i in range(len(self.lights)) :
                #delay = java.util.Random().nextInt(self.offTimes[i])

                xtime = datetime.fromtimestamp(time.time()) + timedelta(minutes=self.offTimes[i])
                delay = xtime -  datetime.fromtimestamp(time.time())                
                print "MineBuilding.py >> Scheduling mine building light " + str(i) + " delay = " + str(delay)
                light = self.lights[i]
                onTime = self.onTimes[i]
                offTime = self.offTimes[i]
                threading.Timer(delay.total_seconds(), self.turnOn, [light, onTime, offTime]).start()

        self.waitMsec(100000)

        return True
            
MineBuilding().start()
