#include "FoggyHollow.h"

FoggyHollowClass::FoggyHollowClass()
{

}

void FoggyHollowClass::blinkLED(LIGHT_DEF *light)
{
	if (light->blinkCount++ > light->blinkRate1 && light->blinkPhase)
	{
		light->blinkCount = 0;
		light->blinkPhase = !light->blinkPhase;
		digitalWrite(light->pin, LOW);
	}
	else if (light->blinkCount++ > light->blinkRate2 && !light->blinkPhase)
	{
		light->blinkCount = 0;
		light->blinkPhase = !light->blinkPhase;
		digitalWrite(light->pin, HIGH);
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

void FoggyHollowClass::fadeOnOff(LIGHT_DEF *light, uint8_t state)
{
#define fadedelay 24
#define fadestep 12

	int lightPin = light->pin;

	if (state != LOW && !light->isOn)
	{
		// Turning on
		for (int t = 0; t < fadestep; t += 1)
		{
			digitalWrite( lightPin, HIGH);
			delay(fadedelay * (t / fadestep));
			digitalWrite( lightPin, LOW);
			delay(fadedelay - (fadedelay * (t / fadestep)));
		}
		digitalWrite( lightPin,  HIGH );
		light->isOn = true;
	} else if (state == LOW && light->isOn) {
		// Turning off
		for (int t = 0; t < fadestep; t += 1)
		{
			digitalWrite( lightPin, LOW);
			delay(fadedelay * (t / fadestep));
			digitalWrite( lightPin, HIGH);
			delay(fadedelay - (fadedelay * (t / fadestep)));
		}
		digitalWrite(lightPin, LOW);
		light->isOn = false;
	}
}

/**
 *
 */
void FoggyHollowClass::flickerLED(LIGHT_DEF *light)
{
	if (light->isOn)
	{
		int phase = LOW;
		if (light->flickerCount++ > light->flickerRate)
		{
			light->flickerCount = 0;
			if (random(1,100) > 50) // Change phase (on/off) of LED to randomly keep the LED on longer or shorter
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

FoggyHollowClass FoggyHollow = FoggyHollowClass();
