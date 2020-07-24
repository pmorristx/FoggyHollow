import sys
sys.path.insert(1, '../../scripts')

import jmri

from java.beans import PropertyChangeListener
from jmri.jmrit.automat import AutomatSummary

import os
import sys
sys.path.insert(1, os.path.expanduser('~') + "/MyJMRI/SpeedTest/scripts")

class LocomotiveChangeListener(PropertyChangeListener) :
	
        def init(self, parent, memories, stopBtn):
                self.memories = memories
                self.parent = parent
                self.stopBtn = stopBtn
                return		

        def propertyChange(self, event) :
                import sys
                
                from Locomotive import Locomotive
                from EmergencyStopListener import EmergencyStopListener
                
                locoNumber = event.source.getValue()
                print "New Loco Number = " + str(locoNumber)

		locomotive = Locomotive()
		locomotive.init("Foggy Hollow & Western", int(locoNumber), self.memories)
                print "Loco number = " + str(locoNumber) + " Loco Mfg = " + locomotive.rosterEntry.getMfg()
                       
                self.memories.getMemory("IM:Loco MFG").setValue(locomotive.rosterEntry.getMfg())
                self.memories.getMemory("IM:Loco Model").setValue(locomotive.rosterEntry.getModel())
                self.memories.getMemory("IM:Loco Decoder").setValue(locomotive.rosterEntry.getDecoderFamily())
                self.memories.getMemory("IM:Loco Decoder Model").setValue(locomotive.rosterEntry.getDecoderModel())                
                self.memories.getMemory("IM:Loco ID").setValue("FH&W " + locomotive.rosterEntry.getDccAddress())

                self.parent.locomotive = locomotive

                #
                #  Remove any locomotives previously registered as listeners to the Emergency Stop button
                nListeners = self.stopBtn.getNumPropertyChangeListeners()               
                listeners = self.stopBtn.getPropertyChangeListeners()
                for i in range (nListeners) :
                        try :
                                listenerClass = listeners[i].getName()
                                if (listenerClass.startswith("EmergencyStopListener")) :
                                        #print "\n\nRemoving listener [" + str(i) + "] " + str(listeners[i])
                                        self.stopBtn.removePropertyChangeListener(listeners[i])
                                        break
                        except :
                                #
                                #  We expect some listeners may not implement getName...don't care.  We only
                                #  want to remove EmergencyStopListeners....
                                dummy = 1
                
                
		emergencyStopListener = EmergencyStopListener()
		emergencyStopListener.init(locomotive)                
                self.stopBtn.addPropertyChangeListener(emergencyStopListener)	                                        

                return	
