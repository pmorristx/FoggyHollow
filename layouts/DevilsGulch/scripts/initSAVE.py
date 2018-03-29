class setStartup(jmri.jmrit.automat.AbstractAutomaton) :
   def init(self):
     return
   def handle(self):

      #
      #  Read the state of the turnouts and set the panel lights to match.

      fullname = jmri.util.FileUtil.getExternalFilename("preference:panels/FoggyHollowControl27.xml")
      jmri.InstanceManager.configureManagerInstance().load(java.io.File(fullname))
      self.waitMsec(1)         # time is in milliseconds


      # For BDL16 (remove the 4 "#" symbols if you have a BDL16)

      #jmri.InstanceManager.powerManagerInstance().setPower(jmri.PowerManager.OFF)
      #print "Power Off"
      #self.waitMsec(1000)
      #jmri.InstanceManager.powerManagerInstance().setPower(jmri.PowerManager.ON)
      #print "Power On"
      #self.waitMsec(1000)


      # For BDL168, SE8C, SIC24 SIC24AD, SRC16, SRC8 

      #l.setOpCode(0xB0)
      #l.setElement(1,0x78)
      #l.setElement(2,0x27)
      #jmri.jmrix.loconet.LnTrafficController.instance().sendLocoNetMessage(l)
      #print " Sent command 0x78"
      #self.waitMsec(1000)

      #l.setElement(1,0x79)
      #jmri.jmrix.loconet.LnTrafficController.instance().sendLocoNetMessage(l)
      #print " Sent command 0x79"
      #self.waitMsec(1000)

      #l.setElement(1,0x7A)
      #jmri.jmrix.loconet.LnTrafficController.instance().sendLocoNetMessage(l)
      #print " Sent command 0x7A"
      #self.waitMsec(1000)

      #l.setElement(1,0x7B)
      #jmri.jmrix.loconet.LnTrafficController.instance().sendLocoNetMessage(l)
      #print " Sent command 0x7B"
      #self.waitMsec(1000)

      #l.setElement(1,0x78)
      #l.setElement(2,0x07)
      #jmri.jmrix.loconet.LnTrafficController.instance().sendLocoNetMessage(l)
      #print " Sent command 0x78 - 0x07"
      #self.waitMsec(1000)

      #l.setElement(1,0x79)
      #jmri.jmrix.loconet.LnTrafficController.instance().sendLocoNetMessage(l)
      #print " Sent command 0x79 - 0x07"
      #self.waitMsec(1000)

      #l.setElement(1,0x7A)
      #jmri.jmrix.loconet.LnTrafficController.instance().sendLocoNetMessage(l)
      #print " Sent command 0x7A - 0x07"
      #self.waitMsec(1000)

      #l.setElement(1,0x7B)
      #jmri.jmrix.loconet.LnTrafficController.instance().sendLocoNetMessage(l)
      #print " Sent command 0x7B - 0x07"
      #print "LocoNet Sensor Initialization Complete"


      #
      #  Start the NIXIE clock on the panel once.
      clockScript = jmri.util.FileUtil.getExternalFilename("preference:scripts/NixiePanelClock.py")
      execfile(clockScript);

      #
      #  Start the Factory Whistle timer once.
      # execfile(jmri.util.FileUtil.getExternalFilename("preference:scripts/FactoryWhistle.py"));
 
      jmri.InstanceManager.logixManagerInstance().getLogix("IX0:RESET").setEnabled(False)


      logixes = jmri.InstanceManager.logixManagerInstance()
      logiList = logixes.getSystemNameArray()
      for i in range(len(logiList)) :
         logiName = logiList[i]
         if (logiName != 'SYS' and logiName != "IS7:POWER") :
            logixes.getLogix(logiName).setEnabled(False)
         else :
            logixes.getLogix(logiName).setEnabled(True)

      #
      #  Turn power off - turn toggle switch off and hide track plan.
      sensors.getSensor("IS7:TS").setState(INACTIVE)
      sensors.getSensor("IS:BLNK").setState(ACTIVE)

      #
      #  Turn switch code buttons off.
      sensors.getSensor("IS1:CB").setState(INACTIVE)
      sensors.getSensor("IS9:CB").setState(INACTIVE)
      sensors.getSensor("IS3:CB").setState(INACTIVE)
      sensors.getSensor("IS11:CB").setState(INACTIVE)

      #
      #  Turn off all route toggle switches
      sensors.getSensor("IS81:RTE").setState(INACTIVE)
      sensors.getSensor("IS82:RTE").setState(INACTIVE)
      sensors.getSensor("IS83:RTE").setState(INACTIVE)
      sensors.getSensor("IS84:RTE").setState(INACTIVE)
      sensors.getSensor("IS85:RTE").setState(INACTIVE)

      #
      #  Set turnout levers to center until we know how the turnouts are set.
      sensors.getSensor("IS1:WL").setState(UNKNOWN)
      sensors.getSensor("IS9:WL").setState(UNKNOWN)
      sensors.getSensor("IS3:WL").setState(UNKNOWN)
      sensors.getSensor("IS11:WL").setState(UNKNOWN)

      #
      #  Set all indicator lights off
      sensors.getSensor("IS1:NWK").setState(INACTIVE)
      sensors.getSensor("IS1:RWK").setState(INACTIVE)

      sensors.getSensor("IS9:NWK").setState(INACTIVE)
      sensors.getSensor("IS9:RWK").setState(INACTIVE)

      sensors.getSensor("IS9:NWK").setState(INACTIVE)
      sensors.getSensor("IS9:RWK").setState(INACTIVE)

      sensors.getSensor("IS11:NWK").setState(INACTIVE)
      sensors.getSensor("IS11:RWK").setState(INACTIVE)

      #
      #  Default order board indicator lights off and levers to center.
      sensors.getSensor("IS8:MCN").setState(INACTIVE)

      #
      #  Turn maintenance call toggle off
      sensors.getSensor("IS8:MCT").setState(INACTIVE)

      return False              # all done, don't repeat again
setStartup().start()          # create one of these, and start it running





 

