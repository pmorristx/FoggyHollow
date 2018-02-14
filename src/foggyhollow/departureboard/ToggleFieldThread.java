package foggyhollow.departureboard;

public class ToggleFieldThread implements Runnable
{
    private DepartureBoard board;
    private String fieldName;
    private String[] words;
    private int row;
    private int delaySeconds;
    
    public ToggleFieldThread(DepartureBoard board, String fieldName, String[] words,  int delaySeconds, int row)
    {
        this.board = board;
        this.fieldName = fieldName.toUpperCase();
        this.words = words;
        this.row = row;
        this.delaySeconds = delaySeconds;
    }
    
    public void run()
    {
        while(!Thread.currentThread().isInterrupted())
        {
            try
            {
                for (String word : words)
                {
                    board.setField(fieldName, word, row, delaySeconds, false);
                    Thread.sleep(1000*60); // Sleep 1 minute
                }
                
            }
            catch (InterruptedException err)
            {
                //System.out.println("ToggleFieldThread interrupted");
                break;
            }
        }
        //System.out.println ("Leaving toggle thread " + fieldName + String.valueOf(row));
    }
}
