package foggyhollow.departureboard;

public class DepartureField {
    
    String title;
    int startCol;
    int numCols;
    boolean isNumeric;
    Thread currentThread;
    
    public DepartureField()
    {
        currentThread = null;
    }
    
    public DepartureField(String title, int startCol, int numCols, boolean isNumeric)
    {
        setTitle(title.toUpperCase());
        setStartCol(startCol);
        setNumCols(numCols);
        setNumeric(isNumeric);
        currentThread = null;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title.toUpperCase();
    }

    public int getStartCol() {
        return startCol;
    }

    public void setStartCol(int startCol) {
        this.startCol = startCol;
    }

    public int getNumCols() {
        return numCols;
    }

    public void setNumCols(int numCols) {
        this.numCols = numCols;
    }

    public boolean isNumeric() {
        return isNumeric;
    }

    public void setNumeric(boolean isNumeric) {
        this.isNumeric = isNumeric;
    }
    
    public void setCurrentThread(Thread thread)
    {
        this.currentThread = thread;
    }
    
    public Thread getCurrentThread()
    {
        return this.currentThread;
    }
    
    public void stopCurrentThread()
    {
        if (this.currentThread != null)
        {
            this.currentThread.interrupt();
            this.currentThread = null;
        }
    }

}
