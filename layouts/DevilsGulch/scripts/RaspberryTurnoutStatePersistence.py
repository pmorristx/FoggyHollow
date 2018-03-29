# Sample script showing how to persist the state of turnouts between sessions.
#
# State is saved to a .csv file at shutdown and re-instated from said .csv file
# when script is launched.
#
# This shows how .csv files can be both written and read-back complete with
# a header row using the javacsv library
#
# This also shows how entries can be added to the log as opposed to using
# 'print' commands
#
# Author: Matthew Harris, copyright 2011
# Part of the JMRI distribution
#
# The next line is maintained by CVS, please don't change it
# $Revision: 27654 $

import java
#import com.csvreader
#from org.apache.log4j import Logger
from com.csvreader import CsvWriter
from com.csvreader import CsvReader

# Define turnout state file
# Default is 'TurnoutState.csv' stored in the preferences directory
#turnoutFile = jmri.util.FileUtil.getUserFilesPath() + "TurnoutState.csv"

# Define task to persist turnout state at shutdown
class PersistTurnoutStateTask(jmri.implementation.AbstractShutDownTask):

    # Get reference to the logger
    #
    # This reference is unique to instances of this class, hence the use of
    # 'self.log' whenever it needs to be used
    #
    # The logger has been instantiated within the pseudo package:
    #   'jmri.jmrit.jython.exec'
    # This allows for easy identification and configuration of log4j.
    #
    # To show debug messages, add the following line (without quotes) to
    # the file 'default.lcf' located in the JMRI program directory:
    #   'log4j.category.jmri.jmrit.jython.exec=DEBUG'
#    log = Logger.getLogger("jmri.jmrit.jython.exec.TurnoutStatePersistence.PersistTurnoutStateTask")

    # Perform any initialisation
    def init(self):
        self.turnoutFile = jmri.util.FileUtil.getExternalFilename("preference:turnoutstate.csv")
        return

    # Function to convert state values to names
    def stateName(self, state):
        if (state == CLOSED):
            return "CLOSED"
        if (state == THROWN):
            return "THROWN"
        if (state == INCONSISTENT):
            return "INCONSISTENT"
        # Anything else is UNKNOWN
        return "UNKNOWN"

    # Function to convert boolean values to names
    def booleanName(self, value):
        if (value == True):
            return "Yes"
        # Anything else is No
        return "No"



# Define task to run at ShutDow
class SignalMonitorShutdown(jmri.implementation.AbstractShutDownTask) :
    # Perform any initialisation
    def init(self):
        self.turnoutFile = jmri.util.FileUtil.getExternalFilename("preference:turnoutstate.csv")
        return

    def execute(self):
        self.turnoutFile = jmri.util.FileUtil.getExternalFilename("preference:turnoutstate.csv")
        logFile = open(self.turnoutFile, "w")
        # Loop through all known turnouts
        for memory in memories.getSystemNameList().toArray():
            if (memory.endswith(":TV")) :
                mem = memories.provideMemory(memory)
                line = str(memory) + " " + str(mem.getValue()) + "\n"
                logFile.write(line)

        logFile.flush()
        logFile.close()
        # All done
        return True     # True to allow ShutDown; False to abort


# Define task to load turnout state at script start
#
# This is implemented as a seperate class so that it can run on a
# different thread in the background rather than holding up the main
# thread while executing
class LoadTurnoutState(jmri.jmrit.automat.AbstractAutomaton):

    # Get reference to the logger
#    log = Logger.getLogger("jmri.jmrit.jython.exec.TurnoutStatePersistence.LoadTurnoutState")

    # Perform any initialisation
    def init(self):
        self.turnoutFile = jmri.util.FileUtil.getExternalFilename("preference:turnoutstate.csv")
        return

    # Define task to run
    def handle(self):

        # Retrieve the state file as a File object
        inFile = java.io.File(self.turnoutFile)

        # Check if state file exists
        if inFile.exists():

            #
            # Process the existing log file, reading each line and updating our internal
            # states as appropriate.
            #
            # Note that the log file MUST exist each time that the script is invoked.  The
            # file can be zero length, which results in all turnouts being set to CLOSED and
            # all lights being set to OFF.
            #
            logFile = open(self.turnoutFile, "r")

            while True:
                line = logFile.readline()
                if (len(line) == 0) :
                    break
                line = line.strip() 
                i = line.find(" ")
                if (i < 0) :
                    print 'Invalid line format: ' + line
                else :
                    systemName = line[0:i].strip()           # Sensor system name
                    value = line[i+1:len(line)].strip()      # Current state [N,R] for turnout or [C,S,P] for signal

                    if (systemName.endswith(":TV")) : 

                        try:
                            try :
                                number = str(systemName[2:])
                                number = number.replace (":TV", "")
                            except Exception :
                                print "Error getting number"


                            button = "CTC:S" + number + ":CB"
                            if (value == "N" or value == "R") :

                                lever = "IS:" + number + ":L"
                                if (value == "N") :
                                    sensors.provideSensor(lever).setState(ACTIVE)
                                else :
                                    sensors.provideSensor(lever).setState(INACTIVE)
                            else :
                                button = "CTC:TO" + number + ":CB"
                                if (value == "C") :
                                    lever = "IS:" + number + ":WLL"
                                    lever1 = "IS:" + number + ":WLC"
                                    lever2 = "IS:" + number + ":WLR"
                                elif (value == "P") :
                                    lever = "IS:" + number + ":WLC"
                                    lever1 = "IS:" + number + ":WLL"
                                    lever2 = "IS:" + number + ":WLR"
                                else :
                                    lever = "IS:" + number + ":WLR"
                                    lever1 = "IS:" + number + ":WLC"
                                    lever2 = "IS:" + number + ":WLL"

                                sensors.provideSensor(lever).setState(ACTIVE)
                                sensors.provideSensor(lever1).setState(INACTIVE)
                                sensors.provideSensor(lever2).setState(INACTIVE)


                            sensors.provideSensor(button).setState(ACTIVE)
                            self.waitMsec(10)
                            sensors.provideSensor(button).setState(INACTIVE)
                        except Exception :
                            print "Problem setting " + number
            logFile.close()

            for memory in memories.getSystemNameList().toArray():
                if (memory.endswith(":TV")) :
                    mem = memories.provideMemory(memory)
                    line = str(memory) + " " + str(mem.getValue()) + "\n"
                    print line

            logFile = open(self.turnoutFile, "w")
            # Loop through all known turnouts
            for memory in memories.getSystemNameList().toArray():
                if (memory.endswith(":TV")) :
                    mem = memories.provideMemory(memory)
                    line = str(memory) + " " + str(mem.getValue()) + "\n"
                    logFile.write(line)

            logFile.flush()
            logFile.close()


        else:
            # It doesn't, so log this fact and carry on
#            self.log.warn("Turnout state file '%s' does not exist" % self.turnoutFile)
            print("Turnout state file '%s' does not exist" % self.turnoutFile)

        # All done
        return False    # Only need to run once

    # Function to convert state names to values
    def stateValue(self, state):
        if (state == "CLOSED"):
            return CLOSED
        if (state == "THROWN"):
            return THROWN
        if (state == "INCONSISTENT"):
            return INCONSISTENT
        # Anything else is UNKNOWN
        return UNKNOWN

    # Function to convert boolean names to values
    def booleanName(self, value):
        if (value == "Yes"):
            return True
        # Anything else is False
        return False

# Register the turnout persistence shutdown task
shutdown.register(SignalMonitorShutdown("PersistTurnoutState"))

# Launch the load task
LoadTurnoutState().start()
