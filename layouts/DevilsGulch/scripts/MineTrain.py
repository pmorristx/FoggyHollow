import jarray
import jmri
import java.util.Random
import sys

class MineTrain(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self, locoNumber, level):
        print "Initializing Mine Train " + str(locoNumber)
        self.locoNumber = locoNumber
        self.level = level
        self.speed = 0.0
        
        self.level_1_blocks = ["L1 Hoist Entrance", "L1 Front Tunnel", "L1 Tipple", "L1 Right Tunnel", "L1 Back Cavern", "L1 Back Tunnel", "L1 Left Tunnel"]
        self.level_2_blocks = ["L2 BOT", "L2 Hoist Cavern", "L2 Middle Tunnel", "L2 Right Bridge", "L2 Right Tunnel", "L2 EOT"]
        
        return            

    def findTrain(self) :    
        trainName = "No. " + str(self.locoNumber)
        print "initializing loco " + trainName
        
        if (self.level == 1):
            levelBlocks = self.level_1_blocks
        else:
            levelBlocks = self.level_2_blocks
            
        blocks = jmri.InstanceManager.blockManagerInstance()                
        for blockName in levelBlocks :
            print "Check occupancy for block " + blockName
            block = blocks.provideBlock(blockName)
            if (block.getSensor().getState() == jmri.Sensor.ACTIVE) :
                block.setValue (trainName)    
    #
    #  Returns a randomized speed.  Reverse speeds are slower than forward
    def getSpeed(self, isForward) :
        if (isForward) :
            if (self.level == 2) :            
                self.speed = 0.15 + 0.1 * self.random.nextInt(3)
            else :
                self.speed = 0.15 + 0.1 * self.random.nextInt(2)                
        else :
            if (self.level == 2) :
                self.speed =  0.15 + 0.1 * self.random.nextInt(1)
            else :
                self.speed =  0.1                 
        if (self.level == 2) :
            print "Getting speed = " + str(self.speed)    
        return self.speed
        
    #
    #  Returns a randomized speed.  Reverse speeds are slower than forward
    def getAspectSpeed(self, isForward, aspect) :
        if (aspect == "Approach" or not isForward) :
                self.speed =  0.15 + 0.1 * self.random.nextInt(1)    
        else :                    
                self.speed = 0.15 + 0.1 * self.random.nextInt(3)
        return self.speed            

    #
    #  Stop the train.  Put headlight to dim, then turn it off.
    def stopTrain(self) :
        print "Stopping train in MineTrain.py"
        self.throttle.setSpeedSetting(0)
        self.waitMsec(1)
        self.throttle.setSpeedSetting(0)
        self.waitMsec(1)
        self.throttle.setSpeedSetting(0)        
        self.waitMsec((self.random.nextInt(3) + 2) * 1000)                                
        self.throttle.setF4(True)
        self.waitMsec((self.random.nextInt(2) + 1) * 1000)                                
        # self.throttle.setF0(False)
        # self.waitMsec((self.random.nextInt(2)+1) * 1000)
        self.singleToot.play()

    #
    #  Start the train moving in the requested direction.  Turn the headlight on first, then undim it, then get
    #  a random speed to start moving.
    def startTrain(self, isForward):

        self.throttle.setF1(True)  # Turn brake light on
        self.throttle.setIsForward(isForward)
        self.throttle.setF2(True)  # Turn on beacon
        self.throttle.setF0(True)  # Turn on headlight                
        self.waitMsec((self.random.nextInt(2) + 1) * 1000)                
        self.throttle.setF4(False)  # Turn dim off
        self.waitMsec((self.random.nextInt(2) + 1) * 1000)
        #
        #  Signal direction
        if (isForward):
            self.doubleToot.play()
        else:
            self.tripleToot.play()
                
        self.waitMsec((self.random.nextInt(3) + 2) * 1000)
        # Start moving
        self.throttle.setSpeedSetting(self.getSpeed(isForward))

    def startTrainSlow(self, isForward):

        self.throttle.setF1(True)  # Turn brake light on
        self.throttle.setIsForward(isForward)
        self.throttle.setF2(True)  # Turn on beacon
        self.throttle.setF0(True)  # Turn on headlight                
        self.waitMsec((self.random.nextInt(2) + 1) * 1000)                
        self.throttle.setF4(False)  # Turn dim off
        self.waitMsec((self.random.nextInt(2) + 1) * 1000)
        #
        #  Signal direction
        if (isForward):
            self.doubleToot.play()
        else:
            self.tripleToot.play()
                
        self.waitMsec((self.random.nextInt(3) + 2) * 1000)
        # Start moving
        self.speed = 0.1
        self.throttle.setSpeedSetting(self.speed)        
        
    #
    #  Start the train moving in the requested direction based on a signal
    def startTrainByAspect(self, isForward, aspect):
        
        if (aspect == "Stop") :
            self.stopTrain()
        else :
            if (self.throttle.getSpeedSetting() == 0) :
                self.throttle.setF1(True)  # Turn brake light on
                self.throttle.setIsForward(isForward)
                self.throttle.setF2(True)  # Turn on beacon
                self.throttle.setF0(True)  # Turn on headlight                
                self.waitMsec((self.random.nextInt(2) + 1) * 1000)                
                self.throttle.setF4(False)  # Turn dim off
                self.waitMsec((self.random.nextInt(2) + 1) * 1000)
                #
                #  Signal direction
                if (isForward):
                    self.doubleToot.play()
                else         :
                    self.tripleToot.play()
                    
                self.waitMsec((self.random.nextInt(3) + 2) * 1000)
                
            # Start moving
            self.throttle.setSpeedSetting(self.getAspectSpeed(isForward, aspect))                
        return

            
    def loadSoundFile(self, path) :
        try :
            print "Loading sound file " + path
            return jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename(path)) # 1.37
        except :
            print "Error creating sound file ", path, sys.exc_info()[0], sys.exc_info()[1]                

# end of class definition
