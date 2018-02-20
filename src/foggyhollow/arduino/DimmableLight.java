package foggyhollow.arduino;

import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;

import jmri.Light;
import jmri.Sensor;

public class DimmableLight implements PropertyChangeListener
{
    private Light arduinoDimLight;
    private Light arduinoOnLight;
    private Sensor guiOnSensor;
    private Sensor guiDimSensor;
    private Sensor guiOffSensor;

    public DimmableLight()
    {
	System.out.println("*** In DimmableLight default constructor");	
    }

    public DimmableLight(Light aDim, Light aOn, Sensor gDim, Sensor gOn, Sensor gOff)
    {
	this.arduinoDimLight = aDim;
	this.arduinoOnLight = aOn;
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
	jmri.Sensor source = (jmri.Sensor) evt.getSource();

	if (source == this.guiOnSensor && source.getState() == jmri.Sensor.ACTIVE)
	{
	    this.arduinoOnLight.setState(jmri.Light.ON);
	    this.arduinoDimLight.setState(jmri.Light.OFF);
	}
	else if (source == this.guiDimSensor && source.getState() == jmri.Sensor.ACTIVE)
	{
	    this.arduinoOnLight.setState(jmri.Light.ON);
	    this.arduinoDimLight.setState(jmri.Light.ON);
	}
	else if (source == this.guiOffSensor && source.getState() == jmri.Sensor.ACTIVE) 
	{
	    this.arduinoOnLight.setState(jmri.Light.OFF);
	    //this.arduinoDimLight.setState(jmri.Light.OFF);
	}
    }

    /*
     * Getters/Setters
     */
    public Light getArduinoDimLight()
    {
	return arduinoDimLight;
    }

    public void setArduinoDimLight(Light arduinoDimLight)
    {
	this.arduinoDimLight = arduinoDimLight;
    }

    public Light getArduinoOnLight()
    {
	return arduinoOnLight;
    }

    public void setArduinoOnLight(Light arduinoOnLight)
    {
	this.arduinoOnLight = arduinoOnLight;
    }

    public Sensor getguiOnSensor()
    {
	return guiOnSensor;
    }

    public void setguiOnSensor(Sensor guiOnSensor)
    {
	this.guiOnSensor = guiOnSensor;
    }

    public Sensor getguiDimSensor()
    {
	return guiDimSensor;
    }

    public void setguiDimSensor(Sensor guiDimSensor)
    {
	this.guiDimSensor = guiDimSensor;
    }

    public Sensor getguiOffSensor()
    {
	return guiOffSensor;
    }

    public void setguiOffSensor(Sensor guiOffSensor)
    {
	this.guiOffSensor = guiOffSensor;
    }
}