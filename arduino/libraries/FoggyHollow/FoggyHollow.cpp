#include "FoggyHollow.h"
#include "LocoNet.h"
#include <SoftwareServo.h>

FoggyHollowClass::FoggyHollowClass() {}

/**
 * Creates a light object using the specified Arduino pin to power an LED and the specified
 * JMRI Sensor address (command) to switch the light on/off.
 */
fh_light FoggyHollowClass::createLight( uint8_t pin, uint8_t onCmd, uint8_t function, uint8_t functionCmd)
{
	fh_light light;

	light.pin = pin;
	light.onCmd = onCmd;
	light.isInverted = false;
	light.function = function;
	light.functionCmd = functionCmd;
	light.isOn = false;

	if (function == BLINKING)
	{
		light.rate1 = 30000;
		light.rate2 = 30000;
	}
	else if (function == DIMMABLE)
	{
		light.rate1 = 1;
		light.rate2 = 8;
	}
	else if (function == FLICKERING)
	{
		light.rate1 = 5;
		light.rate2 = 40;
	}

	pinMode(light.pin, OUTPUT);

	digitalWrite(light.pin, LOW);
	LocoNet.reportSensor(light.onCmd, INACTIVE);

	return light;
}

fh_turnout FoggyHollowClass::createTurnout(uint8_t servoPin,  uint8_t turnoutAddr, uint8_t thrownIndicatorPin,  uint8_t thrownIndicatorAddr,  uint8_t closedIndicatorPin,  uint8_t closedIndicatorAddr)
{

	fh_turnout turnout;

	turnout.servoPin = servoPin;
	turnout.turnoutAddr = turnoutAddr;
	turnout.thrownIndicatorAddr = thrownIndicatorAddr;
	turnout.thrownIndicatorPin = thrownIndicatorPin;
	turnout.closedIndicatorPin = closedIndicatorPin;
	turnout.closedIndicatorAddr = closedIndicatorAddr;

	// Defaults
	turnout.closedPosition = 125;
	turnout.thrownPosition = 75;
	turnout.currentPosition = 100;

    turnout.servoSlowdown = 3;   //servo loop counter limit
	turnout.servoSlowCounter = 1; //servo loop counter to slowdown servo transit

	turnout.hasCtcIndicators = false;

	pinMode(turnout.servoPin, OUTPUT);

	return turnout;
}

/**
 * Add addresses of CTC relay send/receive indicators to a turnout.
 */
void FoggyHollowClass::setCtcIndicators (fh_turnout *turnout, uint8_t sendAddr, uint8_t receiveAddr)
{
	turnout->ctcSendIndicatorAddr = sendAddr;
	turnout->ctcReceiveIndicatorAddr = receiveAddr;
	turnout->hasCtcIndicators = true;
}

/**
 * Change the position of a turnout....also deal with the on/off state of the turnout lantern.
 */

void FoggyHollowClass::changeTurnout(fh_turnout *turnout, uint8_t direction, SoftwareServo *turnoutServo)
{
	//
	// Turn the CTC indicator N/R light off and set the increment for the correct
	// direction
	turnout->direction = direction;
	if ((direction != THROWN))
	{
		turnout->increment = 1;
		digitalWrite(turnout->thrownIndicatorPin, HIGH);
		LocoNet.reportSensor(turnout->thrownIndicatorAddr, INACTIVE);
	}
	else if ((direction == THROWN))
	{
		turnout->increment = -1;
		digitalWrite(turnout->closedIndicatorPin, HIGH);
		LocoNet.reportSensor(turnout->closedIndicatorAddr, INACTIVE);
	}

	turnout->moving = true;
	turnout->currentState = SENDING;
	turnout->direction = direction;
	turnoutServo->attach(turnout->servoPin);

	if (turnout->hasCtcIndicators)
	{
		LocoNet.reportSensor(turnout->ctcSendIndicatorAddr, ACTIVE);
	}

	//
	//  If there is a relay attached to power the frog, turn power
	//  to the frog off & report to JMRI
	if (turnout->frogRelayThrownPin > 0)
	{
		digitalWrite(turnout->frogRelayThrownPin, HIGH);
		digitalWrite(turnout->frogRelayClosedPin, HIGH);
		LocoNet.reportSensor(turnout->frogRelayThrownAddr, INACTIVE);
		LocoNet.reportSensor(turnout->frogRelayClosedAddr, INACTIVE);
	}
}

/**
 * moveTurnout
 *
 * Called repeatedly by the main Arduino loop to advance the turnout servo one degree.  We
 * also control the software CTC relay lights.
 *
 */
void FoggyHollowClass::moveTurnout(fh_turnout *turnout, SoftwareServo *turnoutServo)
{
	if (turnout->currentState == SENDING && turnout->hasCtcIndicators)
	{
		//
		//  If we have CTC send/receive indicators, turn the SEND indicator off
		//  and turn the receive indicator on.
		LocoNet.reportSensor(turnout->ctcSendIndicatorAddr, ACTIVE);
		if (turnout->ctcReceiveCount++ > 1000)
		{
			turnout->ctcReceiveCount = 0;
			LocoNet.reportSensor(turnout->ctcSendIndicatorAddr, INACTIVE);
			LocoNet.reportSensor(turnout->ctcReceiveIndicatorAddr, INACTIVE);
			turnout->currentState = MOVING;
		}
	}
	else if (turnout->currentState == MOVING)
	{
#ifdef DEBUG
		Serial.println("in FoggyHollow::moveTurnout: ");
		Serial.print ("currentPosition: ");
		Serial.print (turnout->currentPosition);
		Serial.print (" increment: ");
		Serial.print (turnout->increment);

		Serial.print (" closedPosition: ");
		Serial.print (turnout->closedPosition);

		Serial.print (" thrownPosition: ");
		Serial.print (turnout->thrownPosition);

		Serial.print (" servoSlowCounter: ");
		Serial.print (turnout->servoSlowCounter);
		Serial.print (" slowdown ");
		Serial.println (turnout->servoSlowdown);
#endif
		//
		//  Don't do anything until we've been through "serverSlowdown" times.
		if (turnout->servoSlowCounter++ > turnout->servoSlowdown)
		{
			turnoutServo->write(turnout->currentPosition);
			turnout->servoSlowCounter = 0;

			turnout->currentPosition = turnout->currentPosition + turnout->increment;
			if (turnout->increment > 0) {
				if (turnout->currentPosition > turnout->closedPosition)
				{
					turnout->currentPosition = turnout->closedPosition;
					LocoNet.reportSensor(turnout->ctcReceiveIndicatorAddr, ACTIVE);
					turnout->currentState = RECEIVING;
					turnout->moving = false;
					turnoutServo->detach();
				}
			}
			if (turnout->increment < 0) {
				if (turnout->currentPosition < turnout->thrownPosition)
				{
					turnout->currentPosition = turnout->thrownPosition;
					LocoNet.reportSensor(turnout->ctcReceiveIndicatorAddr, ACTIVE);
					turnout->currentState = RECEIVING;
					turnout->moving = false;
					turnoutServo->detach();
				}
			}
		}
	}
	else if (turnout->currentState == RECEIVING)
	{
		//
		// Wait a couple of seconds then turn off the CTC Receive Indicator and
		// turn on the turnout THROWN or CLOSED light.  We activate the Arduino
		// pin to turn on the LED on the 'real' control panel and set the JMRI
		// sensor to display on the 'software' control panel.
		//
		if (turnout->ctcReceiveCount++ > 1000)
		{
			LocoNet.reportSensor(turnout->ctcReceiveIndicatorAddr, INACTIVE);
			if (turnout->direction != THROWN)
			{
				LocoNet.reportSensor(turnout->closedIndicatorAddr, ACTIVE);
				digitalWrite(turnout->closedIndicatorPin, LOW);
			}
			else
			{
				LocoNet.reportSensor(turnout->thrownIndicatorAddr, ACTIVE);
				digitalWrite(turnout->thrownIndicatorPin, LOW);
			}

			turnout->currentState = IDLE;
			turnout->ctcReceiveCount = 0;
		}
	}
	else
	{
		//
		// Only fiddle with the frog controls if there is a relay attached to
		// power the frog.
		if (turnout->frogRelayClosedPin > 0)
		{
			if (turnout->direction != THROWN)
			{
				digitalWrite(turnout->frogRelayClosedPin, LOW);
				LocoNet.reportSensor(turnout->frogRelayClosedAddr, ACTIVE);
			}
			else
			{
				digitalWrite(turnout->frogRelayThrownPin, LOW);
				LocoNet.reportSensor(turnout->frogRelayThrownAddr, ACTIVE);
			}
		}
	}
}

/**
 * Called from "loop" to blink an LED.  Note that we have to blink rates that allow
 * for dimming of an LED (pseudo PSM).
 */
void FoggyHollowClass::blinkLED(fh_light *light)
{
	//Serial.println ("Blinking LED");
	if (light->counter++ > light->rate1 && light->phase == HIGH)
	{
		light->counter = 0;
		light->phase = LOW;
	}
	else if (light->counter++ > light->rate2 && light->phase == LOW)
	{
		light->counter = 0;
		light->phase = HIGH;
	}
	digitalWrite(light->pin, light->phase);
}

/**
 * Sets the on/off state of a light.  We set the isBrightening/isDimming flags in the light
 * object, then let the "loop" fade the led to the requested state.
 */
void FoggyHollowClass::setState(fh_light *light, bool state)
{
	light->counter = 0;
	if (!light->isInverted)
	{
		if (state)
		{
			light->isBrightening = true;
			light->isDimming = false;
		}
		else
		{
			light->isDimming = true;
			light->isBrightening = false;
		}
	}
	else
	{
		if (state)
		{
			light->isBrightening = false;
			light->isDimming = true;
		}
		else
		{
			light->isDimming = false;
			light->isBrightening = true;
		}
	}
}

/**
 * Set the state of a light "function" to on/off.  If we set the function to "on",
 * we also turn on the light
 */
void FoggyHollowClass::setFunctionState(fh_light *light, bool state)
{
	light->counter = 0;
	light->isFunctionOn = state;

	//
	//  If light isn't on, but we are turning function on, turn the light on.
	if (state  && !light->isOn)
	{
		light->isBrightening = true;
	}
	else if (!state && light->isOn) // If light is "ON", write to the pin to ensure that we didn't stop the function with the pin off.
	{
		if (!light->isInverted)
		{
			digitalWrite(light->pin, HIGH);
		}
		else
		{
			digitalWrite(light->pin, LOW);
		}
	}
	else
	{
		LocoNet.reportSensor(light->onCmd, INACTIVE);
		if (light->functionCmd > 0)
		{
			LocoNet.reportSensor(light->functionCmd, INACTIVE);
		}
	}
}

void FoggyHollowClass::fadeLED(fh_light light, uint8_t requestedState)
{
	  uint8_t fade_time = 170;
	  float time_fraction;
	  uint8_t del_temp;

	  //
	  //  Only do this if we are changing the state of the light....don't do anything if
	  //  the light is already in the requested state.
	  if ((requestedState != INACTIVE && !light.isOn) || (requestedState == INACTIVE && light.isOn))
	  {
		  boolean start_state = light.isOn ? HIGH : LOW;
		  boolean end_state = light.isOn ? LOW : HIGH;

		  for ( uint8_t loop_time=0; loop_time<fade_time; loop_time++)  {
				time_fraction = (float (loop_time))/(float (fade_time));
				digitalWrite (light.pin, start_state);
				del_temp = 1000 - (1000.*time_fraction);
				if (del_temp<0) del_temp=0;
				delayMicroseconds (del_temp);
				digitalWrite (light.pin, end_state);
				delayMicroseconds (1000.*time_fraction);
				}
		  light.isOn = requestedState != INACTIVE;
	  }
}

/**
 * Fades a light on/off.  Note that this method will execute until the light has
 * transitioned...may cause other lights to quit blinking/flickering/dimming.
 */
void FoggyHollowClass::fadeOnOff(fh_light light, uint8_t state)
{
#define fadedelay 24
#define fadeStep 12

	if (state != LOW && !light.isOn)
	{
		// Turning on
		for ( uint8_t t = 0; t < fadeStep; t += 1)
		{
			digitalWrite( light.pin, HIGH);
			delay(fadedelay * (t / fadeStep));
			digitalWrite( light.pin, LOW);
			delay(fadedelay - (fadedelay * (t / fadeStep)));
		}
		digitalWrite( light.pin,  HIGH );
		light.isOn = true;
		LocoNet.reportSensor(light.onCmd, ACTIVE);
	} else if (state == LOW && light.isOn) {
		// Turning off
		for ( uint8_t t = 0; t < fadeStep; t += 1)
		{
			digitalWrite( light.pin, LOW);
			delay(fadedelay * (t / fadeStep));
			digitalWrite( light.pin, HIGH);
			delay(fadedelay - (fadedelay * (t / fadeStep)));
		}
		digitalWrite(light.pin, LOW);
		light.isOn = false;
		LocoNet.reportSensor(light.onCmd, INACTIVE);
	}
}

/**
 * Fades a light on/off based on the isBrightening/isDimming value.  This method is called within the
 * main loop to avoid locking up the Arduino (and pausing blink/flicker/dim on other lights).
 */
void FoggyHollowClass::fadeOn(fh_light *light)
{
#define fadedelay 24
#define fadeStep 12

	//if ((light.isBrightening && !light.isInverted) || (light.isDimming && light.isInverted))
	if (light->isBrightening)
	{
		//Serial.print ("Turning on light ");
		//Serial.print (light->pin);
		//Serial.print (" counter = ");
		//Serial.println(light->counter);
		// Turning on
		digitalWrite( light->pin, HIGH);
		delay(fadedelay * (light->counter / fadeStep));
		digitalWrite( light->pin, LOW);
		delay(fadedelay - (fadedelay * (light->counter++ / fadeStep)));

		if (light->counter >= fadeStep)
		{
			digitalWrite(light->pin,  HIGH );
			light->isOn = true;
			light->isBrightening = false;
			light->isDimming = false;
			//LocoNet.reportSensor(light->onCmd, ACTIVE);
		}
//	} else if ((light.isDimming && !light.isInverted) || (light.isBrightening && light.isInverted)) {
	} else if (light->isDimming) {
		// Turning off
		//Serial.print ("Turning off light ");
		//Serial.print (light->pin);
		//Serial.print (" counter = ");
		//Serial.println(light->counter);
		digitalWrite( light->pin, LOW);
		delay(fadedelay * (light->counter / fadeStep));
		digitalWrite( light->pin, HIGH);
		delay(fadedelay - (fadedelay * (light->counter++ / fadeStep)));

		if (light->counter >= fadeStep)
		{
			digitalWrite(light->pin, LOW);
			light->isDimming = false;
			light->isBrightening = false;
			light->isOn = false;
			//LocoNet.reportSensor(light->onCmd, INACTIVE);
		}
	}
}

/**
 *  Randomly flickers the light.  The speed of the flicker is determined by the rate2 value.  Typical value is 50.
 */
void FoggyHollowClass::flickerLED(fh_light *light)
{
	if (light->isOn)
	{
		uint8_t phase = LOW;
		if (light->counter++ > light->rate1)
		{
			light->counter = 0;
			if (random(1,100) > light->rate2) // Change phase (on/off) of LED to randomly keep the LED on longer or shorter
			{
				phase = HIGH;
			}
			else
			{
				phase = LOW;
			}
			digitalWrite(light->pin, phase);
		}
	}
}

/**
 * Called repeatedly from Arduino loop for each light.  Handles fade on/off, blink, dim, flicker.
 */
void FoggyHollowClass::loop(fh_light *light)
{
		//Serial.println (light.pin);
		if (light->function == FLICKERING)
		{
			flickerLED(light);
		}

		if (light->function == BLINKING || light->function == DIMMABLE)
		{
			if (light->isFunctionOn && light->isOn)
			{
				blinkLED(light);
			}
			else if (!light->isOn)
			{
				digitalWrite(light->pin, LOW);
			}

		}

		if (light->isBrightening || light->isDimming)
		{
			fadeOn(light);
		}

}

FoggyHollowClass FoggyHollow = FoggyHollowClass();
