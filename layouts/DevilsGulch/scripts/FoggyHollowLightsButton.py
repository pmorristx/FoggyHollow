# Sample script to add a button to the main
# JMRI application window that loads a script file
#
# Author: Bob Jacobsen, copyright 2007
# Part of the JMRI distribution
#
# The next line is maintained by CVS, please don't change it
# $Revision: 17977 $

import javax.swing.JButton
import apps

# create the button, and add an action routine to it
b = javax.swing.JButton("Foggy Hollow Lights")
def whenMyButtonClicked(event) :
    # run a script file
    execfile(jmri.util.FileUtil.getExternalFilename("preference:scripts/initLights.py"));
    return
b.actionPerformed = whenMyButtonClicked

# add the button to the main screen
apps.Apps.buttonSpace().add(b)

# force redisplay
apps.Apps.buttonSpace().revalidate()