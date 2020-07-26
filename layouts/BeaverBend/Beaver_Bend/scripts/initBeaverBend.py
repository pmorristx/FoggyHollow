import os
import sys
sys.path.insert(1, os.path.expanduser('~') + "/MyJMRI/Beaver_Bend/scripts")
sys.path.insert(1, os.path.expanduser('~') + "/MyJMRI/scripts")

import jmri
from jmri.jmrit.automat import AutomatSummary
class setStartup(jmri.jmrit.automat.AbstractAutomaton) :
	def init(self):
		return

	def handle(self):
		#
		#  Start the NIXIE clock on the panel once.
		clockScript = jmri.util.FileUtil.getExternalFilename("preference:scripts/utilities/NixiePanelClock.py")
		execfile(clockScript);

		#
		#  Turn all lights off so the switches work the first time they are clicked.
		sensors.getSensor("IS:STA1:ON").setState(ACTIVE)
		sensors.getSensor("IS:STA2:ON").setState(ACTIVE)
		sensors.getSensor("IS:STA3:ON").setState(ACTIVE)
		sensors.getSensor("IS:STA4:ON").setState(ACTIVE)   
        
		sensors.getSensor("IS:STA1:OFF").setState(INACTIVE)
		sensors.getSensor("IS:STA2:OFF").setState(INACTIVE)
		sensors.getSensor("IS:STA3:OFF").setState(INACTIVE)
		sensors.getSensor("IS:STA4:OFF").setState(INACTIVE)      
		
		sensors.getSensor("Demo Switch").setState(INACTIVE)
		sensors.getSensor("Mine Track Switch").setState(INACTIVE)
        
		#
		#  Turn the order board to "Proceed"
		sensors.getSensor("IS22:BO").setState(INACTIVE)   

		sensors.getSensor("IS21:L").setState(ACTIVE)
		sensors.getSensor("IS25:L").setState(ACTIVE)

		sensors.getSensor("IS21:NK").setState(ACTIVE)
		sensors.getSensor("IS21:RK").setState(INACTIVE)

		sensors.getSensor("IS25:NK").setState(ACTIVE)
		sensors.getSensor("IS25:RK").setState(INACTIVE)

		#
		#  Initialize the mine track departure board to the welcome message...then kill the thread.
		departureBoardScript = jmri.util.FileUtil.getExternalFilename("preference:Beaver_Bend/scripts/MineTrackDepartureBoard.py")
		execfile(departureBoardScript);
                self.waitMsec(90 * 1000)

                try :
                        AutomatSummary.instance().get("Mine Track Departure Board").stop()
                except:
                        print "Unexpected error killing mine train thread in StopTrainListener: ", sys.exc_info()[0], sys.exc_info()[1]	                                                
		

		return False              # all done, don't repeat again
setStartup().start()          # create one of these, and start it running
