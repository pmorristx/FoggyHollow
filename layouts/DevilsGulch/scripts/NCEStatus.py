import jmri
import jmri.jmrix.nce.NceTrafficController

class nceStatus(jmri.jmrit.automat.AbstractAutomaton):
	def init(self):
                print "NCE Status Init"
                
	def handle(self):
                self.nceController = jmri.jmrix.nce.NceTrafficController().instance()
                print "Prog mode = " + str(self.nceController.getNceProgMode())
                if (self.nceController.status()) :

                        print self.nceController.getUserName() + "NCE Status good"
                else:
                        print self.nceController.getUserName() + "NCE Status bad"
		return 0
tst = nceStatus()
tst.start()
