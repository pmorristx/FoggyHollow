package foggyhollow.departureboard;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Point;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;
import jmri.InstanceManager;
import jmri.Memory;
import jmri.jmrit.catalog.NamedIcon;
import jmri.jmrit.display.Editor;
import jmri.jmrit.display.MemoryIcon;
import jmri.jmrit.operations.trains.Train;
import jmri.jmrit.operations.trains.TrainManager;
import org.apache.commons.lang3.StringUtils;

public class DepartureBoard
{
    String iconPath = "preference:resources/icons/misc/flip/tiny";
    Editor editor;
    NamedIcon defaultIcon = null;
    int iconWidth = 15;     //  Default, but check actual size in constructor
    int iconHeight = 24;    //  Default, but check actual size in constructor
    
    int startX;
    int startY;
    int numRows;
    int numCols;
    
    String boardName = "departures";
    
    int rowGap = 0;
    int randomTrainNumber = 0;
    
    char[] letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".toCharArray();
    char[] numbers = "0123456789".toCharArray();
    char[] misc = " -+&$#@!?/\\();:.,'*%".toCharArray();
    
    String alphaNumeric = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-+&#:'()!*";
    
    private List<DepartureBoardTrain> trainMap;  
    HashMap<String, DepartureField> fieldMap;
    HashMap<String, NamedIcon> iconMap;
    HashMap<String, Thread> threadMap;
    List<String> statuses;
        

    private class SetColumn implements Runnable
    {
        private Memory requestedMem = null;
        private String requestedLtr = " ";
        private int delaySeconds = 0;
        private String sortedLetters;
        
        public SetColumn(Memory memory, String ltr, int delaySeconds)
        {
            this.requestedMem = memory;
            this.requestedLtr = ltr;
            this.delaySeconds = delaySeconds;  
            
            String currentLetter = (String) this.requestedMem.getValue();
            if (currentLetter == null)
            {
                currentLetter = " ";
            }
            sortedLetters = getSortedLetters(currentLetter);            
        }
        public void run()
        {
            if (delaySeconds > 0)
            {
                try
                {
                    Thread.sleep(delaySeconds * 1000);
                }
                catch (InterruptedException e)
                {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            for (char l : sortedLetters.toCharArray())
            {
                String ltr = String.valueOf(l);
                this.requestedMem.setValue(ltr);
                if (ltr.equals(this.requestedLtr))
                    break;
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }            
        }
    }   
    
    /**
     *  Create a new Departure board
     */  
    public DepartureBoard(String panelName, String boardName, int startX, int startY, int numRows, int numCols)
    {
        this.startX = startX;
        this.startY = startY;
        this.numRows = numRows;
        this.numCols = numCols;
        this.boardName = boardName;
        
        this.editor = findPanelEditor(panelName);
                
        this.fieldMap = new HashMap<String, DepartureField>();
        this.statuses = new ArrayList<String>();
        this.statuses.add("ON TIME");
        this.statuses.add("DELAYED");
        this.statuses.add("DEPARTD");
        this.statuses.add("ARRIVED");        
        this.statuses.add("SEEAGNT");  
        this.statuses.add("       ");
        
        this.threadMap = new HashMap<String, Thread>();
        //
        //  Create a hashmap of letter icon images so we don't have to keep rereading the image file for every column.
        this.iconMap = initIcons();
        
        createCols();
        
        initTrains();
    }

    /**
     * Initialize the image icons used to display the letters on the departure board.
     * 
     * @return
     */
    private HashMap<String, NamedIcon> initIcons()
    {
        iconMap = new HashMap<String,NamedIcon>();
        
        String path = iconPath + "/flip-space.png"; 
        this.defaultIcon = new NamedIcon(path, "space");
        
        //
        //  Put a black as the first letter in the set
        iconMap.put(" ", this.defaultIcon);
        
        this.iconWidth = this.defaultIcon.getIconWidth();
        this.iconHeight = this.defaultIcon.getIconHeight(); 
        
        for (char c : numbers)
        {
            String ltr = Character.toString(c);
            String columnIconImage = "/flip-" + ltr + ".png";            
            if (ltr.equals("0"))
            {
                columnIconImage = "/flip-o.png";            
            }

            path = iconPath + columnIconImage.toLowerCase();
            iconMap.put(ltr, new NamedIcon(path, ltr));                   
        }            
        
        for (char c : letters)
        {
            String ltr = Character.toString(c);
            String columnIconImage = "/flip-" + ltr + ".png";
            path = iconPath + columnIconImage.toLowerCase();
            iconMap.put(ltr, new NamedIcon(path, ltr));                   
        }  
        
        for (char c : misc)
        {
            String ltr = Character.toString(c);
            String file = "space";
            if (ltr.equals(":")) file = "colon";
            else if (ltr.equals("&")) file = "amp";
            else if (ltr.equals("'")) file = "apost";            
            else if (ltr.equals("@")) file = "at";                        
            else if (ltr.equals("!")) file = "bang";                                    
            else if (ltr.equals(",")) file = "comma";                                                
//            else if (ltr.equals("-")) file = "dash";                                                            
            else if (ltr.equals("$")) file = "dollar";   
            else if (ltr.equals("=")) file = "equal";  
            else if (ltr.equals("-")) file = "minus";    
            else if (ltr.equals("(")) file = "lparen";                
            else if (ltr.equals(")")) file = "rparen";                
            else if (ltr.equals("%")) file = "percent";                            
            else if (ltr.equals(".")) file = "period";                
            else if (ltr.equals("+")) file = "amp";    
            else if (ltr.equals("#")) file = "pound";                            
            else if (ltr.equals("?")) file = "quest";
            else if (ltr.equals(";")) file = "semicolon";                                        
            else if (ltr.equals("*")) file = "star";    
            else if (ltr.equals(" ")) file = "space";                
            else file = "dash";
                
            String columnIconImage = "/flip-" + file + ".png";
            path = iconPath + columnIconImage.toLowerCase();
            iconMap.put(ltr, new NamedIcon(path, ltr));                   
        }         
        
        return iconMap;
    }
    
    /**
     * Returns the fieldname of the requested row/column.
     * @param row
     * @param col
     * @return
     */
    private String getMemoryName(int row, int col)
    {
        return this.boardName + ":R" + Integer.toString(row) + "C" +Integer.toString(col);        
    }
    
    /**
     * Creates the memory and memoryicons for each row/column of the departure board.
     */
    public void createCols()
    {
        for (int row=0; row<this.numRows; row++)
        {
            for (int col=0; col<this.numCols; col++)
            {
                String memName = getMemoryName(row, col);
                String sysName = "IM:" + memName;
                if (InstanceManager.memoryManagerInstance().getBySystemName(sysName) == null)
                {
                    createMemory(sysName, memName);
                    MemoryIcon icon = new MemoryIcon(sysName, editor);
                    
                    int x = this.startX + (col * iconWidth);
                    int y = this.startY + (row * (iconHeight + rowGap));
                    icon.setLocation(new Point(x, y));
                    icon.setDisplayLevel(5);
                    icon.setBackground(Color.black);
                    icon.setForeground(Color.white);
                    icon.setDefaultIcon(this.defaultIcon);
        
                    for (String ltr : this.iconMap.keySet())
                    {
                        icon.addKeyAndIcon(this.iconMap.get(ltr), ltr);                    
                    }           
    
                    icon.setControlling(true);
                    icon.setEditor(editor);
                    icon.setVisible(true);
                    icon.setEnabled(true);
                    icon.setHidden(false);
                    icon.setMemory(memName);
                    icon.setMinimumSize(new Dimension(this.iconWidth, this.iconHeight));
                    icon.setPreferredSize(new Dimension(this.iconWidth, this.iconHeight));
                    icon.setMaximumSize(new Dimension(this.iconWidth, this.iconHeight));            
                    icon.setText(" ");
                }
            }
        }
    }    
    
    /**
     * Sets the specified field on the requested row to blank.
     * 
     * @param fieldName
     * @param row
     * @param delaySeconds
     */
    public void clearField(String fieldName, int row, int delaySeconds)
    {
        fieldName = fieldName.toUpperCase();
        DepartureField field = fieldMap.get(fieldName);
        if (field != null)
        {
            setField(fieldName, " ", row, delaySeconds);
        }
    }
    
    /**
     * Sets all columns of one row of the departure board to a blank space " ".
     * 
     * @param row Specifies which row to clear (0-based)
     * @param wait Flag indicating whether to wait for the row to clear (all column threads complete) before returning This
     * can be useful if the next command will not be populating all columns of the row or to prevent both the clear thread
     * and the next write thread from competing...leading to an unpredictable state. 
     *
     */
    public void clearRow(int row, boolean wait)
    {
        ArrayList<Thread> threads = new ArrayList<Thread>();
        ArrayList<String> deadThreads = new ArrayList<String>();        
        //
        //  Kill any toggling fields on this row
        for (String threadId : threadMap.keySet())
        {
            if (threadId.endsWith(String.valueOf(row)))
            {
                Thread runningThread = threadMap.get(threadId);
                if (runningThread != null)
                {
                    runningThread.interrupt();
                    deadThreads.add(threadId);
                }                 
            }
        }
           
        for (String dead : deadThreads)
        {
            threadMap.remove(dead);
        }
        
        for (int c=0; c<this.numCols; c++)
        {
            String memName = getMemoryName(row, c);
            Memory memory = InstanceManager.memoryManagerInstance().provideMemory(memName);
            Thread t = new Thread(new SetColumn(memory, " ", 0));
            t.setName("ClearRow: Row" + String.valueOf(row) + "C" + String.valueOf(c));
            t.start();
            threads.add(t);
        }   
        
        //
        //  Wait for all threads to complete before continuing....
        boolean done = false;
        while (!done && wait)
        {
            done = true;
            for (Thread t : threads)
            {
                if (t.isAlive())
                {
                    done = false;
                }
            }
        }
    }
    
    /**
     * Sets the specified field, on the requested row, to the specified value.
     * 
     * @param fieldName
     * @param word
     * @param row
     * @param delaySeconds
     */
    public void setField (String fieldName, String word, int row, int delaySeconds)
    {
        //
        //  We need to optionally pass a killThread parameter because the toggle thread uses setField.
        this.setField(fieldName.toUpperCase(),  word,  row,  delaySeconds, true);
    }
    
    /**
     * Sets the specified field, on the requested row, to the specified value.  We optionally
     * kill any threads already running on this field.  Note that for toggling fields, we don't
     * want to kill the threads on each toggle.
     * 
     * @param fieldName
     * @param word
     * @param row
     * @param delaySeconds
     * @param killThread
     */
    public void setField (String fieldName, String word, int row, int delaySeconds, boolean killThread)
    {
        fieldName = fieldName.toUpperCase();
        DepartureField field = fieldMap.get(fieldName);
        if (field != null)
        {
            Thread runningThread = threadMap.get(fieldName+String.valueOf(row));
            if (killThread && runningThread != null)
            {
                runningThread.interrupt();
                threadMap.remove(fieldName+String.valueOf(row));
            }
            String paddedWord = word.toUpperCase();
            if (paddedWord.length() > field.getNumCols())
            {
                paddedWord = StringUtils.remove(paddedWord, " ");
            }
            if (field.isNumeric())
            {
                paddedWord = StringUtils.leftPad(word,  field.getNumCols()); 
            }
            else
            {
                paddedWord = StringUtils.center(word,  field.getNumCols()); 
            }
            paddedWord = paddedWord.toUpperCase();  
            
            try
            {
                for (int c=0; c<field.getNumCols(); c++)
                {
                    String memName = getMemoryName(row, field.getStartCol()+c);
                    Memory memory = InstanceManager.memoryManagerInstance().provideMemory(memName);
                    
                    String newLetter = "";
                    if (c < field.getNumCols()-1)
                        newLetter = paddedWord.substring(c, c+1);  
                    else
                        newLetter = paddedWord.substring(c);
                    
                    Thread t = new Thread(new SetColumn(memory, newLetter, delaySeconds));
                    t.setName("Set" + memName);
                    t.start();                
                }  
            }
            catch (Exception err)
            {
                System.out.println("DepartureBoard.setField:  Padded word = '" + paddedWord + "'");
                err.printStackTrace();
            }
        }
        else
        {
            System.out.println("*** Unknown departure board field requested " + fieldName);
        }
    }
    
    /**
     * Returns the letters sorted starting with the current letter.
     * 
     * @param currentLetter
     * @return
     */
    public String getSortedLetters(String currentLetter)
    {
        int thisIndex = 0;
        if (currentLetter != null)
        {
            thisIndex = this.alphaNumeric.indexOf(currentLetter);
            if (thisIndex < 0)
            {
                currentLetter = this.alphaNumeric.substring(0,1);
                thisIndex = 0;
            }
        }
        String tail = this.alphaNumeric.substring(thisIndex);
        String head = this.alphaNumeric.substring(0,thisIndex);     
        return tail.concat(head);
    }
    
    /**
     * Creates the Memory objects.  I'm not sure why we need to do a newMemory instead of just provideMemory,
     * but it doesn't work if we don't.
     * 
     * @param sysName
     * @param usrName
     * @return
     */
    public Memory createMemory(String sysName, String usrName) 
    {
        Memory memory = null;
        if (InstanceManager.memoryManagerInstance() != null) 
        {
            if (memory == null)
            {
                InstanceManager.memoryManagerInstance().newMemory(sysName, usrName);
                memory = InstanceManager.memoryManagerInstance().provideMemory(sysName);
            }
        }
        return memory;
    }
    
    /**
     * Find the panel editor for the requested panel.  Icons will be added to this panel.
     * 
     * @param panelName
     * @return
     */
    private Editor findPanelEditor(String panelName)
    {
        try 
        {
            //  initialize loop to find all panel editors
            int i = 0;
            ArrayList <Editor>  editorList = new ArrayList<Editor>();
            Editor editor = (Editor)jmri.InstanceManager.configureManagerInstance().findInstance(java.lang.Class.forName("jmri.jmrit.display.panelEditor.PanelEditor"),i);
                   
            // loop, adding each editor found to the list
            while (editor != null) 
            {
                editorList.add(editor);
                // loop again
                editor = (Editor) jmri.InstanceManager.configureManagerInstance().findInstance(java.lang.Class.forName("jmri.jmrit.display.panelEditor.PanelEditor"),i++);
            }     
            // Now we have a list of editors.
            // For each editor, get the related panel and walk down 
            // its object hierarchy until the widgets themselves are reached    
            for (Editor e : editorList)
            {
                if (e.getName().equals(panelName))
                {
                    return e;
                }
            }
        }
        catch (Exception err)
        {
            err.printStackTrace();
        }
        
        return null;
    }
    
    /**
     * Add a new field to the departure board.
     * 
     * @param fieldName
     * @param startCol
     * @param numCols
     * @param isNumeric
     */
    public void addField(String fieldName, int startCol, int numCols, boolean isNumeric)
    {
//        PositionableLabel label = new PositionableLabel(title, this.editor);
//        label.setPositionable(true);
//        
//        label.setEditor(this.editor);        
//        label.setForeground(Color.white);
//        label.setBackground(Color.red);
//        label.setDisplayLevel(4);
//        label.setLevel(4);
//        label.setEditable(true);
////        label.setLocation(new Point(this.startX + startCol*this.iconWidth, this.startY - this.iconHeight*2));
//        label.setLocation(this.startX + startCol*this.iconWidth, this.startY - this.iconHeight*2);     
//        label.setEnabled(true);
//        label.setMinimumSize(new Dimension(title.length()*this.iconWidth, this.iconHeight));
//        label.setPreferredSize(new Dimension(title.length()*this.iconWidth, this.iconHeight));
//        label.setMaximumSize(new Dimension(title.length()*this.iconWidth, this.iconHeight));  
//        label.setControlling(true);
//        label.setPositionable(true);
//        label.setText(StringUtils.center(title, numCols));
//        label.setVisible(true);     

        fieldName = fieldName.toUpperCase();
        DepartureField field = new DepartureField(fieldName, startCol, numCols, isNumeric);
        this.fieldMap.put(fieldName, field);
    }
    
    /**
     * 
     * @param row
     * @param delaySeconds
     */
    public void createRandomRow(int row, int delaySeconds)
    {
        try
        {
            clearRow(row, true);
            RandomTrain randomTrain = new RandomTrain(this, row, delaySeconds);
            Thread t = new Thread(randomTrain);
            threadMap.put("RT:" + String.valueOf(row), t);
            t.setName("RandomTrain row " + row);
            t.start();
        }
        catch (Exception err)
        {
            err.printStackTrace();
        }
    }
    
    /**
     * Displays a count-down clock in the requested field, starting with the supplied delay.
     * @param fieldName
     * @param delaySeconds
     * @param row
     * @param fuzzy randomize the delay.
     */
    public void clock(String fieldName, int delaySeconds, int row, boolean fuzzy)
    {        
        try
        {            
            String threadName = "Clock:" + fieldName + String.valueOf(row);
            Thread t = new Thread(new CountDown(this, threadName, getMemoryName(row, fieldMap.get(fieldName.toUpperCase()).getStartCol()), delaySeconds, row, fuzzy));
            threadMap.put(threadName, t);
            t.setName(threadName);
            t.start();  
        }
        catch (Exception err)
        {
            err.printStackTrace();
        }
    }
    
    /**
     * Set the specified field to toggle (cycle) between the supplied words.
     * 
     * @param fieldName
     * @param words
     * @param row
     * @param delaySeconds
     */
    public void setField (String fieldName, String[] words, int row, int delaySeconds)
    {
        fieldName = fieldName.toUpperCase();
        DepartureField field = fieldMap.get(fieldName);
        if (field != null)
        {
            String mapKey = fieldName+String.valueOf(row);
            if (threadMap.containsKey(mapKey))
            {
                Thread oldThread = threadMap.get(mapKey);
                oldThread.interrupt();
                threadMap.remove(mapKey);
            }
            ToggleFieldThread thread = new ToggleFieldThread(this, fieldName, words, delaySeconds, row);
            try
            {
                Thread t = new Thread(thread);
                threadMap.put(mapKey, t);   
                t.setName("ToggleField " + fieldName + ":" + words[0]);
                t.start();
            }
            catch (Exception err)
            {
                err.printStackTrace();
            }
        }
        else
        {
            System.out.println("*** Unknown departure board field requested " + fieldName);
        }        
    }
    
    /**
     * Stops all (hopefully) running threads associated with the message board.
     */
    public void stop()
    {
        try
        {
            Thread.sleep(1500);  //  Wait for any rows to settle down
        }
        catch (InterruptedException e)
        {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        for (String key : threadMap.keySet())
        {
            Thread runningThread = threadMap.get(key);
            if (runningThread != null)
            {
                runningThread.interrupt();
            }    
        }
        threadMap.clear();        
    }
    
    private void initTrains()
    {
        this.trainMap = new ArrayList<DepartureBoardTrain>();
        
        try
        {
            List<Train> trains = TrainManager.instance().getTrainsByTimeList();
            for (Train train : trains)
            {
                DepartureBoardTrain dbt = new DepartureBoardTrain();
                if (StringUtils.isNumeric(train.getLeadEngineNumber()))
                {
                    dbt.setDestination(train.getTrainTerminatesName());
                    dbt.setTrainName(train.getName());
                    dbt.setTrainId(train.getId());
                    
                    dbt.setEngineNumber(train.getLeadEngineNumber());
                    dbt.setRoadName(train.getEngineRoad());
                    String displayName  = train.getEngineRoad() + " " + Integer.valueOf(train.getLeadEngineNumber()).toString();
                    if (train.getDescription().startsWith("Special"))
                    {
                        displayName = "SPEC'L";
                    }
                    dbt.setTrainNumber(displayName);
    
                    dbt.setDepartureHour(train.getDepartureTimeHour());
                    dbt.setDepartureMinute(train.getDepartureTimeMinute());
                    dbt.setOccupied(Integer.valueOf(train.getLeadEngineNumber()) == 6);
                    trainMap.add(dbt);
                }
            }
        }
        catch (Exception err)
        {
            err.printStackTrace();
        }
        if (trainMap.size() > 0)
        {
            randomTrainNumber = new Random().nextInt(trainMap.size());
        }
    }    
    
    synchronized DepartureBoardTrain getTrain()
    {
        DepartureBoardTrain train = trainMap.get(randomTrainNumber++ % trainMap.size());
        if (Integer.valueOf(train.getEngineNumber()) == 6)
        {
            train = trainMap.get(randomTrainNumber++ % trainMap.size());
        }
        return train;
    }    
}
