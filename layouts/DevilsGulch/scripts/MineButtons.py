import jmri
from Building import Building
from datetime import datetime, timedelta, date
import threading
import time
from time import mktime
from threading import Timer
#import pytz

#Created on Jan 29, 2017

class MineButtons(jmri.jmrit.automat.AbstractAutomaton):
    
    def init(self):
        #
        self.hoistL4 = sensors.provideSensor("IS Call Hoist To L4")
        self.hoistL1 = sensors.provideSensor("IS Call Hoist To L1")
        self.hoistL2 = sensors.provideSensor("IS Call Hoist To L2")
        self.hoistL3 = sensors.provideSensor("IS Call Hoist To L3")
        self.hoistS2 = sensors.provideSensor("IS Call Hoist To S2")
        self.hoistS1 = sensors.provideSensor("IS Call Hoist To S1")
        self.hoistS3 = sensors.provideSensor("IS Call Hoist To S3") 
        
#
#        self.hoistSump = sensors.provideSensor("Hoist Sump")
#        self.hoistL1 = sensors.provideSensor("Hoist Level 1")
#        self.hoistL2 = sensors.provideSensor("Hoist Top")
#        self.hoistL3 = sensors.provideSensor("Hoist Bottom")
#        self.hoistLocker = sensors.provideSensor("Hoist 2nd Floor")
#        self.hoistSurface = sensors.provideSensor("Hoist Surface")
#        self.hoistTipple = sensors.provideSensor("Hoist Tipple") 

        self.hoistLevels = []          
        self.hoistLevels.append(self.hoistL4)
        self.hoistLevels.append(self.hoistL3)                                             
        self.hoistLevels.append(self.hoistL2)                                             
        self.hoistLevels.append(self.hoistL1)                                             
        self.hoistLevels.append(self.hoistS1)                                             
        self.hoistLevels.append(self.hoistS2)   
        self.hoistLevels.append(self.hoistS3)
        

        self.raiseHoistSound = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Short-Short-Long-Signal.wav"))
        self.lowerHoistSound = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Short-Long-Signal.wav"))        
        self.hoistBells = []
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/QuadShortSignal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/TripleShortSignal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/DoubleShortSignal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/SingleShortSignal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Long-Short-Signal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Long-Short-Short-Signal.wav")))
        self.hoistBells.append(jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Long-Short-Short-Short-Signal.wav")))        
        
        self.currentHoistIdx = 0 # Default at sump      
        

    def setHoistLevel (self, gotoIdx):

        #
        #  Turn up the lights if we go to level 1.
        if (gotoIdx == 3) : # Level 1
            sensors.provideSensor("Level 1 Light").setState(ACTIVE)
            sensors.provideSensor("Level 1 Light Dim").setState(INACTIVE)
        else :
            sensors.provideSensor("Level 1 Light Dim").setState(ACTIVE)            

        if (gotoIdx != self.currentHoistIdx) :
            self.windingHouseLights.setF0(True)
            self.windingHouseEngineRoom.setState(jmri.jmrix.nce.NceLight.ON)

        if (gotoIdx > self.currentHoistIdx) :  # Going up
            self.raiseHoistSound.play()
            self.waitMsec(8000)
            self.hoistBells[gotoIdx].play()
            self.waitMsec(8000) 
            sensors.provideSensor("Hoist Moving").setState(jmri.Sensor.ACTIVE)
            sensors.provideSensor("Hoist Moving Up").setState(jmri.Sensor.ACTIVE)
            for i in range(self.currentHoistIdx, gotoIdx + 1) :
                self.waitMsec(2500)
                self.hoistLevels[i].setState(jmri.Sensor.ACTIVE)
                if (i != gotoIdx) :
                    self.waitMsec(2500)
                    self.hoistLevels[i].setState(jmri.Sensor.INACTIVE)
        elif (gotoIdx < self.currentHoistIdx) :  # Going down
            self.lowerHoistSound.play()
            self.waitMsec(8000)
            self.hoistBells[gotoIdx].play()
            self.waitMsec(8000)      
            sensors.provideSensor("Hoist Moving").setState(jmri.Sensor.ACTIVE)
            sensors.provideSensor("Hoist Moving Down").setState(jmri.Sensor.ACTIVE)
            for i in range(self.currentHoistIdx, gotoIdx - 1, -1) :
                self.waitMsec(2500)
                self.hoistLevels[i].setState(jmri.Sensor.ACTIVE)
                if (i != gotoIdx) :
                    self.waitMsec(2500)
                    self.hoistLevels[i].setState(jmri.Sensor.INACTIVE)
        sensors.provideSensor("Hoist Moving Up").setState(jmri.Sensor.INACTIVE)
        sensors.provideSensor("Hoist Moving Down").setState(jmri.Sensor.INACTIVE)
        sensors.provideSensor("Hoist Moving").setState(jmri.Sensor.INACTIVE)
        
                                
    def handle (self):
        
        self.waitChange(self.scheduleTimes)
        
        return True
            
MineButtons().start()
