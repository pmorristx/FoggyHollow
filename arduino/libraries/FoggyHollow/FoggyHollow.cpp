#include "FoggyHollow.h"
#include <LocoNet.h>
FoggyHollowClass::FoggyHollowClass()
{

}


LIGHT_DEF* FoggyHollowClass::createLight( int pin, int onCmd)
{
	LIGHT_DEF* light = new LIGHT_DEF;

	light->pin = pin;
	light->onCmd = onCmd;
	light->function = ON_OFF;
	light->isInverted = false;

	pinMode(light->pin, OUTPUT);
	light->isOn = false;

	return light;
}

LIGHT_DEF* FoggyHollowClass::createFlickeringLight( int pin, int onCmd, int rate)
{
	LIGHT_DEF* light = new LIGHT_DEF;

	light->pin = pin;
	light->onCmd = onCmd;
	light->rate1 = 5;
	light->rate2 = rate;
	light->function = FLICKERING;
	light->isFunctionOn = true;
	light->isInverted = false;

	pinMode(light->pin, OUTPUT);
	light->isOn = false;

	return light;
}

LIGHT_DEF* FoggyHollowClass::createDimmableLight(int pin, int onCmd, int dimCmd)
{
	LIGHT_DEF* light = new LIGHT_DEF;

	light->pin = pin;
	light->onCmd = onCmd;
	light->function = DIMMABLE;
	light->functionCmd = dimCmd;
	light->isFunctionOn = false;
	light->isInverted = false;
	//light->rate1 = 20;
	//light->rate2 = 160;
	light->rate1 = 1;
	light->rate2 = 8;

	pinMode(light->pin, OUTPUT);
	light->isOn = false;

	return light;
}

LIGHT_DEF* FoggyHollowClass::createBlinkingLight(int pin, int onCmd, int blinkCmd)
{
	LIGHT_DEF* light = new LIGHT_DEF;

	light->pin = pin;
	light->onCmd = onCmd;
	light->function = BLINKING;
	light->functionCmd = blinkCmd;
	light->isFunctionOn = false;
	light->isInverted = false;
	light->rate1 = 30000;
	light->rate2 = 30000;

	pinMode(light->pin, OUTPUT);
	light->isOn = false;

	return light;
}

/**
 * Called from "loop" to blink an LED.  Note that we have to blink rates that allow
 * for dimming of an LED (pseudo PSM).
 */
void FoggyHollowClass::blinkLED(LIGHT_DEF *light)
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
void FoggyHollowClass::setState(LIGHT_DEF *light, bool state)
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
void FoggyHollowClass::setFunctionState(LIGHT_DEF *light, bool state)
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
		LocoNet.reportSensor(light->functionCmd, INACTIVE);
	}
}

void FoggyHollowClass::fadeLED(LIGHT_DEF *light, uint8_t requestedState)
{
	  int fade_time = 170;
	  float time_fraction;
	  int del_temp;

	  //
	  //  Only do this if we are changing the state of the light....don't do anything if
	  //  the light is already in the requested state.
	  if ((requestedState != INACTIVE && !light->isOn) || (requestedState == INACTIVE && light->isOn))
	  {
		  boolean start_state = light->isOn ? HIGH : LOW;
		  boolean end_state = light->isOn? LOW : HIGH;

		  for (int loop_time=0; loop_time<fade_time; loop_time++)  {
				time_fraction = (float (loop_time))/(float (fade_time));
				digitalWrite (light->pin, start_state);
				del_temp = 1000 - (1000.*time_fraction);
				if (del_temp<0) del_temp=0;
				delayMicroseconds (del_temp);
				digitalWrite (light->pin, end_state);
				delayMicroseconds (1000.*time_fraction);
				}
		  light->isOn = requestedState != INACTIVE;
	  }
}

/**
 * Fades a light on/off.  Note that this method will execute until the light has
 * transitioned...may cause other lights to quit blinking/flickering/dimming.
 */
void FoggyHollowClass::fadeOnOff(LIGHT_DEF *light, uint8_t state)
{
#define fadedelay 24
#define fadeStep 12

	int lightPin = light->pin;

	if (state != LOW && !light->isOn)
	{
		// Turning on
		for (int t = 0; t < fadeStep; t += 1)
		{
			digitalWrite( lightPin, HIGH);
			delay(fadedelay * (t / fadeStep));
			digitalWrite( lightPin, LOW);
			delay(fadedelay - (fadedelay * (t / fadeStep)));
		}
		digitalWrite( lightPin,  HIGH );
		light->isOn = true;
		LocoNet.reportSensor(light->onCmd, ACTIVE);
	} else if (state == LOW && light->isOn) {
		// Turning off
		for (int t = 0; t < fadeStep; t += 1)
		{
			digitalWrite( lightPin, LOW);
			delay(fadedelay * (t / fadeStep));
			digitalWrite( lightPin, HIGH);
			delay(fadedelay - (fadedelay * (t / fadeStep)));
		}
		digitalWrite(lightPin, LOW);
		light->isOn = false;
		LocoNet.reportSensor(light->onCmd, INACTIVE);
	}
}

/**
 * Fades a light on/off based on the isBrightening/isDimming value.  This method is called within the
 * main loop to avoid locking up the Arduino (and pausing blink/flicker/dim on other lights).
 */
void FoggyHollowClass::fadeOn(LIGHT_DEF *light)
{
#define fadedelay 24
#define fadeStep 12

	//if ((light->isBrightening && !light->isInverted) || (light->isDimming && light->isInverted))
	if (light->isBrightening)
	{
		//Serial.print ("Turning on light ");
		//Serial.print (light->pin);
		//Serial.print ("counter = ");
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
			LocoNet.reportSensor(light->onCmd, ACTIVE);
		}
//	} else if ((light->isDimming && !light->isInverted) || (light->isBrightening && light->isInverted)) {
	} else if (light->isDimming) {
		// Turning off
		//Serial.print ("Turning off light ");
		//Serial.print (light->pin);
		//Serial.print ("counter = ");
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
			LocoNet.reportSensor(light->onCmd, INACTIVE);
		}
	}
}

/**
 *  Randomly flickers the light.  The speed of the flicker is determined by the rate2 value.  Typical value is 50.
 */
void FoggyHollowClass::flickerLED(LIGHT_DEF *light)
{
	if (light->isOn)
	{
		int phase = LOW;
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
void FoggyHollowClass::loop(LIGHT_DEF *light)
{
		//Serial.println (light->pin);
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
				//Serial.print ("Turning off light ");
				digitalWrite(light->pin, LOW);
				//Serial.print (light->pin);
			}

		}

		if (light->isBrightening || light->isDimming)
		{
			//Serial.print ("Fading on");
			fadeOn(light);
		}

}

FoggyHollowClass FoggyHollow = FoggyHollowClass();
