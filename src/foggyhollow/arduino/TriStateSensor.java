package foggyhollow.arduino;

import java.time.Duration;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.TemporalAccessor;
import java.util.Vector;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import jmri.JmriException;
import jmri.NamedBean;
import jmri.Sensor;

/**
 * JMRI extension to support tri-state sensors. Typically used to control lights
 * that can have 3 states: on, dim, or off.
 * 
 * @author Paul Morris
 *
 */
public class TriStateSensor
{
    public final static int ON = 1;
    public final static int OFF = 0;
    public final static int DIM = 2;

    private NamedBean onSensor;
    private NamedBean offSensor;
    private NamedBean dimSensor;

    private int state;
    private DateTimeFormatter formatter;
    
    private Vector<ScheduledFuture<?>> taskList;

    //private static final ScheduledThreadPoolExecutor scheduler = (ScheduledThreadPoolExecutor) Executors.newScheduledThreadPool(1);
    private ScheduledThreadPoolExecutor scheduler;
    public TriStateSensor()
    {
    }

    /**
     * Constructor to create a new TriStateSensor.
     * 
     * @param dimSensor
     *            - JMRI sensor used to indicate the tri-state sensor is dimmed.
     * @param onSensor
     *            - JMRI sensor used to indicate the tri-state sensor is on
     *            (bright).
     * @param offSensor
     *            - JMRI sensor used to indicate the tri-state sensor is off.
     */
    public TriStateSensor(NamedBean dimSensor, NamedBean onSensor, NamedBean offSensor)
    {
	
	this.onSensor = onSensor;
	this.offSensor = offSensor;
	this.dimSensor = dimSensor;

	taskList = new Vector<ScheduledFuture<?>>();
	scheduler = (ScheduledThreadPoolExecutor) Executors.newScheduledThreadPool(1);	
	scheduler.setRemoveOnCancelPolicy(true);

	try
	{
	    if (this.onSensor != null)
	    {
		this.onSensor.setState(jmri.Sensor.INACTIVE);
	    }
	    if (this.dimSensor != null)
	    {
		this.dimSensor.setState(jmri.Sensor.INACTIVE);
	    }
	    if (this.offSensor != null)
	    {
		this.offSensor.setState(jmri.Sensor.ACTIVE);
	    }
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
     * 
     * @param int
     *            state
     * @param float
     *            minutes
     */
    public void scheduleStateChange(int state, float minutes)
    {
	try
	{
	    ScheduledFuture<?> task = scheduler.schedule(new Runnable() {
		@Override
		public void run()
		{
		    setState(state);
		}
	    }, new Double(minutes * 60.0).intValue(), TimeUnit.SECONDS);
	    taskList.add(task);
	}
	catch (Exception ex)
	{
	    System.out.println(ex.getMessage());
	}
    }

    /**
     * Schedule the sensor to change state delayMinutes after the scheduleTime.
     * 
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

	scheduled = scheduled.plusSeconds(new Double(delayMinutes * 60).intValue());
	Duration delay = Duration.between(Instant.now(), scheduled);
	try
	{
	    ScheduledFuture<?> task = scheduler.schedule(new Runnable() {
		@Override
		public void run()
		{
		    setState(state);
		}
	    }, delay.getSeconds(), TimeUnit.SECONDS);
	    taskList.add(task);	    
	}
	catch (Exception ex)
	{
	    System.out.println(ex.getMessage());
	}
    }

    /**
     * Schedule the sensor to change state delayMinutes before the scheduleTime
     * 
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

	scheduled = scheduled.minusSeconds(new Double(delayMinutes * 60).intValue());
	Duration delay = Duration.between(Instant.now(), scheduled);
	try
	{
	    ScheduledFuture<?> task = scheduler.schedule(new Runnable() {
		@Override
		public void run()
		{
		    setState(state);
		}
	    }, delay.getSeconds(), TimeUnit.SECONDS);
	    taskList.add(task);
	}
	catch (Exception ex)
	{
	    System.out.println(ex.getMessage());
	}
    }

    public void setPeriodicStateChange(float initDelayMinutes, float onMinutes, float offMinutes, boolean goDim)
    {
	int initDelay = new Double(initDelayMinutes * 60.0).intValue();
	int onDelay = new Double(onMinutes * 60.0).intValue();
	int offDelay = new Double(offMinutes * 60.0).intValue();

	try
	{
	    ScheduledFuture<?> task = scheduler.scheduleAtFixedRate(new Runnable() {
		@Override
		public void run()
		{
		    setState(ON);
		}
	    }, initDelay, onDelay + offDelay, TimeUnit.SECONDS);
	    taskList.add(task);

	    task = scheduler.scheduleAtFixedRate(new Runnable() {
		@Override
		public void run()
		{
		    if (goDim)
			setState(DIM);
		    else
			setState(OFF);
		}
	    }, initDelay + onDelay, onDelay + offDelay, TimeUnit.SECONDS);
	    taskList.add(task);
	}
	catch (Exception ex)
	{
	    System.out.println(ex.getMessage());
	}
    }

    /**
     * Set the current state of the Tri-Sensor
     * 
     * @param state
     */
    public void setState(int state)
    {
	try
	{
	    if (state == ON)
	    {
		if (this.onSensor != null)
		{
		    this.onSensor.setState(jmri.Sensor.ACTIVE);
		}
		if (this.offSensor != null)
		{
		    this.offSensor.setState(jmri.Sensor.INACTIVE);
		}
		if (this.dimSensor != null)
		{
		    this.dimSensor.setState(jmri.Sensor.INACTIVE);
		}
	    }
	    else if (state == DIM)
	    {
		if (this.dimSensor != null)
		{
		    this.dimSensor.setState(jmri.Sensor.ACTIVE);
		}
		if (this.offSensor != null)
		{
		    this.offSensor.setState(jmri.Sensor.INACTIVE);
		}
		if (this.onSensor != null)
		{
		    this.onSensor.setState(jmri.Sensor.INACTIVE);
		}
	    }
	    else if (state == OFF)
	    {
		if (this.offSensor != null)
		{
		    this.offSensor.setState(jmri.Sensor.ACTIVE);
		}
		if (this.onSensor != null)
		{
		    this.onSensor.setState(jmri.Sensor.INACTIVE);
		}
		if (this.dimSensor != null)
		{
		    this.dimSensor.setState(jmri.Sensor.INACTIVE);
		}
	    }
	}
	catch (JmriException err)
	{
	    err.printStackTrace();
	}
    }

    /**
     * Returns the current state of the trisensor
     * 
     * @return state
     */
    public int getState()
    {
	return state;
    }
    
    /**
     * Cancels any scheduled state change events
     */
    public void cancelScheduledTasks()
    {
	//System.out.println("Canceling " + scheduler.getTaskCount() + " scheduled tasks for " + onSensor.getUserName());
	for (int i=0; i<taskList.size(); i++)
	{
	    taskList.get(i).cancel(true);
	    scheduler.remove((Runnable) taskList.get(i));
	}
	scheduler.purge();
	scheduler.getQueue().clear();	
	taskList.removeAllElements();
	//System.out.println("After canceling " + scheduler.getTaskCount() + " tasks in queue");
    }
}
