# Listens for Block Detection Sensor (Sensor #4) and plays crossing gate sound on train entering block.
#
# Based on Listen example and sound example by Bob Jacobsen, copyright 2004
# Modified by Scott CR Henry
#
# NOTES ON USAGE:
# This script looks for a specific sensor to go active, and based on that change, plays a sound once.
# The first step is to tell the script what sound to play. The script is configure to look in the JMRI
# program directory (folder), then to the resources, then sounds directories. To change the sound it is 
# recommend that you save the sound in the same directory, then replace the text crossing.wav with the
# correct name. It is case sensitive. Also, the sound must be in the wave format. 
#
# The next line is maintained by CVS, please don't change it
# $Revision: 1.4 $

# create the sound object by loading a file
# change the file name (Crossing.wav) to match your sound file.
snd = jmri.jmrit.Sound("resources/sounds/Crossing.wav")

# Create the listener (don't change).  
class MyListener(java.beans.PropertyChangeListener):
  
  def propertyChange(self, event):
    if ((event.newValue == ACTIVE) and (event.oldValue == INACTIVE)) : snd.play()
    # play the sound once
    
    # You can also do snd.loop() to start playing the sound
    # as a continuous loop, and snd.stop() to stop it

# Assign the sensor within the quotation marks, currently LS4 for Loconet Sensor 4.
t = sensors.provideSensor("LS4")
m = MyListener()
t.addPropertyChangeListener(m)