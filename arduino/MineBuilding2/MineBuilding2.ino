#define DEBUG
//
//********************************************************************************
//
//  Mine Building 2
//
//
//********************************************************************************
//
#include <LocoNet.h>

const uint8_t ACTIVE = 16;
const uint8_t INACTIVE = 0;

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

//
// Pin connections
const int surface1Pin = 2;
const int loadingDockPin = 3;
const int sideDoorPin = 4;
const int roofSignPin1 = 5;
const int roofSignPin2 = 6;

const int LN_TX_PIN = 7;
const int LN_RX_PIN = 8;

const int surface2Pin = 9;
const int surface3Pin1 = 10;
const int surface3Pin2 = 11;

const int numLights = 8;

struct LIGHT_DEF
{
	int pin = -1;
	uint8_t currentIntensity = 0;
	uint8_t maxIntensity = 255;
	uint8_t dimIntensity = 70;
	uint8_t targetIntensity = 0;
	bool isDimmed = false;
	bool isOn = false;
	bool isDimming = false;
	bool isBrightening = false;
	bool isPWM = false;
	int rate = 2;
	int counter = 0;
	int dimCmd = -1;
	int onCmd = -1;
};

LIGHT_DEF* light[numLights];

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
	}

	//
	// Initialize pins
	light[0]->pin = loadingDockPin;
	light[1]->pin = sideDoorPin;
	light[2]->pin = surface1Pin;
	light[3]->pin = surface2Pin;
	light[4]->pin = surface3Pin1;
	light[5]->pin = surface3Pin2;
	light[6]->pin = roofSignPin1;
	light[7]->pin = roofSignPin2;

	light[0]->isPWM = true; // Loading Dock
	light[3]->isPWM = false; // S2
  light[3]->dimIntensity = 254; // S2

  // S3
	light[4]->isPWM = false;
	light[5]->isPWM = false;
  light[4]->dimIntensity = 200;
  light[5]->dimIntensity = 200;
 
	light[6]->isPWM = true;
	light[7]->isPWM = true;

	// Initialize on/off commands
	light[0]->onCmd = loadingDockCmd;
	light[1]->onCmd = sideDoorCmd;
	light[2]->onCmd = surface1Cmd;
	light[3]->onCmd = surface2Cmd;
	light[4]->onCmd = surface3Cmd;
	light[5]->onCmd = surface3Cmd;
	light[6]->onCmd = roofSignCmd;
	light[7]->onCmd = roofSignCmd;

  light[0]->dimCmd = loadingDockDim;
	light[3]->dimCmd = surface2Dim;
  light[4]->dimCmd = surface3Dim;
  light[5]->dimCmd = surface3Dim;
  light[6]->dimCmd = roofSignDim;
  light[7]->dimCmd = roofSignDim;    

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

/**
 * dimLight
 */
void dimLight(LIGHT_DEF *light, int increment)
{

	if (light->counter++ > light->rate)
	{
#ifdef DEBUG
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

		// Change light intensity 1 step
		light->currentIntensity = light->currentIntensity + increment;
		analogWrite(light->pin, light->currentIntensity);

		// Determine if we have reached the limit
		if (light->isDimming
				&& light->currentIntensity <= light->targetIntensity)
		{
			light->isDimming = false;
			light->isBrightening = false;
		}

		if (light->isBrightening
				&& light->currentIntensity >= light->targetIntensity)
		{
			light->isDimming = false;
			light->isBrightening = false;
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
			if (light[i]->currentIntensity == light[i]->maxIntensity)
			{
				LocoNet.reportSensor(light[i]->onCmd, ACTIVE);
				if (light[i]->dimCmd > 0)
					LocoNet.reportSensor(light[i]->dimCmd, INACTIVE);
			}
			else if (light[i]->currentIntensity == light[i]->dimIntensity)
			{
				LocoNet.reportSensor(light[i]->onCmd, ACTIVE);
				if (light[i]->dimCmd > 0)
					LocoNet.reportSensor(light[i]->dimCmd, ACTIVE);
			}
			else if (light[i]->currentIntensity == 0)
			{
				LocoNet.reportSensor(light[i]->onCmd, INACTIVE);
				if (light[i]->dimCmd > 0)
					LocoNet.reportSensor(light[i]->dimCmd, INACTIVE);
			}
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
void notifySensor(uint16_t address, uint8_t state)
{

	for (int i = 0; i < numLights; i++)
	{
		if (address == light[i]->dimCmd)
		{
			light[i]->isDimming = (state == ACTIVE) && light[i]->isOn;
			light[i]->isBrightening = (state == INACTIVE) && light[i]->isOn;
			if (state == ACTIVE)
			{
				//Serial.println ("Setting dim");
				light[i]->targetIntensity = light[i]->dimIntensity;
			}
			else
			{
				//Serial.println ("Unsetting dim");
				light[i]->targetIntensity = light[i]->maxIntensity;
			}
			light[i]->isDimmed = state == ACTIVE;
		}
		else if (address == light[i]->onCmd)
		{
			if (state == INACTIVE)
			{
				//Serial.println("Turning light off");
				if (light[i]->isPWM)
				{
					light[i]->isDimming = true;
					light[i]->isBrightening = false;
					light[i]->targetIntensity = 0;
				}
				else
				{
					digitalWrite(light[i]->pin, LOW);
				}
				light[i]->isOn = false;
			}
			else
			{
				//Serial.println("Turning light on");
				if (light[i]->isPWM)
				{
					light[i]->isDimming = false;
					light[i]->isBrightening = true;
					if (light[i]->isDimmed)
					{
						light[i]->targetIntensity = light[i]->dimIntensity;
					}
					else
					{
						light[i]->targetIntensity = light[i]->maxIntensity;
					}
				}
				else
				{
					digitalWrite(light[i]->pin, HIGH);
				}
				light[i]->isOn = true;
			}
		}
	}
}
