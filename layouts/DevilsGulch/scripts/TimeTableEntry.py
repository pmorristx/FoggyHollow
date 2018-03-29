class TimeTableEntry(object):

    def setDirection(self, direction):
        self.direction = direction;
    def getDirection(self):
        return self.direction

    def setTrainNumber(self, number):
        self.trainNumber = number
    def getTrainNumber(self):
        return self.trainNumber

    def setTrainName(self, name):
        self.trainName = name
    def getTrainName (self):
        return self.trainName

    def setScheduleTime(self, schedTime):
        self.scheduleTime = schedTime
    def getScheduleTime(self):
        return self.scheduleTime

    def setArLv(self, arlv):
        self.arlv = arlv
    def getArLv(self):
        return self.arlv

    def setDestination(self, destination):
        self.destination = destination
    def getDestination(self):
        return self.destination

    def setRemark(self, remark):
        self.remark = remark
    def getRemark(self):
        return self.remark

    def __init__(self):
        self.direction = "UNK"
        self.trainNumber = "-1"
        self.trainName = "UNK"
        self.scheduleTime = "UNK"
        self.arlv = "UNK"
        self.destination = "UNK"
        self.remark = ""
