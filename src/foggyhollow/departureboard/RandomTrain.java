package foggyhollow.departureboard;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.List;
import jmri.jmrit.operations.locations.Location;
import jmri.jmrit.operations.locations.LocationManager;

public class RandomTrain implements Runnable
{
    private int row;
    private int delaySeconds;
    private List<Location> locations = null;
    private java.util.Random random = null;
    private DepartureBoard board = null;
    private DateFormat dateFormat;
    
    public RandomTrain (DepartureBoard board, int row, int delaySeconds)
    {
        this.dateFormat = new SimpleDateFormat("hh:mm");
        
        this.row = row;
        this.delaySeconds = delaySeconds;
        this.locations = LocationManager.instance().getList();
        this.random = new java.util.Random();
        this.board = board;       
    }
    
    public void run()
    {
        try
        {
            Thread.sleep(delaySeconds*1000);
            
            while (!Thread.currentThread().isInterrupted())
            {
                //
                //  Look for a train that isn't already used.
                DepartureBoardTrain train = board.getTrain();
                
                Calendar now = Calendar.getInstance();
                //int offset = random.nextInt((Integer.valueOf(hour) - 10) + 1) + 10;
                int offset = random.nextInt(10) + 5;
                now.add(Calendar.MINUTE, offset);
                
                String status = "ON TIME";
                int trainDelayMinutes = random.nextInt(15);
                
                if (train.getTrainName().startsWith("Fierce Sparrow"))
                {
                    trainDelayMinutes = 0;
                }

                String field = "DESTINATION";
                if (board.fieldMap.containsKey(field))
                {
                    String[] destinations = new String[2];
                    destinations[0] = train.getDestination();
                    destinations[1] = train.getTrainName();
                
                    this.board.setField("Destination", destinations, this.row, 0);
                }
                field = "TRAIN";
                if (board.fieldMap.containsKey(field))                
                    this.board.setField(field, train.getTrainNumber(), this.row, 0);  
                
                field = "STATUS";
                if (board.fieldMap.containsKey(field))                
                    this.board.setField(field, status, this.row, 0);    
                
                field = "DEPARTS";
                if (board.fieldMap.containsKey(field))                
                    this.board.setField(field, dateFormat.format(now.getTime()), this.row, 0); 
                
                field = "TRACK";
                if (board.fieldMap.containsKey(field))                
                    this.board.setField(field, String.valueOf(this.row+1), this.row, 0);                        
                
                // Wait for scheduled departure time
                Thread.sleep(offset * 1000 * 60 );
                
                //
                //  If train is delayed, update status and wait.
                if (trainDelayMinutes > 0)
                {
                    //
                    // Update the departure time to the delayed time....
                    now = Calendar.getInstance();
                    now.add(Calendar.MINUTE, trainDelayMinutes);
                    field = "DEPARTS";
                    if (board.fieldMap.containsKey(field))                
                        this.board.setField(field, dateFormat.format(now.getTime()), this.row, 0);                     
                    
                    if (trainDelayMinutes > 10)
                        status = "SEEAGNT";
                    else if (trainDelayMinutes > 5)
                        status = "DELAYED"; 
                    
                    field = "STATUS";
                    if (board.fieldMap.containsKey(field))                
                        this.board.setField(field, status, this.row, 0);   
                    Thread.sleep(trainDelayMinutes*60*1000);                    
                }
                
                field = "STATUS";
                if (board.fieldMap.containsKey(field))                
                    this.board.setField(field, "DEPARTD", this.row, 0);                     
                
                Thread.sleep(60*1000);                    

                field = "STATUS";
                if (board.fieldMap.containsKey(field))                
                    this.board.setField(field, "       ", this.row, 0);                     

                Thread.sleep(60*1000);                    
                
                train.setOccupied(false);
            }
            //board.stop();
        }
        catch (InterruptedException err)
        {
           // System.out.println("Stopping random train thread");
        }
    }
}
