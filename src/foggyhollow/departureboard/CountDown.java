package foggyhollow.departureboard;

import jmri.InstanceManager;
import jmri.Memory;

public class CountDown implements Runnable
{
    int clockDelay;
    Memory m_msb;
    Memory m_lsb;
    Memory colon;
    Memory s_msb;
    Memory s_lsb;
    DepartureBoard board;
    String threadName;
    
    public CountDown(DepartureBoard board, String threadName, String firstColName, int delaySeconds, int row, boolean fuzzy)
    {        
        this.board = board;
        this.threadName = threadName;
        
        int idx = firstColName.indexOf("C")+1;
        String prefix = firstColName.substring(0, idx);
        int firstCol = Integer.valueOf(firstColName.substring(idx));
        m_msb = InstanceManager.memoryManagerInstance().provideMemory(prefix + String.valueOf(firstCol));            
        m_lsb = InstanceManager.memoryManagerInstance().provideMemory(prefix + String.valueOf(firstCol+1));            
        colon = InstanceManager.memoryManagerInstance().provideMemory(prefix + String.valueOf(firstCol+2));            
        s_msb = InstanceManager.memoryManagerInstance().provideMemory(prefix + String.valueOf(firstCol+3));            
        s_lsb = InstanceManager.memoryManagerInstance().provideMemory(prefix + String.valueOf(firstCol+4));                        
        
        clockDelay = delaySeconds;
        if (fuzzy)
        {
            java.util.Random random = new java.util.Random();
            Double randomDelay = new Double(delaySeconds + random.nextGaussian()*(delaySeconds *.2));
            clockDelay = randomDelay.intValue();
        }        
    }
    public void run()
    {
        colon.setValue(":");        
        for (int s=clockDelay; s>-1; s--)
        {
            String minMSB = String.valueOf((s/60) / 10 );
            String minLSB = String.valueOf((s / 60) % 10);
            String secMSB = String.valueOf((s % 60) / 10);
            String secLSB = String.valueOf(s % 10);          
            s_msb.setValue(secMSB); 
            s_lsb.setValue(secLSB);         
            m_msb.setValue(minMSB);
            m_lsb.setValue(minLSB) ;        
            if (s > 0) 
            {
                try {
                    Thread.sleep(1000);
                    board.threadMap.remove(threadName);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    //e.printStackTrace();
                }                    
            }
        }            
    }
} 
