#define DEBUG
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


const int numCommands = 19;
const int numLights = 14;

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
	LocoNet.init(LN_TX_PIN);

	light[officeIdx] = FoggyHollow.createDimmableLight(officePin, officeCmd, officeDimCmd); // Office
	light[platform1Idx] = FoggyHollow.createDimmableLight(platform1Pin, platformCmd, platformDimCmd); // Platform1
	light[platform2Idx] = FoggyHollow.createDimmableLight(platform2Pin, platformCmd, platformDimCmd); // Platform2
	light[waitingRoom1Idx] = FoggyHollow.createDimmableLight(waitingRoom1Pin, waitingRoomCmd, waitingRoomDimCmd); // Waiting Room 1
	light[waitingRoom2Idx] = FoggyHollow.createDimmableLight(waitingRoom2Pin, waitingRoomCmd, waitingRoomDimCmd); // Waiting Room 2

	light[sign1Idx] = FoggyHollow.createLight(16, 174); // Sign 1
	light[sign2Idx] = FoggyHollow.createLight(17, 174); // Sign 2

	light[stove11Idx] = FoggyHollow.createFlickeringLight(12, 170, 65); // Stove 11
	light[stove12Idx] = FoggyHollow.createFlickeringLight(13, 170, 65); // Stove 12
	light[stove21Idx] = FoggyHollow.createFlickeringLight(14, 170, 65); // Stove 21
	light[stove22Idx] = FoggyHollow.createFlickeringLight(15, 170, 65); // Stove 22

	light[gh1Idx] = FoggyHollow.createBlinkingLight(4, 178, 181); // GH1
	light[gh1Idx]->isInverted = true;
	light[gh2Idx] = FoggyHollow.createBlinkingLight(5, 180, 183); // GH2
	light[gh2Idx]->isInverted = true;
	light[ghrIdx] = FoggyHollow.createBlinkingLight(6, 179, 182); // GHR
	light[ghrIdx]->isInverted = true;

	for (int i = 0; i < numLights; i++)
	{
		FoggyHollow.setState(light[i], false);
		FoggyHollow.setFunctionState(light[i], false);
	}


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
		FoggyHollow.loop(light[i]);
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
		}

		for (int i=0; i<numLights; i++)
		{
			if (light[i]->isOn == ACTIVE)
				LocoNet.reportSensor(light[i]->onCmd, ACTIVE);
			else
				LocoNet.reportSensor(light[i]->onCmd, INACTIVE);

			if (light[i]->functionCmd > 0)
			{
				if (light[i]->isFunctionOn == ACTIVE)
					LocoNet.reportSensor(light[i]->functionCmd, ACTIVE);
				else
					LocoNet.reportSensor(light[i]->functionCmd, INACTIVE);
			}
		}
	}
}
//
//---------------------------------------------------------------------------------------
//

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

		if (address == stoveIntensityCmd)
		{
			if (state == SWITCH_ON)
			{
				for (int i=7; i<=10; i++)
				{
					light[i]->isOn = true;
					light[i]->rate2 = 40;
				}
			}
			else
			{
				light[7]->isOn = true;
				light[8]->isOn = false;
				light[9]->isOn = true;
				light[10]->isOn = false;
				light[7]->rate2 = 65;
				light[9]->rate2 = 65;
			}
		}
		for (int i=0; i<numLights; i++)
		{
			if (address == light[i]->onCmd)
			{
				FoggyHollow.setState(light[i], state == SWITCH_ON);
			}
			else if (address == light[i]->functionCmd)
			{
				FoggyHollow.setFunctionState(light[i], (state == SWITCH_ON));
			}
		}



#ifdef DEBUG
		Serial.print ("In notifySwitch, reporting sensor at address");
		Serial.print (address);
		Serial.print (" state = ");
		Serial.println (state == SWITCH_OFF ? "INACTIVE" : "ACTIVE");

#endif
	}
}
