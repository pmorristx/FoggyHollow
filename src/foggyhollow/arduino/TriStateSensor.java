package foggyhollow.arduino;

import java.time.Duration;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.TemporalAccessor;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

import jmri.JmriException;
import jmri.Sensor;
/**
 * JMRI extension to support tri-state sensors.  Typically used to control lights that can have 3 states: on, dim, or off.
 * 
 * @author Paul Morris
 *
 */
public class TriStateSensor
{
    public final static int ON = 1;
    public final static int OFF = 0;
    public final static int DIM = 2;

    private Sensor onSensor;
    private Sensor offSensor;
    private Sensor dimSensor;
    
    private int state;
    private DateTimeFormatter formatter;
    
    private static final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);    

    public TriStateSensor()
    {
    }

    /**
     * Constructor to create a new TriStateSensor.
     * 
     * @param dimSensor - JMRI sensor used to indicate the tri-state sensor is dimmed.
     * @param onSensor - JMRI sensor used to indicate the tri-state sensor is on (bright).
     * @param offSensor - JMRI sensor used to indicate the tri-state sensor is off.
     */
    public TriStateSensor(Sensor dimSensor, Sensor onSensor, Sensor offSensor)
    {
	this.onSensor = onSensor;
	this.offSensor = offSensor;
	this.dimSensor = dimSensor;
	
	try
	{
	    if (this.onSensor != null) { this.onSensor.setState(jmri.Sensor.INACTIVE);}
	    if (this.dimSensor != null) { this.dimSensor.setState(jmri.Sensor.INACTIVE);	}
	    if (this.offSensor != null) { this.offSensor.setState(jmri.Sensor.ACTIVE);}
	}
	catch (JmriException err)
	{
	    err.printStackTrace();
	}
	this.state = OFF;
	this.formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");		
    }

    /**
     * Schedule the sensor to change state sometime in the future.
     * @param int state
     * @param float minutes
     */
    public void scheduleStateChange(int state, float minutes)
    {
        ScheduledFuture<?> countdown = scheduler.schedule(new Runnable() {
            @Override
            public void run() {
        	setState(state);
            }}, new Double(minutes*60.0).intValue(), TimeUnit.SECONDS);	
    }
    
    /**
     * Schedule the sensor to change state delayMinutes after the scheduleTime.
     * @param state
     * @param scheduleTimeStr
     * @param delayMinutes
     */
    public void scheduleStateChangeAfter(int state, String scheduleTimeStr, float delayMinutes)
    {	
	TemporalAccessor temporalAccessor = formatter.parse(scheduleTimeStr);
	LocalDateTime localDateTime = LocalDateTime.from(temporalAccessor);
	ZonedDateTime zonedDateTime = ZonedDateTime.of(localDateTime, ZoneId.systemDefault());
	Instant scheduled = Instant.from(zonedDateTime);	
	
	scheduled = scheduled.plusSeconds(new Double(delayMinutes*60).intValue());
	Duration delay = Duration.between(Instant.now(),  scheduled);
	System.out.println("ScheduleChangeAfter in " + delay.toString() + " seconds, scheduledTime = " + scheduled.toString());
        ScheduledFuture<?> countdown = scheduler.schedule(new Runnable() {
            @Override
            public void run() {
        	setState(state);
            }}, delay.getSeconds(), TimeUnit.SECONDS);	
    }
    
    /**
     * Schedule the sensor to change state delayMinutes before the scheduleTime
     * @param state
     * @param scheduleTimeStr
     * @param delayMinutes
     */
    public void scheduleStateChangeBefore(int state, String scheduleTimeStr, float delayMinutes)
    {
	TemporalAccessor temporalAccessor = formatter.parse(scheduleTimeStr);
	LocalDateTime localDateTime = LocalDateTime.from(temporalAccessor);
	ZonedDateTime zonedDateTime = ZonedDateTime.of(localDateTime, ZoneId.systemDefault());
	Instant scheduled = Instant.from(zonedDateTime);
	
	scheduled = scheduled.minusSeconds(new Double(delayMinutes*60).intValue());
	Duration delay = Duration.between(Instant.now(),  scheduled);
	System.out.println("ScheduleChangeAfter in " + delay.toString() + " seconds, scheduledTime = " + scheduled.toString());	
        ScheduledFuture<?> countdown = scheduler.schedule(new Runnable() {
            @Override
            public void run() {
        	setState(state);
            }}, delay.getSeconds(), TimeUnit.SECONDS);	
    }    
    
    /**
     * Set the current state of the Tri-Sensor
     * @param state
     */
    public void setState(int state)
    {
	try
	{
	    if (state == ON)
	    {
		if (this.onSensor != null) { this.onSensor.setState(jmri.Sensor.ACTIVE); }
		if (this.offSensor != null) { this.offSensor.setState(jmri.Sensor.INACTIVE); }
		if (this.dimSensor != null) { this.dimSensor.setState(jmri.Sensor.INACTIVE); }
	    }
	    else if (state == DIM)
	    {
		if (this.dimSensor != null) { this.dimSensor.setState(jmri.Sensor.ACTIVE);}
		if (this.offSensor != null) { this.offSensor.setState(jmri.Sensor.INACTIVE);}
		if (this.onSensor != null) { this.onSensor.setState(jmri.Sensor.INACTIVE);}
	    }
	    else if (state == OFF)
	    {
		if (this.offSensor != null) { this.offSensor.setState(jmri.Sensor.ACTIVE);}
		if (this.onSensor != null) { this.onSensor.setState(jmri.Sensor.INACTIVE);}
		if (this.dimSensor != null) { this.dimSensor.setState(jmri.Sensor.INACTIVE);}
	    }
	}
	catch (JmriException err)
	{
	    err.printStackTrace();
	}
    }
    
    /**
     * Returns the current state of the trisensor
     * @return state 
     */
    public int getState()
    {
	return state;
    }
}
