import jmri
import java.util.Random
import datetime
from datetime import datetime, timedelta, date
import time
from time import mktime
import threading
from threading import Timer
#import pytz

#Created on Jan 29, 2017

class OreBin(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):

        self.autoSwitch  = sensors.provideSensor("S3 Auto")
        
        self.debug = sensors.provideSensor("Private").getState() == ACTIVE
        self.random = java.util.Random()
        
        self.insideLights = sensors.provideSensor("Tipple Inside Lights");
        self.bridgeLeft = sensors.provideSensor("Tipple Bridge Light Left");
        self.bridgeRight = sensors.provideSensor("Tipple Bridge Light Right");                
        self.chuteLight = sensors.provideSensor("Tipple Chute Light");
        self.gateLight = sensors.provideSensor("Tipple Gate Light");

        self.whiteLantern = sensors.provideSensor("Tipple EOT White Lantern");
        self.redLantern = sensors.provideSensor("Tipple EOT Red Lantern");                        

        self.chuteLeft = sensors.provideSensor("Tipple Chute Left");
        self.chuteRight = sensors.provideSensor("Tipple Chute Right");

        self.scheduleTimes = []
        self.scheduleTimes.append(memories.provideMemory("Arrives Depot"))        
        
    def turnOn(self, sensor):
        if (self.debug) :
            print "Turning on " + sensor.getUserName() + " at " +  datetime.fromtimestamp(time.time()).strftime("%I:%M");                       
                
        sensor.setState(ACTIVE)

    def turnOff(self, sensor):
        if (self.debug) :
            print "Turning off " + sensor.getUserName() + " at " + datetime.fromtimestamp(mktime(time.localtime())).strftime("%I:%M");                               
        sensor.setState(INACTIVE)

    

    def turnOffLightAfter(self, departureTime, offset, sensor):
        xtime = departureTime + timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.turnOff, [sensor]).start()
            
            
    def turnOnLightAfter(self, arrivalTime, offset, sensor):
        xtime = arrivalTime + timedelta(minutes=offset)
        delay = xtime -  datetime.fromtimestamp(time.time())
        threading.Timer(delay.total_seconds(), self.turnOn, [sensor]).start()            

        
        
    def scheduleUpperLevel(self, dummy):

        now = datetime.fromtimestamp(time.time())
        if (self.autoSwitch.getState() != ACTIVE) :
            prob = self.random.nextInt(100)
            if (prob < 70) :
                self.turnOnLightAfter(now, 0, self.insideLights)
                self.turnOffLightAfter(now, 5, self.insideLights)

                if (self.random.nextInt(100) < 60) :
                    self.turnOnLightAfter(now, 0.5, self.bridgeLeft)
                    self.turnOffLightAfter(now, 4.5, self.bridgeLeft)

                if (self.random.nextInt(100) > 60) :            
                    self.turnOnLightAfter(now, 0.7, self.bridgeRight)
                    self.turnOffLightAfter(now, 4.6, self.bridgeRight)                        

                self.turnOnLightAfter(now, 2.3, self.whiteLantern)
                self.turnOnLightAfter(now, 3.4, self.redLantern)
                self.turnOffLightAfter(now, 4.2, self.redLantern)                        
            elif (prob < 85) :
                self.turnOnLightAfter(now, 0, self.whiteLantern)
                self.turnOffLightAfter(now, 4.2, self.whiteLantern)
            else :
                self.turnOnLightAfter(now, 0, self.insideLights)
                self.turnOffLightAfter(now, 5, self.insideLights)

            probDump = self.random.nextInt(100)
            if (probDump < 65) :
                lowerT = self.random.nextInt(3) + 3
                self.turnOnLightAfter(now, lowerT, self.chuteLight)
                self.turnOffLightAfter(now, lowerT+4, self.chuteLight)
                self.turnOnLightAfter(now, lowerT+1, self.gateLight);
                self.turnOffLightAfter(now, lowerT + 6, self.gateLight);

                if (self.random.nextInt(100) < 50) :
                    self.turnOnLightAfter(now, lowerT + 1, self.chuteLeft)
                    self.turnOffLightAfter(now, lowerT + 3, self.chuteLeft)
                else :
                    self.turnOnLightAfter(now, lowerT + 1, self.chuteRight)
                    self.turnOffLightAfter(now, lowerT + 3, self.chuteRight)
            
        return
            
                    
    def handle (self):
#        self.debug = sensors.provideSensor("Private").getState() == ACTIVE  
#        self.waitChange(self.scheduleTimes)

        self.scheduleUpperLevel(0)
        self.waitMsec(10 * 60 * 1000)                             
        return True
            
OreBin().start()
