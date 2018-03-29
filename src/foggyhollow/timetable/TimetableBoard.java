package foggyhollow.timetable;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.format.TextStyle;
import java.util.Locale;
import java.util.Timer;
import java.util.TimerTask;
import java.util.Vector;
import foggyhollow.departureboard.DepartureBoard;

public class TimetableBoard
{
    private Connection conn = null;
    private PreparedStatement pstmt = null;
    private ResultSet resultSet = null;
    private final String ipAddr;

    private Boolean showDeparture;
    private Boolean showTrainName;
    private int numDeparturePages;
    private int currentPage;
    private DepartureBoard departureBoard;
    private final Vector<String[]> messages;
    private int msgNum;
    private Vector<TimetableEntry> timeTable;
    private final Timer timer;
    private int numRows;
    private int numCols;
    private String stationName;

    public TimetableBoard(String ipAddr)
    {
	this.ipAddr = ipAddr;
	this.showDeparture = true;
	this.numDeparturePages = 0;
	this.currentPage = 0;
	this.showTrainName = true;
	this.msgNum = 0;
	this.timer  = new Timer("FHTimeTable");
	this.messages = new Vector<String[]>();
    }

    public Vector<TimetableEntry> getTimetable(String stationName) throws Exception
    {
	this.stationName = stationName;
	String query;
	timeTable = new Vector<TimetableEntry>();

	try
	{
	    LocalDate date = LocalDate.now();
	    DayOfWeek dow = date.getDayOfWeek();
	    String dayName = dow.getDisplayName(TextStyle.SHORT_STANDALONE, Locale.ENGLISH);
	    // This will load the MySQL driver, each DB has its own driver
	    Class.forName("com.mysql.jdbc.Driver");
	    // Setup the connection with the DB
	    conn = DriverManager.getConnection(
		    "jdbc:mysql://" + ipAddr + "/foggyhollow?user=foggyhollow&password=foggyhollow");

	    // Result set get the result of the SQL query
	    query = " select * " 
		    + " from station_schedules "
		    + " where ((station like ?) and (arlv='Lv') and (((trainDays like ?) or (trainDays like 'Daily')))) "
		    + " order by str_to_date(scheduleTime, '%h:%m %a')";
	    pstmt = conn.prepareStatement(query);
	    pstmt.setString(1, stationName);
	    pstmt.setString(2, "%" + dayName + "%");
	    System.out.println(query);
	    resultSet = pstmt.executeQuery();
	    while (resultSet.next())
	    {
		TimetableEntry entry = new TimetableEntry();
		entry.setTrainNumber(resultSet.getString("trainNumber"));
		entry.setTrainName(resultSet.getString("trainName"));
		entry.setDestination(resultSet.getString("destination"));
		entry.setDirection(resultSet.getString("direction"));
		entry.setArLv(resultSet.getString("arlv"));
		entry.setScheduleTime(resultSet.getString("scheduleTime"));

		timeTable.add(entry);
	    }
	    numDeparturePages = (int) Math.ceil(timeTable.size() / numRows);
	}
	catch (Exception e)
	{
	    throw e;
	}
	finally
	{
	    close();
	}
	return timeTable;
    }

    private void close()
    {
	try
	{
	    if (resultSet != null)
	    {
		resultSet.close();
	    }

	    if (conn != null)
	    {
		conn.close();
	    }
	}
	catch (Exception e)
	{
	    e.printStackTrace();
	}
    }
/*
 *         DevilsGulchDepartureBoard.departureBoard = jmri.jmrit.foggyhollow.departureboard.DepartureBoard("Ace of Spades Mine", "Departures", 375, 220, 4, 30)        
 */
    public void createDepartureBoard(String panelName, String boardName, int startX, int startY, int numRows,
	    int numCols)
    {
	this.stationName = boardName;
	this.numRows = numRows;
	this.numCols = numCols;
	
	departureBoard = new DepartureBoard(panelName, boardName, startX, startY, numRows, numCols);

        departureBoard.addField("GenericMsg", 0, 30, false);
        departureBoard.addField("TrainNo", 0, 3, false);
        departureBoard.addField("TrainName", 4, 20, false);
        departureBoard.addField("Departs", 25, 5, false);
        
	String[] message = new String[numRows]; 
	message[0] = "";
	message[1] = "Welcome to the";
	message[2] = "Foggy Hollow & Western Railroad";
	message[3] = boardName + " Division";
        addMessage(message);
    }

    public void addMessage(String[] message)
    {
	messages.add(message);
    }
    
    public void start()
    {
	TimerTask updateDepartureBoard = new TimerTask() {
	    @Override
	    public void run()
	    {
		if (showDeparture)
		{
		    System.out.println("*** - showing departure info");
		    if (numDeparturePages > 0)
		    {
			int r = currentPage * 4;
			int c = 0;
			if (showTrainName)
			{
			    departureBoard.clearRow(0, true);
			    departureBoard.clearRow(1, true);
			    departureBoard.clearRow(2, true);
			    departureBoard.clearRow(3, true);

			    while (c < Math.min(4, timeTable.size() - (currentPage * 4)))
			    {
				TimetableEntry entry = timeTable.get(r);
				departureBoard.setField("TrainNo", entry.getTrainNumber(), c, 0);
				departureBoard.setField("TrainName", entry.getTrainName(), c, 0);
				departureBoard.setField("Departs", entry.getScheduleTime(), c, 0);
				r = r++;
				c = c++;
			    }
			    showTrainName = false;
			}
			else
			{
			    showTrainName = true;
			    while (c < Math.min(4, timeTable.size() - (currentPage * 4)))
			    {
				TimetableEntry entry = timeTable.get(r);
				departureBoard.setField("TrainName", entry.getDestination(), c, 0);
				r = r++;
				c = c++;
			    }
			    currentPage = currentPage++;
			    if (currentPage >= numDeparturePages)
			    {
				currentPage = 0;
				showDeparture = false;
			    }
			}
		    }
		    else
		    {
			System.out.println("Showing msg number " + msgNum);
			int r = 0;
			String[] msg = messages.get(msgNum);
			while (r < msg.length)
			{
			    System.out.println("r = " + r + " msg.length = " + msg.length);
			    if (msg.length == 0)
			    {
				departureBoard.clearRow(r, true);
			    }
			    else
			    {
				departureBoard.setField("GenericMsg", msg[r], r, 0);
			    }
			    r = r + 1;
			}
			msgNum = msgNum + 1;
			if (msgNum >= msg.length) msgNum = 0;
			showDeparture = true;
		    }
		}
	    }
	};


	long delay = 1000L;
	long period = 1000L * 60;
	timer.scheduleAtFixedRate(updateDepartureBoard, delay, period);
    }

    public void stop()
    {
	timer.cancel();
    }
    /*
    public static void main(String[] args) throws Exception
    {
	TimetableBoard timeboard = new TimetableBoard("192.168.0.14");
	timeboard.createDepartureBoard("test", "Devil's Gulch", 100, 100, 4, 30);
	timeboard.getTimetable("Devil's Gulch");
	timeboard.start();
    }
    */
}