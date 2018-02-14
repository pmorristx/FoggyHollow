package foggyhollow.minetrain;

import java.util.Random;

public class MineTrain extends jmri.jmrit.automat.AbstractAutomaton 
{
    private Random random;
    private jmri.Throttle throttle;
    private int locoNumber;
    private int level;
    private jmri.jmrit.Sound singleToot;
    private jmri.jmrit.Sound doubleToot;    
    private boolean isForward;
    
    
    public MineTrain(int locoNumber, int level)
    {
        random = new java.util.Random();
        this.locoNumber = locoNumber;
        this.level = level;
        this.isForward = true;
    }
    
    //
    //  Returns a randomized speed.  Reverse speeds are slower than forward
    protected int getSpeed(boolean isForward)
    {
        int speed;
        if (isForward)
                speed = new Double(0.15 + 0.1 * random.nextInt(3)).intValue();
        else
                speed =  new Double(0.15 + 0.1 * random.nextInt(2)).intValue();   
        return speed;    
    }
    
    protected void startTrain()
    {
        throttle.setF1(true); // Turn brake light on
        throttle.setIsForward(isForward);
        throttle.setF2(true); // Turn on beacon
        throttle.setF0(true);  // Turn on headlight              
        waitMsec((random.nextInt(2) + 1) * 1000);            
        throttle.setF4(false);  // Turn dim off
        waitMsec((random.nextInt(2) + 1) * 1000);
        
        //  Signal direction
        if (isForward)
            doubleToot.play();
        else
            singleToot.play();
                
        waitMsec((random.nextInt(3) + 2) * 1000);
        // Start moving
        throttle.setSpeedSetting(getSpeed(isForward));      
    }
    
    protected void stopTrain()
    {
        throttle.setSpeedSetting(0);
        waitMsec((random.nextInt(3) + 2) * 1000);
        throttle.setF4(true);
        waitMsec((random.nextInt(2) + 1) * 1000);                              
        singleToot.play();        
    }

    public jmri.Throttle getThrottle() {
        return throttle;
    }

    public void setThrottle(jmri.Throttle throttle) {
        this.throttle = throttle;
    }

    public int getLocoNumber() {
        return locoNumber;
    }

    public void setLocoNumber(int locoNumber) {
        this.locoNumber = locoNumber;
    }

    public int getLevel() {
        return level;
    }

    public void setLevel(int level) {
        this.level = level;
    }

    public jmri.jmrit.Sound getSingleToot() {
        return singleToot;
    }

    public void setSingleToot(jmri.jmrit.Sound singleToot) {
        this.singleToot = singleToot;
    }
    
}
