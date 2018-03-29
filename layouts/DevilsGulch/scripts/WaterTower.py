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

class WaterTower(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):

        self.waterLevel = memories.provideMemory("Water Level")

        self.waterLevel10 =  memories.provideMemory("Water Level 10")
        self.waterLevel1 =  memories.provideMemory("Water Level 1")
        
        self.wl0 = sensors.provideSensor("Water Level 0")
        self.wl1 = sensors.provideSensor("Water Level 1")
        self.wl2 = sensors.provideSensor("Water Level 2")
        self.wl3 = sensors.provideSensor("Water Level 3")        
        
    def handle (self):

        self.waitChange([self.wl0, self.wl1, self.wl2, self.wl3])
        self.waitMsec(1000) # Wait for all to get set
        val = 0
        if (self.wl0.getState() == ACTIVE) :
            val = val + 1

        if (self.wl1.getState() == ACTIVE) :
            val = val + 2

        if (self.wl2.getState() == ACTIVE) :
            val = val + 4

        if (self.wl3.getState() == ACTIVE) :
            val = val + 8

        self.waterLevel.setValue(val)

        self.waterLevel10.setValue(val/10)
        self.waterLevel1.setValue(val%10)

        self.waitMsec(1000)
        return True
            
WaterTower().start()
