# This is an example script for a JMRI "Automat" in Python
# Written by Ron McKinnon, Wellington, New Zealand.
# Sept 2005.
# This is a simple clock for showing Train Time separately from your Panel.
# It can be enhanced with different time & string formats as you wish.
# Chimes or bells for the hour or whatever could be easily added with sound
# files
# $Revision: 1.3 $ revision of AutomatonExample distributed with JMRI
#                   from which this script has been developed.
#
# add this to your defaults file or uncomment it.
#clock = jmri.InstanceManager.timebaseInstance()
#

import java
import java.util as util
import javax.swing as swing
import javax.swing.border as border
import javax.swing.SwingConstants as SwingConstants
import java.awt as awt
import java.awt.Toolkit as Toolkit
import jarray
import jmri

class Traintime(jmri.jmrit.automat.AbstractAutomaton) :
	def init(self):
		self.mkclk()
		return

	def handle(self):
		
		return

	#  this constructs the time panel using java.swing components.
	#  before it displays the first time it calls updclk() to get the current
#  time
	def mkclk(self):
		global tmlab
		# create a borderless frame
		fclk = swing.JFrame("Clk",size=(390,295))
		fclk.setUndecorated(True)
		fclk.getContentPane().setOpaque(True)
		fclk.contentPane.setLayout(swing.BoxLayout(fclk.contentPane,swing.BoxLayout.X_AXIS))
		pan = swing.JPanel(size=(390,295),border= border.EtchedBorder(border.EtchedBorder.RAISED))
		tmlab=swing.JLabel()
		self.updclk()
		pan.add(tmlab)
		
		fclk.contentPane.add(pan)
		fclk.setSize(awt.Dimension(400,200))

		#  this sets the location on the screen 400 across and 15 down.
		fclk.setLocation(awt.Point(400,15))
		fclk.pack()
		fclk.show()
		#print "fin clk"
		return

	#  this is the routine called by the minute listener to update the 
	#  time that is displayed. It is text concatenated with the current time.
	def updclk(self):
		global tmlab
		tmlab.setText("Train Time = " + self.caltime2())
		
		return

	#  this routine is for showing a timestamp in other places like a 
	#  Dispatchers Log which I am working on.
	def caltime(ptime):
		time= clock.getTime()
		ptime= " [" + str(time.getHours())+":"+ str(time.getMinutes())+":"+ str(time.getSeconds())+ "]"
		return ptime 

	#  This is the time display routine called by Update Clock (updclk)
	#  as Traintime().updclk()
	def caltime2(self):
		time= clock.getTime()
		ptHrs= str(time.getHours())
		ptMins1= str(time.getMinutes())
		# always display two digits for mins.
		if len(ptMins1)== 1 :
			ptMins2="0"+ptMins1
		else:
			ptMins2= ptMins1
		ptime2= ptHrs+":"+ ptMins2
		return ptime2 
#  this is the listener routine which watches until the minute changes
#  and then updates the time displayed.
class AdjClk(java.beans.PropertyChangeListener):
	def propertyChange(self, event):
		if (event.newValue != event.oldValue) : self.setOutputclk()
	
	def setOutputclk(self):
		#print "beep"
		Traintime().updclk()
		return

clk = AdjClk()
clock.addMinuteChangeListener(clk)


# end of class definitions
Traintime().start()

