//#define DEBUG
//
//********************************************************************************
//
//  Mine Building 2
//
//
//********************************************************************************
//
#include <LocoNet.h>
#include <FoggyHollow.h>
#include <Arduino.h>

const uint8_t ON = 1;
const uint8_t OFF = 0;
const uint8_t DIM = 2;

//
// Function Address Controls
const int loadingDockCmd = 140;
const int sideDoorCmd = 141;
const int surface1Cmd = 142;
const int surface2Cmd = 143;
const int surface3Cmd = 144;
const int roofSignCmd = 145;

const int loadingDockDim = 146;
const int surface2Dim = 147;
const int surface3Dim = 148;
const int roofSignDim = 149;
const int surface2Light2Cmd = 150;

//
// Pin connections
const int surface1Pin = 2;
const int loadingDockPin = 3;
const int sideDoorPin = 4;
const int roofSignPin1 = 5;
const int roofSignPin2 = 6;

const int LN_TX_PIN = 7;
const int LN_RX_PIN = 8;

const int surface2Pin1 = 9;
const int surface3Pin1 = 10;
const int surface3Pin2 = 11;
const int surface2Pin2 = 12;

const int numLights = 9;
const int numCommands = 11;

const int loadingDockIdx = 0;
const int sideDoorIdx = 1;
const int surface1Idx = 2;
const int surface21Idx = 3;
const int surface22Idx = 4;
const int surface31Idx = 5;
const int surface32Idx = 6;
const int roof1Idx = 7;
const int roof2Idx = 8;

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
		commands[i]->address = loadingDockCmd + i;
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
		light[i]->dimCmd = -1;
		light[i]->isPWM = false;
	}

	//
	// Initialize pins
	light[loadingDockIdx]->pin = loadingDockPin;
	light[sideDoorIdx]->pin = sideDoorPin;
	light[surface1Idx]->pin = surface1Pin;
	light[surface21Idx]->pin = surface2Pin1;
	light[surface22Idx]->pin = surface2Pin2;
	light[surface31Idx]->pin = surface3Pin1;
	light[surface32Idx]->pin = surface3Pin2;
	light[roof1Idx]->pin = roofSignPin1;
	light[roof2Idx]->pin = roofSignPin2;

	light[loadingDockIdx]->isPWM = true; // Loading Dock

	light[roof1Idx]->isPWM = true;
	light[roof2Idx]->isPWM = true;

	// Initialize on/off commands
	light[loadingDockIdx]->onCmd = loadingDockCmd;
	light[sideDoorIdx]->onCmd = sideDoorCmd;
	light[surface1Idx]->onCmd = surface1Cmd;
	light[surface21Idx]->onCmd = surface2Cmd;
	light[surface22Idx]->onCmd = surface2Light2Cmd;
	light[surface31Idx]->onCmd = surface3Cmd;
	light[surface32Idx]->onCmd = surface3Cmd;
	light[roof1Idx]->onCmd = roofSignCmd;
	light[roof2Idx]->onCmd = roofSignCmd;

	light[loadingDockIdx]->dimCmd = loadingDockDim;
	light[surface21Idx]->dimCmd = surface2Dim;
	light[surface31Idx]->dimCmd = surface3Dim;
	light[surface32Idx]->dimCmd = surface3Dim;
	light[roof1Idx]->dimCmd = roofSignDim;
	light[roof2Idx]->dimCmd = roofSignDim;

	for (int i = 0; i < numLights; i++)
	{
		pinMode(light[i]->pin, OUTPUT);
		if (light[i]->isPWM)
			analogWrite(light[i]->pin, 0);
		else
			digitalWrite(light[i]->pin, LOW);
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
	}
}


void changeDim(LIGHT_DEF *light, int state)
{
	light->isDimming = (state == SWITCH_ON) && light->isOn;
	light->isBrightening = (state == SWITCH_OFF) && light->isOn;
	if (state == SWITCH_ON)
	{
		//Serial.println ("Setting dim");
		light->targetIntensity = light->dimIntensity;
	}
	else
	{
		//Serial.println ("Unsetting dim");
		light->targetIntensity = light->maxIntensity;
	}
	light->isDimmed = state == SWITCH_ON;
}

void changeOnOff(LIGHT_DEF *light, int state)
{
	if (state == SWITCH_OFF)
	{
		//Serial.println("Turning light off");
		light->isDimming = true;
		light->isBrightening = false;
		light->targetIntensity = 0;
		light->isOn = false;
	}
	else
	{
		//Serial.println("Turning light on");
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
#ifdef DEBUG2
		Serial.print("In dimLight");
		Serial.print(" currentIntensity = ");
		Serial.print(light->currentIntensity);
		Serial.print(" targetIntensity = ");
		Serial.print(light->targetIntensity);
		Serial.print(" increment = ");
		Serial.print(increment);
		Serial.println("");
#endif   
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
#ifdef DEBUG
	Serial.print ("In notifySwitchRequest, Address = ");
	Serial.print (address);
	Serial.print (" Output = ");
	Serial.print (output);
	Serial.print (" state = ");
	Serial.println (state);
#endif
	if (address >= loadingDockCmd && address <= surface2Light2Cmd)
	{
		switch (address){
		case surface2Dim:
			if (state == SWITCH_ON)
			{
				FoggyHollow.fadeLED(light[surface21Idx], SWITCH_ON);
				FoggyHollow.fadeLED(light[surface22Idx], SWITCH_OFF);
			}
			else
			{
				FoggyHollow.fadeLED(light[surface21Idx], SWITCH_ON);
				delay(2000);
				FoggyHollow.fadeLED(light[surface22Idx], SWITCH_ON);
			}
			break;
		case surface2Cmd:
			FoggyHollow.fadeLED(light[surface21Idx], state);
			delay(2000);
			FoggyHollow.fadeLED(light[surface22Idx], state);
			break;

		case surface3Dim:
			if (state == SWITCH_ON)
			{
				FoggyHollow.fadeLED(light[surface31Idx], SWITCH_ON);
				FoggyHollow.fadeLED(light[surface32Idx], SWITCH_OFF);
			}
			else
			{
				FoggyHollow.fadeLED(light[surface31Idx], SWITCH_ON);
				delay(2000);
				FoggyHollow.fadeLED(light[surface32Idx], SWITCH_ON);
			}
			break;
		case surface3Cmd:
			FoggyHollow.fadeLED(light[surface31Idx], state);
			delay(2000);
			FoggyHollow.fadeLED(light[surface32Idx], state);
			break;

		case sideDoorCmd:
			FoggyHollow.fadeLED(light[sideDoorIdx], state);
			break;


		case loadingDockDim:
			changeDim(light[loadingDockIdx], state);
			break;

		case loadingDockCmd:
			changeOnOff(light[loadingDockIdx], state);
			break;

		case roofSignDim:
			changeDim(light[roof1Idx], state);
			changeDim(light[roof2Idx], state);
			break;
		case roofSignCmd:
			changeOnOff(light[roof1Idx], state);
			changeOnOff(light[roof2Idx], state);
			break;
		}
		commands[address-loadingDockCmd]->state = (state == SWITCH_OFF) ? INACTIVE : ACTIVE;
#ifdef DEBUG
		Serial.print ("In notifySwitch, reporting sensor at address");
		Serial.print (address);
		Serial.print (" state = ");
		Serial.println (state == SWITCH_OFF ? "INACTIVE" : "ACTIVE");

#endif
		LocoNet.reportSensor(address, (state == SWITCH_OFF) ? INACTIVE : ACTIVE);
	}
}
void notifySwitchReport( uint16_t Address, uint8_t Output, uint8_t Direction )
{
#ifdef DEBUG
	Serial.print ("In notifySwitchReport, Address = ");
	Serial.print (Address);
	Serial.print (" Output = ");
	Serial.print (Output);
	Serial.print (" Direction = ");
	Serial.println (Direction);
#endif
}


void notifySwitchState( uint16_t Address, uint8_t Output, uint8_t Direction )
{
#ifdef DEBUG
	Serial.print ("In notifySwitchState, Address = ");
	Serial.print (Address);
	Serial.print (" Output = ");
	Serial.print (Output);
	Serial.print (" Direction = ");
	Serial.println (Direction);
#endif
}
