//#define DEBUG
//
//********************************************************************************
//
//  Depot
//
//
//********************************************************************************
//
#include <LocoNet.h>
#include <FoggyHollow.h>
#include <Arduino.h>

int fireIntensity = HIGH;

const uint8_t ON = 1;
const uint8_t OFF = 0;
const uint8_t DIM = 2;

//
// Function Address Controls
const int stoveCmd = 170;
const int platformCmd = 171;
const int waitingRoomCmd = 172;
const int officeCmd = 173;
const int signCmd = 174;
const int officeDimCmd = 175;
const int platformDimCmd = 176;
const int waitingRoomDimCmd = 177;
const int gh1Cmd = 178;
const int ghrCmd = 179;
const int gh2Cmd = 180;
const int gh1BlinkCmd = 181;
const int ghrBlinkCmd = 182;
const int gh2BlinkCmd = 183;
const int stoveIntensityCmd = 184;

const int stove11Cmd = 185;
const int stove12Cmd = 186;
const int stove21Cmd = 187;
const int stove22Cmd = 188;

//
// Pin connections

const int officePin = 2;
const int platform1Pin = 3;
const int gh1Pin = 4;
const int gh2Pin = 5;
const int ghrPin = 6;
const int platform2Pin = 9;
const int waitingRoom1Pin = 10;
const int waitingRoom2Pin = 11;
const int stove11Pin = 12;
const int stove12Pin = 13;
const int stove21Pin = 14;
const int stove22Pin = 15;
const int sign1Pin = 16;
const int sign2Pin = 17;

const int officeIdx = 0;
const int platform1Idx = 1;
const int gh1Idx = 2;
const int gh2Idx = 3;
const int ghrIdx = 4;
const int platform2Idx = 5;
const int waitingRoom1Idx = 6;
const int waitingRoom2Idx = 7;
const int stove11Idx = 8;
const int stove12Idx = 9;
const int stove21Idx = 10;
const int stove22Idx = 11;
const int sign1Idx = 12;
const int sign2Idx = 13;

const int LN_TX_PIN = 7;
const int LN_RX_PIN = 8;

const int numLights = 14;
const int numCommands = 19;



struct LIGHT_CMD
{
	uint16_t address;
	uint8_t state;
};

LIGHT_DEF* light[numLights];
LIGHT_CMD* commands[numCommands];

lnMsg *LnPacket;          // pointer to a received LNet packet
//
//********************************************************************************
//
//  Arduino calls setup once on power-up.  Note that this usually happens before
//  JMRI has started.
//
//********************************************************************************
//
void setup()
{
#ifdef DEBUG
	Serial.begin(115200);
	Serial.println("In setup");
#endif

	for (int i=0;  i<numCommands; i++)
	{
		commands[i]->address = stoveCmd + i;
		commands[i]->state = INACTIVE;
	}

	for (int i = 0; i < numLights; i++)
	{
		light[i] = new LIGHT_DEF;
		light[i]->dimIntensity = 50;
		light[i]->maxIntensity = 255;
		light[i]->currentIntensity = 0;
		light[i]->targetIntensity = 0;
		light[i]->isDimming = false;
		light[i]->isBrightening = false;
		light[i]->counter = 0;
		light[i]->rate = 5;
		light[i]->dimCmd = -1;
		light[i]->isPWM = false;
		light[i]->isOn = false;
		light[i]->isBlinking = false;
	}

	//
	// Initialize pins
	light[stove11Idx]->pin = stove11Pin;
	light[stove12Idx]->pin = stove12Pin;
	light[stove21Idx]->pin = stove21Pin;
	light[stove22Idx]->pin = stove22Pin;

	light[platform1Idx]->pin = platform1Pin;
	light[platform2Idx]->pin = platform2Pin;
	light[waitingRoom1Idx]->pin = waitingRoom1Pin;
	light[waitingRoom2Idx]->pin = waitingRoom2Pin;

	light[officeIdx]->pin = officePin;
	light[sign1Idx]->pin = sign1Pin;
	light[sign2Idx]->pin = sign2Pin;
	light[gh1Idx]->pin = gh1Pin;
	light[gh2Idx]->pin = gh2Pin;
	light[ghrIdx]->pin = ghrPin;

	light[platform1Idx]->isPWM = true;
	light[platform2Idx]->isPWM = true;
	light[waitingRoom1Idx]->isPWM = true;
	light[waitingRoom2Idx]->isPWM = true;
	light[platform1Idx]->dimIntensity = 150;
	light[platform2Idx]->dimIntensity = 150;
	light[platform1Idx]->blinkRate1 = 20;
	light[platform1Idx]->blinkRate2 = 160;
	light[platform2Idx]->blinkRate1 = 20;
	light[platform2Idx]->blinkRate2 = 160;

	light[waitingRoom1Idx]->dimIntensity = 50;
	light[waitingRoom2Idx]->dimIntensity = 50;
	light[waitingRoom1Idx]->blinkRate1 = 20;
	light[waitingRoom1Idx]->blinkRate2 = 160;
	light[waitingRoom2Idx]->blinkRate1 = 20;
	light[waitingRoom2Idx]->blinkRate2 = 160;

	light[officeIdx]->blinkRate1 = 20;
	light[officeIdx]->blinkRate2 = 160;


	// Initialize on/off commands
	light[stove11Idx]->onCmd = stoveCmd;
	light[stove12Idx]->onCmd = stoveCmd;
	light[stove21Idx]->onCmd = stoveCmd;
	light[stove22Idx]->onCmd = stoveCmd;
	light[platform1Idx]->onCmd = platformCmd;
	light[platform2Idx]->onCmd = platformCmd;
	light[waitingRoom1Idx]->onCmd = waitingRoomCmd;
	light[waitingRoom2Idx]->onCmd = waitingRoomCmd;
	light[officeIdx]->onCmd = officeCmd;
	light[sign1Idx]->onCmd = signCmd;
	light[sign2Idx]->onCmd = signCmd;
	light[gh1Idx]->onCmd = gh1Cmd;
	light[gh2Idx]->onCmd = gh2Cmd;
	light[ghrIdx]->onCmd = ghrCmd;

	light[platform1Idx]->dimCmd = platformDimCmd;
	light[platform2Idx]->dimCmd = platformDimCmd;
	light[waitingRoom1Idx]->dimCmd = waitingRoomDimCmd;
	light[waitingRoom2Idx]->dimCmd = waitingRoomDimCmd;

	for (int i = 0; i < numLights; i++)
	{
		pinMode(light[i]->pin, OUTPUT);
		light[i]->isOn = false;
		if (i >= gh1Idx && i <= ghrIdx)
		{
			digitalWrite(light[i]->pin, LOW);
			digitalWrite(light[i]->pin, HIGH);
		}
		else
		{
			digitalWrite(light[i]->pin, LOW);
		}
	}

	LocoNet.init(LN_TX_PIN);

#ifdef DEBUG
Serial.println("Setup complete");
#endif
}

//
//********************************************************************************
//
//  Arduino calls loop over and over.  This is where we monitor for LocoNet messages
//  and adjust the servos.
//
//********************************************************************************
//
void loop()
{
	// Check for any received LocoNet packets - Only one we get is to raise/lower spout
	LnPacket = LocoNet.receive();
	if (LnPacket)
	{
		LocoNet.processSwitchSensorMessage(LnPacket);
	}

	for (int i = 0; i < numLights; i++)
	{
		if (light[i]->isDimming)
		{
			dimLight(light[i], -1);
		}
		else if (light[i]->isBrightening)
		{
			dimLight(light[i], 1);
		}
		else if (light[i]->isBlinking)
		{
			FoggyHollow.blinkLED(light[i]);
		}
	}

	FoggyHollow.flickerLED(light[stove11Idx]);
	FoggyHollow.flickerLED(light[stove21Idx]);
	if (fireIntensity == HIGH)
	{
		FoggyHollow.flickerLED(light[stove12Idx]);
		FoggyHollow.flickerLED(light[stove22Idx]);
	}
}



void changeOnOff(LIGHT_DEF *light, int state)
{
	if (state == SWITCH_OFF)
	{
		Serial.println("Turning light off");
		light->isDimming = true;
		light->isBrightening = false;
		light->targetIntensity = 0;
		light->isOn = false;
	}
	else
	{
		Serial.println("Turning light on");
		light->isDimming = false;
		light->isBrightening = true;
		if (light->isDimmed)
		{
			light->targetIntensity = light->dimIntensity;
		}
		else
		{
			light->targetIntensity = light->maxIntensity;
		}
		light->isOn = true;
	}
}
/**
 * dimLight
 */
void dimLight(LIGHT_DEF *light, int increment)
{

	if (light->counter++ > light->rate)
	{
		// Reset counter for next time through
		light->counter = 0;

		// Determine if we have reached the limit
		if (light->isDimming
				&& light->currentIntensity <= light->targetIntensity)
		{
			light->isDimming = false;
			light->isBrightening = false;
		}

		else if (light->isBrightening
				&& light->currentIntensity >= light->targetIntensity)
		{
			light->isDimming = false;
			light->isBrightening = false;
		}
		else
		{
#ifdef DEBUG
		Serial.print("In dimLight");
		Serial.print(" currentIntensity = ");
		Serial.print(light->currentIntensity);
		Serial.print(" targetIntensity = ");
		Serial.print(light->targetIntensity);
		Serial.print(" increment = ");
		Serial.print(increment);
		Serial.print(" pin # = ");
		Serial.print(light->pin);
		Serial.println("");
#endif
			// Change light intensity 1 step
			light->currentIntensity = light->currentIntensity + increment;
			analogWrite(light->pin, light->currentIntensity);
		}
	}
}

//
//---------------------------------------------------------------------------------------
//
// notifyPower - used to trigger reporting of sensor state when JMRI powers up.
//
//---------------------------------------------------------------------------------------
//
void notifyPower(uint8_t state)
{
	if (state)
	{
		for (int i = 0; i < numLights; i++)
		{
#ifdef DEBUG
			Serial.print ("In notifyPower, Address = ");
			Serial.print (light[i]->onCmd);
#endif
			LocoNet.reportSwitch(light[i]->onCmd);
			if (light[i]->dimCmd >= 0)
			{
				LocoNet.reportSwitch(light[i]->dimCmd);
			}
		}

		for (int i=0; i<numCommands; i++)
		{
			LocoNet.reportSensor(commands[i]->address, commands[i]->state);
		}
	}
}
//
//---------------------------------------------------------------------------------------
//
// notifySensor - Called by JMRI/LocoNet when a sensor changes on JMRI.
//
//---------------------------------------------------------------------------------------
//
/*
void notifySensor(uint16_t address, uint8_t state)
{
}
 */
void notifySwitchRequest( uint16_t address, uint8_t output, uint8_t state )
{
	uint8_t invertedState = ACTIVE;
	if (address >= stoveCmd && address <= stove22Cmd)
	{
#ifdef DEBUG
	Serial.print ("In notifySwitchRequest, Address = ");
	Serial.print (address);
	Serial.print (" Output = ");
	Serial.print (output);
	Serial.print (" state = ");
	Serial.println (state);
#endif
		if (state == INACTIVE)
			invertedState = ACTIVE;
		else
			invertedState = INACTIVE;

		switch (address){
		case stoveCmd:
			if (state == SWITCH_ON)
			{
				light[stove11Idx]->isOn = true;
				light[stove12Idx]->isOn = true;
				light[stove21Idx]->isOn = true;
				light[stove22Idx]->isOn = true;
				digitalWrite(light[stove11Idx]->pin, HIGH);
				digitalWrite(light[stove12Idx]->pin, HIGH);
				digitalWrite(light[stove21Idx]->pin, HIGH);
				digitalWrite(light[stove22Idx]->pin, HIGH);
			}
			else
			{
				light[stove11Idx]->isOn = false;
				light[stove12Idx]->isOn = false;
				light[stove21Idx]->isOn = false;
				light[stove22Idx]->isOn = false;
				digitalWrite(light[stove11Idx]->pin, LOW);
				digitalWrite(light[stove12Idx]->pin, LOW);
				digitalWrite(light[stove21Idx]->pin, LOW);
				digitalWrite(light[stove22Idx]->pin, LOW);
			}
			break;
		case platformDimCmd:
			light[platform1Idx]->isBlinking = state == SWITCH_ON;
			light[platform1Idx]->blinkCount = 0;
			if (state == SWITCH_OFF)
			{
				if (light[platform1Idx]->isOn)
				{
					digitalWrite(light[platform1Idx]->pin, HIGH);
					LocoNet.reportSensor(platform1Idx, ACTIVE);
				}
				else
				{
					digitalWrite(light[platform1Idx]->pin, LOW);
					LocoNet.reportSensor(platform1Idx, INACTIVE);
				}
			}

			light[platform2Idx]->isBlinking = state == SWITCH_ON;
			light[platform2Idx]->blinkCount = 0;
			if (state == SWITCH_OFF)
			{
				if (light[platform2Idx]->isOn)
				{
					digitalWrite(light[platform2Idx]->pin, HIGH);
					LocoNet.reportSensor(platform2Idx, ACTIVE);
				}
				else
				{
					digitalWrite(light[platform2Idx]->pin, LOW);
					LocoNet.reportSensor(platform2Idx, INACTIVE);
				}
			}
			break;
		case platformCmd:
			FoggyHollow.fadeLED(light[platform1Idx], state);
			FoggyHollow.fadeLED(light[platform2Idx], state);
			break;

		case waitingRoomDimCmd:
			light[waitingRoom1Idx]->isBlinking = state == SWITCH_ON;
			light[waitingRoom1Idx]->blinkCount = 0;
			if (state == SWITCH_OFF)
			{
				if (light[waitingRoom1Idx]->isOn)
				{
					digitalWrite(light[waitingRoom1Idx]->pin, HIGH);
					LocoNet.reportSensor(waitingRoom1Idx, ACTIVE);
				}
				else
				{
					digitalWrite(light[waitingRoom1Idx]->pin, LOW);
					LocoNet.reportSensor(waitingRoom1Idx, INACTIVE);
				}
			}

			light[waitingRoom2Idx]->isBlinking = state == SWITCH_ON;
			light[waitingRoom2Idx]->blinkCount = 0;
			if (state == SWITCH_OFF)
			{
				if (light[waitingRoom2Idx]->isOn)
				{
					digitalWrite(light[waitingRoom2Idx]->pin, HIGH);
					LocoNet.reportSensor(waitingRoom2Idx, ACTIVE);
				}
				else
				{
					digitalWrite(light[waitingRoom2Idx]->pin, LOW);
					LocoNet.reportSensor(waitingRoom2Idx, INACTIVE);
				}
			}
			break;

		case waitingRoomCmd:
			FoggyHollow.fadeLED(light[waitingRoom1Idx], state);
			FoggyHollow.fadeLED(light[waitingRoom2Idx], state);
			break;

		case officeCmd:
			FoggyHollow.fadeLED(light[officeIdx], state);
			break;
		case officeDimCmd:
			light[officeIdx]->isBlinking = state == SWITCH_ON;
			light[officeIdx]->blinkCount = 0;
			if (state == SWITCH_OFF)
			{
				if (light[officeIdx]->isOn)
				{
					digitalWrite(light[officeIdx]->pin, HIGH);
					LocoNet.reportSensor(officeIdx, ACTIVE);
				}
				else
				{
					digitalWrite(light[officeIdx]->pin, LOW);
					LocoNet.reportSensor(officeIdx, INACTIVE);
				}
			}
			break;

		case signCmd:
			FoggyHollow.fadeLED(light[sign1Idx], state);
			FoggyHollow.fadeLED(light[sign2Idx], state);
			break;

		case gh1Cmd:
			//FoggyHollow.fadeLED(light[gh1Idx], invertedState);
			if (invertedState == ACTIVE)
				digitalWrite(light[gh1Idx]->pin, HIGH);
			else
				digitalWrite(light[gh1Idx]->pin, LOW);
			light[gh1Idx]->isBlinking = false;
			LocoNet.reportSensor(gh1BlinkCmd, INACTIVE);
			break;

		case gh2Cmd:
			//FoggyHollow.fadeLED(light[gh2Idx], invertedState);
			if (invertedState == ACTIVE)
				digitalWrite(light[gh2Idx]->pin, HIGH);
			else
				digitalWrite(light[gh2Idx]->pin, LOW);
			light[gh2Idx]->isBlinking = false;
			LocoNet.reportSensor(gh2BlinkCmd, INACTIVE);
			break;

		case ghrCmd:
			light[ghrIdx]->isBlinking = false;
			//FoggyHollow.fadeLED(light[ghrIdx], invertedState);
			if (invertedState == ACTIVE)
				digitalWrite(light[ghrIdx]->pin, HIGH);
			else
				digitalWrite(light[ghrIdx]->pin, LOW);
			LocoNet.reportSensor(ghrBlinkCmd, INACTIVE);
			break;

		case gh1BlinkCmd:
			light[gh1Idx]->isBlinking = state == SWITCH_ON;
			light[gh1Idx]->blinkCount = 0;
			light[gh1Idx]->blinkRate1 = 32000;
			light[gh1Idx]->blinkRate2 = 32000;
			if (state == SWITCH_OFF)
			{
				light[gh1Idx]->isOn = false;
				digitalWrite(light[gh1Idx]->pin, HIGH);
				LocoNet.reportSensor(gh1Cmd, INACTIVE);
			}
			break;

		case gh2BlinkCmd:
			light[gh2Idx]->isBlinking = state == SWITCH_ON;
			light[gh2Idx]->blinkCount = 0;
			light[gh2Idx]->blinkRate1 = 30000;
			light[gh2Idx]->blinkRate2 = 30000;
			if (state == SWITCH_OFF)
			{
				light[gh2Idx]->isOn = false;
				digitalWrite(light[gh2Idx]->pin, HIGH);
				LocoNet.reportSensor(gh2Cmd, INACTIVE);
			}
			break;

		case ghrBlinkCmd:
			light[ghrIdx]->isBlinking = state == SWITCH_ON;
			light[ghrIdx]->blinkCount = 0;
			light[ghrIdx]->blinkRate1 = 31000;
			light[ghrIdx]->blinkRate2 = 31000;
			if (state == SWITCH_OFF)
			{
				light[ghrIdx]->isOn = false;
				digitalWrite(light[ghrIdx]->pin, HIGH);
				LocoNet.reportSensor(ghrCmd, INACTIVE);
			}
			break;

		case stoveIntensityCmd:
			if (state == SWITCH_ON)
			{
				fireIntensity = HIGH;
				light[stove12Idx]->isOn = true;
				light[stove22Idx]->isOn = true;
			}
			else
			{
				fireIntensity = LOW;
				light[stove12Idx]->isOn = false;
				light[stove22Idx]->isOn = false;
			}
			break;

		case stove11Cmd:
			FoggyHollow.fadeLED(light[stove11Idx], state);
			break;

		case stove12Cmd:
			FoggyHollow.fadeLED(light[stove12Idx], state);
			break;

		case stove21Cmd:
			FoggyHollow.fadeLED(light[stove21Idx], state);
			break;

		case stove22Cmd:
			FoggyHollow.fadeLED(light[stove22Idx], state);
			break;

		}
		commands[address-stoveCmd]->state = (state == SWITCH_OFF) ? INACTIVE : ACTIVE;
#ifdef DEBUG
		Serial.print ("In notifySwitch, reporting sensor at address");
		Serial.print (address);
		Serial.print (" state = ");
		Serial.println (state == SWITCH_OFF ? "INACTIVE" : "ACTIVE");

#endif
		LocoNet.reportSensor(address, (state == SWITCH_OFF) ? INACTIVE : ACTIVE);
	}
}
