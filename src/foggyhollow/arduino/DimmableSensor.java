package foggyhollow.arduino;

import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;

import jmri.JmriException;
import jmri.Sensor;

public class DimmableSensor implements PropertyChangeListener
{
    private Sensor arduinoDimSensor;
    private Sensor arduinoOnSensor;
    private Sensor guiOnSensor;
    private Sensor guiDimSensor;
    private Sensor guiOffSensor;

    public DimmableSensor()
    {
    }
    
    public DimmableSensor(Sensor aDim, Sensor aOn, Sensor gDim, Sensor gOn, Sensor gOff)
    {
	this.arduinoDimSensor = aDim;
	this.arduinoOnSensor = aOn;
	this.guiDimSensor = gDim;
	this.guiOnSensor = gOn;
	this.guiOffSensor = gOff;
	
	init();
    }

    public void init()
    {
	guiOnSensor.addPropertyChangeListener(this);
	guiOffSensor.addPropertyChangeListener(this);
	guiDimSensor.addPropertyChangeListener(this);
    }



    @Override
    public void propertyChange(PropertyChangeEvent evt)
    {
	try
	{
	    jmri.Sensor source = (jmri.Sensor) evt.getSource();
	    if (source == this.guiOnSensor && source.getState() == jmri.Sensor.ACTIVE)
	    {
		System.out.println("*** In DimmableSensor, source = " + source.getUserName() + " state = " + source.getState());	    				
		this.arduinoOnSensor.setState(jmri.Sensor.ACTIVE);
		this.arduinoDimSensor.setState(jmri.Sensor.INACTIVE);
	    }
	    else if (source == this.guiDimSensor && source.getState() == jmri.Sensor.ACTIVE)
	    {
		System.out.println("*** In DimmableSensor, source = " + source.getUserName() + " state = " + source.getState());	    				
		this.arduinoOnSensor.setState(jmri.Sensor.ACTIVE);
		this.arduinoDimSensor.setState(jmri.Sensor.ACTIVE);
	    }
	    else if (source == this.guiOffSensor && source.getState() == jmri.Sensor.ACTIVE)
	    {
		System.out.println("*** In DimmableSensor, source = " + source.getUserName() + " state = " + source.getState());	    		
		this.arduinoOnSensor.setState(jmri.Sensor.INACTIVE);
		//this.arduinoDimSensor.setState(jmri.Sensor.INACTIVE);
	    }
	}
	catch (JmriException err)
	{
	    System.out.println("JmriException in foggyhollow.dimmableLight" + err);
	}
    }
    
    /*
     * Getters/Setters
     */
    public Sensor getArduinoDimSensor()
    {
	return arduinoDimSensor;
    }

    public void setArduinoDimSensor(Sensor arduinoDimSensor)
    {
	this.arduinoDimSensor = arduinoDimSensor;
    }

    public Sensor getArduinoOnSensor()
    {
	return arduinoOnSensor;
    }

    public void setArduinoOnSensor(Sensor arduinoOnSensor)
    {
	this.arduinoOnSensor = arduinoOnSensor;
    }

    public Sensor getGuiOnSensor()
    {
	return guiOnSensor;
    }

    public void setGuiOnSensor(Sensor guiOnSensor)
    {
	this.guiOnSensor = guiOnSensor;
    }

    public Sensor getGuiDimSensor()
    {
	return guiDimSensor;
    }

    public void setGuiDimSensor(Sensor guiDimSensor)
    {
	this.guiDimSensor = guiDimSensor;
    }

    public Sensor getGuiOffSensor()
    {
	return guiOffSensor;
    }

    public void setGuiOffSensor(Sensor guiOffSensor)
    {
	this.guiOffSensor = guiOffSensor;
    }    
}