class setStartup(jmri.jmrit.automat.AbstractAutomaton) :
	def init(self):
		return

	def handle(self):

		#
		#  Read the state of the turnouts and set the panel lights to match.
		fullname = jmri.util.FileUtil.getExternalFilename("preference:panels/BeaverBendTrainBoard.xml")
		jmri.InstanceManager.configureManagerInstance().load(java.io.File(fullname))
		self.waitMsec(1)         # time is in milliseconds

		turnoutScript = jmri.util.FileUtil.getExternalFilename("preference:scripts/BeaverBendTurnoutMonitor.py")
		execfile(turnoutScript);
		#
		#  Start the NIXIE clock on the panel once.
		clockScript = jmri.util.FileUtil.getExternalFilename("preference:scripts/NixiePanelClock.py")
		execfile(clockScript);

		#
		#  Start the mine track animation script
		mineScript = jmri.util.FileUtil.getExternalFilename("preference:scripts/MineTrack.py")
		execfile(mineScript);
		
		#
		#  Start the Beaver Bend train board script
		boardScript = jmri.util.FileUtil.getExternalFilename("preference:scripts/TrainBoard.py")
		execfile(boardScript);		
		
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
        
		#
		#  Turn the order board to "Proceed"
		#sensors.getSensor("IS22:BO").setState(INACTIVE)   

		return False              # all done, don't repeat again
setStartup().start()          # create one of these, and start it running