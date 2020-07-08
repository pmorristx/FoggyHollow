import jmri.jmrit

class Locomotive(jmri.jmrit.automat.AbstractAutomaton) :

    #
    #  Initialize the locomotive using the Roadname and Road number used in the 
    #  JMRI Roster.  This needs to be a unique match.
    def init(self, roadName, locoNumber):
        self.rosterEntry = []
        self.functionMap = {}
                
        self.locoNumber = locoNumber
        self.roadName = roadName

        print "*** Getting throttle for ", self.locoNumber
        self.throttle = self.getThrottle(self.locoNumber, False)
        print "*** Get throttle complete"
        
        rosterlist = jmri.jmrit.roster.Roster.getDefault().matchingList(roadName, str(locoNumber), None, None, None, None, None) 
        if (len(rosterlist) == 1) :
            self.rosterEntry = rosterlist[0]
        else :
            print "Error finding locomotive ", roadName, " #", str(locoNumber), "in Roster"
            
        #
        # Map the functions to the names in the JMRI function labels.  This allows different
        # decoders to have functions on different function numbers.
        self.mapFunctions()
        
        return 0
    
    #=======================================================================================
    #
    #  Function Mapping
    #
    #  Map the function numbers to the labels identified in the roster
    def mapFunctions(self):

        self.functionMap["Light"] = self.findFunction("Light")        
        self.functionMap["Bell"] = self.findFunction("Bell")
        self.functionMap["Whistle"] = self.findFunction("Whistle")        
        self.functionMap["Toot"] = self.findFunction("Toot")        
        self.functionMap["Quill"] = self.findFunction("Quill")        
        self.functionMap["TenderMarkers"] = self.findFunction("Tender")        
        self.functionMap["CabLight"] = self.findFunction("Cab")
        self.functionMap["SteamRelease"] = self.findFunction("Steam")
        self.functionMap["BlowOutBoiler"] = self.findFunction("BlowOut")          
        self.functionMap["WaterFill"] = self.findFunction("Water")        
        self.functionMap["BrakeSet"] = self.findFunction("BrakeSet")        
        self.functionMap["BrakeRelease"] = self.findFunction("BrakeRel")
        self.functionMap["AirCompressor"] = self.findFunction("Air")        
        self.functionMap["AshDump"] = self.findFunction("Ash")
        self.functionMap["Coupler"] = self.findFunction("Coupler")
        self.functionMap["Blower"] = self.findFunction("Blower")
        self.functionMap["BlowOut"] = self.findFunction("BlowOut")  
        self.functionMap["Safety"] = self.findFunction("Safety")
        self.functionMap["J-Bar Down"] = self.findFunction("J-Bar Down")                                      
        self.functionMap["CylinderCox"] = self.findFunction("Cyl")                                              
        self.functionMap["DimLight"] = self.findFunction("Dim")                                                      
        
        print "\n\n", self.roadName, " #", self.locoNumber, ": ", self.functionMap, "\n\n"  
        return 0                                                             
    
    #
    #  Search the roster entry function map for the function with the specified label      
    def findFunction(self, label):
        for fn in range(0, 29) :
            fnlabel = self.rosterEntry.getFunctionLabel(fn)
            if (fnlabel != None and fnlabel.startswith(label)) :
                return fn
        return -1
    
    #
    #  Set the function identified by the label to the specified state.     
    def setFunction(self, label, state):
        import sys
        try :
            if (self.functionMap[label] >= 0) :
                getattr(self.throttle, "setF" + str(self.functionMap[label]))(state)
        except :
            print "Unable to set function ", label, " on ", self.roadName, " #",  str(self.locoNumber) 
            print "***", sys.exc_info()[0], " ", sys.exc_info()[1]
        return 0
    
    def getFunction(self, label):
        return getattr(self.throttle, "getF" + str(self.functionMap[label]))()

    #
    #========================================================================================             
    #
    #  Locomotive Functions
    #
    # Set the speed of the locomotive
    def setSpeed(self, speed):
        self.throttle.setSpeedSetting(speed)
    #
    # Change the direction of the locomotive.  Parameter should be "Forward" or "Reverse"
    def changeDirection(self, direction):

        #print "Locomotive.changeDirection ", self.roadName, " #",  str(self.locoNumber), " to ", direction
        self.reseting = False
        if (direction == "Reverse"):
            self.throttle.setIsForward(False)
            self.setJohnsonBar(True)
        else :
            self.throttle.setIsForward(True)
            self.setJohnsonBar(False)    
   
        self.waitMsec(2000)    
        return 0
    #
    #========================================================================================
    #  
    #  Light Functions
    #
    #========================================================================================
    #
    #  Headlight     
    def setLight(self, state):  
        self.setFunction("Light", state) 
        return 0
    #
    #  Cab Light
    def setCabLight(self, state):
        self.setFunction("CabLight", state)
        self.waitMsec(1000)
        return 0    
    #
    #  Tender Markers
    def setTenderMarkers(self, state) :
        self.setFunction("TenderMarkers", state)

    #
    #  Dim the headlight
    def dimLight(self, state):
        self.setFunction("DimLight", state)
        return 
        
    #
    #========================================================================================
    #  
    #  Whistle Functions
    #
    #========================================================================================
    #
    #  Whistle Quill
    def quillWhistle(self) :
        if (self.isWOWDecoder()) :
            self.setFunction("Quill", True)
        else :
            self.longWhistle(1)
            self.waitMsec(500)
            self.longWhistle(1)
            self.waitMsec(500)
            self.tootWhistle(1)
            self.waitMsec(500)
            self.longWhistle(1)
        return 0

    #
    #  Short toot of the whistle 
    def tootWhistle(self, numToots):
        for n in range(numToots) :
            self.setFunction("Toot", not self.getFunction("Toot"))            
            self.waitMsec(500)
        return 0
    
    #
    #  Long whistle
    def forwardWhistle(self):
        self.longWhistle(2)
        return 0
        
    #
    #  Signal reverse with 3 short toots
    def reverseWhistle(self):
        self.tootWhistle(3)
        return 0
    
    #
    #  Signal stop with one short toot
    def stopWhistle(self):
        self.tootWhistle(1)
        return 0
    
    #
    #  Long whistle
    def longWhistle(self, numBlows):
        import java
        import sys
        
        gap = 500 # milliseconds between whistle blows
        seconds = 1500 # avg duration of whistle blow
        
        try:
            seconds = float(seconds) / 2.0
            for n in range(numBlows) :
                self.setFunction("Whistle", True)
                self.waitMsec(int(round(750 + java.util.Random().nextFloat() * 1500)))
                self.setFunction("Whistle", False)
                randomGap = gap + java.util.Random().nextInt(10)*(gap*.2)
                self.waitMsec(int(randomGap))
        except :
            print "Unexpected error in longWhistle: ", sys.exc_info()[0], sys.exc_info()[1]
        return 0
    #
    #========================================================================================
    #
    #  Brake
    def setBrake(self, state):
        if (self.isWOWDecoder()) :
            if (state) :
                self.setFunction("BrakeSet", True)
            else:
                self.setFunction("BrakeRelease", True)
        else:
            self.setFunction("BrakeSet", state)
        self.waitMsec(1500)
        
        return 0
    

    #
    #  Tap Brake
    def tapBrake(self, numTaps) :
        if (self.isWOWDecoder()) :
            for t in range(numTaps) :
                self.setBrake(True)
                self.waitMsec(200)
        else :
            self.SetBrake(True)
        self.waitMsec(1500)
        return 0

    #
    #  Emergency Stop
    def emergencyStop(self) :
        self.throttle.setSpeedSetting(-1)
        return 0
    #
    #  Ring the bell
    def ringBell(self, state):
        self.setFunction("Bell", state)
        return 0
    #
    #  Play the sound of the fireman dumping the ashes
    def dumpAshes(self, seconds):
        self.throttle.setF19(True)
        self.waitMsec(seconds * 1000)
        self.throttle.setF19(False) 
        return 0   
    
    #
    #  Play the sound of the fireman blowing out the boiler the specified number of seconds
    def steamRelease(self, seconds):
        self.setFunction("BlowOutBoiler", True)
        self.waitMsec(seconds * 1000)
        self.setFunction("BlowOutBoiler", False) 
        return 0   
    
    #
    #  Randomly blow out the boiler
    def blowoutBoiler(self) :
        import java
        if (java.util.Random().nextInt(100) < 20) :
            self.steamRelease(1 + java.util.Random().nextInt(3))
        
    #
    #  Play the sound of filling the tender with water for the specified number of seconds.
    def waterFill(self, seconds):
        self.setFunction("WaterFill", True)
        self.waitMsec(seconds * 1000)
        self.setFunction("WaterFill", False)
        return 0
    
    #
    #  Returns True if the locomotive has a TCS WOW decoder
    def isWOWDecoder(self) :
        return self.rosterEntry.getDecoderFamily().startswith("WOW")
    #
    #  Open the cylinder cocks on WOW decoders
    def openCylinderCocks(self, state) :
        if(self.isWOWDecoder()) :
            self.setFunction("CylinderCox", state)
        return 0
    
    #
    #  Throw the Johnson bar
    def setJohnsonBar(self, state) :
        if(self.isWOWDecoder()) :
            self.setFunction("J-Bar Down", state)
        return 0
