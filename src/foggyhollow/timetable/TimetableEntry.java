package foggyhollow.timetable;

public class TimetableEntry
{
    private String trainNumber;
    private String trainName;
    private String destination;
    private String arLv;
    private String scheduleTime;
    private String direction;
    
    public TimetableEntry()
    {
	
    }
    public String getTrainNumber()
    {
        return trainNumber;
    }

    public void setTrainNumber(String trainNumber)
    {
        this.trainNumber = trainNumber;
    }

    public String getTrainName()
    {
        return trainName;
    }

    public void setTrainName(String trainName)
    {
        this.trainName = trainName;
    }

    public String getDestination()
    {
        return destination;
    }

    public void setDestination(String destination)
    {
        this.destination = destination;
    }

    public String getArLv()
    {
        return arLv;
    }

    public void setArLv(String arLv)
    {
        this.arLv = arLv;
    }

    public String getScheduleTime()
    {
        return scheduleTime;
    }

    public void setScheduleTime(String scheduleTime)
    {
        this.scheduleTime = scheduleTime;
    }

    public String getDirection()
    {
        return direction;
    }

    public void setDirection(String direction)
    {
        this.direction = direction;
    }    
}
