import java.beans.PropertyChangeListener
import jarray
import jmri
import jmri.jmrit.roster


class LocoChangeListener(java.beans.PropertyChangeListener) :
	
	def propertyChange(self, event) :
		rosterlist = jmri.jmrit.roster.Roster.instance().matchingList(None, None, memories.getMemory("Mine Locomotive").getValue(), None, None, None, None)		
		for entry in rosterlist.toArray() :
			if ((entry.getDecoderFamily().startswith("Tsunami Steam")) or (entry.getDecoderFamily().startswith("WOW Sound")) or len(rosterlist) == 1):
				memories.getMemory("Roster ID").setValue(entry.getRoadName() + " #" + entry.getDccAddress() )
				memories.getMemory("Roster Description").setValue(entry.getMfg() + " - " + entry.getModel() )	
		return